from fastapi.routing import APIRouter

from src.api.v1.notifications import router as notification_router

router = APIRouter()
router.include_router(notification_router)
