FROM python:3.14.5-slim-bookworm AS build
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
RUN pip install --no-cache-dir uv==0.12.9
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.14.5-slim-bookworm AS runtime
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
RUN useradd --uid 10001 --create-home dotick
COPY --from=build --chown=dotick:dotick /app/.venv .venv
COPY --chown=dotick:dotick apps/api apps/api
USER dotick
EXPOSE 8000
CMD ["uvicorn", "config.asgi:application", "--app-dir", "apps/api", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
