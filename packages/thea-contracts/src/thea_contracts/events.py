"""Inbound events: perception services -> agent (POST /api/v1/triggers)."""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field

from thea_contracts._base import Message


class TriggerSource(StrEnum):
    WAKE_WORD = "wake_word"
    AMBIENT = "ambient"
    VISION = "vision"
    SCHEDULER = "scheduler"


class VoiceUtterance(Message):
    """Speech that cleared the wake-word or relevance gate. Transcript only -- never raw audio."""

    kind: Literal["voice_utterance"] = "voice_utterance"
    source: Literal[TriggerSource.WAKE_WORD, TriggerSource.AMBIENT]
    transcript: str
    room: str | None = None
    speaker: str | None = None  # None = unrecognized voice; the agent may switch to privacy mode
    confidence: float = Field(ge=0.0, le=1.0)


class VisionEvent(Message):
    """A camera observation that cleared the motion/person gate."""

    kind: Literal["vision_event"] = "vision_event"
    source: Literal[TriggerSource.VISION] = TriggerSource.VISION
    room: str | None = None
    label: str  # e.g. "person_entered", "package_at_door"
    summary: str | None = None  # filled in only if the expensive scene-analysis pass ran
    confidence: float = Field(ge=0.0, le=1.0)


Trigger = Annotated[VoiceUtterance | VisionEvent, Field(discriminator="kind")]
