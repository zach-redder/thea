# Ambient presence and the home

Requirements covered: microphones through the house with a wake word,
understanding *when Zach is talking to her* without one, cameras, controlling
lights and other electronics, and picking up on things "randomly" (she
notices and connects). The pipeline mechanics are in
[voice-pipeline.md](voice-pipeline.md); this doc covers the behavior.

> **Status:** designed, not built. Phases 5, 6 and 8 of the
> [implementation plan](implementation-plan.md).

## Three ways she gets activated

| Mode | Trigger | Behavior |
|---|---|---|
| **Explicit** | Wake word ("Hey THEA") or push-to-talk in an app | Always responds |
| **Implicit (addressed)** | No wake word, but it's clearly directed at her | Responds, quietly confident |
| **Passive (notice)** | Not directed at her, but worth noticing | Doesn't speak; may note a memory or queue a reminder |

The hard part is the middle one. Everything else is a gate.

## Understanding when he's talking to her

A cascade, cheapest signals first. Each stage can decide, defer or discard.

1. **Is it speech, and is it Zach?** VAD, then speaker ID (pyannote /
   embedding match against his enrolled voice). Other voices default to
   *guest*: don't act on them, enable `privacy_mode`.
2. **Is there a wake word?** If yes → explicit.
3. **Conversation window.** If she spoke in the last ~20 s in this room, a
   follow-up is almost certainly for her. No wake word needed.
4. **Acoustic cues.** Short utterance after a pause, directed energy, speaking
   toward a mic. No phone-call cadence. Not overlapping with other voices.
5. **Contextual cues.** Is he alone? Is he on a call (calendar, mic
   activity, headset)? Is the TV on (cross-check with media state)? Is a
   camera showing him facing a device or alone in the room?
6. **Semantic classifier.** If still ambiguous, a tiny model scores the
   transcript: does it sound like a request, a question to an assistant, or a
   musing for himself? ("What was that library…" → yes. "Ugh, this bug" → no.)
   Output: `{addressed: 0..1, intent_hint}`.

Decision thresholds, tuned over time:
- ≥ 0.85 → respond.
- 0.5–0.85 → *ambient memory only* or a very short, optional response, and
  log it so thresholds can be tuned from his corrections.
- < 0.5 → discard.

**He can always teach her.** "THEA, I wasn't talking to you" lowers confidence
on similar utterances; "you can chime in when I'm stuck on code" raises it for
a context. These preferences are stored (`thea.config` / a preferences table),
not hard-coded.

### Safeguards
- A visible/audible **state**: the orb in the web app, an LED on the mic
  hardware, and a spoken "I'm listening" setting.
- **Mute everywhere** with one phrase or button (`is_listening=false`), and a
  physical mute on the mic arrays.
- Calls, meetings and guests default to *not captured*.

## Randomly picking up on things

"Notice" behavior should feel like attentiveness, not surveillance.

- **Ambient mentions → memory.** Only when addressed or when Zach states a
  durable fact in her hearing and is alone ("I need to renew my passport
  before March"). Stored as a candidate memory, confirmed lightly later
  ("Want me to set a reminder for the passport?").
- **Cross-signal connections.** She correlates calendar, location, habits and
  home state: "You've been at the desk since 8 and haven't eaten."
- **Event-driven.** Doorbell, a package, a person at the door
  (vision) → decides if it's worth saying.
- All of this passes the **worth-interrupting?** gate in
  [agent-runtime.md](agent-runtime.md#proactivity). Noticing is cheap, but
  speaking is rationed.

## Microphones

- **One far-field USB mic array per room** (ReSpeaker-class; beamforming, echo
  cancellation, an LED ring). Start with one room.
- **Always-on cheap, expensive on demand:** VAD runs continuously; wake word and
  relevance only on speech; STT only on a trigger.
- **No audio storage.** A few seconds in RAM so the words before the wake word
  aren't lost. Nothing is recorded to disk.
- **Self-trigger suppression:** while THEA is speaking in a room, that room's
  wake-word detector is gated (or uses acoustic echo cancellation).
- **Phone as a mic:** the PWA/Shortcuts path is the "mic" when he's away.

## Cameras

- **IP cameras (RTSP)** on the LAN, or USB, read by `services/vision`. Frames
  are processed in memory, never stored.
- **Cheap gate:** motion / person detection (OpenCV + a small YOLO model).
  This runs continuously and costs almost nothing.
- **Expensive pass only when flagged:** a vision-language model describes the
  scene ("a person put a package at the door").
- **What she uses it for:** presence per room (so speech goes to the right
  speakers), arrival/departure, package and visitor events, "where did I leave
  my keys" (only if enabled), and the context cues above.
- **Privacy defaults:** no cameras in bedrooms/bathrooms; per-camera
  enable/disable; vision events carry labels and short summaries only; a
  global "camera privacy" switch in the dashboard and by voice.

## Presence model

Presence is derived, not detected by one sensor:

```
mic activity + speaker ID + camera person-events + phone location/Wi-Fi + Home Assistant occupancy
                         │
                   fuse in the agent ──▶ presence: {room, confidence, since}  (Redis, 15 min TTL)
```

Presence drives:
- **Where speech comes out** (`SpeakCommand.rooms` defaults to the current
  room).
- **Context** ("you're in the kitchen").
- **Automation** ("goodnight" turns off the downstairs).
- **Whether it's okay to speak at all** (asleep, in a meeting).

## Controlling the home

`services/home` executes; the **agent** decides. Home Assistant is the hub, so
every protocol (Zigbee, Z-Wave, Matter, Wi-Fi, cloud) is HA's problem and
THEA gets one clean API.

| Domain | Examples | Autonomy |
|---|---|---|
| Lighting | on/off, brightness, color, scenes | 2: act, then tell |
| Climate | thermostat, fans, AC | 2 |
| Media | speakers, TV, music (Spotify/Snapcast) | 2 |
| Appliances / plugs | desk lamp, coffee maker, fans, printers | 2 |
| Blinds | open/close | 2 |
| Security | locks, garage, alarm, cameras on/off | 3: ask first |
| Computers | wake/sleep/lock PC (via the desktop bridge or Wake-on-LAN) | 3 |

How devices are known: `environment.devices` rows map to Home Assistant
entity ids (`home_assistant/entities.py`). Rooms are `environment.rooms`.
Natural-language targets ("the lamp by the couch") resolve against these
tables, so she never needs command syntax.

Scenes and routines ("movie mode", "goodnight", "leaving") are defined as HA
scenes/scripts and referenced by name from her tools. Adding one in HA makes it
voice-controllable with no code change.

Two integration paths exist, and the plan starts with the simpler one:
1. **Direct tool** (recommended first): the agent calls Home Assistant via its
   MCP server / REST API as a tool.
2. **`services/home` mediator:** for retries, local-network-only calls, and
   non-HA devices (MQTT, Kasa). Introduced when path 1 isn't enough.

## Hardware shopping list (starter)

| Item | Why |
|---|---|
| Home server (Beelink SER7 / NUC 13 Pro, 32 GB) | Runs the whole stack |
| Home Assistant (Green/Yellow, or container) + Zigbee dongle | Device hub |
| ReSpeaker-class USB mic array × rooms | Far-field voice input |
| Raspberry Pi + speaker × rooms (Snapcast clients) | Synchronized speech/music output |
| 1–2 RTSP IP cameras | Presence and events |
| Smart bulbs/plugs (Zigbee, Matter) | Things to control |
| Optional GPU | Faster local STT / vision |
