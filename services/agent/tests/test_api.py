import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from starlette.websockets import WebSocketDisconnect

from thea_agent.core.config import Settings, get_settings
from thea_agent.main import create_app

TOKEN = "test-token"


def make_client(token: str | None) -> TestClient:
    settings = Settings(thea_api_token=SecretStr(token) if token else None, environment="test")
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    return TestClient(app)


def test_health_is_public() -> None:
    response = make_client(TOKEN).get("/health")

    assert response.status_code == 200
    assert response.json()["service"] == "thea-agent"


def test_api_rejects_a_missing_token() -> None:
    assert make_client(TOKEN).post("/api/v1/chat", json={"message": "hi"}).status_code == 401


def test_api_fails_closed_when_no_token_is_configured() -> None:
    assert make_client(None).post("/api/v1/chat", json={"message": "hi"}).status_code == 503


def test_unbuilt_endpoints_report_501() -> None:
    response = make_client(TOKEN).post(
        "/api/v1/chat", json={"message": "hi"}, headers={"Authorization": f"Bearer {TOKEN}"}
    )

    assert response.status_code == 501


def test_websocket_closes_on_a_bad_token() -> None:
    with make_client(TOKEN).websocket_connect("/api/v1/ws") as ws:
        ws.send_json({"type": "auth", "token": "wrong"})
        with pytest.raises(WebSocketDisconnect) as closed:
            ws.receive_json()

    assert closed.value.code == 1008


def test_websocket_accepts_a_good_token() -> None:
    with make_client(TOKEN).websocket_connect("/api/v1/ws") as ws:
        ws.send_json({"type": "auth", "token": TOKEN})

        assert ws.receive_json()["type"] == "error"  # authenticated; feature not built yet
