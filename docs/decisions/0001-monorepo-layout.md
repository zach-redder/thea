# 0001: One monorepo with `apps/`, `services/`, `packages/`

**Status:** accepted (2026-11-05)

## Context

THEA began as six repos (`thea-brain`, `-heart`, `-senses`, `-muscles`,
`-body`, `-bones`). They change together, share contracts, and one of them
(`bones`: Docker and CI) existed only to know about the other five. The first
consolidation merged them with history but kept six top-level folders, and
every Python service still named its package `app`, so any cross-service
import would collide.

## Decision

- One repo, grouped by **kind**, a convention shared by Turborepo, Nx and
  most polyglot monorepos:
  - `apps/`: things a person looks at (`web`, `desktop`)
  - `services/`: long-running processes (`agent`, `voice`, `vision`, `home`)
  - `packages/`: libraries services import (`thea-db`, `thea-contracts`)
  - `infra/`: deployment-only assets
- Python uses the **`src/` layout** with unique import names (`thea_agent`,
  `thea_db`, ...) in a single `uv` workspace (one lockfile).
- JS uses one `pnpm` workspace.
- Each service keeps its Dockerfile next to its code. Compose and CI live at
  the root, where the tools require them.

## Consequences

- One PR can change a contract and both of its ends atomically.
- The `src/` layout makes tests run against the installed package, which
  catches packaging bugs.
- Pre-merge history is reachable via `git log --all`, but `git log --follow`
  doesn't cross the original merge commits.
