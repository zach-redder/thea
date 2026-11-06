# thea-heart

Core orchestration for thea — the process that turns a trigger into a response. Everything else in the thea system exists to feed this repo data or carry out what it decides.

## Overview

thea-heart is the only repo that talks to Claude. It receives triggers (wake word, ambient audio, vision events, or scheduled jobs), assembles context from thea-brain, calls the Claude API, dispatches any tool calls, and produces the final response. It also owns the proactive scheduler and the post-conversation memory extraction pass.

If you're trying to understand how thea "thinks," this is the repo to read.

## Role in the thea system

thea-heart is the hub — every other repo either feeds it input or receives commands from it:

- **thea-senses → thea-heart**: perception events (wake word triggers, filtered ambient audio, vision events) arrive here for classification.
- **thea-heart → thea-brain**: direct DB connection (not HTTP — see thea-brain's README for why) for context assembly and memory read/write.
- **thea-heart → thea-muscles**: dispatches actuation commands (speak this, turn on that light) and receives no direct response back beyond confirmation.
- **thea-heart ↔ MCP servers / native tools**: owns all tool orchestration, per `thea.tools` and `thea.integrations`.
- **thea-body** reads from thea-heart (via a future thin HTTP API) for dashboard display — thea-heart doesn't call thea-body.

## Tech stack

- **Python 3.11+**
- **FastAPI** — webhook endpoints for inbound triggers from thea-senses and the scheduler
- **Anthropic Python SDK** — Claude API calls, prompt caching, MCP server connections via `mcp_servers`
- **APScheduler** — proactive scheduler (morning brief, stale-data checks, daily synthesis)
- **SQLAlchemy** (via thea-brain) — direct DB access, no ORM boundary between repos
- **redis-py** — session state via thea-brain's session store
- **Voyage AI Python client** — embedding generation for memory writes (thea-brain never calls this itself)

## Planned structure

```
thea-heart/
├── app/
│   ├── main.py
│   ├── router/
│   │   ├── intent_router.py       # fast-path vs full-reasoning decision
│   │   └── webhooks.py            # inbound triggers from senses/scheduler
│   ├── context/
│   │   ├── builder.py             # assembles cached + dynamic layers, in order
│   │   ├── retrieval.py           # decides what's relevant, calls thea-brain repos
│   │   └── prompt_loader.py       # pulls thea.prompts, picks situational prompt
│   ├── claude/
│   │   ├── client.py              # API wrapper, prompt caching
│   │   └── tool_dispatch.py       # routes to MCP vs native handlers
│   ├── tools/
│   │   ├── mcp_config.py          # server configs per thea.integrations row
│   │   └── native/
│   │       ├── plaid.py
│   │       ├── weather.py
│   │       └── maps.py
│   ├── memory/
│   │   ├── extraction.py          # post-turn fast-model pass
│   │   └── writer.py              # calls thea-brain's memory_repo
│   ├── scheduler/
│   │   ├── proactive.py           # APScheduler setup
│   │   └── jobs/
│   │       ├── morning_brief.py
│   │       ├── stale_data_check.py
│   │       └── daily_synthesis.py # rewrites identity.context
│   └── output/
│       └── dispatch.py            # → thea-muscles or thea-body
├── tests/
└── requirements.txt
```

## Status

**Not yet implemented.** This README documents the intended structure based on the architecture designed in planning — no code exists in this repo yet. thea-brain should be built and migrated first, since thea-heart's context builder depends on real tables to query against.

## Related repos

thea-brain · thea-senses · thea-muscles · thea-bones · thea-body
