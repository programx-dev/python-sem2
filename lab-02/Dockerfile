FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

COPY src/ ./src/
COPY tests/ ./tests/
COPY data/ ./data/

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["lab2"]

CMD ["read", "--help"]