from fastapi import APIRouter

router = APIRouter()

@router.post("/predict")
def predict():
    return {"detail": "endpoint predict placeholder"}
