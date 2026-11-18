# Patterns borrowed from Hermes Agent

[Hermes Agent](https://github.com/NousResearch/hermes-agent) (Nous Research)
is a mature open-source personal agent with the same core shape: one agent
behind a CLI, a messaging gateway, a TUI and a desktop app, with memory,
skills, scheduled jobs and tool use. A local clone sits next to this repo
(`H:\codebases\THEA\hermes-agent`) as **reference only**. No code is copied
and it's not a dependency.

| Hermes pattern | Where in Hermes | THEA equivalent |
|---|---|---|
| **Platform adapter ABC.** Every surface (Telegram, Discord, API server, ...) implements one base class, and the runtime never knows which surface it's talking to | `gateway/platforms/base.py` | `thea_agent/channels/base.py` (`Channel`, `InboundMessage`, `OutboundMessage`) |
| **Central tool registry** with a schema, handler and `check_fn` availability per tool, so unconfigured tools never reach the model | `tools/registry.py`, `model_tools.py` | `thea_agent/tools/registry.py` (`ToolSpec.is_available`); enabled and confirm flags come from `thea.tools` |
| **OpenAI-style API server** with sessions, runs, an SSE event stream, approvals and stop/steer | `gateway/platforms/api_server.py` | `thea_agent/api/v1/` (chat, chat/stream, sessions, approvals, ws) |
| **"Prompt caching is sacred."** The system prompt is byte-stable for a conversation, and toolsets aren't swapped mid-session | `AGENTS.md` | The invariant is documented in `runtime/loop.py` and `context_builder.py` |
| **Strict role alternation.** No synthetic user messages mid-loop | `AGENTS.md` | Same invariant |
| **`.env` is for secrets only;** behavior goes in config | `AGENTS.md` | [ADR 0008](../decisions/0008-env-for-secrets-only.md); behavior in `thea.config` |
| **The footprint ladder.** Prefer extending code → a skill → a gated tool → a plugin → an MCP server → a new core tool, because every core tool costs tokens on every call | `AGENTS.md` | Prefer MCP servers and `thea.tools` rows over new native tools |
| **Skills as `SKILL.md`** (frontmatter + instructions), loaded on demand | `skills/*/SKILL.md` | Planned: `services/agent/src/thea_agent/skills/` for user-authored procedures ("how I like my morning brief") |
| **Memory provider + manager** split | `agent/memory_manager.py`, `agent/memory_provider.py` | `thea_agent/memory/` (retrieval, extraction, writer) over `thea_db` |
| **Background curator.** A forked side-agent with isolated state, triggered by inactivity rather than a cron daemon | `agent/curator.py` | Model for the post-conversation memory extraction and nightly synthesis jobs |
| **Voice tools.** Wake word, transcription, TTS, voice mode | `tools/wake_word.py`, `tools/transcription_tools.py`, `tools/tts_tool.py` | THEA splits these into the `voice` service, since her voice is ambient and always-on, not per-session |
| **Root `AGENTS.md`** for AI contributors | `AGENTS.md` | THEA's [`AGENTS.md`](../../AGENTS.md) |

## Where THEA deliberately differs

- **Postgres + pgvector, not SQLite.** THEA's memory is structured (identity,
  wardrobe, environment) as well as episodic, and needs vector search.
- **Separate perception and actuation services.** Hermes is mostly
  conversational. THEA lives in a house with always-on mics, cameras and
  devices that need their own processes and hardware access.
- **Single user, single provider.** No multi-profile or multi-provider
  routing; Claude via the Anthropic SDK.
