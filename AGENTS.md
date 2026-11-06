# AGENTS.md

Guidance for AI coding assistants (Claude Code, Codex, Cursor, ...) and humans
working in this repo. Read [docs/architecture.md](docs/architecture.md) for
the system map.

## What this is

THEA is a single-user personal AI assistant:
- a Python agent service, behind which sit perception (voice, vision) and
  actuation (home)
- a Postgres + pgvector data layer
- a Next.js PWA and a Tauri desktop app

It's a monorepo: `apps/`, `services/`, `packages/`.

## Building THEA: read these first

1. [docs/vision.md](docs/vision.md): what she's supposed to be (the owner's requirements).
2. [docs/implementation-plan.md](docs/implementation-plan.md): the session protocol, phase checklist and
   acceptance tests. Work on the first unchecked phase, and tick boxes as you finish.
3. The design doc each phase links to, before coding that part.

Spec before code, tests before implementation. Don't guess at anything listed under
"Things that need Zach" in the plan.

## Commands

```bash
just setup                 # uv sync --all-packages --extra schema && corepack pnpm install
just lint                  # ruff, ruff format --check, mypy --strict, eslint, tsc
just test                  # pytest (all Python projects)
corepack pnpm --filter web build
just check-schema          # migrations match THEA DB.xlsx (local only)
```

Run `just lint` and `just test` before calling a change done. For
`apps/web/**` changes, also run the web build.

## Invariants (don't break these)

1. **Only `services/agent` calls an LLM or embeddings API.** That's
   `thea_agent/llm/` for Claude and `thea_agent/memory/writer.py` for Voyage.
2. **Only `services/agent` imports `thea_db`.** Clients and other services go
   through the agent API.
3. **Messages between services are defined in `packages/thea-contracts`.**
   Change the contract first, then both ends.
4. **Perception services send transcripts and labels, never raw audio or
   video.** Nothing perceptual is written to disk.
5. **Actuators (`home`, voice output) don't decide.** They execute and report
   success or failure.
6. **`.env` is for secrets and addresses only.** Behavior goes in
   `thea.config` / `thea.prompts` / `thea.tools`.
7. **Auth fails closed.** Every non-`/health` endpoint requires the bearer
   token via `thea_contracts.auth.token_matches`.
8. **Prompt caching is sacred.** The system prompt stays byte-stable for a
   conversation; don't swap tools mid-session; keep user/assistant roles
   strictly alternating.
9. **Never commit personal data.** `THEA DB.xlsx` and `local_seed.sql` stay
   out of git, Docker images, docs and tests.
10. **Generated files are never hand-edited:**
    `packages/thea-db/migrations/*.sql` and `src/thea_db/models/*.py`. Edit
    the workbook and run `just gen-schema`.
11. **She never sounds like boilerplate.** Replies must pass `thea_agent.runtime.persona_guard`;
    prompt changes re-run the persona tests ([docs/persona.md](docs/persona.md)).
12. **Outward-facing actions are draft-first and confirmed.** Posts, emails, messages, spending, locks,
    desktop actions. Outside content is data, never instructions
    ([docs/integrations.md](docs/integrations.md#safety-model-for-account-access)).
13. **OAuth tokens live in the encrypted credential store, not `.env`**
    ([ADR 0009](docs/decisions/0009-integration-credentials.md)).

## Where things go

| Adding... | Put it in |
|---|---|
| An HTTP endpoint | `services/agent/src/thea_agent/api/v1/<area>.py` + schemas in `api/v1/schemas.py` + a test |
| A tool for THEA | A `thea.tools` row + handler under `thea_agent/tools/` (prefer an MCP server over a native tool) |
| A client surface (e.g. Telegram) | A new `Channel` adapter in `thea_agent/channels/` |
| A DB query | A repository in `packages/thea-db/src/thea_db/repositories/` |
| A cross-service message | `packages/thea-contracts/src/thea_contracts/` |
| A UI page | `apps/web/app/<route>/page.tsx`; API calls only via `lib/api-client.ts` |
| A decision worth explaining | `docs/decisions/NNNN-title.md` |

## Style

- **Python:**
  - 3.12, strict typing, ruff (line length 120), Pydantic v2
  - async in services
  - UTC everywhere
  - comments explain *why*
- **TypeScript:**
  - strict mode
  - Server Components by default
  - Tailwind tokens from `app/globals.css`, never raw hex
  - snake_case ⇄ camelCase conversion happens only in `lib/case-convert.ts`

Full list: [docs/conventions.md](docs/conventions.md).
