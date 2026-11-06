# 0004: The agent imports the DB layer directly; everyone else goes through the agent

**Status:** accepted (carried over from the original `thea-brain` design)

## Context

A voice turn needs several queries (config, prompts, profile, context,
relevant memories) before the first token. An HTTP data service in between
would add a network hop to every one of them. Meanwhile a browser dashboard
must never hold database credentials.

## Decision

- `packages/thea-db` is a **library** (models, repositories, session store)
  plus generated SQL migrations. It's not a service.
- Only the agent imports it, and talks to Postgres and Redis directly.
- Every other consumer (web, phone, desktop, voice, vision) goes through the
  agent's authenticated API.

## Consequences

- Low-latency context assembly; one place to enforce what's readable.
- Dashboard reads cost the agent some work. That's fine at single-user scale.
- Migrations run as a one-shot `migrate` job (`infra/migrate`), not at agent
  startup.
