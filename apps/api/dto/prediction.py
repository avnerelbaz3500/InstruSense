from pydantic import BaseModel


class PredictOut(BaseModel):
    instruments: list[str]
    # scores: dict[str, float]
