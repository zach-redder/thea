import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from thea_agent.api.v1 import health
from thea_agent.api.v1 import router as v1_router
from thea_agent.core.config import Settings, get_settings
from thea_agent.core.logging import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title="THEA Agent", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(health.router)
    app.include_router(v1_router)
    return app


app = create_app()


def run() -> None:
    uvicorn.run("thea_agent.main:app", host="0.0.0.0", port=8000)  # noqa: S104 -- LAN/container service
