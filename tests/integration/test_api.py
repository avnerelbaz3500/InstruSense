def test_health(api_client):
    r = api_client.get("/health")
    assert r.status_code == 200


def test_root(api_client):
    r = api_client.get("/")
    assert r.status_code == 200


def test_predict_no_file(api_client):
    r = api_client.post("/api/predict")
    assert r.status_code == 422
