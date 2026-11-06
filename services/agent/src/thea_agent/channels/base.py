"""The contract every client surface implements (web, phone, voice, desktop).

Borrowed from hermes-agent's platform-adapter ABC (gateway/platforms/base.py):
the agent runtime talks to one interface, and each surface adapts its own
transport to it. Adding a surface (say, Telegram) means one new adapter, with
no change to the runtime.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class ChannelKind(StrEnum):
    WEB = "web"
    PHONE = "phone"
    VOICE = "voice"
    DESKTOP = "desktop"


@dataclass(frozen=True)
class InboundMessage:
    channel: ChannelKind
    session_id: str
    text: str
    room: str | None = None
    received_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class OutboundMessage:
    session_id: str
    text: str
    speak: bool = False  # also voice it via the voice service


class Channel(ABC):
    kind: ChannelKind

    @abstractmethod
    async def send(self, message: OutboundMessage) -> None:
        """Deliver a reply (or a streamed chunk) back to this surface."""

    @abstractmethod
    async def request_confirmation(self, session_id: str, summary: str) -> bool:
        """Ask the user to approve a tool call flagged requires_confirm in thea.tools."""
