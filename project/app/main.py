"""fast api service to automatically apply metadata to media files stored in box"""
# project/app/main.py

from fastapi import FastAPI

from app.api import info, metadata


def create_application() -> FastAPI:
    """Create the FastAPI application."""
    application = FastAPI()
    application.include_router(info.router)
    application.include_router(metadata.router)
    return application


app = create_application()
