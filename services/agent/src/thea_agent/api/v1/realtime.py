"""WebSocket for live clients: streamed replies, push-to-talk audio, approvals and proactive pushes.

Browsers can't set an Authorization header on a WebSocket, so the token travels
as the first message: {"type": "auth", "token": "..."}.
"""

from fastapi import APIRouter, WebSocket, status

router = APIRouter(tags=["realtime"])


@router.websocket("/ws")
async def realtime(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_json({"type": "error", "detail": "realtime channel is not implemented yet"})
    await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
