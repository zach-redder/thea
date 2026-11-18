# Security and privacy

THEA holds your identity, finances, health, relationships and home, and she
can act on all of them. Treat her like a password manager with arms.

## Threat model, briefly

- **The user** is trusted.
- **The network** is not: everything outside the home server goes through
  Tailscale. ([remote-access.md](remote-access.md))
- **Guests in the house** are partially trusted. They can talk to THEA but
  shouldn't hear your private details. (privacy mode)
- **Model output** is not trusted. Tool calls can be wrong, or steered by
  injected content (an email, a web page). Confirmation gates and tool scoping
  limit the blast radius.

## Secrets

- Secrets live only in the root **`.env`** (gitignored). `.env.example` lists
  every key.
- `.env` is for secrets and addresses only. Behavior lives in `thea.config`.
  ([ADR 0008](decisions/0008-env-for-secrets-only.md))
- Production: the same `.env` on the home server, readable only by the deploy
  user. Never bake it into images (`.dockerignore` excludes it).

## Personal data never enters git

- `THEA DB.xlsx` and `**/seed/local_seed.sql` are blocked three ways:
  `.gitignore`, `.dockerignore`, and a pre-commit hook that fails on them.
- Docs and tests use structure only, never real rows.

## API authentication

- One personal bearer token (`THEA_API_TOKEN`) for every client and service.
  The check lives in `thea_contracts.auth.token_matches`: constant-time,
  byte-wise, and **fail-closed**. If no token is configured, protected
  endpoints return 503 instead of opening up.
- Only `/health` is public, on every service.
- WebSocket: the token is the first message. Nothing else is read until it
  passes, and a bad token closes with code 1008.
- CORS only allows the web app and Tauri origins (`CORS_ORIGINS`).
- Later: per-device tokens with revocation.

## Tool permissions

- `thea.tools.requires_confirm` marks tools that need a human yes. The agent
  pauses, asks over the originating channel (or pushes an approval), and waits
  for `POST /api/v1/approvals/resolve`.
- These should always require confirmation:
  - unlocking doors or disarming anything
  - spending or moving money
  - sending messages as you
  - deleting data
  - any desktop-bridge action ([desktop.md](desktop.md))
- Only tools whose integration is configured and enabled are offered to the
  model at all (the registry's availability check).

## Privacy in the room

- Raw audio and video stay in RAM inside the voice and vision services. Only
  transcripts and labels go to the agent. Nothing is recorded to disk.
- An unrecognized speaker (`speaker=None`) lets the agent apply `privacy_mode`:
  no personal details spoken aloud.
- `do_not_disturb` and its window silence proactive speech. Direct requests
  still work.

## Third parties

Claude, Voyage AI and ElevenLabs receive the text needed for a turn. Keep
that minimal: retrieve only the memories relevant to the turn, and never send
whole tables. Plaid balances are fetched live and not persisted.

## Account access and autonomy

THEA will hold read access, and sometimes write access, to GitHub, calendar, social and other accounts.
The controls are layered: narrow provider scopes, per-tool autonomy levels, confirmation for anything
outward-facing, draft-first writes, prompt-injection hygiene, and an audit log of every tool call.
See [integrations.md](integrations.md#safety-model-for-account-access) and
[agent-runtime.md](agent-runtime.md#autonomy-levels). OAuth tokens are stored encrypted
([ADR 0009](decisions/0009-integration-credentials.md)).

## Ambient listening

Always-on mics and cameras are the most sensitive part of the system. Defaults: no audio or video
stored; calls, meetings and guests not captured; an obvious "listening" indicator; one-phrase and
physical mute; cameras off in private rooms. See [ambient-and-home.md](ambient-and-home.md).
