from services.prediction_service import PredictionService


def test_service_url():
    service = PredictionService()
    assert "8001" in service.inference_url
