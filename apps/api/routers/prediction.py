from fastapi import APIRouter
from typing import Dict

from apps.api.dto.prediction import PredictIn, PredictOut
from services.prediction_service import predict_from_path
from core.ml.model_loader import load_model

router = APIRouter()

@router.post("/predict", response_model=PredictOut)
def predict(input_data: str)-> PredictOut:  # convertir les données en objet PredictIn (comme avner a fait)
    # Récupérer les données de la requête
    path =PredictIn(audio_path=input_data)
    model = load_model("C:/Users/asus/InstruSense/models/v1/instrument_model.pkl")
    # appeler le service de prédiction
    result = predict_from_path(path=path, model=model)
    output = PredictOut(instrument=result['instrument'], confidence=result['confidence'])
    # convertir la réponse en objet PredictOut
    # retourner la réponse
    return {"detail": "endpoint predict placeholder"}
