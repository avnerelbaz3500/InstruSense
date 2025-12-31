import json
from pathlib import Path
from typing import Any, Callable

import torch
import yaml
from torch import Tensor

from .audio_loader import audio_to_input
from .structure import Model
from .import_weights import ModelLoader


class Overseer:
    folder_path: Path
    config_path: Path
    weight_path: Path
    stat_path: Path
    device: torch.device
    params: dict[str, Any]
    thresholds: Tensor
    instrument_dict: dict[str, str]
    reverse_instrument_dict: dict[str, str]
    preprocessor: Callable[..., list[Tensor]]
    model: Model
    optimiser: torch.optim.Adam

    def __init__(self, folder_path: Path) -> None:
        self.folder_path = folder_path
        self.config_path = folder_path / "config"
        self.weight_path = folder_path / "weight"
        self.stat_path = folder_path / "stats"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_all()

    def _load_all(self) -> None:
        self.load_parameters()
        self._load_instrument_dict()
        self._load_preprocessor()
        self._load_classifier()

    def load_parameters(self) -> None:
        with open(self.config_path / "parameters.yaml", "r", encoding="utf-8") as f:
            self.params = yaml.safe_load(f)
        thresholds_path: Path = self.config_path / "thresholds.json"
        if thresholds_path.is_file():
            with open(thresholds_path, "r", encoding="utf-8") as f:
                dict_thresholds: dict[str, float] = yaml.safe_load(f)
                thresholds: list[float] = [
                    dict_thresholds[str(i)] for i in range(self.params["n_instr"])
                ]
                self.thresholds = torch.tensor(thresholds, device=torch.device("cpu"))
        else:
            self.thresholds = torch.full(
                (self.params["n_instr"],),
                self.params["threshold"],
                device=torch.device("cpu"),
            )

    def _load_instrument_dict(self) -> None:
        with open(self.config_path / "instruments.json") as f:
            self.instrument_dict = json.load(f)
            self.reverse_instrument_dict = {
                v: k for k, v in self.instrument_dict.items()
            }

    def _load_preprocessor(self) -> None:
        self.preprocessor = audio_to_input

    def _load_classifier(self) -> None:
        self.model = Model(self.params["n_instr"]).to(self.device)
        self.optimiser = torch.optim.Adam(self.model.parameters(), lr=self.params["lr"])
        if not (self.weight_path / "best.pth").exists():
            print(f"Poids non trouvés dans {self.weight_path}. Téléchargement...")
            loader = ModelLoader(repo_id="gandalfbob/Instru")
            loader.load()
        checkpoint: dict[str, Any] = torch.load(
            self.weight_path / "checkpoint.pth",
            map_location=self.device,
            weights_only=True,
        )
        self.model.load_state_dict(checkpoint["model_state"])
        self.optimiser.load_state_dict(checkpoint["optimizer_state"])

    def visualise_pred(self, preds: Tensor) -> None:
        for i in range(len(preds)):
            print(
                f"{self.instrument_dict[str(i)]} : {round(float(preds[i]), 2)}, "
                f"threshold: {self.thresholds[i].item()}, "
                f"ratio = {round(float(preds[i]), 2) / self.thresholds[i].item()}"
            )

    def aggregate_predictions(self, preds: Tensor, min_ratio: float = 0.6) -> list[str]:
        y_bin: Tensor = preds > self.thresholds
        ratio: Tensor = y_bin.float().mean(dim=0)
        y_final: Tensor = ratio >= min_ratio

        return [
            self.instrument_dict[str(i)]
            for i in range(self.params["n_instr"])
            if y_final[i]
        ]

    def predict(self, wav_path: str) -> list[str]:
        self.model.eval()
        chunks: list[Tensor] = self.preprocessor(wav_path)

        preds_list: list[Tensor] = []
        with torch.no_grad():
            for mel in chunks:
                x: Tensor = mel.unsqueeze(0).to(self.device)
                y: Tensor = self.model(x)
                y = torch.sigmoid(y)
                preds_list.append(y.cpu())
        preds: Tensor = torch.cat(preds_list, dim=0)
        return self.aggregate_predictions(preds)

    def save_epoch(self, dico_epoch: dict[str, Any]) -> None:
        best: bool = True
        epoch_data_path: Path = self.stat_path / "epoch_data.jsonl"
        with open(epoch_data_path, "r") as f:
            n_epoch: int = 1
            for line in f:
                n_epoch += 1
                record: dict[str, Any] = json.loads(line)
                if dico_epoch["valid_loss"] > record["valid_loss"]:
                    best = False
        with open(epoch_data_path, "a") as f:
            data: dict[str, Any] = {"epoch": n_epoch}
            for key in dico_epoch.keys():
                data[key] = dico_epoch[key]
            f.write(json.dumps(data) + "\n")
        torch.save(
            {
                "model_state": self.model.state_dict(),
                "optimizer_state": self.optimiser.state_dict(),
            },
            self.weight_path / "checkpoint.pth",
        )
        if best:
            torch.save(
                {
                    "model_state": self.model.state_dict(),
                    "optimizer_state": self.optimiser.state_dict(),
                },
                self.weight_path / "best.pth",
            )
