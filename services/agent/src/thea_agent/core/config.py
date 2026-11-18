"""Process settings: secrets and service addresses only.

Behavior (model choice, voice, wake word, DND window, privacy mode) lives in the
thea.config row so it can change at runtime without a redeploy. Don't add
behavioral flags here. See docs/decisions/0008-env-for-secrets-only.md.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# services/agent/src/thea_agent/core/config.py -> repo root
REPO_ROOT = Path(__file__).resolve().parents[5]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", extra="ignore")

    environment: Literal["development", "production", "test"] = "development"
    log_level: str = "INFO"

    # Bearer token every client (web, phone, desktop, other services) must send.
    thea_api_token: SecretStr | None = None
    # Origins allowed to call the API from a browser (the web app, the Tauri webview).
    cors_origins: list[str] = ["http://localhost:3000", "tauri://localhost", "http://tauri.localhost"]

    database_url: str = "postgresql://thea:thea@localhost:5432/thea"
    redis_url: str = "redis://localhost:6379/0"

    anthropic_api_key: SecretStr | None = None
    voyage_api_key: SecretStr | None = None

    voice_service_url: str = "http://localhost:8010"
    home_service_url: str = "http://localhost:8030"


@lru_cache
def get_settings() -> Settings:
    return Settings()
