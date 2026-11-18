# Conventions

## Naming

| Thing | Convention | Example |
|---|---|---|
| Top-level dirs | By kind: `apps/`, `services/`, `packages/`, `infra/`, `docs/` | `services/voice` |
| Service / app dir | Short, lowercase, what it *does* | `agent`, `voice`, `home`, `web` |
| Python distribution | `thea-<name>` (kebab) | `thea-agent` |
| Python import package | `thea_<name>` (snake), always under `src/` | `thea_agent` |
| JS packages | Bare app name (private, unpublished) | `web`, `desktop` |
| Python modules, functions, variables | `snake_case` | `context_builder.py`, `build_context()` |
| Python classes | `PascalCase`; ABCs are nouns (`Channel`), implementations are specific (`WebChannel`) | |
| TS variables, functions | `camelCase`; React components `PascalCase`; files `kebab-case.tsx` | `talk-panel.tsx` exports `TalkPanel` |
| DB schemas, tables, columns | `snake_case`, plural tables | `environment.devices` |
| JSON over the wire | `snake_case` | `"session_id"` |
| Env vars | `SCREAMING_SNAKE_CASE`, provider prefix if there is one | `ANTHROPIC_API_KEY`, `HOME_ASSISTANT_TOKEN` |
| Docs | lowercase kebab `.md`; ADRs `NNNN-title.md` | `voice-pipeline.md` |
| Git branches | `feature/<slug>`, `fix/<slug>`, `chore/<slug>` | `feature/agent-turn-loop` |

The body-part codenames (heart, senses, ...) are kept in
[overview.md](overview.md#codenames) only. Don't use them in code.

## Python

- Python 3.12. Type hints everywhere: `mypy --strict` must pass (generated
  models are exempt).
- ruff for lint and format, line length 120.
- Pydantic v2 for anything that crosses a boundary (API bodies, contracts,
  settings).
- `async` all the way down in services. Never block the event loop (use
  `httpx.AsyncClient`, and async DB calls or `run_in_threadpool`).
- Settings come from `pydantic-settings` and hold secrets only.
- No `print`; use `logging`, which is formatted in UTC.
- Comments explain *why*, not *what*. Don't write docstrings that restate the
  name.

## TypeScript / React

- Strict TypeScript. `pnpm --filter web typecheck` and `build` must pass
  before committing.
- Server Components by default. Add `'use client'` only where there's state or
  browser APIs.
- Tailwind with the tokens in `app/globals.css` (`ink`, `panel`, `ember`,
  `tide`, ...). Don't use raw hex values in components.
- Every API call goes through `lib/api-client.ts`, which handles case
  conversion, the token and error messages.
- Accessibility basics:
  - visible focus rings
  - 44 px touch targets
  - `aria-live` for status changes
  - `prefers-reduced-motion` respected

## Data and time

- Everything is **UTC**: `TIMESTAMPTZ` in Postgres, timezone-aware `datetime`
  in Python, ISO 8601 with `Z` over the wire. Convert to local time only for
  display.
- The user's timezone is a *preference* (`thea.config.timezone`), used for
  scheduling ("9 AM my time"). Don't store it next to timestamps.

## Commits and PRs

- Small, focused commits with an imperative subject line ("Add memory
  retrieval repository").
- Generated files (migrations, models, lockfiles) are committed together with
  whatever produced them.
- Never commit `.env`, `*.xlsx` or `local_seed.sql`. The pre-commit hook blocks
  them.
