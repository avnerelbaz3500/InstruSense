import sys
import tempfile
from pathlib import Path
from typing import Any


class InferenceAdapter:
    model: Any

    def __init__(self, model_dir: str) -> None:
        model_path = Path(model_dir)
        sys.path.insert(0, str(model_path / "config"))

        from models.CNN10_v1.config.overseer import Overseer

        self.model = Overseer(model_path)

    def predict(self, audio_bytes: bytes) -> dict[str, list[str]]:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        instruments = self.model.predict(tmp_path)
        Path(tmp_path).unlink()

        return {"instruments": instruments}
