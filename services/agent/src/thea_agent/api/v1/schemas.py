"""Request/response models for the public API. JSON is snake_case and timestamps are UTC."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from thea_agent.channels.base import ChannelKind


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str
    version: str


class DependencyStatus(BaseModel):
    name: str
    ok: bool
    detail: str | None = None


class DetailedHealthResponse(HealthResponse):
    dependencies: list[DependencyStatus]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None  # None = start a new session
    channel: ChannelKind = ChannelKind.WEB
    speak: bool = False  # also say the reply out loud through the voice service


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    created_at: datetime


class ListRequest(BaseModel):
    search: str | None = None
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=200)


class ApprovalDecision(BaseModel):
    approval_id: str
    approved: bool
