'''
import json
from pathlib import Path
import torch
import yaml

from .audio_loader import audio_to_input
from .structure import Model
from .import_weights import ModelLoader


class Overseer:
    def __init__(self, folder_path: Path):
        self.folder_path = folder_path
        self.config_path = folder_path / "config"
        self.weight_path = folder_path / "weight"
        self.stat_path = folder_path / "stats"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_all()

    def _load_all(self):
        self.load_parameters()
        self._load_instrument_dict()
        self._load_preprocessor()
        self._load_classifier()

    def load_parameters(self):
        with open(self.config_path / "parameters.yaml", "r", encoding="utf-8") as f:
            self.params = yaml.safe_load(f)

    def _load_instrument_dict(self):
        with open(self.config_path / "instruments.json") as f:
            self.instrument_dict = json.load(f)
            self.reverse_instrument_dict = {
                v: k for k, v in self.instrument_dict.items()
            }

    def _load_preprocessor(self):
        self.preprocessor = audio_to_input

    def _load_classifier(self):
        self.model = Model(self.params["n_instr"]).to(self.device)
        self.optimiser = torch.optim.Adam(self.model.parameters(), lr=self.params["lr"])
        
        if not (self.weight_path / "best.pth").exists():
            print(f"Poids non trouvés dans {self.weight_path}. Téléchargement...")
            loader = ModelLoader(
                repo_id="gandalfbob/Instru"
       
            )
            loader.load()

        checkpoint = torch.load(
            self.weight_path / "best.pth",
            map_location=self.device,
            weights_only=True,
        )
        self.model.load_state_dict(checkpoint["model_state"])
        self.optimiser.load_state_dict(checkpoint["optimizer_state"])

    def predict(self, wav_path):
        self.model.eval()
        x = self.preprocessor(wav_path).unsqueeze(0).to(self.device)
        with torch.no_grad():
            y = self.model(x)
            y = torch.sigmoid(y)
        # print("Raw scores:", y)
        # print("Max score:", y.max().item())
        y_thresh = (y > self.params["threshold"]).squeeze(0)
        l_instr = []
        for i in range(self.params["n_instr"]):
            if y_thresh[i]:
                l_instr.append(self.instrument_dict[str(i)])
        return l_instr

    def save_epoch(self, dico_epoch):
        # put this in a abstract class
        # that the architectures are inheriting from ?
        best = True
        epoch_data_path = self.stat_path / "epoch_data.jsonl"
        with open(epoch_data_path, "r") as f:
            n_epoch = 1
            for line in f:
                n_epoch += 1
                record = json.loads(line)
                if dico_epoch["valid_loss"] > record["valid_loss"]:
                    best = False
        with open(epoch_data_path, "a") as f:
            data = {}
            data["epoch"] = n_epoch
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
'''
import json
from pathlib import Path
import torch
import yaml

from .audio_loader import audio_to_input
from .structure import Model
from .import_weights import ModelLoader

class Overseer:
    def __init__(self, folder_path: Path):
        self.folder_path = folder_path
        self.config_path = folder_path / "config"
        self.weight_path = folder_path / "weight"
        self.stat_path = folder_path / "stats"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._load_all()

    def _load_all(self):
        self.load_parameters()
        self._load_instrument_dict()
        self._load_preprocessor()
        self._load_classifier()

    def load_parameters(self):
        with open(self.config_path/ "parameters.yaml", "r", encoding="utf-8") as f:
            self.params = yaml.safe_load(f)
        thresholds_path = self.config_path/ "thresholds.json"
        if thresholds_path.is_file():
            with open(self.config_path/ "thresholds.json", "r", encoding="utf-8") as f:
                dict_thresholds = yaml.safe_load(f)
                thresholds = [dict_thresholds[str(i)] for i in range(self.params["n_instr"])]
                self.thresholds = torch.tensor(thresholds,
                                        device=torch.device("cpu"))
        else:
            self.thresholds = torch.full((self.params["n_instr"],), self.params["threshold"], device=torch.device("cpu"))

    def _load_instrument_dict(self):
        with open(self.config_path / "instruments.json") as f:
            self.instrument_dict = json.load(f)
            self.reverse_instrument_dict = {v: k for k, v in self.instrument_dict.items()}

    def _load_preprocessor(self):
        self.preprocessor = audio_to_input

    def _load_classifier(self):
        self.model = Model(self.params["n_instr"]).to(self.device)
        self.optimiser = torch.optim.Adam(self.model.parameters(), lr= self.params["lr"])
        if not (self.weight_path / "best.pth").exists():
            print(f"Poids non trouvés dans {self.weight_path}. Téléchargement...")
            loader = ModelLoader(
                repo_id="gandalfbob/Instru"
       
            )
            loader.load()
        checkpoint = torch.load(self.weight_path/ "checkpoint.pth", map_location=self.device, weights_only=True)
        self.model.load_state_dict(checkpoint["model_state"])
        self.optimiser.load_state_dict(checkpoint["optimizer_state"])

    def visualise_pred(self, preds):
        for i in range(len(preds)):
            print(f"{self.instrument_dict[str(i)]} : {round(float(preds[i]), 2)}, threshold: {self.thresholds[i].item()}, ratio = {round(float(preds[i]), 2)/self.thresholds[i].item()}")

    def aggregate_predictions(self, preds, min_ratio=0.6):
        """
        min_ratio = 0.2 → présent dans au moins 20% des chunks
        """
        y_bin = preds > self.thresholds
        ratio = y_bin.float().mean(dim=0)   # (n_instr,)
        y_final = ratio >= min_ratio

        return [
            self.instrument_dict[str(i)]
            for i in range(self.params["n_instr"])
            if y_final[i]
        ]


    def predict(self, wav_path):
        self.model.eval()
        chunks = self.preprocessor(
            wav_path
        )

        preds = []
        with torch.no_grad():
            for mel in chunks:
                x = mel.unsqueeze(0).to(self.device)
                y = self.model(x)
                y = torch.sigmoid(y)
                preds.append(y.cpu())
        preds = torch.cat(preds, dim=0)
        return self.aggregate_predictions(preds)
    
    def save_epoch(self, dico_epoch):
        # put this in a abstract class that the architectures are inheriting from ?
        best = True
        epoch_data_path = self.stat_path / "epoch_data.jsonl"
        with open(epoch_data_path, "r") as f:
            n_epoch = 1
            for line in f:
                n_epoch += 1
                record = json.loads(line)
                if dico_epoch["valid_loss"] > record["valid_loss"]:
                    best = False
        with open(epoch_data_path, "a") as f:
            data = {}
            data["epoch"] = n_epoch
            for key in dico_epoch.keys():
                data[key] = dico_epoch[key]
            f.write(json.dumps(data) + "\n")
        torch.save({
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimiser.state_dict(),
        }, self.weight_path / "checkpoint.pth")
        if best:
            torch.save({
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimiser.state_dict(),
        }, self.weight_path / "best.pth")