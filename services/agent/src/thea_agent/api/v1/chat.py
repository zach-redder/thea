"""Text chat: the endpoint the web app, the phone PWA and iOS Shortcuts call."""

from fastapi import APIRouter

from thea_agent.api.v1._not_implemented import not_implemented
from thea_agent.api.v1.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(request: ChatRequest) -> ChatResponse:
    not_implemented("chat")


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> None:
    """Same as /chat, but the reply streams back as Server-Sent Events."""
    not_implemented("streaming chat")
