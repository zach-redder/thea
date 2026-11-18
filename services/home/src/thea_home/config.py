"""Secrets and addresses only; behavior comes from the agent (which reads thea.config)."""

from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=REPO_ROOT / ".env", extra="ignore")

    agent_url: str = "http://localhost:8000"
    thea_api_token: SecretStr | None = None
    home_assistant_url: str = "http://homeassistant.local:8123"
    home_assistant_token: SecretStr | None = None
    mqtt_broker_url: str = "mqtt://localhost:1883"


@lru_cache
def get_settings() -> Settings:
    return Settings()
