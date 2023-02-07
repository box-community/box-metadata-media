""" metadata entry points """
# project/app/api/metadata.py
import json
import os

from fastapi import APIRouter, Depends, HTTPException

from app.box_auth import jwt_check_client
from app.box_metadata_template import (
    metadata_template_check_by_name,
    metadata_template_from_dict,
)
from app.config import Settings, get_settings

router = APIRouter()


@router.get("/metadata")
async def metadata_template_details(settings: Settings = Depends(get_settings)):
    """Returns this service metadata template details"""

    client = jwt_check_client(settings)

    template = metadata_template_check_by_name(
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

    client = jwt_check_client(settings)

    template = metadata_template_check_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )

    if template is not None:
        if force:
            template.delete()
        else:
            raise HTTPException(
                status_code=400,
                detail="Demo template already exists.",
            )

    with open(
        os.path.join(
            os.path.dirname(__file__), "../../tests/samples/json/BigBuckBunny.mp4.json"
        ),
        "r",
        encoding="utf-8",
    ) as file:
        bunny_dict = json.load(file)

    client = jwt_check_client(settings)

    track_generic = bunny_dict["tracks"][0].items()
    track_name = settings.MEDIA_METADATA_TEMPLATE_NAME

    template = metadata_template_from_dict(client, track_name, track_generic)

    result = template.response_object
    return {"status": "success", "data": result}


@router.delete("/metadata")
async def delete_metadata_template(settings: Settings = Depends(get_settings)):
    """Deletes the metadata template in user by this servoce.
    This can not be undone, and will remove all metadata of this template from all files"""

    client = jwt_check_client(settings)

    template = metadata_template_check_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )

    if template is None:
        raise HTTPException(
            status_code=404,
            detail="Demo template not found.",
        )

    template.delete()

    return {"status": "success"}
