from pydantic import TypeAdapter

from thea_contracts import Command, DeviceCommand, SpeakCommand, Trigger, TriggerSource, VoiceUtterance


def test_trigger_round_trips_through_json_and_keeps_its_type() -> None:
    sent = VoiceUtterance(source=TriggerSource.WAKE_WORD, transcript="turn on the lights", confidence=0.9)

    received: Trigger = TypeAdapter(Trigger).validate_json(sent.model_dump_json())

    assert received == sent
    assert isinstance(received, VoiceUtterance)


def test_command_discriminator_picks_the_right_model() -> None:
    adapter: TypeAdapter[Command] = TypeAdapter(Command)

    assert isinstance(adapter.validate_python({"kind": "speak", "text": "hi"}), SpeakCommand)
    assert isinstance(adapter.validate_python({"kind": "device", "device": "lamp", "action": "turn_on"}), DeviceCommand)


def test_timestamps_are_utc() -> None:
    assert SpeakCommand(text="hi").created_at.utcoffset() is not None
