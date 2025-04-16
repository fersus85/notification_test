from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from src.core.exceptions import (
    NotificationNotFoundError,
    NotificationRepositoryError,
)


async def repository_error_handler(
    _: Request,
    exc: NotificationRepositoryError,
) -> Response:
    """Notification repo error handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message},
    )


async def not_found_notification_error_handler(
    _: Request,
    exc: NotificationNotFoundError,
) -> Response:
    """Notification not found error handler"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Notification not found"},
    )


exception_handlers = {
    NotificationRepositoryError: repository_error_handler,
    NotificationNotFoundError: not_found_notification_error_handler,
}
