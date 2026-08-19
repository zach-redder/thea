# THEA

## What she is

THEA is a persistent, personal AI assistant. The long-term goal is ambient,
home-wide presence — closer to JARVIS than to a voice assistant you open an
app to talk to. Not a chatbot confined to one screen or one conversation:
a presence that persists across sessions, remembers what's happened before,
and is eventually meant to reach into the physical spaces she runs in
(lights, audio, climate, other devices) rather than just answering
questions about them.

She's built as part of the Keystone app ecosystem and evolved from there
into a standalone assistant with her own architecture and her own
six-repo — now one monorepo — codebase.

## Design intent

A few decisions run through the whole system, stated explicitly in the
individual services' design docs (see `docs/ARCHITECTURE.md` for where
each one is implemented):

- **Natural, not robotic.** THEA's system prompt (`thea.prompts`, seeded
  from the schema source described below) is written to sound like a
  specific person's voice — direct, dry, occasionally sardonic — not a
  generic assistant persona reciting disclaimers.
- **Persistent memory across sessions.** Conversations, facts, and context
  aren't thrown away between turns. `identity`, `wardrobe`, and
  `environment` schemas hold structured long-term facts; `thea.memories`
  is meant to hold embedded episodic recall of specific events and
  conversations.
- **Eventual smart-home interconnection.** THEA is meant to notice and act
  on the physical environment she runs in, not just talk about it —
  device control, multi-room audio, and presence-aware behavior are part
  of the design from the start, not a later add-on.

## The anatomical metaphor

The six systems are named after body parts on purpose — the metaphor is
core to how the project is conceived, not decorative. Each is (or will be)
its own service; only `brain`'s data layer has real, working code today.

| System | Role | What it does |
|---|---|---|
| **brain** | Data | PostgreSQL + pgvector data layer — the structured facts and long-term memory THEA draws on. The one system with real, working code (schema + migrations); the Python data-access layer above it is still scaffolding. |
| **heart** | Orchestration | The hub. Receives triggers, assembles context from `brain`, calls the Claude API, dispatches tool calls, produces the response. Owns the proactive scheduler and post-conversation memory extraction. If you're trying to understand how THEA "thinks," this is the system to read. Not yet implemented. |
| **senses** | Perception | Always-on, local: wake word detection, ambient audio filtering, vision events. A filter, not a thinker — cheap, continuous detection that escalates only what clears the bar, publishing validated triggers to `heart`. Not yet implemented; lowest priority to build first among the core-path systems. |
| **muscles** | Actuation | The only system that changes something in the physical world — Home Assistant integration, MQTT device control, multi-room audio output via ElevenLabs + Snapcast. Receives commands from `heart` and reports back success/failure only. Not yet implemented. |
| **body** | Visibility | A read-only dashboard — memory browser, logs, system health. The one system THEA functions entirely without; deliberately last priority, built after everything else is talking to itself. Not yet implemented. |
| **bones** | Structure | DevOps — Docker, compose, CI/CD spanning every other system. Not a runtime service, so it isn't a top-level folder in this monorepo; see `docs/ARCHITECTURE.md` for why and where its pieces live now. |

## Status, honestly

As of this consolidation, THEA is in early scaffolding. The only genuinely
implemented piece is `brain`'s Postgres/pgvector schema — everything else
(orchestration, perception, actuation, the dashboard) is designed in
detail (each system's own README is a real design document) but not yet
built. See `docs/ARCHITECTURE.md` for the precise built-vs-planned
breakdown per system, and the reasoning behind decisions made while
consolidating six separate repos into this one.
