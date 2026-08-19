# THEA

THEA is a persistent, personal AI assistant with the long-term goal of
ambient, home-wide presence — closer to JARVIS than to a chatbot confined
to one app. She's organized into six systems named after body parts
(`brain`, `heart`, `senses`, `muscles`, `body`, plus `bones` as the
connective infrastructure); see [`docs/THEA.md`](docs/THEA.md) for what
she is and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for how she's
built.

**Status**: early scaffolding. `brain`'s Postgres/pgvector schema is the
one system with real, working code today; everything else is designed in
detail but not yet implemented. Don't expect a working assistant yet —
expect a monorepo skeleton with one real data layer and five detailed
blueprints.

## Quickstart

```
docker compose up
```

Postgres, Redis, and the one-shot schema migration will come up healthy.
`heart`, `muscles`, `senses`, and `body` will build but won't stay running
yet — their application code doesn't exist. See
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md#local-dev-what-docker-compose-up-actually-does-today)
for exactly what that means.

For Python work outside Docker: [`uv`](https://docs.astral.sh/uv/) manages
`brain`, `heart`, `muscles`, and `senses` as one workspace —
`uv sync --all-extras` from the repo root.

## Structure

```
thea/
├── brain/      Postgres + pgvector schema, migrations, data layer
├── heart/      Core orchestration -- context, Claude API, tool routing
├── senses/     Always-on perception -- wake word, ambient audio, vision
├── muscles/    Actuation -- Home Assistant, MQTT, multi-room audio
├── body/       Read-only dashboard (Next.js)
├── docs/       THEA.md, ARCHITECTURE.md
└── docker-compose.yml
```

## Learn more

- [`docs/THEA.md`](docs/THEA.md) — what THEA is, the anatomical metaphor, design intent
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — tech stack, data flow, what's built vs. planned
