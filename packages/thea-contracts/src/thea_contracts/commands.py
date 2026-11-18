"""Outbound commands: agent -> actuator services. Actuators reply with success/failure only."""

from typing import Annotated, Any, Literal

from pydantic import Field

from thea_contracts._base import Message


class SpeakCommand(Message):
    """Say something out loud. Handled by the voice service (POST /api/v1/speak)."""

    kind: Literal["speak"] = "speak"
    text: str
    rooms: list[str] = Field(default_factory=list)  # empty = wherever the user currently is
    voice: str | None = None  # None = thea.config.voice


class DeviceCommand(Message):
    """Change a device's state. Handled by the home service (POST /api/v1/commands)."""

    kind: Literal["device"] = "device"
    device: str  # environment.devices name or Home Assistant entity_id
    action: str  # e.g. "turn_on", "set_temperature"
    params: dict[str, Any] = Field(default_factory=dict)


Command = Annotated[SpeakCommand | DeviceCommand, Field(discriminator="kind")]
