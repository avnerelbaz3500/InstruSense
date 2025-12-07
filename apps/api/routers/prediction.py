from fastapi import APIRouter
from typing import Dict

from apps.api.dto.prediction import PredictIn, PredictOut

router = APIRouter()

@router.post("/predict", response_model=PredictOut)
async def predict(input_data: PredictIn)-> PredictOut:  # convertir les données en objet PredictIn (comme avner a fait)
    # Récupérer les données de la requête
    # appeler le service de prédiction
    # convertir la réponse en objet PredictOut
    # retourner la réponse
    return {"detail": "endpoint predict placeholder"}
