# THEA

A personal AI assistant: a persistent presence that knows you, remembers, and
acts. She lives on a home server and reaches you through room speakers, a web
dashboard, an app on your phone, and your desktop. Closer to JARVIS than to a
chatbot.

**Status:** foundation. The schema, service skeletons, auth, CI and the web
shell are real. The agent loop, voice, home control and desktop bridge are
designed but not built. See [docs/roadmap.md](docs/roadmap.md).

## Quickstart

```bash
cp .env.example .env     # set THEA_API_TOKEN (and ANTHROPIC_API_KEY when Phase 1 lands)
just setup               # uv sync + pnpm install
just db                  # Postgres (pgvector) + Redis + migrations, in Docker
just agent               # API   -> http://localhost:8000/docs
just web                 # UI    -> http://localhost:3000
```

Everything in Docker instead: `docker compose up --build`. Without `just`,
every recipe in the `justfile` is a plain `uv` / `pnpm` / `docker` command.
Full guide: [docs/development.md](docs/development.md).

## Layout

```
apps/
  web/              Next.js PWA: talk screen, memory, logs, health (also the phone app)
  desktop/          Tauri 2 desktop app + desktop bridge (scaffold)
services/
  agent/            the brain: agent loop, Claude, tools, memory, scheduler, and the API every client uses
  voice/            wake word, speech-to-text, speaker ID, text-to-speech, multi-room output
  vision/           camera motion gate -> scene analysis
  home/             Home Assistant / MQTT device control
packages/
  thea-db/          Postgres + pgvector schema (generated from THEA DB.xlsx), models, repositories
  thea-contracts/   message models shared between services
infra/              migrate image, deploy notes
docs/               start at docs/README.md
```

## Docs

- [Overview](docs/overview.md): what THEA is, principles, codenames
- [Architecture](docs/architecture.md): system map, boundaries, stack
- [API](docs/api.md): endpoints for web, phone, desktop and Shortcuts
- [Data model](docs/data-model.md): schemas, and how they're generated from the workbook
- [Roadmap](docs/roadmap.md): what to build next
- [AGENTS.md](AGENTS.md): rules for AI coding assistants working in this repo
