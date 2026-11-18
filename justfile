# THEA task runner -- https://just.systems (winget install Casey.Just)
# Run `just` to list recipes.

set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

default:
    @just --list

# Install every Python and JS dependency
setup:
    uv sync --all-packages --extra schema
    corepack pnpm install

# Run the agent API with hot reload (http://localhost:8000/docs)
agent:
    uv run --package thea-agent uvicorn thea_agent.main:app --reload --port 8000

# Run the web UI (http://localhost:3000)
web:
    corepack pnpm --filter web dev

# Start Postgres + Redis and apply migrations in Docker
db:
    docker compose up -d postgres redis migrate

# Full local stack in Docker (add --profile perception for voice/vision)
up *args:
    docker compose up --build {{args}}

# Lint, typecheck and format-check everything
lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run mypy services packages
    corepack pnpm --filter web lint
    corepack pnpm --filter web typecheck

# Run every test suite
test:
    uv run pytest

# Auto-fix formatting
fmt:
    uv run ruff check --fix .
    uv run ruff format .
    corepack pnpm --filter web format

# Regenerate migrations and models from THEA DB.xlsx
gen-schema:
    uv run python packages/thea-db/scripts/generate_migrations.py
    uv run python packages/thea-db/scripts/generate_models.py

# Fail if migrations are out of date with THEA DB.xlsx
check-schema:
    uv run python packages/thea-db/scripts/generate_migrations.py --check

# Extract personal seed data from THEA DB.xlsx (gitignored output)
seed:
    uv run python packages/thea-db/seed/import_from_sheet.py
