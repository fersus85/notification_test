FROM ghcr.io/astral-sh/uv:python3.10-alpine AS base

RUN adduser -D -h /home/www_user www_user

WORKDIR /app/src

COPY ./pyproject.toml ./uv.lock /app/

RUN uv sync

COPY ./alembic /app/src/alembic

COPY ./src ./.env ./scripts/celery_worker.sh ./alembic.ini /app/src/

RUN mkdir -p /app/logs && \
    chown -R www_user:www_user /app && \
    chmod +x ./celery_worker.sh

USER www_user

ENV PATH=$PATH:/home/www_user/.local/bin:/usr/local/bin

ENV PYTHONPATH=/app

FROM base as worker

CMD ["./celery_worker.sh"]

FROM base AS service

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn_worker.UvicornWorker", "--forwarded-allow-ips", "*"]
