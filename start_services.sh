#!/bin/bash

# Lancer API
uv run uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 &

# Lancer Inference
uv run uvicorn apps.inference.server:app --host 0.0.0.0 --port 8001 &

# Lancer Interface (port exposé)
uv run uvicorn apps.interface.server:app --host 0.0.0.0 --port 3000

# Garder le conteneur actif
wait
