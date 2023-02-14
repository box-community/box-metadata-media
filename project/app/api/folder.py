""" file entry points """
# project/app/api/metadata.py

import time

from boxsdk import BoxAPIException
from fastapi import APIRouter, Depends, HTTPException

from app.box_client import get_box_client
from app.box_file import get_files_by_folder_id
from app.box_metadata import file_metadata_set
from app.box_metadata_template import get_metadata_template_by_name
from app.config import Settings, get_settings
from app.media_info import get_media_info_by_url

router = APIRouter()


@router.post("/folder/{folder_id}", status_code=201)
async def set_folder_items_metadata(
    folder_id: str,
    settings: Settings = Depends(get_settings),
):
    """Process folder and fill in the metadata info for each file item"""

    await set_folder_items_metadata_as_user(folder_id, None, settings)


@router.post("/folder/{folder_id}/{as_user_id}", status_code=201)
async def set_folder_items_metadata_as_user(
    folder_id: str,
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

    files = get_files_by_folder_id(client, folder_id)
    files_metadata = []

    for file in files:

        # get media info
        media_info = get_media_info_by_url(file.get_download_url())
        if media_info is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unable to get media info for file {file.id}",
            )

        # set the metadata
        try:
            metadata = file_metadata_set(file, template, media_info)
            files_metadata.append(metadata)
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
        "total_files": len(files),
        "data": files_metadata,
    }
