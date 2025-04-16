class NotificationRepositoryError(Exception):
    """Ошибка репозитория нотификаций"""

    def __init__(self, message: str, original_exc: Exception | None = None):
        # super().__init__(message)
        self.message = message
        self.original_exc = original_exc


class NotificationNotFoundError(Exception):
    """Запрашиваемая нотификация не найдена"""
