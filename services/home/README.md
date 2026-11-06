# home

*Codename: muscles.* The only service that changes the physical world. It
receives `DeviceCommand`s from the agent, carries them out through Home
Assistant (or MQTT / Kasa for devices HA doesn't cover), and reports success
or failure. It holds no state and makes no decisions.

```bash
uv run --package thea-home uvicorn thea_home.main:app --reload --port 8030
```

## Layout

```
src/thea_home/
  main.py                  /health, POST /api/v1/commands (auth'd)
  dispatch.py              DeviceCommand -> backend
  home_assistant/          REST/WebSocket client, environment.devices -> entity mapping
  mqtt/                    MQTT client
```

**Status:** skeleton ([roadmap](../../docs/roadmap.md), Phase 6). Open question:
the agent could instead call Home Assistant's own MCP server as a tool. Decide
when building. This service is still the place for anything that needs local
network access or retries.
