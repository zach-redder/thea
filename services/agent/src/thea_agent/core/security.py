"""Bearer-token auth shared by every non-health endpoint.

One personal token is enough for a single-user assistant that's only reachable
on the LAN or over Tailscale (see docs/security.md). Per-device tokens can come
later without changing callers.
"""

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from thea_agent.core.config import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)


def require_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    expected = settings.thea_api_token
    if expected is None:
        # Fail closed: an unconfigured token must never mean "open to everyone".
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "THEA_API_TOKEN is not configured")
    if credentials is None or not secrets.compare_digest(credentials.credentials, expected.get_secret_value()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid or missing token")
