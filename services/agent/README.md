# agent

*Codename: heart.* THEA's brain at runtime, and the API every client uses. It
turns a trigger (a typed message, a voice utterance, a scheduled job) into a
response: it assembles context from the database, calls Claude, runs tools,
replies over the right channel, and remembers what mattered.

```bash
just agent        # uv run --package thea-agent uvicorn thea_agent.main:app --reload --port 8000
```

Open http://localhost:8000/docs. Every `/api/v1/*` route needs
`Authorization: Bearer $THEA_API_TOKEN`.

## Layout

```
src/thea_agent/
  main.py         app factory
  core/           settings (secrets only), UTC logging, bearer auth
  api/v1/         chat, sessions, memory, approvals, triggers, phone, stats, control, realtime WebSocket
  channels/       Channel ABC + web / phone / voice / desktop adapters
  runtime/        turn loop, context builder, prompt loader, intent router, output dispatch
  llm/            Claude client (the only LLM caller in the repo)
  tools/          registry, MCP connections, native tools, desktop tools
  memory/         retrieval, extraction, writer (Voyage embeddings)
  integrations/   Integration ABC + calendar, GitHub, Twitch, social, Spotify, health
  stats/          collectors and aggregators for the dashboard and get_stats
  scheduler/      proactive jobs (morning brief, stale data, daily synthesis)
tests/
```

**Status:** `/health`, auth and the full route surface work. Routes return
`501` until the runtime is built ([roadmap](../../docs/roadmap.md), Phase 1).

More: [architecture](../../docs/architecture.md#inside-the-agent) · [api](../../docs/api.md)
