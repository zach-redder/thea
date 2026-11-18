import pytest

from thea_agent.runtime.persona_guard import find_banned
from thea_agent.runtime.prompt_loader import load_core_fallback


def test_core_prompt_fallback_loads_and_is_the_persona() -> None:
    prompt = load_core_fallback()

    assert prompt.startswith("You are THEA.")
    assert "Never do any of these" in prompt


@pytest.mark.parametrize(
    "reply",
    [
        "I'm an AI assistant, how can I help you today?",
        "Certainly! I'd be happy to help with that.",
        "Done. Is there anything else I can help with?",
        "As an AI, I don't have preferences.",
        "I’d be happy to look into it.",  # typographic apostrophe
    ],
)
def test_boilerplate_replies_are_flagged(reply: str) -> None:
    assert find_banned(reply)


@pytest.mark.parametrize(
    "reply",
    [
        "Yeah, most of the afternoon. Take the jacket.",
        "Rough one? You were up until 2. Want me to clear the evening?",
        "Done, living room's at 30%.",
    ],
)
def test_human_replies_pass(reply: str) -> None:
    assert find_banned(reply) == []
