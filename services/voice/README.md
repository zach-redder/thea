# voice

*Codename: senses (ears) + muscles (voice).* Everything THEA hears and says.
Always on and local:
- **Input:** VAD → wake word / ambient relevance → speech-to-text → speaker
  ID → `VoiceUtterance` trigger to the agent.
- **Output:** `SpeakCommand` → TTS → Snapcast, to the right room.

It filters, it doesn't think: no LLM calls, no database, and raw audio never
leaves memory.

```bash
uv run --package thea-voice uvicorn thea_voice.main:app --reload --port 8010
uv sync --package thea-voice --extra models    # the heavy model stack, when you start building it
```

## Layout

```
src/thea_voice/
  main.py              /health, POST /api/v1/speak (auth'd)
  pipeline.py          frame pipeline wiring (Pipecat-style)
  buffer.py            in-memory rolling buffer
  publisher.py         triggers -> agent
  input/               vad, wake_word, stt, diarization, relevance_filter
  output/              tts, snapcast
models/                downloaded weights (gitignored)
```

**Status:** skeleton. Design: [docs/voice-pipeline.md](../../docs/voice-pipeline.md).
