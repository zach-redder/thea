"""The contract every account/service integration implements (docs/integrations.md).

An integration has two separate jobs:
- awareness: `sync()` / `handle_webhook()` keep THEA informed without being asked.
- action: `tools()` exposes what the model may call, gated by thea.tools and autonomy levels.
"""
