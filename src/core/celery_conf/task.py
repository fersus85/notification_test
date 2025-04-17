from celery import Celery

from src.core.config import settings

celery = Celery(
    "tasks",
    broker=f"{settings.redis.connection_url}/0",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_acks_late=True,
)

celery.autodiscover_tasks(["src.tasks.analyze"])
