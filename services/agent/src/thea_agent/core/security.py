"""Bearer-token auth shared by every non-health endpoint.

One personal token is enough for a single-user assistant that's only reachable
on the LAN or over Tailscale (see docs/security.md). Per-device tokens can come
later without changing callers.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from thea_agent.core.config import Settings, get_settings
from thea_contracts.auth import token_matches

_bearer = HTTPBearer(auto_error=False)


def configured_token(settings: Settings) -> str | None:
    return settings.thea_api_token.get_secret_value() if settings.thea_api_token else None


def require_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    expected = configured_token(settings)
    if expected is None:
        # Fail closed: an unconfigured token must never mean "open to everyone".
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "THEA_API_TOKEN is not configured")
    if not token_matches(credentials.credentials if credentials else None, expected):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid or missing token")
