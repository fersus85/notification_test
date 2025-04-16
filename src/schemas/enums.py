from enum import Enum


class NotificationCategory(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
