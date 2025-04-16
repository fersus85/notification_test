import uuid
from typing import Any

from src.models.notification import Notification
from src.repositories.notification_repo import NotificationRepository
from src.schemas.filters import NotificationFilter


class NotificationService:
    """Сервис для работы с уведомлениями."""

    def __init__(self, repo: NotificationRepository) -> None:
        self.repo = repo

    async def create_notification(
        self, user_id: uuid.UUID, title: str, text: str
    ) -> Notification:
        """
        Создает новое уведомление, инициирует запуск AI анализа.
        """
        new_notification = Notification(
            user_id=user_id, title=title, text=text
        )
        created = await self.repo.create(new_notification)
        # вызов Celery-задачи для анализа уведомления
        return created

    async def list_notifications(
        self,
        filters: NotificationFilter,
    ) -> list[Notification]:
        """
        Возвращает список уведомлений пользователя.
        """
        return await self.repo.list(filters)

    async def get_notification(
        self, notification_id: uuid.UUID
    ) -> Notification | None:
        """
        Получает уведомление по ID.
        """
        return await self.repo.get_by_id(notification_id)

    async def mark_as_read(
        self, notification_id: uuid.UUID
    ) -> Notification | None:
        """
        Отмечает уведомление как прочитанное, обновляя поле read_at.
        """
        notification = await self.repo.read(notification_id)
        if not notification:
            return None
        return notification

    async def check_notification_status(
        self, notification_id: uuid.UUID
    ) -> dict[str, Any] | None:
        """
        Возвращает статус обработки уведомления,
        а также результат AI-анализа, если он есть.
        """
        notification = await self.repo.get_by_id(notification_id)
        if not notification:
            return None
        return {
            "processing_status": notification.processing_status,
            "category": notification.category,
            "confidence": notification.confidence,
        }
