"""Inbound triggers from the perception services (voice, vision). Service-to-service, same bearer token."""

from fastapi import APIRouter, status

from thea_agent.api.v1._not_implemented import not_implemented
from thea_contracts import Trigger

router = APIRouter(prefix="/triggers", tags=["triggers"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def receive_trigger(trigger: Trigger) -> None:
    not_implemented("trigger handling")
