""" info entry point """
# project/app/api/info.py

from fastapi import APIRouter, Depends

from app.config import get_settings, Settings


router = APIRouter()
@router.get("/info")
async def get_server_info(settings:Settings = Depends(get_settings)):
    """Returns current service info and settings"""

    settings_out = settings.dict()
    if not settings.testing:
        settings_out.pop('FERNET_KEY')
    return settings_out
