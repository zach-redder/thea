# 0010: Tiered model routing for fast, smart responses

**Status:** accepted (2026-11-05)

## Context

The requirement is "fast response time, but smart about it." A single large
model for everything is slow and costly for "lights off"; a single small
model is shallow for planning and analysis. Voice makes latency a core part of
how natural she feels.

## Decision

Route each request through four tiers (reflex, fast, default, deep), picked by
`runtime/intent_router.py`, with models configured in `thea.config`. See
[agent-runtime.md](../agent-runtime.md#model-routing-the-speedintelligence-trade).

- Tier 0 uses no LLM (deterministic device/timer commands).
- Streaming is mandatory end to end, including sentence-level TTS.
- Prompt caching is protected as an invariant: the prefix is byte-stable and
  the tool list is fixed per session.
- Mid-turn escalation is allowed, covered by a short spoken filler.

## Consequences

- Most voice turns are answered in about a second or less.
- The router is a new piece to tune and test. Misrouting is a quality bug.
- Cost drops, because the big model runs only when needed.
- Persona must hold across tiers, so the same core prompt is used (shorter
  context for fast tiers, not a different personality).
