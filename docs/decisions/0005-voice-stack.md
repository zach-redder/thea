# 0005: Local-first voice stack in its own service

**Status:** accepted (2026-11-05)

## Context

THEA should hear the house continuously, which means always-on audio
processing. Streaming every room's audio to a cloud service would be costly,
slow and a privacy problem.

## Decision

- A dedicated `voice` service owns the audio hardware in both directions.
- Input is a gate cascade, cheapest first:
  - Silero VAD runs always.
  - Porcupine wake word, or the ambient relevance filter, runs only on speech.
  - faster-whisper STT runs locally, only on a trigger.
  - pyannote identifies the speaker.
  - Only transcripts leave the service.
- Output uses ElevenLabs TTS (local fallback possible behind the same
  interface) and Snapcast for synchronized multi-room playback.
- Build the pipeline with [Pipecat](https://github.com/pipecat-ai/pipecat)'s
  frame-processor model, which already integrates these components and offers
  a FastAPI WebSocket transport for client push-to-talk.

## Consequences

- Raw audio never leaves RAM on the home server.
- The service needs real hardware (mics, speakers), so it's an opt-in compose
  profile (`perception`) and heavy dependencies are an optional extra
  (`--extra models`).
- STT quality and latency depend on the server's CPU or GPU.
