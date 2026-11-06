"""Tool registry: the single place the runtime discovers tools.

Modeled on hermes-agent's tools/registry.py. Each tool declares a JSON schema,
a handler, and an availability check, so tools for unconfigured integrations
never reach the model (every offered tool costs tokens on every call).
Enabled flags and requires_confirm come from thea.tools rows. Code supplies the
handler; the DB decides whether and how it's offered.
"""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

ToolHandler = Callable[[dict[str, Any]], Awaitable[str]]


def _always_available() -> bool:
    return True


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: ToolHandler
    requires_confirm: bool = False
    is_available: Callable[[], bool] = _always_available


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    def available(self) -> list[ToolSpec]:
        return [spec for spec in self._tools.values() if spec.is_available()]

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)
