""" file entry points """
# project/app/api/metadata.py

import time

from boxsdk import BoxAPIException
from fastapi import APIRouter, Depends, HTTPException

from app.box_auth import jwt_check_client
from app.box_metadata import file_metadata_set
from app.config import Settings, get_settings

router = APIRouter()


@router.post("/file/{file_id}", status_code=201)
async def box_file_metadata_set(
    file_id: str,
    settings: Settings = Depends(get_settings),
):
    """processes file and fills in the metadata with the MediaFile info"""

    await box_file_metadata_set_with_user(file_id, None, settings)


@router.post("/file/{file_id}/{user_id}", status_code=201)
async def box_file_metadata_set_with_user(
    file_id: str,
    user_id: str | None = None,
    settings: Settings = Depends(get_settings),
):
    """processes file and fills in the metadata with the MediaFile info"""
    client = jwt_check_client(settings)

    exec_start = time.perf_counter()

    try:
        metadata = file_metadata_set(
            client, file_id, user_id, settings.MEDIA_METADATA_TEMPLATE_NAME
        )
    except BoxAPIException as error:
        raise HTTPException(
            status_code=error.status,
            detail=error.message,
        ) from error

    exec_end = time.perf_counter()
    exec_time = exec_end - exec_start

    return {"status": "success", "data": metadata, "executed_in": exec_time}
