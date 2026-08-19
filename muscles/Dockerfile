# Build context must be the repo root -- part of the shared uv workspace.
#
# NOTE: this image builds successfully (dependency install only), but the
# container will not actually serve anything yet -- muscles/app/main.py is
# still an empty stub with no `app` object for uvicorn to run. See
# docs/ARCHITECTURE.md for what's built vs planned.
FROM python:3.11-slim
RUN pip install --no-cache-dir uv==0.9.17

WORKDIR /repo
COPY pyproject.toml uv.lock ./
COPY brain ./brain
COPY heart ./heart
COPY muscles ./muscles
COPY senses ./senses
RUN uv sync --frozen --package muscles

WORKDIR /repo/muscles
EXPOSE 8001
CMD ["uv", "run", "--project", "/repo", "--package", "muscles", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
