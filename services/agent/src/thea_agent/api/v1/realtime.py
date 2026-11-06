"""WebSocket for live clients: streamed replies, push-to-talk audio, approvals and proactive pushes.

Browsers can't set an Authorization header on a WebSocket, so the token travels
as the first message: {"type": "auth", "token": "..."}. Nothing else is read or
sent until that check passes.
"""

import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status

from thea_agent.core.config import Settings, get_settings
from thea_agent.core.security import configured_token
from thea_contracts.auth import token_matches

router = APIRouter(tags=["realtime"])
AUTH_TIMEOUT_SECONDS = 5.0


async def _authenticate(websocket: WebSocket, expected: str | None) -> bool:
    try:
        first = await asyncio.wait_for(websocket.receive_json(), timeout=AUTH_TIMEOUT_SECONDS)
    except (TimeoutError, ValueError, WebSocketDisconnect):
        return False
    token = first.get("token") if isinstance(first, dict) and first.get("type") == "auth" else None
    return token_matches(token if isinstance(token, str) else None, expected)


@router.websocket("/ws")
async def realtime(websocket: WebSocket, settings: Annotated[Settings, Depends(get_settings)]) -> None:
    await websocket.accept()
    if not await _authenticate(websocket, configured_token(settings)):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.send_json({"type": "error", "detail": "realtime channel is not implemented yet"})
    await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
