import logging
import uuid
from contextlib import asynccontextmanager

from sqlalchemy import func, select, update
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

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

    def __init__(self, session: AsyncSession):
        """Инициализация репозитория с асинхронной сессией."""
        self.session = session

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

    async def read(
        self,
        notification_id: uuid.UUID,
    ) -> Notification | None:
        async with self._transaction_handler("Failed read notification"):
            result = await self.session.execute(
                update(Notification)
                .where(Notification.id == notification_id)
                .values(read_at=func.now())
                .returning(Notification)
            )
            return result.scalar_one_or_none()

    async def get_by_id(self, notific_id: uuid.UUID) -> Notification | None:
        """Получает уведомление по идентификатору."""
        try:
            result = await self.session.execute(
                select(Notification).where(Notification.id == notific_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as exc:
            logger.error("Failed to get notification %s: %s", notific_id, exc)
            raise NotificationRepositoryError("Failed get notificat") from exc

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
