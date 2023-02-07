""" file entry points """
# project/app/api/metadata.py

import os
import time

from boxsdk import BoxAPIException
from fastapi import APIRouter, Depends, HTTPException

from app.box_client import get_box_client
from app.box_file import download_file_to_path, get_file_by_id
from app.box_metadata import file_metadata_set
from app.box_metadata_template import get_metadata_template_by_name
from app.config import Settings, get_settings
from app.media_info import (
    get_media_info_by_file_path,
    get_media_info_by_url,
)

router = APIRouter()


@router.post("/file/{file_id}", status_code=201)
async def set_file_metadata(
    file_id: str,
    settings: Settings = Depends(get_settings),
):
    """Process file and fill in the metadata info"""

    await set_file_metadata_as_user(file_id, None, settings)


@router.post("/file/{file_id}/{as_user_id}", status_code=201)
async def set_file_metadata_as_user(
    file_id: str,
    as_user_id: str | None = None,
    settings: Settings = Depends(get_settings),
):
    """Process media file and fill in the metadata info using 'as-user'
    security context"""
    exec_start = time.perf_counter()

    client = get_box_client(settings, as_user_id)
    template = get_metadata_template_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    if template is None:
        raise HTTPException(
            status_code=404,
            detail=f"Metadata template {settings.MEDIA_METADATA_TEMPLATE_NAME} does not exist",
        )

    file = get_file_by_id(client, file_id)
    if file is None:
        raise HTTPException(
            status_code=404,
            detail=f"File {file_id} does not exist",
        )

    media_info = get_media_info_by_url(file.get_download_url())
    if media_info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to get media info for file {file_id}",
        )

    try:
        metadata = file_metadata_set(file, template, media_info)
    except BoxAPIException as error:
        raise HTTPException(
            status_code=error.status,
            detail=error.message,
        ) from error

    exec_end = time.perf_counter()
    exec_time = exec_end - exec_start

    return {
        "status": "success",
        "executed_in_seconds": exec_time,
        "data": metadata,
    }


@router.post("/file_local/{file_id}/{as_user_id}", status_code=201)
async def set_file_metadata_as_user_local(
    file_id: str,
    as_user_id: str | None = None,
    settings: Settings = Depends(get_settings),
):
    """Process media file and fill in the metadata info using 'as-user'
    but downloading it locally first"""

    exec_start = time.perf_counter()

    client = get_box_client(settings, as_user_id)
    template = get_metadata_template_by_name(
        client, settings.MEDIA_METADATA_TEMPLATE_NAME
    )
    if template is None:
        raise HTTPException(
            status_code=404,
            detail=f"Metadata template {settings.MEDIA_METADATA_TEMPLATE_NAME} does not exist",
        )

    file = get_file_by_id(client, file_id)
    if file is None:
        raise HTTPException(
            status_code=404,
            detail=f"File {file_id} does not exist",
        )

    # get current path
    path = os.path.join(os.getcwd(), "tmp")

    download_file_to_path(file, path, file.name, True)

    media_info = get_media_info_by_file_path(os.path.join(path, file.name))

    if media_info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unable to get media info for file {file_id}",
        )

    try:
        metadata = file_metadata_set(file, template, media_info)
    except BoxAPIException as error:
        raise HTTPException(
            status_code=error.status,
            detail=error.message,
        ) from error

    exec_end = time.perf_counter()
    exec_time = exec_end - exec_start

    return {
        "status": "success",
        "executed_in_seconds": exec_time,
        "data": metadata,
    }
