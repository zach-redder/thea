# steve-body

Frontend dashboard for STEVE — memory browser, logs, and system health. The one repo STEVE functions entirely without.

## Overview

steve-body is an observability and management layer, not part of STEVE's request/response loop. It exists so Zach can browse what STEVE remembers, see recent activity, and check whether integrations are actually connected — without needing to query Postgres directly. Lowest priority of the six repos; build it last, after steve-heart, steve-brain, steve-senses, and steve-muscles are actually talking to each other.

## Role in the STEVE system

steve-body is read-only and one-directional — it never issues commands, only displays state:

- **steve-body → steve-heart**: reads via a thin, read-only HTTP API (not yet built) rather than connecting to steve-brain's Postgres instance directly. Decision made explicitly: a browser-facing dashboard shouldn't hold raw DB credentials, even on a local network.
- Displays `steve.memories`, `steve.integrations` connection status, recent conversation logs, and system health — all sourced from steve-brain via that API layer.

## Tech stack

- **React** + **TypeScript**
- **Vite**
- Component/styling approach to be decided when this repo is actually built — no framework lock-in yet beyond React/TS

## Planned structure

```
steve-body/
├── src/
│   ├── pages/
│   │   ├── MemoryBrowser.tsx     # steve.memories + identity/wardrobe/environment
│   │   ├── Logs.tsx
│   │   └── SystemHealth.tsx      # steve.integrations status per row
│   ├── components/
│   ├── api/
│   │   └── client.ts             # read-only calls into steve-heart's dashboard API
│   └── main.tsx
└── package.json
```

## Status

**Not yet implemented, and lowest priority.** Depends on steve-heart exposing a read-only HTTP API that doesn't exist yet either — don't start this until that's in place.

## Related repos

steve-heart (sole data source, via HTTP) · steve-brain · steve-senses · steve-muscles · steve-bones
