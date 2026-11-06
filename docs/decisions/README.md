# Architecture Decision Records

Short records of decisions that shape the codebase: what was decided, why, and
what it costs. Add one when a choice would surprise a future reader. Use the
next number, and never rewrite an accepted ADR; supersede it with a new one.

| ADR | Decision |
|---|---|
| [0001](0001-monorepo-layout.md) | One monorepo: `apps/`, `services/`, `packages/` |
| [0002](0002-descriptive-names.md) | Descriptive names in code; body-part names stay as codenames |
| [0003](0003-claude-only-from-agent.md) | Only the agent calls Claude |
| [0004](0004-agent-owns-the-database.md) | The agent imports the DB layer directly; everyone else goes through the agent |
| [0005](0005-voice-stack.md) | Local-first voice stack in its own service |
| [0006](0006-tauri-desktop.md) | Tauri 2 for the desktop app; a local MCP bridge for PC control |
| [0007](0007-tailscale-remote-access.md) | Tailscale for remote access; nothing on the public internet |
| [0008](0008-env-for-secrets-only.md) | `.env` holds secrets only; behavior lives in `thea.config` |
