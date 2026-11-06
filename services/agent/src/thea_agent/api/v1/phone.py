"""Phone -> THEA: context pushed by automations, and things shared from the share sheet.

THEA -> phone goes the other way, over Web Push (docs/integrations.md#phone).
"""

from fastapi import APIRouter, status

from thea_agent.api.v1._not_implemented import not_implemented
from thea_agent.api.v1.schemas import ShareRequest
from thea_contracts import PhoneContext

router = APIRouter(prefix="/phone", tags=["phone"])


@router.post("/context", status_code=status.HTTP_202_ACCEPTED)
async def push_context(context: PhoneContext) -> None:
    """Arriving home, focus mode changed, battery low: events, not a constant stream."""
    not_implemented("phone context")


@router.post("/share", status_code=status.HTTP_202_ACCEPTED)
async def share(request: ShareRequest) -> None:
    not_implemented("phone share")
