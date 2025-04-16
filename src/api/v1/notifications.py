import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.dependencies import get_notific_service
from src.schemas.filters import NotificationFilter
from src.schemas.notifications import NotificationCreate, NotificationResponse
from src.services.notifications_service import NotificationService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание уведомления",
    description="Создает новое уведомление и инициирует его анализ через AI",
)
async def create_notification(
    payload: NotificationCreate,
    service: NotificationService = Depends(get_notific_service),
):
    logger.info("Request for create notification, user_id=%s", payload.user_id)
    notification = await service.create_notification(
        user_id=payload.user_id,
        title=payload.title,
        text=payload.text,
    )
    logger.info("Success created notification: %s", notification.id)
    return NotificationResponse.model_validate(notification)


@router.get(
    "/",
    response_model=List[NotificationResponse],
    summary="Получить список уведомлений",
    description="Возвращает список уведомлений с фильтрацией и пагинацией.",
)
async def list_notifications(
    filters: NotificationFilter = Depends(),
    service: NotificationService = Depends(get_notific_service),
):
    logger.info("Request for list notifications")
    notifications = await service.list_notifications(filters)
    logger.info("Success sending notifications with filters")
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    summary="Получить детали уведомления",
    description="Возвращает информацию по уведомлению по заданному ID.",
)
async def get_notification(
    notification_id: uuid.UUID,
    service: NotificationService = Depends(get_notific_service),
):
    logger.info("Request info for notification: %s", notification_id)
    notification = await service.get_notification(notification_id)
    if not notification:
        logger.info("Notification with id: %s not found", notification_id)
        raise HTTPException(status_code=404, detail="Notification not found")
    logger.info("Success sending info for notification: %s", notification_id)
    return NotificationResponse.model_validate(notification)


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Отметить уведомление как прочитанное",
    description="Устанавливает время прочтения уведомления.",
)
async def mark_notification_as_read(
    notification_id: uuid.UUID,
    service: NotificationService = Depends(get_notific_service),
):
    logger.info("Request for read notification")
    notification = await service.mark_as_read(notification_id)
    if not notification:
        logger.info("Notification with id: %s not found", notification_id)
        raise HTTPException(status_code=404, detail="Notification not found")
    logger.info("Success updating info for notification: %s", notification_id)
    return NotificationResponse.model_validate(notification)


@router.get(
    "/{notification_id}/status",
    summary="Проверка статуса обработки уведомления",
    description="""
    Возвращает статус обработки AI анализа вместе с категорией и
    confidence, если они имеются.
    """,
    response_model=dict,
)
async def check_notification_status(
    notification_id: uuid.UUID,
    service: NotificationService = Depends(get_notific_service),
):
    logger.info("Request for check status notification")
    status_info = await service.check_notification_status(notification_id)
    if not status_info:
        raise HTTPException(status_code=404, detail="Notification not found")
    logger.info("Success check status for notification: %s", notification_id)
    return status_info
