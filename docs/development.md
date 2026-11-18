# Development

## Prerequisites

| Tool | Why | Install (Windows) |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | Python 3.12 + every Python dependency | `winget install astral-sh.uv` |
| Node.js 22+ (with corepack) | Web app; pnpm comes via corepack | `winget install OpenJS.NodeJS.LTS` |
| [just](https://just.systems) | Task runner (optional; every recipe is a plain command) | `winget install Casey.Just` |
| Docker Desktop | Postgres, Redis, full stack | `winget install Docker.DockerDesktop` |
| Rust + Tauri prerequisites | Only for `apps/desktop` | [tauri.app/start/prerequisites](https://tauri.app/start/prerequisites/) |

uv downloads Python 3.12 automatically (pinned in `.python-version`), and
corepack fetches the pnpm version pinned in `package.json`.

## First run

```bash
cp .env.example .env          # set THEA_API_TOKEN at minimum
just setup                    # uv sync + pnpm install
just db                       # Postgres + Redis in Docker, migrations applied
just agent                    # API on http://localhost:8000 (docs at /docs)
just web                      # UI on http://localhost:3000
```

Or run everything in Docker: `just up` (add `--profile perception` for voice
and vision).

## Everyday commands

| Command | Does |
|---|---|
| `just lint` | ruff, ruff format check, mypy (strict), ESLint, tsc |
| `just test` | pytest across every service and package |
| `just fmt` | Auto-format Python and TypeScript |
| `just gen-schema` | Regenerate migrations and models from `THEA DB.xlsx` |
| `just check-schema` | Fail if migrations are stale relative to the workbook |
| `just seed` | Write your personal seed SQL (gitignored) |

Without `just`, run the commands shown in the `justfile`. They're plain
`uv`, `pnpm` and `docker` calls.

## Workspaces

- **Python:** one `uv` workspace (root `pyproject.toml`) with members
  `services/*` and `packages/*`. There's one lockfile (`uv.lock`) and one
  `.venv`. Workspace packages depend on each other with
  `{ workspace = true }` sources.
  - `uv run --package thea-agent ...` runs inside a member.
  - `uv add --package thea-agent httpx` adds a dependency to it.
- **JavaScript:** one pnpm workspace (`pnpm-workspace.yaml`, `apps/*`) with one
  lockfile. Use `pnpm --filter web <script>` to target an app.

## Adding things

- **A Python service:**
  1. Copy the shape of `services/home`: a `pyproject.toml` with a `src/`
     layout, a `thea_<name>` package, a `/health` endpoint with a test, and a
     Dockerfile.
  2. Add the package to `known-first-party` and `mypy_path` in the root
     `pyproject.toml`.
  3. Add a compose service.
- **A message between services:** add the model to `packages/thea-contracts`
  first, then the producer, then the consumer.
- **A tool for THEA:** add a row to `thea.tools` (and `thea.integrations` if it
  needs credentials), then register a handler in `thea_agent/tools/`. Prefer
  an existing MCP server over writing a native tool.
- **A table or column:** edit `THEA DB.xlsx`, run `just gen-schema`, and commit
  the generated files. Never hand-edit migrations or models.

## Testing

- Every service has at least a `/health` test. New behavior comes with tests
  (red → green → refactor).
- Tests live in `<project>/tests/`. pytest runs them with
  `--import-mode=importlib`, so the same file name can exist in several
  projects.
- Use FastAPI's `TestClient` with `dependency_overrides` for settings (see
  `services/agent/tests/test_api.py`).

## CI

`.github/workflows/ci.yml` runs on every push and PR:
- **Python:** ruff, format check, mypy, pytest
- **Web:** ESLint, tsc, `next build`
- **Docker:** `compose config`, and building the agent, home, web and migrate
  images

The schema drift check can't run in CI, because the workbook never leaves your
machine. Run `just check-schema` before committing schema work.

## Deploying

See [`infra/deploy/README.md`](../infra/deploy/README.md).
