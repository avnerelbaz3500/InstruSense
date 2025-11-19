#!/usr/bin/env python3
"""
generate_structure_v2.py
Génère l'arborescence InstruSense v2, avec logging propre.
"""

import os
import logging
from pathlib import Path
import stat

# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("generator")

# -----------------------------------------------------------------------------
# Project name & file map
# -----------------------------------------------------------------------------

PROJECT_NAME = "InstruSense"

FILES = {
    # --- API ---
    "apps/api/main.py": '''from fastapi import FastAPI
app = FastAPI(title="InstruSense API")

@app.get("/health")
def health():
    return {"status": "ok"}
''',

    "apps/api/routers/prediction.py": '''from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
def predict():
    return {"detail": "endpoint predict placeholder"}
''',

    "apps/api/dto/prediction.py": '''from pydantic import BaseModel

class PredictIn(BaseModel):
    audio_path: str

class PredictOut(BaseModel):
    instrument: str
    confidence: float
''',

    "apps/api/dependencies.py": '''# Dépendances FastAPI (loader de modèle, etc.)
def get_model():
    raise NotImplementedError
''',

    "apps/api/config.py": '''API_HOST = "0.0.0.0"
API_PORT = 8000
''',

    # --- Inference ---
    "apps/inference/server.py": '''from fastapi import FastAPI
app = FastAPI(title="InstruSense Inference")

@app.get("/health")
def health():
    return {"status": "inference ok"}
''',

    "apps/inference/adapter.py": '''def predict_from_bytes(audio_bytes):
    raise NotImplementedError
''',

    "apps/inference/config.py": '''MODEL_PATH = "/models/instrument_model.pkl"
''',

    # --- Training ---
    "apps/training/train_model.py": '''def main():
    print("Train script placeholder")

if __name__ == "__main__":
    main()
''',

    "apps/training/dataset_loader.py": '''def load_dataset(path):
    raise NotImplementedError
''',

    # --- Core ---
    "core/audio/processor.py": '''def load_audio(path):
    raise NotImplementedError
''',

    "core/audio/analyzer.py": '''def extract_features(waveform, sr):
    raise NotImplementedError
''',

    "core/ml/model_loader.py": '''import pickle

_model_cache = None

def load_model(path):
    global _model_cache
    if _model_cache is None:
        with open(path, "rb") as f:
            _model_cache = pickle.load(f)
    return _model_cache
''',

    "core/ml/predictor.py": '''def predict(model, features):
    raise NotImplementedError
''',

    "core/ml/postprocess.py": '''def to_response(pred):
    return {"instrument": str(pred), "confidence": 1.0}
''',

    "core/interfaces/model_loader_port.py": '''from typing import Any

class ModelLoaderPort:
    def load(self, path: str) -> Any:
        raise NotImplementedError
''',

    "core/interfaces/predictor_port.py": '''class PredictorPort:
    def predict(self, features):
        raise NotImplementedError
''',

    "core/interfaces/audio_port.py": '''class AudioPort:
    def load(self, path: str):
        raise NotImplementedError
''',

    "core/exceptions.py": '''class InferenceError(Exception):
    pass
''',

    # --- Services ---
    "services/prediction_service.py": '''def predict_from_path(path, model):
    raise NotImplementedError
''',

    "services/audio_adapter.py": '''def load_and_process(path):
    raise NotImplementedError
''',

    "services/model_loader_adapter.py": '''def load(path):
    raise NotImplementedError
''',

    # --- Infra ---
    "infra/logging/config.py": '''import logging

def configure_logging():
    logging.basicConfig(level=logging.INFO)
''',

    "infra/settings/base.py": '''import os

ENV = os.getenv("ENV", "dev")
MODEL_DIR = os.getenv("MODEL_DIR", "/models")
''',

    "infra/utils/paths.py": '''from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
''',

    # --- Models ---
    "models/v1/instrument_model.pkl": None,

    # --- Data ---
    "data/raw/.gitkeep": "",
    "data/processed/.gitkeep": "",
    "data/features/.gitkeep": "",

    # --- Docker ---
    "docker/api.Dockerfile": '''FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install fastapi uvicorn
EXPOSE 8000
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
''',

    "docker/inference.Dockerfile": '''FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install fastapi uvicorn
EXPOSE 8001
CMD ["uvicorn", "apps.inference.server:app", "--host", "0.0.0.0", "--port", "8001"]
''',

    "docker/training.Dockerfile": '''FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install numpy scipy scikit-learn
CMD ["python", "apps/training/train_model.py"]
''',

    "docker/docker-compose.yml": '''version: "3.9"

services:
  api:
    build:
      context: ..
      dockerfile: docker/api.Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ..:/app
      - models:/models

  inference:
    build:
      context: ..
      dockerfile: docker/inference.Dockerfile
    ports:
      - "8001:8001"
    volumes:
      - ..:/app
      - models:/models

  training:
    build:
      context: ..
      dockerfile: docker/training.Dockerfile
    volumes:
      - ..:/app
      - models:/models

volumes:
  models:
''',

    # --- Root ---
    ".env.example": '''ENV=dev
MODEL_DIR=/models
''',

    "README.md": f"# {PROJECT_NAME}\nArchitecture générée automatiquement.\n",
    "pyproject.toml": '''[tool.uv]
name = "instru-sense"
version = "0.1.0"
''',
    ".gitignore": '''__pycache__/
.env
''',

    # --- Scripts ---
    "scripts/dev/start_dev.sh": '''#!/usr/bin/env bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
''',

    "tests/unit/.gitkeep": "",
    "tests/integration/.gitkeep": "",
    "tests/e2e/.gitkeep": "",
}

# -----------------------------------------------------------------------------
# Write helpers
# -----------------------------------------------------------------------------

def write_file(path: Path, content: str | None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if content is None:
        path.write_bytes(b"")
    else:
        path.write_text(content, encoding="utf-8")
    if path.suffix == ".sh":
        mode = path.stat().st_mode
        path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# -----------------------------------------------------------------------------
# Main generator
# -----------------------------------------------------------------------------

def main(base_dir: str = "."):
    base = Path(base_dir).resolve()
    log.info(f"Starting generation in: {base}")

    for rel_path, content in FILES.items():
        target = base / rel_path
        if target.exists():
            log.warning(f"Skipping existing: {rel_path}")
            continue

        write_file(target, content)
        log.info(f"Created: {rel_path}")

    # extra top-level folders
    for folder in ["apps", "core", "infra", "services", "models", "data", "docker", "scripts", "tests"]:
        (base / folder).mkdir(exist_ok=True)

    log.info("Generation complete.")

if __name__ == "__main__":
    main()
