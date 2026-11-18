from fastapi.testclient import TestClient

from thea_home.main import create_app


def test_health_is_public() -> None:
    response = TestClient(create_app()).get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "thea-home"


def test_commands_require_a_token() -> None:
    response = TestClient(create_app()).post(
        "/api/v1/commands", json={"kind": "device", "device": "lamp", "action": "turn_on"}
    )

    assert response.status_code in (401, 503)
