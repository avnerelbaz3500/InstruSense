import pytest


def test_health(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_no_file(api_client):
    response = api_client.post("/predict")
    assert response.status_code == 422


def test_predict_wrong_content_type(api_client):
    response = api_client.post(
        "/predict",
        files={"file": ("test.txt", b"not audio", "text/plain")}
    )
    assert response.status_code == 400
