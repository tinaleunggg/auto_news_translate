FROM mcr.microsoft.com/playwright/python:v1.55.0

COPY --from=ghcr.io/astral-sh/uv:0.9.18 /uv /uvx /bin/


ADD . /app

WORKDIR /app

RUN uv sync --locked

CMD ["uv", "run", "newsbot.py"]