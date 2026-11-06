"""Voice service entrypoint: a FastAPI app for health and speech output (SpeakCommand)."""

from importlib.metadata import version

import uvicorn
from fastapi import FastAPI

from thea_contracts import SpeakCommand

SERVICE = "thea-voice"
PORT = 8010


def create_app() -> FastAPI:
    app = FastAPI(title="THEA Voice", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": SERVICE, "version": version(SERVICE)}

    @app.post("/api/v1/speak", status_code=501)
    async def speak(command: SpeakCommand) -> dict[str, str]:
        """Synthesize and play speech in the requested rooms. See docs/voice-pipeline.md."""
        return {"detail": "speech output is not implemented yet"}

    return app


app = create_app()


def run() -> None:
    uvicorn.run("thea_voice.main:app", host="0.0.0.0", port=PORT)  # noqa: S104 -- LAN/container service
