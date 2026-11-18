# 0002: Descriptive names in code; body-part names stay as codenames

**Status:** accepted (2026-11-05)

## Context

The original names (`heart`, `senses`, `muscles`, `brain`, `body`, `bones`)
carry the project's personality, but they don't say what the code does, and
they split one concern across two folders: speech *input* lived in `senses`
and speech *output* in `muscles`. New contributors (and AI assistants) have
to learn a mapping before they can find anything.

## Decision

- Folders and packages are named for what they do: `agent`, `voice`,
  `vision`, `home`, `thea-db`, `web`, `desktop`.
- Voice input and output merge into one `voice` service, the standard shape
  for voice pipelines (one process owns the audio device in both directions).
  Vision splits out of `senses` because it has a different runtime and
  different hardware.
- The anatomy names survive as **codenames** in one table in
  [`docs/overview.md`](../overview.md#codenames), and nowhere in code.

## Consequences

- The layout explains itself, and searching for "voice" finds voice.
- The old names only appear in `docs/archive/` and the codename table.
