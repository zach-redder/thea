"""Vision service entrypoint: a FastAPI app for health and nothing else yet (it only publishes)."""

from importlib.metadata import version

import uvicorn
from fastapi import FastAPI

SERVICE = "thea-vision"
PORT = 8020


def create_app() -> FastAPI:
    app = FastAPI(title="THEA Vision", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": SERVICE, "version": version(SERVICE)}

    return app


app = create_app()


def run() -> None:
    uvicorn.run("thea_vision.main:app", host="0.0.0.0", port=PORT)  # noqa: S104 -- LAN/container service
