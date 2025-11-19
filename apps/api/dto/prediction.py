from pydantic import BaseModel

class PredictIn(BaseModel):
    audio_path: str

class PredictOut(BaseModel):
    instrument: str
    confidence: float
