"""Inbound events: perception services and clients -> agent (POST /api/v1/triggers)."""

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field

from thea_contracts._base import Message


class TriggerSource(StrEnum):
    WAKE_WORD = "wake_word"
    AMBIENT = "ambient"
    VISION = "vision"
    PHONE = "phone"
    SCHEDULER = "scheduler"


class VoiceUtterance(Message):
    """Speech that cleared the wake-word or relevance gate. Transcript only -- never raw audio."""

    kind: Literal["voice_utterance"] = "voice_utterance"
    source: Literal[TriggerSource.WAKE_WORD, TriggerSource.AMBIENT]
    transcript: str
    room: str | None = None
    speaker: str | None = None  # None = unrecognized voice; the agent may switch to privacy mode
    confidence: float = Field(ge=0.0, le=1.0)
    # How sure the relevance filter is that this was meant for THEA (1.0 for an explicit wake word).
    addressed: float = Field(default=1.0, ge=0.0, le=1.0)


class VisionEvent(Message):
    """A camera observation that cleared the motion/person gate."""

    kind: Literal["vision_event"] = "vision_event"
    source: Literal[TriggerSource.VISION] = TriggerSource.VISION
    room: str | None = None
    label: str  # e.g. "person_entered", "package_at_door"
    summary: str | None = None  # filled in only if the expensive scene-analysis pass ran
    confidence: float = Field(ge=0.0, le=1.0)


class PhoneContext(Message):
    """Context the phone pushes on events (arriving home, focus mode changed), not continuously.

    Locations are named places resolved on the phone (geofences), never raw coordinates, so the
    agent only learns what it needs.
    """

    kind: Literal["phone_context"] = "phone_context"
    source: Literal[TriggerSource.PHONE] = TriggerSource.PHONE
    place: str | None = None  # "home", "gym", "work", or None when between places
    movement: Literal["arriving", "leaving", "stationary", "walking", "driving"] | None = None
    battery_percent: int | None = Field(default=None, ge=0, le=100)
    charging: bool | None = None
    focus_mode: str | None = None  # "sleep", "work", "do_not_disturb", ...
    now_playing: str | None = None


Trigger = Annotated[VoiceUtterance | VisionEvent | PhoneContext, Field(discriminator="kind")]
