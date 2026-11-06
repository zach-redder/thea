"""Emergency stop: cancel in-flight turns and any queued actions."""

from fastapi import APIRouter

from thea_agent.api.v1._not_implemented import not_implemented

router = APIRouter(tags=["control"])


@router.post("/stop")
async def stop() -> None:
    not_implemented("emergency stop")
