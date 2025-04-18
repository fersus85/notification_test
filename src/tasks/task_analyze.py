import logging
from uuid import UUID

from src.celery_app import app_celery
from src.core.db import get_sync_db_session
from src.repositories.notification_repo import NotificationRepository
from src.schemas.enums import ProcessingStatus
from src.services.mock_ai_service import AIService

logger = logging.getLogger(__name__)


@app_celery.task
def analyze_notification(notification_id: UUID, text: str):
    """
    Задача для анализа уведомления.
    Принимает notification_id и text, обновляет статус и результаты в БД.
    """
    logger.info("Task started for notification %s", notification_id)
    with get_sync_db_session() as session:
        repo = NotificationRepository(session)
        note = repo.sync_get_by_id(notification_id)

        if note and note.processing_status == ProcessingStatus.PENDING:
            logger.info("Start analyze notification: %s", notification_id)
            repo.sync_update(
                notification_id,
                {"processing_status": ProcessingStatus.PROCESSING},
            )

            try:
                ai_service = AIService()
                analysis = ai_service.analyze_text(text)
                update_data = {
                    "category": analysis["category"],
                    "confidence": analysis["confidence"],
                    "processing_status": ProcessingStatus.COMPLETED,
                }
                repo.sync_update(notification_id, update_data)
                logger.info("Success analyze note: %s", notification_id)
                return {"status": "success"}
            except Exception as exc:
                repo.sync_update(
                    notification_id,
                    {"processing_status": ProcessingStatus.FAILED},
                )
                logger.error("Error analyz note %s:%s", notification_id, exc)
        else:
            logger.info(
                "Note %s already done or not found", str(notification_id)
            )
