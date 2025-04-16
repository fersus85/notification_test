import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, Index, String, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base
from src.schemas.enums import NotificationCategory, ProcessingStatus


class Notification(Base):
    """Модель уведомлений."""

    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    category: Mapped[Optional[NotificationCategory]] = mapped_column(
        Enum(NotificationCategory, name="notification_category"),
        nullable=True,
        index=True,
    )
    confidence: Mapped[Optional[float]] = mapped_column(nullable=True)

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        Enum(ProcessingStatus, name="notification_processing_status"),
        default=ProcessingStatus.PENDING,
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index(
            "ix_notifications_user_status_created",
            "user_id",
            "processing_status",
            "created_at",
        ),
    )
