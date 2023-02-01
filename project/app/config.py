""" application config setting """
# project/app/config.py

import logging
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """Application settings"""

    environment: str = "dev"
    testing: bool = False

    FERNET_KEY: str = "FERNET_KEY"
    JWT_PATH: str = "app/.jwt.config.json"
    JWT_PUBLIC_KEY_ID: str = "JWT_PUBLIC_KEY_ID"
    JWT_EXPIRATION_SECONDS: int = 3300
    MEDIA_METADATA_TEMPLATE_NAME: str = "Demo Media Metadata"
    MEDIA_FOLDER_ID: str = "MEDIA_FOLDER_ID"
    MEDIA_FOLDER_USER_ID: str = "MEDIA_FOLDER_USER_ID"
    MEDIA_FILE_ID: str = "MEDIA_FILE_ID"

    class Config:
        """environment variables to read from"""

        env_file = "app/.env"


@lru_cache()
def get_settings() -> BaseSettings:
    """Returns application settings"""
    log.info("Loading config settings from the environment...")
    return Settings()
