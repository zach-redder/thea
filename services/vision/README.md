# vision

*Codename: senses (eyes).* Camera perception. A cheap always-on gate (motion
or person detection) per camera, escalating to an expensive vision-language
pass only when something is flagged. It publishes `VisionEvent` triggers to
the agent and never stores frames.

```bash
uv run --package thea-vision uvicorn thea_vision.main:app --reload --port 8020
uv sync --package thea-vision --extra models
```

## Layout

```
src/thea_vision/
  main.py              /health
  motion_detector.py   always-on gate
  scene_analysis.py    expensive pass, only on flag
  publisher.py         triggers -> agent
models/                downloaded weights (gitignored)
```

**Status:** skeleton; the lowest-priority service ([roadmap](../../docs/roadmap.md), Phase 8).
