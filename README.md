# thea-body

Frontend dashboard for thea — memory browser, logs, and system health. The one repo thea functions entirely without.

## Overview

thea-body is an observability and management layer, not part of thea's request/response loop. It exists so Zach can browse what thea remembers, see recent activity, and check whether integrations are actually connected — without needing to query Postgres directly. Lowest priority of the six repos; build it last, after thea-heart, thea-brain, thea-senses, and thea-muscles are actually talking to each other.

## Role in the thea system

thea-body is read-only and one-directional — it never issues commands, only displays state:

- **thea-body → thea-heart**: reads via a thin, read-only HTTP API (not yet built) rather than connecting to thea-brain's Postgres instance directly. Decision made explicitly: a browser-facing dashboard shouldn't hold raw DB credentials, even on a local network.
- Displays `thea.memories`, `thea.integrations` connection status, recent conversation logs, and system health — all sourced from thea-brain via that API layer.

## Tech stack

- **Next.js 15** (App Router) + **TypeScript**
- **React 18**
- Styling approach to be decided when this repo is actually built — no CSS framework lock-in yet

## Structure

```
thea-body/
├── app/
│   ├── layout.tsx          # required root layout -- minimal, no real UI yet
│   ├── page.tsx             # root route stub
│   ├── memory/
│   │   └── page.tsx         # thea.memories + identity/wardrobe/environment
│   ├── logs/
│   │   └── page.tsx
│   └── health/
│       └── page.tsx         # thea.integrations status per row
├── components/
├── lib/
│   └── api-client.ts        # read-only calls into thea-heart's dashboard API
├── package.json
├── tsconfig.json
├── next.config.mjs
├── .env.example
└── .gitignore
```

Note on why `app/layout.tsx` and each `page.tsx` have minimal placeholder content rather than being fully empty like the rest of the scaffold: Next.js's App Router requires a valid root layout and a valid default export in every routed `page.tsx` just to build. Unlike the old Vite setup (where an empty, unrouted component file didn't block the build), an empty `page.tsx` here would fail `next build` outright. So these are connective tissue only — `return null`, nothing more — not real UI.

## Status

**Not yet implemented, and lowest priority.** Depends on thea-heart exposing a read-only HTTP API that doesn't exist yet either — don't start this until that's in place.

## Related repos

thea-heart (sole data source, via HTTP) · thea-brain · thea-senses · thea-muscles · thea-bones
