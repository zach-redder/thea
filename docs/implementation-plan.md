# Implementation plan

**Audience: future Claude (or human) sessions that will build THEA.** Read this
before writing code. It turns [vision.md](vision.md) into ordered, testable
work. Update it as you go. It's a living document, and the checkboxes are the
project's memory of what's done.

## Session protocol

Do this at the start of every session:

1. Read [AGENTS.md](../AGENTS.md) (rules, invariants), then
   [vision.md](vision.md), then this file.
2. Find the **first phase with unchecked tasks**. Work there. Don't skip
   ahead: later phases assume earlier ones. If you must, say why in the
   phase's *Notes*.
3. Read the design doc each phase links to *before* coding it.
4. **Spec before code, tests before implementation** (red → green →
   refactor). Every task below lists its acceptance test.
5. Run `just lint` and `just test` (and the web build for `apps/web` changes)
   before calling anything done. See [development.md](development.md).
6. Tick the boxes you completed, add anything you discovered under *Notes*, and
   if you made a decision a future reader would question, write an ADR in
   `docs/decisions/`.
7. Don't commit personal data, and don't hand-edit generated files
   (`migrations/`, `models/`). Schema changes go through `THEA DB.xlsx` and
   `just gen-schema` ([data-model.md](data-model.md)).
8. Keep a phase **shippable**: at the end of it, THEA does something new that
   Zach can use. Prefer a thin vertical slice over broad scaffolding.

### Things that need Zach (don't guess; ask)

- Real secrets (API keys, OAuth client secrets), never invent or commit them.
- Editing `THEA DB.xlsx` (it holds personal data and lives outside the repo).
  Prepare the registry rows as text in the PR/notes, and ask him to paste
  them, or edit it only when he's explicitly said to.
- Anything in [vision.md → Open questions](vision.md#open-questions).
- Hardware purchases and physical setup (mics, cameras, hubs).
- Any action on his real accounts (posting, sending, spending, unlocking).

## Status

| Phase | Name | State |
|---|---|---|
| 0 | Foundation | ✅ done |
| 1 | She talks (text, persona, sessions) | ⬜ next |
| 2 | She remembers | ⬜ |
| 3 | She can do things (tools, approvals, calendar, GitHub) | ⬜ |
| 4 | She's on your phone and you can see your life (dashboard, stats, habits) | ⬜ |
| 5 | She speaks and hears (ElevenLabs, STT, wake word) | ⬜ |
| 6 | She runs the house | ⬜ |
| 7 | She's on your desktop | ⬜ |
| 8 | She's aware and proactive (ambient, addressee detection, vision) | ⬜ |
| 9 | More accounts, production hardening | ⬜ |

## Starting values and conventions to reuse

- **Models** (verify current IDs with the `claude-api` skill before
  hard-coding; they're data in `thea.config`): `default_model` Sonnet-class,
  `fast_model` Haiku-class, deep work Opus-class. Embeddings: Voyage, 1536-d.
- **Reuse what exists:**
  `thea_agent.core.config.Settings` (secrets only), `core.security.require_token`,
  `channels.base.Channel`, `tools.registry.ToolRegistry`,
  `api.v1.schemas`, `thea_contracts` messages, `thea_db.db`
  (`make_engine`, `make_session_factory`, `transaction`), and the
  `_not_implemented` helper in `api/v1/` (remove it from a route when you
  implement it).
- **Test style:** FastAPI `TestClient` + `dependency_overrides` (see
  `services/agent/tests/test_api.py`). For DB tests use a real Postgres
  (pgvector image, via `testcontainers` or the compose `postgres`), not mocks.
  Mock only the network edges (Anthropic, Voyage, ElevenLabs, providers).
- **Where new code goes:** [AGENTS.md → Where things go](../AGENTS.md#where-things-go).

---

## Phase 0: Foundation ✅

Done: monorepo, workspaces, CI, Docker, schema generated from the workbook,
service skeletons with health + auth, the web shell and the docs. See
[architecture.md](architecture.md).

---

## Phase 1: She talks

**Goal:** In the web app, Zach has a real conversation with THEA. She sounds
like a person ([persona.md](persona.md)), uses what she knows about him from
the database, and the conversation survives a refresh and moves between
devices.

**Prereqs:** `THEA DB.xlsx` seeded locally (`just db`, `just seed`, load the
seed); `ANTHROPIC_API_KEY` and `THEA_API_TOKEN` in `.env`.

### Tasks

**1a. Schema first** (needs Zach to edit the workbook, see
[data-model.md](data-model.md#planned-schema-additions))
- [ ] Move `thea.memories` into the workbook registry; delete the generator
  fallback.
- [ ] Add `thea.conversations`, `thea.messages`, `thea.tool_calls`.
- [ ] `just gen-schema`; review the diff; apply migrations (`just db`).
- *Accept:* `just check-schema` clean; tables exist in Postgres.

**1b. Data access**
- [ ] `thea_db/repositories/config_repo.py`: `get_config()` (single row).
- [ ] `prompts_repo.py`: `active_prompts(context)`.
- [ ] `profile_context_repo.py`: `get_profile_block()` (profile, personality,
  context).
- [ ] `conversation_repo.py` (new): create/append/list/get conversations and
  messages.
- [ ] `session_store.py`: Redis working memory (keys and TTLs in
  [memory.md](memory.md#redis-working-memory)); session lookup by recency so
  sessions span channels.
- *Accept:* repository tests against a real Postgres/Redis.

**1c. The persona**
- [ ] Write `runtime/prompts/core.md` from [persona.md](persona.md) (the
  versioned fallback); `prompt_loader.py` prefers an active `thea.prompts`
  row named `core`, else the file.
- [ ] `context_builder.py`: assemble layers in cache order
  ([agent-runtime.md](agent-runtime.md#prompt-caching)); stable-prefix
  byte-identical across turns (test it).
- [ ] Channel-style blocks (`web`, `phone`, `voice`, `desktop`).
- *Accept:* a snapshot test proving the prefix is identical turn to turn; a
  banned-phrase test over canned model outputs
  (`tests/persona/test_banned_phrases.py`).

**1d. The model**
- [ ] `llm/claude_client.py`: async Anthropic client, prompt caching (cache
  breakpoint after the stable prefix), streaming, retries/timeouts, model
  from `thea.config`. The only Claude caller in the repo.
- [ ] `runtime/loop.py`: single-turn loop without tools yet; strict role
  alternation; per-turn budget.
- [ ] `runtime/intent_router.py`: tiers 1–2 only for now (tier 0 arrives with
  tools).
- *Accept:* tests with the Anthropic client stubbed; one opt-in live test
  (`pytest -m live`, skipped without a key).

**1e. API + web**
- [ ] Implement `POST /api/v1/chat` and `/chat/stream` (SSE),
  `POST /api/v1/sessions/list`, `GET /api/v1/session`.
- [ ] Implement the WebSocket `/api/v1/ws` for streaming + session events
  (auth already done).
- [ ] Web: streaming replies in `talk-panel.tsx`; **token pairing screen**
  (Settings → paste `THEA_API_TOKEN`; `apiToken.set`); load history on
  refresh; Logs page lists sessions.
- *Accept:* typed chat works end to end; refresh keeps history; a second
  browser/device continues the same session; `/health/detailed` reports real
  Postgres/Redis status.

**1f. Persona evaluation**
- [ ] `tests/persona/` golden conversations with an LLM-judged rubric (opt-in,
  `-m live`): no boilerplate, brevity, uses a known fact, no lists in
  `voice` channel.

**Definition of done:** Zach chats with her in the browser; she's warm and
brief; she mentions something from his profile naturally; history persists.

**Notes / risks:** Prompt-cache breakage is the silent cost bug. Keep the
prefix test. Don't add retrieval yet; it's Phase 2.

---

## Phase 2: She remembers

**Goal:** Things Zach tells her stick, and come back at the right moment.
[memory.md](memory.md) is the design.

### Tasks
- [ ] Schema: `thea.memories` gets `status`, `superseded_by`,
  `last_recalled_at` (workbook).
- [ ] `memory/writer.py`: Voyage embeddings (1536-d), insert, dedupe by
  similarity threshold.
- [ ] `memory/extraction.py`: fast-model pass → structured operations
  (`remember`, `update_fact`, `link`, `forget`) validated with Pydantic.
- [ ] Trigger extraction on session idle (Redis TTL event or a scheduler
  sweep) and via `POST /api/v1/sessions/end`.
- [ ] `memory_repo.py` + `memory/retrieval.py`: pgvector search, scoring
  (similarity × recency × salience + entity boost), entity-linked retrieval,
  top ≈ 6.
- [ ] Wire retrieval into `context_builder.py` (below the cache breakpoint).
- [ ] "Forget that" flow: explicit user command and the web browser delete.
- [ ] `POST /api/v1/memories/list` (semantic search when `search` set); web
  Memory page becomes real (search, filter, delete, "why do you remember
  this?" provenance).
- [ ] `scheduler/jobs/daily_synthesis.py`: nightly consolidation + rewrite of
  `identity.context`.
- *Accept:* tell her a fact in one session, she uses it in a new session next
  day (integration test with a fake clock); a correction supersedes the old
  fact; near-duplicate statements don't create new rows; ambient/guest turns
  write nothing.

**Definition of done:** the "Mid-thought" and "Across surfaces" scenes in
[vision.md](vision.md#what-good-feels-like) work in text.

---

## Phase 3: She can do things

**Goal:** Tools, with confirmation, plus the first real integrations
(calendar, GitHub). [integrations.md](integrations.md) is the design.

### Tasks
- [ ] Credential store: `thea.integration_credentials` (workbook), encryption
  helper, [ADR 0009](decisions/0009-integration-credentials.md).
- [ ] `tools/registry.py`: load `thea.tools` ⨝ `thea.integrations`; honor
  `enabled`, `requires_confirm`; stable tool list per session.
- [ ] Tool loop in `runtime/loop.py`: tool use, iteration cap, deadline,
  `POST /api/v1/stop`.
- [ ] **Approvals:** pending approval in Redis → pushed on the WebSocket →
  `POST /api/v1/approvals/resolve`; timeout = deny. Web UI approval cards.
- [ ] `tools/mcp.py`: connect MCP servers from `thea.integrations` rows
  (Google Calendar, Notion first).
- [ ] `integrations/base.py` `Integration` ABC (exists as skeleton) +
  `integrations/google_calendar.py` and `integrations/github.py` (read first;
  webhook receiver for GitHub).
- [ ] `scheduler/proactive.py` + a sync job per integration; notable events →
  memories.
- [ ] Tier 0 reflexes in the intent router (timers, simple commands).
- [ ] Audit log: every tool call into `thea.tool_calls`; shown on the Logs
  page.
- [ ] Prompt-injection guard: tool results wrapped as untrusted data; test that
  injected text can't trigger a `requires_confirm` tool without approval.
- [ ] Native: `tools/native/weather.py`, `maps.py`.
- *Accept:* "what's on tomorrow?" answers from the real calendar; a write tool
  pauses for approval and is denied on timeout; GitHub PR status is known
  without being asked; every write tool has `requires_confirm` (test).

**Definition of done:** the "Morning" scene works over text (agenda + PR
status), and an approval round-trips on web.

---

## Phase 4: Phone and the life dashboard

**Goal:** THEA lives on the phone, and Zach can see his own stats and habits.
[stats-and-dashboard.md](stats-and-dashboard.md), [remote-access.md](remote-access.md).

### Tasks
- [ ] Deploy to the home server; Tailscale + `tailscale serve` HTTPS
  ([infra/deploy/README.md](../infra/deploy/README.md)); fix CORS origins.
- [ ] PWA hardening: install flow, offline shell, **Web Push** (VAPID keys;
  service worker; subscribe endpoint) for approvals and reminders.
- [ ] Phone context API: implement `POST /api/v1/phone/context` and
  `/phone/share` (contract `PhoneContext` exists); an iOS Shortcut and an
  automation pack documented in [api.md](api.md).
- [ ] Schema: `identity.habit_logs`, `stats.metrics` (workbook).
- [ ] `stats/collectors/*` (calendar load, GitHub activity, habits, THEA
  usage, phone context) and `stats/aggregators.py`.
- [ ] Implement `GET /api/v1/today`, `/stats/summary`, `/stats/series`,
  `POST /habits/list`, `/habits/log`, `/life/list`.
- [ ] Agent tool `get_stats` backed by the same aggregators.
- [ ] Web: Today, Stats, Habits, Life log, Settings pages; nav revamp (5 tabs);
  mini orb in the header.
- [ ] Health data path (Apple Health export via Shortcut → `phone/context` or
  a `metrics` batch endpoint).
- *Accept:* installed on the phone via Tailscale; a Shortcut can talk to her;
  habits can be checked off with one tap and the streak updates; asking "how
  did I sleep?" and the Sleep card agree.

**Definition of done:** the "From the phone" scene works; Today shows a real
agenda and habits.

---

## Phase 5: She speaks and hears

**Goal:** A natural spoken voice, then ears. [voice-pipeline.md](voice-pipeline.md),
[ADR 0005](decisions/0005-voice-stack.md).

Order matters: **voice out first** (cheap, big payoff), then push-to-talk,
then room mics.

### Tasks
- [ ] `services/voice/output/tts.py`: ElevenLabs streaming TTS; `voice` from
  `thea.config`; sentence-chunked streaming from the agent's token stream.
- [ ] `POST /api/v1/speak` implemented (auth exists) + `speak: true` in chat;
  web plays streamed audio (`<audio>`/MediaSource) so THEA speaks in the
  browser/phone.
- [ ] Persona for speech: write-for-the-ear rules enforced in the `voice`
  channel style; number/date normalization.
- [ ] Push-to-talk: mic audio over the WebSocket → STT → agent → TTS stream
  back.
- [ ] `input/stt.py`: faster-whisper (local), VAD-gated.
- [ ] Room hardware: one mic array; `input/vad.py`, `input/wake_word.py`
  (Porcupine "Hey THEA"; see open questions), `buffer.py`, `publisher.py` →
  `POST /api/v1/triggers`.
- [ ] Implement `/api/v1/triggers` for `VoiceUtterance` in the agent (voice
  channel).
- [ ] `output/snapcast.py` + room routing (later in the phase; one room works
  without it).
- [ ] Self-trigger suppression; speculative context start on wake word.
- [ ] Latency instrumentation (stage timings in logs) and a budget test
  against [voice-pipeline.md](voice-pipeline.md#latency-budget).
- *Accept:* she speaks replies in the web app with first audio < 1.5 s;
  saying "Hey THEA, …" in the room gets a spoken answer; she never triggers
  herself.

**Definition of done:** a hands-free spoken conversation in one room.

---

## Phase 6: She runs the house

**Goal:** Lights and electronics by voice or text. [ambient-and-home.md](ambient-and-home.md).

### Tasks
- [ ] Stand up Home Assistant (container or hardware); add devices.
- [ ] Map `environment.rooms`/`devices` ↔ HA entities
  (`home_assistant/entities.py`).
- [ ] Start with the **direct path**: HA as an MCP/REST tool from the agent;
  introduce `services/home` (`dispatch.py`, `client.py`, `POST /api/v1/commands`)
  where retries or non-HA devices need it.
- [ ] Natural-language target resolution ("the lamp by the couch") against
  the tables; ambiguity → one short question.
- [ ] Tier 0 reflexes for common device commands.
- [ ] Scenes/routines by name; security devices at autonomy level 3.
- [ ] Presence: fuse HA occupancy + speaker/room + phone location into
  Redis `presence`; route `SpeakCommand.rooms` from it.
- [ ] Web Home page: rooms, devices, scenes, big tap targets.
- *Accept:* "lights off" < 300 ms (Tier 0); "movie mode" runs a scene; the
  lock requires approval.

**Definition of done:** the "Morning" scene's lights, by voice.

---

## Phase 7: She's on your desktop

**Goal:** Native app, then the PC bridge. [desktop.md](desktop.md),
[ADR 0006](decisions/0006-tauri-desktop.md).

### Tasks
- [ ] Install Rust + Tauri prerequisites; generate icons; build and run
  `apps/desktop`.
- [ ] Tray icon, global push-to-talk shortcut, native notifications.
- [ ] Add `apps/desktop` to CI (build only on tags or a separate job).
- [ ] Desktop channel: authenticated WebSocket from the app; the agent offers
  `tools/desktop/*` only while connected.
- [ ] Bridge sidecar (MCP, `127.0.0.1`): open file/app/URL → clipboard/active
  window → screenshot → shell command (always confirmed, verbatim) → computer
  use.
- [ ] Per-action confirmation UI in the window; deny list; audit log.
- *Accept:* THEA opens a file after a confirmation; closing the app removes
  desktop tools from the next session; nothing listens on non-loopback.

---

## Phase 8: She's aware and proactive

**Goal:** She notices things and knows when he's talking to her.
[ambient-and-home.md](ambient-and-home.md), [agent-runtime.md](agent-runtime.md#proactivity).

### Tasks
- [ ] Speaker enrollment and `input/diarization.py`; guest handling and
  `privacy_mode`.
- [ ] `input/relevance_filter.py`: the addressee cascade (conversation window,
  acoustic cues, contextual cues, semantic classifier); thresholds and
  feedback ("I wasn't talking to you") stored as preferences
  (`thea.preferences`, workbook).
- [ ] Ambient memory rules (only when addressed or alone and stating a durable
  fact); no capture during calls/guests.
- [ ] Worth-interrupting gate; DND, meeting and sleep suppression; rate limit.
- [ ] Scheduler jobs: `morning_brief`, `stale_data_check`, evening wrap-up,
  weekly review (spoken in the current room).
- [ ] `services/vision`: RTSP ingest, `motion_detector.py` gate,
  `scene_analysis.py` pass, `publisher.py`; per-camera privacy switches.
- [ ] Cross-signal connections ("at the desk since 8, no lunch").
- [ ] Autonomy levels: add `thea.tools.autonomy`, enforce in the loop, expose
  in Settings.
- *Accept:* a metrics notebook of addressee decisions against a labeled
  recording set; she stays silent in a call; she greets in the kitchen with
  the morning brief.

**Definition of done:** the "Morning", "Not for her" and "Mid-thought" scenes
all work in the real house.

---

## Phase 9: More accounts, production hardening

### Tasks
- [ ] Twitch adapter (EventSub, stream stats), YouTube, then social platforms
  one by one (check API terms first; read-only by default).
- [ ] Per-device API tokens with revocation; rotate `THEA_API_TOKEN`.
- [ ] Backups (`pg_dump` nightly, restore drill), monitoring/alerting,
  cost and latency dashboards (agent's own stats).
- [ ] Deployment pipeline (self-hosted runner), image pinning, migration
  gating.
- [ ] Security review: prompt-injection tests, secrets scan in CI, dependency
  audit.
- [ ] Load/soak test of the always-on voice path.
- *Accept:* restore from backup works; a lost phone's token can be revoked in
  the UI.

---

## Cross-cutting workstreams

These run through every phase. Don't leave them to the end.

| Workstream | Standing rules |
|---|---|
| **Persona quality** | Re-run `tests/persona/` on any prompt change. Listen to TTS samples occasionally. |
| **Latency** | Instrument each stage from Phase 1. Budget in [agent-runtime.md](agent-runtime.md#staying-fast). |
| **Cost** | Log tokens and cache hits per turn; surface in stats; set a daily soft cap. |
| **Privacy** | No raw A/V storage; guests don't write memory; every new integration documents its data flow in [security.md](security.md). |
| **Schema** | Workbook → generator only. Keep [data-model.md](data-model.md) current. |
| **Docs** | Update the relevant doc in the same change. Tick this file. |
| **Observability** | Structured UTC logs; request id per turn; `/health/detailed` stays honest. |

## Decision log (open items to resolve in order)

| # | Question | Needed by | Default if unanswered |
|---|---|---|---|
| 1 | ElevenLabs voice choice | Phase 5 | Pick a stock conversational voice; make it a `thea.config.voice` change |
| 2 | Wake phrase and custom Porcupine keyword | Phase 5 | "Hey THEA" |
| 3 | Server hardware and GPU | Phase 4 deploy / Phase 5 STT | CPU `small.en` |
| 4 | Camera type | Phase 8 | RTSP IP cameras |
| 5 | Which accounts allow write access | Phase 3/9 | None; read-only |
| 6 | Home Assistant hardware | Phase 6 | Container on the server |
| 7 | Direct HA tool vs `services/home` mediator | Phase 6 | Direct tool first |
