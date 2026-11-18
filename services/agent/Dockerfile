# Build context: repo root (the uv workspace needs every member's pyproject).
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1 TZ=UTC

WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY packages ./packages
COPY services ./services
RUN uv sync --frozen --no-dev --package thea-agent

RUN useradd --create-home --uid 1000 thea && chown -R thea /repo
USER thea
ENV PATH="/repo/.venv/bin:$PATH"

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --retries=5   CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "thea_agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
