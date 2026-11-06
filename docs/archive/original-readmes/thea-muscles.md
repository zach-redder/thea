# thea-muscles

Actuation for thea — the only repo that changes something in the physical world. Home Assistant control, MQTT, and multi-room audio output.

## Overview

thea-muscles receives commands from thea-heart and carries them out: controlling smart home devices, generating and routing speech output to the right room, and nothing else. It deliberately owns output only — audio *input* (perception) lives in thea-senses, not here, since the two have completely different runtime characteristics (continuous/low-latency vs. command/response).

## Role in the thea system

thea-muscles receives from thea-heart and reports back only success/failure — it holds no independent state and makes no autonomous decisions:

- **thea-heart → thea-muscles**: dispatches actuation commands (device control, speech output) via whatever internal transport thea-heart's `output/dispatch.py` uses.
- **thea-muscles → Home Assistant**: reads/writes device state for whatever's exposed in `environment.devices`.
- **thea-muscles → ElevenLabs → Snapcast**: generates speech and routes it to the correct room, using presence data thea-heart provides (not detected here).

## Tech stack

- **Python 3.11+**
- **Home Assistant** — official REST/WebSocket API, or the built-in MCP Server integration if thea-heart is calling it as a tool directly rather than through this repo (architectural choice to confirm when building)
- **Mosquitto MQTT** — for devices not natively supported by Home Assistant
- **ElevenLabs API** — TTS generation
- **Snapcast** — multi-room audio synchronization and per-room routing
- **Kasa/TP-Link local API** — for smart plugs not routed through Home Assistant

## Planned structure

```
thea-muscles/
├── app/
│   ├── main.py
│   ├── home_assistant/
│   │   ├── client.py
│   │   └── entities.py         # maps environment.devices rows → HA entities
│   ├── mqtt/
│   │   └── client.py
│   ├── audio_output/
│   │   ├── tts.py               # ElevenLabs generation
│   │   └── snapcast.py          # presence-aware room routing
│   └── dispatch.py              # receives commands from thea-heart
└── requirements.txt
```

## Status

**Not yet implemented.** Can be developed against a real Home Assistant instance once one exists, or stubbed with mocked device state early — it doesn't block thea-heart's core logic development.

## Related repos

thea-heart (sole command source) · thea-brain · thea-senses · thea-bones · thea-body
