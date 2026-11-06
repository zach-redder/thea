"""Wire contracts shared by THEA services.

Every message that crosses a service boundary (voice -> agent, agent -> home,
agent -> voice) is defined here once, so producers and consumers can't drift.
Timestamps are always UTC; JSON field names are snake_case.
"""

from thea_contracts.commands import Command, DeviceCommand, SpeakCommand
from thea_contracts.events import PhoneContext, Trigger, TriggerSource, VisionEvent, VoiceUtterance

__all__ = [
    "Command",
    "DeviceCommand",
    "PhoneContext",
    "SpeakCommand",
    "Trigger",
    "TriggerSource",
    "VisionEvent",
    "VoiceUtterance",
]
