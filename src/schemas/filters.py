import uuid

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.enums import NotificationCategory, ProcessingStatus


class NotificationFilter(BaseModel):
    user_id: uuid.UUID | None = Field(
        default=None, description="UUID пользователя"
    )

    category: NotificationCategory | None = Field(
        default=None, description="Категория уведомления"
    )

    processing_status: ProcessingStatus | None = Field(
        default=None, description="Статус обработки уведомления"
    )

    limit: int = Field(
        default=20, ge=1, le=100, description="Максимум на страницу"
    )
    offset: int = Field(default=0, ge=0, description="Смещение для пагинации")

    model_config = ConfigDict(from_attributes=True)
