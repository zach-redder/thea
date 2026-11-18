"""Loads THEA's system prompts.

Prompts live in thea.prompts so her voice can be tuned without a deploy. When the database has no
active `core` prompt (first run, tests), the versioned fallback shipped in prompts/core.md is used.

Selecting the situational prompt (morning brief, guest present, ...) from thea.prompts is not
implemented yet. See docs/persona.md#how-the-prompt-is-built.
"""

from importlib.resources import files


def load_core_fallback() -> str:
    return files("thea_agent.runtime").joinpath("prompts", "core.md").read_text(encoding="utf-8").strip()
