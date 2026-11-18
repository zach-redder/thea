"""Cheap deterministic check that a reply doesn't sound like an assistant-boilerplate script.

Used by persona tests today, and later as a post-generation filter that triggers a regenerate.
Deliberately blunt: the nuanced judgment of "does she sound human?" is an LLM-judged eval
(docs/persona.md#testing-does-she-sound-human).
"""

BANNED_PHRASES: tuple[str, ...] = (
    "as an ai",
    "i'm an ai assistant",
    "i am an ai assistant",
    "how can i help you today",
    "i'd be happy to",
    "i would be happy to",
    "is there anything else",
    "certainly!",
    "absolutely!",
)


def find_banned(text: str) -> list[str]:
    """Return every banned phrase present in `text` (case-insensitive, apostrophe-insensitive)."""
    normalized = text.lower().replace("’", "'")
    return [phrase for phrase in BANNED_PHRASES if phrase in normalized]
