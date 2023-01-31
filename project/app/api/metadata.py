""" metadata entry points """
# project/app/api/metadata.py

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.box_auth import jwt_check_client

router = APIRouter()


@router.get("/metadata")
async def get_metadata_details(settings: Settings = Depends(get_settings)):
    """Returns the metadata configuration details"""

    client = jwt_check_client(settings)

    templates = client.get_metadata_templates()

    for template in templates:
        print(template)

    return templates
