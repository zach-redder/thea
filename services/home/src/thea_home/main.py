"""Home service entrypoint: a FastAPI app for health and device commands (DeviceCommand)."""

from importlib.metadata import version

import uvicorn
from fastapi import Depends, FastAPI

from thea_contracts import DeviceCommand
from thea_home.security import require_token

SERVICE = "thea-home"
PORT = 8030


def create_app() -> FastAPI:
    app = FastAPI(title="THEA Home", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": SERVICE, "version": version(SERVICE)}

    @app.post("/api/v1/commands", status_code=501, dependencies=[Depends(require_token)])
    async def execute(command: DeviceCommand) -> dict[str, str]:
        """Carry out a device command and report success/failure only."""
        return {"detail": "device control is not implemented yet"}

    return app


app = create_app()


def run() -> None:
    uvicorn.run("thea_home.main:app", host="0.0.0.0", port=PORT)  # noqa: S104 -- LAN/container service
