#!/bin/sh

uv run celery -A src.celery_app worker \
  --loglevel=${CELERY_LOGLEVEL:-info} \
  --hostname=note_worker_%h \
