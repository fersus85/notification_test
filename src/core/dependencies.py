from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.repositories.notification_repo import NotificationRepository
from src.services.notifications_service import NotificationService


def get_notification_repo(
    db: AsyncSession = Depends(get_db),
) -> NotificationRepository:
    """Возвращает экземпляр NotificationRepository."""
    return NotificationRepository(db)


def get_notific_service(
    repo: NotificationRepository = Depends(get_notification_repo),
) -> NotificationService:
    """Возвращает экземпляр NotificationService."""
    return NotificationService(repo)
