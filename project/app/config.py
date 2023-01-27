# project/app/config.py

import logging
from functools import lru_cache
from pydantic import BaseSettings

log = logging.getLogger('uvicorn')

class Settings(BaseSettings):
    """Application settings"""
    environment: str = 'dev'
    testing: bool = False

@lru_cache()
def get_settings() -> BaseSettings:
    """Returns application settings"""
    log.info('Loading config settings from the environment...')
    return Settings()
