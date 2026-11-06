"""Human-in-the-loop: approve or deny a pending tool call (requires_confirm in thea.tools)."""

from fastapi import APIRouter

from thea_agent.api.v1._not_implemented import not_implemented
from thea_agent.api.v1.schemas import ApprovalDecision

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.post("/resolve")
async def resolve(decision: ApprovalDecision) -> None:
    not_implemented("tool approvals")
