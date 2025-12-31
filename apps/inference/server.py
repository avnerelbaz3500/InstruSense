from fastapi import FastAPI, UploadFile, File
from .config import MODEL_PATH
from .adapter import InferenceAdapter

app = FastAPI(title="InstruSense Inference Service")

adapter = InferenceAdapter(MODEL_PATH)


@app.post("/infer")
async def infer(file: UploadFile = File(...)) -> dict[str, list[str]]:
    audio_bytes = await file.read()
    return adapter.predict(audio_bytes)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
