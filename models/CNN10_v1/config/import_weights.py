#This file downloads the weights of our latest CNN model from hugging face, and put them in the folder weight

from pathlib import Path
import shutil
import torch
from loguru import logger
from huggingface_hub import hf_hub_download


class ModelLoader:
    def __init__(
        self,
        repo_id: str,
        revision: str = "main",
    ):
        self.repo_id = repo_id
        self.revision = revision

        # Destination finale
        self.model_dir = Path("models/CNN10_v1/weight")
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self.best_path = self.model_dir / "best.pth"
        self.checkpoint_path = self.model_dir / "checkpoint.pth"

        self.state_dict = None

    def _download_and_copy(self, hf_path: str, dst_path: Path):
        """
        Télécharge via le cache HF puis copie UNIQUEMENT le fichier
        vers la destination finale (sans recréer les dossiers).
        """
        cached_file = hf_hub_download(
            repo_id=self.repo_id,
            filename=hf_path,
            revision=self.revision,
        )

        shutil.copyfile(cached_file, dst_path)
        logger.info(f"Copié : {dst_path}")

    def load(self):
        if self.state_dict is not None:
            return self.state_dict

        logger.info("Téléchargement des fichiers depuis Hugging Face")

        # Téléchargement + copie propre
        self._download_and_copy(
            "CNN6_IRMAS/weight/best.pth",
            self.best_path,
        )

        self._download_and_copy(
            "CNN6_IRMAS/weight/checkpoint.pth",
            self.checkpoint_path,
        )

        # Chargement du modèle
        self.state_dict = torch.load(
            self.best_path,
            map_location="cpu",
            weights_only=True,
        )

        if not isinstance(self.state_dict, dict):
            raise RuntimeError("Le fichier chargé n'est pas un state_dict")

        logger.info(f"{len(self.state_dict)} tenseurs chargés depuis best.pth")
        return self.state_dict


if __name__ == "__main__":
    loader = ModelLoader(repo_id="gandalfbob/Instru")
    weights = loader.load()
