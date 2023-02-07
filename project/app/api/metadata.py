""" metadata entry points """
# project/app/api/metadata.py

from fastapi import APIRouter, Depends, HTTPException

from app.box_auth import jwt_check_client
from app.box_client import get_box_client
from app.box_metadata_template import (
    create_metadata_template_from_dict,
    get_metadata_template_by_name,
    get_sample_dictionary,
)
from app.config import Settings, get_settings

router = APIRouter()


@router.get("/metadata")
async def metadata_template_details(settings: Settings = Depends(get_settings)):
    """Returns this service metadata template details"""

    client = jwt_check_client(settings)

    template = get_metadata_template_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Service template not found.",
        )

    response = template.response_object
    return {"status": "success", "data": response}


@router.post("/metadata", status_code=201)
async def create_metadata_template(
    force: bool | None = False, settings: Settings = Depends(get_settings)
):
    """Creates the metadata template for use in this service"""

    client = get_box_client(settings)

    template = get_metadata_template_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )

    if template is not None:
        if force:
            template.delete()
        else:
            raise HTTPException(
                status_code=400,
                detail="Service template already exists.",
            )

    media_info = get_sample_dictionary()

    template = create_metadata_template_from_dict(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME, media_info
    )

    result = template.response_object
    return {"status": "success", "data": result}


@router.delete("/metadata")
async def delete_metadata_template(settings: Settings = Depends(get_settings)):
    """Deletes the metadata template in user by this servoce.
    This can not be undone, and will remove all metadata of this template from all files"""

    client = jwt_check_client(settings)

    template = get_metadata_template_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Service template not found.",
        )

    template.delete()

    return {"status": "success"}
