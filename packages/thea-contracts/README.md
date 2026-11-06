# thea-contracts

Pydantic models for every message that crosses a service boundary:

| Model | Direction | Endpoint |
|---|---|---|
| `VoiceUtterance`, `VisionEvent` (`Trigger`) | voice / vision -> agent | `POST /api/v1/triggers` |
| `SpeakCommand` | agent -> voice | `POST /api/v1/speak` |
| `DeviceCommand` | agent -> home | `POST /api/v1/commands` |

Rules:
- Messages are immutable and strict (`extra="forbid"`).
- They carry a UUID `id` and a UTC `created_at`.
- JSON uses snake_case.
- Perception events carry **transcripts and labels, never raw audio or video**.

Add a field here first, then update the producer and consumer.

See [`docs/architecture.md`](../../docs/architecture.md).
