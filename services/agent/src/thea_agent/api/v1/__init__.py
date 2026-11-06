from fastapi import APIRouter, Depends

from thea_agent.api.v1 import approvals, chat, memory, realtime, sessions, triggers
from thea_agent.core.security import require_token

router = APIRouter(prefix="/api/v1")
for module in (chat, sessions, memory, approvals, triggers):
    router.include_router(module.router, dependencies=[Depends(require_token)])
# The WebSocket authenticates in-band (first message); see realtime.py.
router.include_router(realtime.router)
