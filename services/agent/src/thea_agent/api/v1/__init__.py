from fastapi import APIRouter, Depends

from thea_agent.api.v1 import approvals, chat, control, memory, phone, realtime, sessions, stats, triggers
from thea_agent.core.security import require_token

router = APIRouter(prefix="/api/v1")
for module in (chat, sessions, memory, approvals, triggers, phone, stats, control):
    router.include_router(module.router, dependencies=[Depends(require_token)])
# Browsers can't send headers on a WebSocket, so /ws checks the token in its first message (realtime.py).
router.include_router(realtime.router)
