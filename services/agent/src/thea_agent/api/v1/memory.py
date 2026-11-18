"""Read-only views for the dashboard's memory browser. Writes only happen via the agent's own memory pass."""

from fastapi import APIRouter

from thea_agent.api.v1._not_implemented import not_implemented
from thea_agent.api.v1.schemas import ListRequest

router = APIRouter(tags=["memory"])


@router.post("/memories/list")
async def list_memories(request: ListRequest) -> None:
    not_implemented("memory listing")


@router.get("/integrations")
async def list_integrations() -> None:
    """thea.integrations connection status, for the dashboard's health page."""
    not_implemented("integration status")
