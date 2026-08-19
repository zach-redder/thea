# Build context must be the repo root -- heart depends on brain via the uv workspace.
#
# NOTE: this image builds successfully (dependency install only), but the
# container will not actually serve anything yet -- heart/app/main.py is
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
RUN uv sync --frozen --package heart

WORKDIR /repo/heart
EXPOSE 8000
CMD ["uv", "run", "--project", "/repo", "--package", "heart", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
