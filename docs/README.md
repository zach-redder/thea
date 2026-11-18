# THEA documentation

**Building THEA? Read [vision.md](vision.md), then [implementation-plan.md](implementation-plan.md).**
Everything else is reference.

## Product and plan

| Doc | Read it when |
|---|---|
| [vision.md](vision.md) | You need to know what THEA is *supposed* to be: requirements, capability map, scenes, open questions |
| [implementation-plan.md](implementation-plan.md) | You're about to build something. Phased tasks, acceptance tests, session protocol |
| [roadmap.md](roadmap.md) | You want the one-screen version of the plan |
| [overview.md](overview.md) | You want the short "what is she" and the codename map |

## How she works

| Doc | Read it when |
|---|---|
| [persona.md](persona.md) | You're writing a prompt, a voice setting, or anything she says |
| [memory.md](memory.md) | You're touching Redis, `thea.memories`, extraction or retrieval |
| [agent-runtime.md](agent-runtime.md) | You're working on the turn loop, model routing, latency, autonomy or proactivity |
| [ambient-and-home.md](ambient-and-home.md) | You're working on mics, the wake word, "is he talking to me?", cameras or home control |
| [voice-pipeline.md](voice-pipeline.md) | You're working on STT, TTS, ElevenLabs or room routing |
| [integrations.md](integrations.md) | You're connecting an account (GitHub, Twitch, calendar, social) or the phone |
| [stats-and-dashboard.md](stats-and-dashboard.md) | You're working on stats, habits or the dashboard screens |
| [desktop.md](desktop.md) | You're working on the desktop app or letting THEA use your PC |

## System reference

| Doc | Read it when |
|---|---|
| [architecture.md](architecture.md) | You need the system map: services, boundaries, data flow, stack |
| [api.md](api.md) | You're building a client (web, phone, desktop, Shortcuts) or a service |
| [data-model.md](data-model.md) | You need the database tables, or the planned additions |
| [security.md](security.md) | You're touching auth, secrets, tool permissions or privacy |
| [remote-access.md](remote-access.md) | You want to reach THEA from your phone outside the house |
| [development.md](development.md) | You're setting up a machine or running anything locally |
| [conventions.md](conventions.md) | You're about to write code or name something |
| [decisions/](decisions/) | You want to know *why* something is the way it is (ADRs) |
| [reference/hermes-agent.md](reference/hermes-agent.md) | You want the patterns borrowed from the Hermes agent |
| [archive/](archive/) | You want the original six-repo READMEs |
