import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    """
    Схема для создания уведомления.
    """

    user_id: uuid.UUID = Field(..., description="UUID пользователя")
    title: str = Field(
        ..., max_length=256, description="Заголовок уведомления"
    )
    text: str = Field(..., description="Текст уведомления")


class NotificationResponse(BaseModel):
    """
    Схема для вывода уведомления.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    text: str
    created_at: datetime
    updated_at: datetime
    read_at: datetime | None = None
    category: str | None = None
    confidence: float | None = None
    processing_status: str

    model_config = ConfigDict(from_attributes=True)
