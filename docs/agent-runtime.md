# Agent runtime

How THEA decides, how fast she answers, and how much she's allowed to do on
her own. Requirement: **fast response time, but smart about it.**

## Model routing (the speed/intelligence trade)

Not every request needs the biggest model. The agent routes in tiers, and
models are named in `thea.config` (`fast_model`, `default_model`) so they can
change without code.

| Tier | When | Path | Target latency to first audio/text |
|---|---|---|---|
| **0: Reflex** | Unambiguous device/timer/volume commands ("lights off", "stop") | Regex/grammar + local rules → tool, no LLM | < 300 ms |
| **1: Fast** | Short factual or conversational turns, tool-light | `fast_model`, minimal context, no retrieval | ~ 0.8–1.2 s |
| **2: Default** | Normal conversation, memory-aware, a few tools | `default_model`, full context, prompt-cached | ~ 1.5 s |
| **3: Deep** | Planning, analysis, long documents, multi-step tool work | `default_model` (or larger), extended thinking, streams progress | seconds; she says she's on it |

The **intent router** (`runtime/intent_router.py`) picks the tier. Its rules:
- Start at Tier 0 with deterministic matching against known device phrases
  and `thea.tools` aliases.
- Otherwise ask a very cheap classifier (or the fast model with a tiny
  prompt) for `{tier, needs_memory, needs_tools}`.
- **Escalate** mid-turn: if the fast model signals it's out of its depth, hand
  off to Tier 2/3 without the user noticing (a short filler line covers the
  gap).
- Err toward the fast tier for voice, toward the default tier for typed
  chat.

## Staying fast

- **Stream everything.** Tokens stream to the client; sentence boundaries
  stream to TTS. First audio before the answer is finished.
- **Prompt caching.** See below. The big stable prefix is paid for once.
- **Parallelize context gathering.** Postgres config/profile, pgvector
  retrieval, Redis session and calendar next-up run concurrently
  (`asyncio.gather`).
- **Precompute.** The stable profile block and persona are built at start-up
  and on change, not per turn.
- **Speculative start.** For voice, start context assembly on the wake word,
  before the utterance ends.
- **Never block on side effects.** Memory extraction, logging and stats
  updates run after the reply.
- **Warm connections.** Persistent HTTP/2 clients for Anthropic, Voyage,
  ElevenLabs, Home Assistant.
- **Backchannel.** For tool calls over ~1 s, a short spoken acknowledgement
  ("one sec") keeps it feeling alive.

## Prompt caching

Anthropic prompt caching makes the long prefix nearly free after the first
call. Protect it:

- Order the prompt **most-stable-first**: persona → stable profile →
  situational prompt → channel style → *(cache breakpoint)* → memories → live
  context → conversation.
- The prefix must be **byte-identical** between turns of a conversation. No
  timestamps, no random ordering, no re-serialized JSON in it.
- Don't add or remove tools mid-conversation. The tool list is part of the
  prefix. Offer a stable set per session; availability changes apply to the
  *next* session.
- Strict user/assistant alternation; never inject synthetic user messages.

## The turn loop

```
receive message ─▶ route (tier) ─▶ build context ─▶ call model (stream)
                                         ▲                │
                                         │          tool call? ──▶ confirm? ──▶ run tool
                                         └──────────── result ◀──────────────────┘
                                                          │
                                           final text ─▶ dispatch (channel, voice) ─▶ post-turn: log, extract memory, update stats
```

Safety valves in the loop: a maximum number of tool iterations per turn, a
per-turn token/cost budget, a wall-clock deadline, and an emergency stop
(`POST /api/v1/stop`) that cancels in-flight work and any queued actions.

## Autonomy levels

How much she may do without asking is a setting per *capability*, stored with
the tool (`thea.tools.requires_confirm`, plus an `autonomy` level to be
added). Defaults are conservative and loosen as trust is earned.

| Level | Behavior | Example |
|---|---|---|
| **0: Observe** | Reads and notices, says nothing | Watching GitHub activity, calendar changes |
| **1: Suggest** | Brings it up when relevant, doesn't act | "You've got a conflict Thursday" |
| **2: Act, then tell** | Does low-risk, reversible things on her own | Dim lights, set a timer, add a calendar reminder, log a habit |
| **3: Ask first** | Prepares the action; waits for a yes | Send a message, post, spend, unlock, run a shell command |
| **4: Never** | Refuses regardless | Destructive operations on accounts, anything in the deny list |

Defaults by capability class:

| Class | Default level |
|---|---|
| Reading accounts (GitHub, Twitch, social, calendar, finance) | 0–1 |
| Smart-home comfort (lights, music, thermostat) | 2 |
| Smart-home security (locks, alarms, garage) | 3 |
| Writing to accounts (post, comment, email, DM, calendar invite to others) | 3 |
| Money (Plaid is read-only; any payment) | 3 / never |
| Desktop bridge | 3 for everything |

## Proactivity

Scheduled jobs and event triggers let her speak first, but **she earns the
interruption**:

- **Event triggers** (a PR finishes, a stream goes live, a door opens, a
  calendar item approaches) go through a *worth-interrupting?* check: urgency
  × relevance × his current state (in a meeting, asleep, DND, focused).
- **Scheduled jobs:** morning brief, evening wrap-up, stale-data nudges,
  nightly synthesis, weekly review.
- **Respect state.** `do_not_disturb`, meetings (calendar), sleep, and
  `privacy_mode` suppress speech; she queues non-urgent items for the next
  natural moment or for the dashboard.
- **Rate limit** unprompted speech; repeated dismissals reduce frequency.

## Failure behavior

- LLM down or slow → fall back to Tier 0 reflexes and a plain "I'm having
  trouble thinking right now"; device control keeps working.
- A tool fails → tell him in a sentence, say what she tried, don't loop.
- Actuator unreachable → say so, don't pretend it worked.
- Nothing retried silently for anything that spends money, sends a message or
  changes a lock.
