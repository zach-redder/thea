# API

The agent (`services/agent`, port 8000) is the single API every client uses:
the web app, the phone, the desktop app, and the other THEA services. FastAPI
serves interactive docs at **`http://<host>:8000/docs`**.

> **Status:** `/health` works. Every `/api/v1/*` route exists with its final
> request schema and auth, but returns `501 Not Implemented` until the agent
> runtime is built. The WebSocket authenticates, then reports "not implemented".

## Conventions

- **JSON is snake_case.** The web client converts to and from camelCase at the
  boundary (`apps/web/lib/case-convert.ts`).
- **Timestamps are UTC ISO 8601** (`2026-11-05T14:30:00Z`). Clients format them
  for display.
- **Reads are `GET` and writes or actions are `POST`.** IDs go in query
  parameters (`GET /api/v1/session?id=...`), not path segments. Lists are
  `POST .../list` with `offset`, `limit` and filters in the body.
- **Errors** look like `{"detail": "human-readable message"}`. Show `detail`
  to the user, not the HTTP status text.

## Authentication

Every route except `/health*` needs:

```
Authorization: Bearer <THEA_API_TOKEN>
```

- If no token is configured on the server, protected routes return **503**.
  They never fall open.
- A wrong or missing token returns **401**.
- Browsers can't set headers on a WebSocket, so `/api/v1/ws` expects the
  token as its **first message**.

See [security.md](security.md).

## Endpoints

### Health (public)

| Method | Path | Returns |
|---|---|---|
| GET | `/health` | `{status, service, version}`, used for liveness and Docker healthchecks |
| GET | `/health/detailed` | Plus `dependencies: [{name, ok, detail}]` for Postgres, Redis, voice, home |

### Conversation

| Method | Path | Body / query | Purpose |
|---|---|---|---|
| POST | `/api/v1/chat` | `{message, session_id?, channel?, speak?}` | Send a message and get the full reply: `{session_id, reply, created_at}` |
| POST | `/api/v1/chat/stream` | same | Same, but the reply streams back as Server-Sent Events |
| WS | `/api/v1/ws` | first message `{"type":"auth","token":"..."}` | Live channel: streamed replies, push-to-talk audio, approvals, proactive pushes |

`channel` is one of `web`, `phone`, `desktop` and tells THEA how to answer.
For example, phone replies are shorter. `speak: true` also voices the reply
through the house speakers.

### Sessions and memory (dashboard)

| Method | Path | Body / query | Purpose |
|---|---|---|---|
| POST | `/api/v1/sessions/list` | `{search?, offset, limit}` | Recent conversations |
| GET | `/api/v1/session` | `?id=` | One conversation with its messages and tool calls |
| POST | `/api/v1/memories/list` | `{search?, offset, limit}` | Browse `thea.memories` (semantic search when `search` is set) |
| GET | `/api/v1/integrations` | — | `thea.integrations` connection status |

### Approvals

| Method | Path | Body | Purpose |
|---|---|---|---|
| POST | `/api/v1/approvals/resolve` | `{approval_id, approved}` | Approve or deny a pending tool call that needs confirmation |

Pending approvals are pushed over the WebSocket, and appear as a push
notification on the phone once that's built.

### Service-to-service

| Method | Path | Called by | Body |
|---|---|---|---|
| POST | `/api/v1/triggers` (agent) | voice, vision | `VoiceUtterance` or `VisionEvent` |
| POST | `/api/v1/speak` (voice, :8010) | agent | `SpeakCommand` |
| POST | `/api/v1/commands` (home, :8030) | agent | `DeviceCommand` |

These bodies are defined once, in `packages/thea-contracts`, and use the same
bearer token.

## Examples

```bash
TOKEN=...   # from your .env

curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"message": "What is on my calendar tomorrow?", "channel": "phone"}'
```

### iOS Shortcut ("Hey Siri, ask THEA")

1. **Dictate Text** → store as `Message`.
2. **Get Contents of URL**:
   - URL `https://<server>.<tailnet>.ts.net/api/v1/chat`
   - method POST
   - headers `Authorization: Bearer <token>`, `Content-Type: application/json`
   - JSON body `{"message": Message, "channel": "phone"}`
3. **Get Dictionary Value** `reply` → **Speak Text**.

Android works the same way with Tasker's HTTP Request action. Reaching the
server from outside the house: [remote-access.md](remote-access.md).
