from fastapi import APIRouter, UploadFile, File, Depends
from ..dto.prediction import PredictOut
from ..dependencies import get_prediction_service
from services.prediction_service import PredictionService


router = APIRouter()


@router.post("/predict", response_model=PredictOut)
async def predict(
    file: UploadFile = File(...),
    service: PredictionService = Depends(get_prediction_service)
)-> PredictOut:
    audio_bytes = await file.read()
    result = await service.predict(audio_bytes)
    return PredictOut(**result)