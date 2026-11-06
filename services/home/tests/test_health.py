from fastapi.testclient import TestClient

from thea_home.main import create_app


def test_health() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "thea-home"
