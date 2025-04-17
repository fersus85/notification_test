#!/bin/sh

celery -A src.core.celery_conf.worker worker \
  --loglevel=${CELERY_LOGLEVEL:-info} \
  --hostname=note_worker_%h \
