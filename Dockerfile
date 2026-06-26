# Use the official uv image with Python preinstalled
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Compile bytecode for faster startup and copy (not link) packages into the venv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first (cached layer) using the lockfile, without the project itself
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the project and install it
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Put the project's virtualenv on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Creates a non-root user with an explicit UID and gives it access to /app
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Run the installed console script
CMD ["brewcli"]
