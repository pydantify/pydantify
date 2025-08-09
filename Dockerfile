# Edit python version here.
ARG VERSION=3.13

FROM python:${VERSION}-slim

ARG VERSION
WORKDIR /app

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --frozen --no-cache --all-extras

# Run your project as a module.
CMD ["python", "-m", "pydantify", "--help"]
