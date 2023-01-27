# project/app/api/ping.py


from fastapi import APIRouter, Depends

from app.config import get_settings, Settings


router = APIRouter()
@router.get("/info")
async def get_server_info(settings = Depends(get_settings)):
    """Returns current service info and settings"""
    # TODO: Scrub sensitive settings
    return settings.dict()