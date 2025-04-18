from celery import Celery

from src.core.config import settings

app_celery = Celery(
    "tasks",
    broker=f"{settings.redis.connection_url}/0",
    include="tasks",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_acks_late=True,
    broker_connection_retry_on_startup=True,
)
