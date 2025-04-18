import logging
import uuid
from contextlib import asynccontextmanager

from sqlalchemy import select, update
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.core.cache import CacheManager
from src.core.exceptions import (
    NotificationRepositoryError,
)
from src.models.notification import Notification
from src.schemas.filters import NotificationFilter

logger = logging.getLogger(__name__)


class NotificationRepository:
    """
    Репозиторий для работы с уведомлениями в базе данных.
    Предоставляет методы для создания, получения и обновления уведомлений
    с поддержкой фильтрации и пагинации.
    """

    def __init__(self, session: AsyncSession | Session):
        """Инициализация репозитория с асинхронной сессией."""
        self.session = session
        self.cache = CacheManager()

    @asynccontextmanager
    async def _transaction_handler(self, error_message: str):
        """
        Управляет асинхронной транзакцией с логированием и обработкой ошибок
        """
        try:
            yield
            await self.session.commit()
        except (IntegrityError, DataError) as exc:
            logger.error("%s: %s", error_message, str(exc))
            await self.session.rollback()
            raise NotificationRepositoryError(error_message, str(exc)) from exc
        except OperationalError as exc:
            logger.error("Database connection error: %s", str(exc))
            await self.session.rollback()
            raise NotificationRepositoryError(error_message, str(exc)) from exc
        except Exception as exc:
            logger.critical(
                "Unexpected transaction error: %s", str(exc), exc_info=True
            )
            await self.session.rollback()
            raise NotificationRepositoryError(
                "Unexpected repository error"
            ) from exc

    async def create(self, notification: Notification) -> Notification:
        """Создает новое уведомление в базе данных."""
        async with self._transaction_handler("Failed create notification"):
            self.session.add(notification)
        await self.session.refresh(notification)
        logger.info("Created notification %s", notification.id)
        return notification

    async def update(
        self,
        notification_id: uuid.UUID,
        update_data: dict,
    ) -> Notification | None:
        async with self._transaction_handler("Failed read notification"):
            result = await self.session.execute(
                update(Notification)
                .where(Notification.id == notification_id)
                .values(**update_data)
                .returning(Notification)
            )
            cache_key = f"notification:{notification_id}"
            await self.cache.delete(cache_key)
        return result.scalar_one_or_none()

    async def get_by_id(self, notific_id: uuid.UUID) -> Notification | None:
        """Получает уведомление по идентификатору."""
        cache_key = f"notification:{notific_id}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data
        try:
            result = await self.session.execute(
                select(Notification).where(Notification.id == notific_id)
            )
        except SQLAlchemyError as exc:
            logger.error("Failed to get note %s: %s", notific_id, exc)
            raise NotificationRepositoryError("Fail get note") from exc

        notification = result.scalar_one_or_none()
        if notification:
            await self.cache.set(cache_key, notification, ttl=100)
        return notification

    async def list(
        self,
        filters: NotificationFilter,
    ) -> list[Notification]:
        """Получает список уведомлений с фильтрацией и пагинацией."""
        query = select(Notification)

        if filters.user_id:
            query = query.where(Notification.user_id == filters.user_id)
        if filters.category:
            query = query.where(Notification.category == filters.category)
        if filters.processing_status:
            query = query.where(
                Notification.processing_status == filters.processing_status
            )

        query = query.offset(filters.offset).limit(filters.limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    def sync_get_by_id(self, notific_id) -> Notification | None:
        result = self.session.execute(
            select(Notification).where(Notification.id == notific_id)
        )
        return result.scalars().one_or_none()

    def sync_update(
        self,
        notification_id: uuid.UUID,
        update_data: dict,
    ) -> Notification | None:
        result = self.session.execute(
            update(Notification)
            .where(Notification.id == notification_id)
            .values(**update_data)
            .returning(Notification)
        )
        self.session.commit()
        return result.scalar_one_or_none()
