# THEA

## What she is

THEA is a personal AI assistant: one persistent presence that knows you,
remembers what happened, and can act in the real world. The goal is closer to
JARVIS than to a chatbot you open in an app.

- **Persistent.** She remembers across conversations. Structured facts (your
  profile, goals, people, home, wardrobe) live in Postgres. Episodic memories
  ("we talked about the lease renewal on Tuesday") are embedded for semantic
  recall.
- **Everywhere you are.** One agent behind every surface: a voice in each room,
  the web dashboard, an installable app on your phone, and a desktop app on
  your PC.
- **Able to act.** She controls lights, audio and climate through Home Assistant,
  calls integrations (calendar, Notion, Spotify, Plaid) and, with your
  confirmation, uses your computer.
- **Proactive, within limits.** Morning briefs, stale-data nudges and a nightly
  synthesis of where your life is at. All of it respects do-not-disturb and
  privacy mode.

The full product definition (requirements, capability map and the scenes the finished system should handle)
is [vision.md](vision.md). The persona brief is [persona.md](persona.md).

## Personality

THEA should sound like a specific person, not a generic assistant: direct, dry,
occasionally sardonic, with no disclaimers recited. Her voice is defined in
data, not code. The system prompts live in `thea.prompts`, and tone guidance
(vocabulary, phrases to avoid, humor style) lives in `identity.context`. So
you shape her personality by editing rows, not redeploying.

## Design principles

1. **One brain, many surfaces.** Only the agent service reasons or calls an LLM.
   Every other service perceives, displays or actuates.
2. **Cheap gates before expensive work.** Voice activity detection runs always;
   speech-to-text only when someone's talking; Claude only when it's for THEA.
   The same goes for vision.
3. **Configuration is data.** Behavior lives in `thea.config`, `thea.prompts` and
   `thea.tools`. `.env` holds secrets only.
4. **Act carefully.** Any tool marked `requires_confirm` (unlocking doors,
   spending money, running things on your PC) needs an explicit yes.
5. **Private by default.** Raw audio and video never leave the perception
   services or touch disk. Your data stays on hardware you own, except the
   model calls themselves.

## Codenames

The project started as six repos named after body parts. The code now uses
plain descriptive names, but the metaphor still says what each piece is for:

| Codename | Directory | Role |
|---|---|---|
| **heart** | `services/agent` | Orchestration: context, Claude, tools, memory, scheduler, the API |
| **senses** | `services/voice`, `services/vision` | Perception: wake word, ambient audio, cameras |
| **muscles** | `services/home` (+ speech output in `services/voice`) | Actuation: the only thing that changes the physical world |
| **brain** | `packages/thea-db` | Memory: Postgres + pgvector schema, models, repositories |
| **body** | `apps/web` (+ `apps/desktop`) | Visibility: what you see and touch |
| **bones** | `docker-compose.yml`, `.github/`, `infra/` | Structure: build, run, deploy |

Why the names changed: [decisions/0002-descriptive-names.md](decisions/0002-descriptive-names.md).

## Status

Early scaffolding. The plan for the rest is [implementation-plan.md](implementation-plan.md). What's real today:
- the database schema (generated from `THEA DB.xlsx`)
- runnable service skeletons with health checks, auth and tests
- the web app shell (talk screen with the orb, dashboard pages, installable on a phone)

The agent loop, voice pipeline, home control and desktop bridge are designed
but not built. [roadmap.md](roadmap.md) has the order.
