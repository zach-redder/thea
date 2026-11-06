from fastapi import APIRouter

from thea_agent.api.v1._not_implemented import not_implemented
from thea_agent.api.v1.schemas import ListRequest

router = APIRouter(tags=["sessions"])


@router.post("/sessions/list")
async def list_sessions(request: ListRequest) -> None:
    not_implemented("session listing")


@router.get("/session")
async def get_session(id: str) -> None:
    not_implemented("session detail")
