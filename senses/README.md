# thea-senses

Always-on perception for thea — wake word, ambient audio, and vision. Runs continuously and locally, independent of whether a conversation is active.

## Overview

thea-senses is what makes thea feel present rather than purely reactive. It handles three input channels — explicit wake-word activation, filtered ambient audio (so thea can notice things said without being addressed directly), and vision events (motion/person detection escalating to scene analysis when warranted) — and publishes validated triggers to thea-heart.

This repo deliberately does **not** talk to Claude, Postgres, or any external API for reasoning. It's a filter, not a thinker: cheap, continuous, always-on detection gating expensive processing, only escalating what actually clears the bar.

## Role in the thea system

thea-senses → thea-heart only, one direction. It has no other dependencies in the system:

- Publishes trigger events (with transcript/classification, not raw audio) to thea-heart's webhook endpoints.
- Does not persist raw audio or video beyond a short in-memory rolling buffer — nothing here writes to thea-brain directly.
- Speaker diarization output feeds `config.privacy_mode` indirectly, via thea-heart, when an unfamiliar voice is detected.

## Tech stack

- **Python 3.11+**
- **Porcupine** (Picovoice) — wake word detection
- **Silero VAD** — the always-on gate before anything more expensive runs
- **Whisper** (local, e.g. faster-whisper) — speech-to-text, only invoked when VAD triggers
- **pyannote.audio** (or similar) — speaker diarization / guest detection
- **A lightweight local vision model** (motion/person detection) gating a heavier vision-language pass only when flagged
- **ReSpeaker USB mic array** — hardware target for multi-room capture

## Planned structure

```
thea-senses/
├── app/
│   ├── main.py
│   ├── audio/
│   │   ├── wake_word.py
│   │   ├── vad.py
│   │   ├── stt.py
│   │   ├── diarization.py
│   │   └── relevance_filter.py    # directed-at-Zach? escalate or discard
│   ├── vision/
│   │   ├── motion_detector.py     # cheap always-on gate
│   │   └── scene_analysis.py      # expensive pass, only on flag
│   ├── publisher.py                # sends validated triggers to thea-heart
│   └── buffer.py                   # short rolling buffer, nothing persisted
├── models/                         # local model weights
└── requirements.txt
```

## Status

**Not yet implemented.** Lowest-priority to build first among the core-path repos — thea-heart can be developed and tested against manually-triggered/mocked input before real always-on perception exists. Build once thea-heart's context builder and intent router are working.

## Related repos

thea-heart (only direct dependency) · thea-brain · thea-muscles · thea-bones · thea-body
