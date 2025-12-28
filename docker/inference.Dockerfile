FROM python:3.11-slim

WORKDIR /app

# Dépendances système pour audio
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn torch torchaudio soundfile pyyaml

COPY apps/inference /app/apps/inference
COPY models /app/models

EXPOSE 8001

CMD ["uvicorn", "apps.inference.server:app", "--host", "0.0.0.0", "--port", "8001"]