import os
import httpx

INFERENCE_URL = os.getenv("INFERENCE_URL", "http://localhost:8001/infer")


class PredictionService:
    def __init__(self, inference_url: str = INFERENCE_URL) -> None:
        self.inference_url = inference_url

    async def predict(self, audio_bytes: bytes) -> dict[str, list[str]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
            response = await client.post(self.inference_url, files=files)
            return response.json()
