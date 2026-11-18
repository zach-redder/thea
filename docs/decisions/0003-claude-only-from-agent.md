# 0003: Only the agent calls Claude

**Status:** accepted (carried over from the original `thea-heart` design)

## Context

LLM calls are where cost, latency, safety and personality all concentrate.
If several services called the model, prompts, caching and tool permissions
would fragment.

## Decision

`services/agent` (`thea_agent/llm/claude_client.py`) is the only code that
calls an LLM. Perception services send transcripts and labels; actuators get
commands. Models are chosen at runtime from `thea.config.default_model` and
`fast_model`.

Claude is the reasoning model because of its tool use, prompt caching, native
MCP support and long context. Embeddings come from Voyage AI (Anthropic's
recommended embeddings provider), also called only from the agent.

## Consequences

- Prompt caching works, because there's one stable prefix per conversation.
- Swapping or adding a provider touches one module.
- The agent is a single point of failure for reasoning. Actuators and
  perception keep running without it, but THEA can't think.
