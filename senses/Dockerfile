# Build context must be the repo root -- part of the shared uv workspace.
#
# senses doesn't serve HTTP (see README: "a filter, not a thinker" that
# publishes to heart's webhooks), so there's no port to expose.
#
# NOTE: this image builds successfully (dependency install only), but the
# container has nothing to run yet -- senses/app/main.py is still an empty
# stub, and senses' own dependencies were never pinned upstream (see
# senses/pyproject.toml). See docs/ARCHITECTURE.md for what's built vs planned.
FROM python:3.11-slim
RUN pip install --no-cache-dir uv==0.9.17

WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY brain ./brain
COPY heart ./heart
COPY muscles ./muscles
COPY senses ./senses
RUN uv sync --frozen --package senses

WORKDIR /repo/senses
CMD ["uv", "run", "--project", "/repo", "--package", "senses", "python", "app/main.py"]
