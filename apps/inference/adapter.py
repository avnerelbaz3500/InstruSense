import sys
import tempfile
from pathlib import Path


class InferenceAdapter:
    def __init__(self, model_dir: str):
        model_path = Path(model_dir)
        sys.path.insert(0, str(model_path / "config"))

        from models.CNN10_v1.config.overseer import Overseer

        self.model = Overseer(model_path)

    def predict(self, audio_bytes: bytes) -> dict:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        instruments = self.model.predict(tmp_path)
        Path(tmp_path).unlink()

        return {"instruments": instruments}
