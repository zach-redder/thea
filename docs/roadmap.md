# Roadmap

Each phase ends with something you can actually use. Build them in order:
each one sits on the one before it.

## Phase 0: Foundation ✅

- Monorepo layout, uv + pnpm workspaces, CI, Docker Compose
- Database schema generated from `THEA DB.xlsx`, models, seed importer
- Service skeletons with `/health`, settings, fail-closed auth, tests
- Web shell: talk screen with the orb, dashboard pages, installable PWA

## Phase 1: THEA can talk (text)

**Goal:** chat with THEA in the web app and she answers in her own voice, using
what she knows about you.

- `thea_db` repositories: `config_repo`, `prompts_repo`, `profile_context_repo`
- `llm/claude_client.py`: model from `thea.config`, prompt caching
- `runtime/context_builder.py` + `prompt_loader.py` (no memory retrieval yet)
- `runtime/loop.py`, without tools
- `POST /api/v1/chat` and `/chat/stream` for real; Redis session store
- Web: streaming replies and an API-token pairing screen

## Phase 2: THEA remembers

- `memory/extraction.py` (fast model, post-conversation), then `writer.py`
  (Voyage embeddings), then `thea.memories`
- `memory/retrieval.py`: pgvector similarity, plus salience and recency
- Web: a real memory browser and logs page
- Add `thea.memories` to the workbook and remove the generator fallback

## Phase 3: THEA can do things

- `tools/registry.py` loaded from `thea.tools`; native tools (weather, maps)
- MCP connections from `thea.integrations` (Google Calendar, Notion, Spotify)
- The approval flow: `requires_confirm` → WebSocket prompt → `/approvals/resolve`
- Web: approval cards and the integrations health page

## Phase 4: THEA on your phone

- Tailscale on the server, HTTPS via `tailscale serve`
- Install the PWA; push notifications for approvals and proactive messages
- An iOS Shortcut / Tasker task for hands-free use

## Phase 5: THEA can hear and speak

- Voice service via Pipecat: VAD → wake word → STT → trigger, and
  `/speak` → TTS → speaker
- One room first, then Snapcast for multi-room
- Intent-router fast path for device commands (latency)
- Web: push-to-talk over the WebSocket

## Phase 6: THEA runs the house

- Home service: Home Assistant client; `environment.devices` → entity mapping
- Device tools exposed to the agent; MQTT and Kasa for the stragglers
- Presence-aware speech output

## Phase 7: THEA on your desktop

- Tauri app build: tray, global push-to-talk shortcut, notifications
- Desktop bridge MCP sidecar: open, clipboard, screenshot, then shell, then
  computer use, each confirmed

## Phase 8: THEA is proactive

- Scheduler: morning brief, stale-data check, nightly synthesis of
  `identity.context`
- Ambient relevance filter, speaker ID and privacy mode
- Vision service: motion gate, then scene pass, then triggers

## Phase 9: Production

- Home-server deploy (self-hosted runner or SSH), backups of the Postgres
  volume, monitoring
- Per-device tokens, audit log of every tool call
