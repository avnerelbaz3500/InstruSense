import pytest


def test_health(inference_client):
    response = inference_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
