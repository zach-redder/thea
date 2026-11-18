# Vision

This is the product definition: what THEA is supposed to become, in the
owner's own terms. It's the source of truth that [implementation-plan.md](implementation-plan.md)
is derived from. When a design question comes up, resolve it against this file
first.

## One sentence

A JARVIS-style personal AI: one persistent, warm, sharp presence that knows
Zach's life, remembers everything that matters, hears the house, controls it,
reaches into his accounts and devices, and talks like a thoughtful person, not
a bot.

## The four core requirements

1. **Persistent memory.** She remembers context, preferences, ongoing
   projects and past conversations across sessions, not just inside one chat
   window. Memory accumulates and is retrievable and updatable over time, like
   a real assistant building a working understanding of the person they
   support. → [memory.md](memory.md)
2. **Home interconnection.** She extends beyond the phone/app into ambient
   presence throughout the house: voice-accessible, aware of location and
   environment, able to trigger and respond to home systems.
   → [ambient-and-home.md](ambient-and-home.md)
3. **Natural conversational tone.** *Critical.* She sounds like a warm,
   normal conversation partner. No menu options, no command syntax, no "I am
   an AI assistant, how can I help you today?" She feels like talking to a
   sharp, thoughtful person. → [persona.md](persona.md)
4. **Cross-context continuity.** She behaves the same through voice,
   the phone, the desktop, the web, and any future surface. One memory, one
   persona, one relationship, not fragmented instances. This is why every
   surface is a thin *channel* into the single agent service.
   → [architecture.md](architecture.md)

## Grounding

- **The name.** Thea is the Greek titaness of sight and light, mother of the
  sun, moon and dawn, and the root of "theory" (*theasthai*, "to behold").
  The intended feel is **clarity, insight and thoughtful judgment**, not
  pure task execution.
- **The backronym.** *Thoughtful Holistic Execution Assistant.*
- **The ethics.** Her personality and interaction style are grounded in
  Aristotelian virtue ethics: **practical wisdom (*phronesis*)**, not just
  efficiency. She should weigh what matters, say the honest thing kindly, and
  know when to do less.

## Capability map

Everything the owner asked for, and where it lives. The **Phase** column
points at [implementation-plan.md](implementation-plan.md).

| # | Capability | What it means | Home in the repo | Phase |
|---|---|---|---|---|
| 1 | **Natural conversation** | Warm, human, never boilerplate | `runtime/prompts/`, `thea.prompts`, [persona.md](persona.md) | 1 |
| 2 | **Fast but smart** | Quick replies; depth only when needed | `runtime/intent_router.py`, `llm/` model tiers, [agent-runtime.md](agent-runtime.md) | 1, 5 |
| 3 | **Persistent memory (Redis + Postgres)** | Short-term in Redis, long-term structured + semantic in Postgres | `thea_db`, `memory/`, [memory.md](memory.md) | 1–2 |
| 4 | **Spoken, human voice (ElevenLabs)** | AI voice that sounds natural, streamed | `services/voice/output/tts.py` | 5 |
| 5 | **Microphones + wake word** | Mics through the house, a wake word to activate | `services/voice/input/` | 5 |
| 6 | **Knows when she's addressed** | Picks up on things; understands when Zach is talking *to* her, without the wake word | `input/relevance_filter.py`, [ambient-and-home.md](ambient-and-home.md) | 8 |
| 7 | **Cameras** | Home cameras linked in, as a cheap gate then a scene pass | `services/vision` | 8 |
| 8 | **Home control** | Lights and other tech and electronics | `services/home` | 6 |
| 9 | **Phone connection via API** | Phone sends context and talks to her; she can notify it | `channels/phone.py`, `/api/v1/phone/*`, [integrations.md](integrations.md#phone) | 4 |
| 10 | **Desktop connection** | Native app, plus the agent using the PC with permission | `apps/desktop`, [desktop.md](desktop.md) | 7 |
| 11 | **Accounts and social awareness** | GitHub, Twitch, social media and the rest | `integrations/`, [integrations.md](integrations.md) | 3, 9 |
| 12 | **Calendar, habits, life documentation** | Linked to calendar, tracks habits, keeps the documentation of life | `integrations/calendar`, `identity.*`, `stats/` | 3, 4 |
| 13 | **Stats about me, easy to reach** | A dashboard of Zach's own numbers, a tap away | `stats/`, `apps/web/app/stats`, [stats-and-dashboard.md](stats-and-dashboard.md) | 4 |
| 14 | **Frontend from phone or desktop** | Easy to pull up anywhere | `apps/web` (PWA), `apps/desktop` | 1, 4, 7 |
| 15 | **Database access** | She reads and writes the THEA database | `packages/thea-db` | 1 |
| 16 | **Autonomy** | Acts on her own within agreed limits; proactive | `scheduler/`, autonomy levels in [agent-runtime.md](agent-runtime.md#autonomy-levels) | 8 |

## What "good" feels like

Concrete scenes the finished system should handle. Use them as acceptance
tests for the whole product.

- **Morning.** Zach walks into the kitchen. THEA, quietly, without being
  asked: "Morning. You've got the dentist at 10, and that PR from last night
  finally went green. Want coffee going?" The lights come up slowly. She
  said none of that like a menu.
- **Mid-thought.** Zach, to nobody in particular, working at the desk: "What
  was that library I looked at last week for the websockets thing?" She
  answers from memory, in a sentence, because it was clearly meant for her.
- **Not for her.** Zach is on a call. She hears him talking and stays quiet.
  She never interrupts, never transcribes it into memory, and notes only that
  he was in a meeting.
- **From the phone.** Zach, in a car: "Hey THEA, remind me about the lease
  when I get home." One shortcut, one sentence back, and it fires when he
  arrives.
- **Across surfaces.** He starts a thought out loud in the living room and
  finishes it in the web app at his desk. She picks up the thread without
  being told.
- **Her judgment.** Zach asks her to post something sharp on social media
  late at night. She asks one honest question before doing it. That's
  *phronesis*, not a rule.
- **Her self-awareness.** Asked how he's been doing on sleep, she answers
  with real numbers from his stats, not generalities.

## Non-goals (for now)

- Multi-user or family accounts. THEA is one person's assistant.
- A public SaaS. Nothing is exposed to the internet ([ADR 0007](decisions/0007-tailscale-remote-access.md)).
- Fully autonomous action on money, locks or social posting. Those stay
  behind confirmation until trust is earned ([security.md](security.md)).

## Open questions

Decide these when you reach them. Don't guess in code.

1. **Account access scope.** Read-only by default for social, GitHub and
   Twitch. Which accounts get write access (post, comment, moderate), and
   behind what confirmation?
2. **Camera hardware.** RTSP IP cameras vs. USB. This sets the vision
   service's design.
3. **Server hardware.** Beelink SER7 vs. NUC 13 Pro, and whether a GPU is
   worth it for local speech-to-text.
4. **Wake word.** The phrase ("Hey THEA"?), and whether to train a custom
   Porcupine keyword.
5. **Voice.** Which ElevenLabs voice, and whether to clone one.
