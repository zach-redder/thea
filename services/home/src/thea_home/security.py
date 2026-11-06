"""Bearer-token check for endpoints the agent calls. Only /health is public."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from thea_contracts.auth import token_matches
from thea_home.config import Settings, get_settings

_bearer = HTTPBearer(auto_error=False)


def require_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> None:
    expected = settings.thea_api_token.get_secret_value() if settings.thea_api_token else None
    if expected is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "THEA_API_TOKEN is not configured")
    if not token_matches(credentials.credentials if credentials else None, expected):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid or missing token")
