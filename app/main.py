import logging
from fastapi import FastAPI

from app.api.v1.endpoints import phone
from app.core.logging_config import setup_logging
from app.core.settings import settings


def create_app() -> FastAPI:
    # Setting up logging
    setup_logging()

    application = FastAPI(
        title=settings.app_name,
        description="API for storing and retrieving addresses by phone numbers using FastAPI and Redis.",
        version="1.0.0",
    )

    # Connecting routes
    application.include_router(phone.router, prefix="/api/v1")

    # Logging the successful start of the application
    logger = logging.getLogger("app")
    logger.info("Application startup complete")

    return application

# Creating and initializing an application
app = create_app()
