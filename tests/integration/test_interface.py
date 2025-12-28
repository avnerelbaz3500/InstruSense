def test_health(interface_client):
    response = interface_client.get("/health")
    assert response.status_code == 200


def test_index(interface_client):
    response = interface_client.get("/")
    assert response.status_code == 200
    assert b"InstruSense" in response.content


def test_static_css(interface_client):
    response = interface_client.get("/static/css/style.css")
    assert response.status_code == 200
