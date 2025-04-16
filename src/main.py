import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.api import router as api_router
from src.core.error_handlers import exception_handlers
from src.core.log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Notification API",
    description="Notification service",
    version="1.0.0",
    # lifespan=lifespan,
    exception_handlers=exception_handlers,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


# app.middleware("http")(log_stuff)
# if settings.ENV == EnvMode.PROD:
#     app.middleware("http")(limiter)
#     app.middleware("http")(before_request)
#     configure_tracer()
#     FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
