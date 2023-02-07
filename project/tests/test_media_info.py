"""tests for the media info module to return the media info for a file"""

import os

from app.box_file import download_file_to_path, get_file_by_id
from app.media_info import (
    get_media_info_by_file_path,
    get_media_info_by_url,
)
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_get_media_info_by_url(box_client_user):
    """should return media info from a download url file"""

    file = get_file_by_id(box_client_user, settings.MEDIA_FILE_ID)
    download_url = file.get_download_url()

    media_info = get_media_info_by_url(download_url)

    assert media_info is not None


def test_get_media_info_by_file_path(box_client_user):
    """should return media info from a file path"""

    file = get_file_by_id(box_client_user, settings.MEDIA_FILE_ID)

    # get current path
    path = os.path.join(os.getcwd(), "tmp")

    download_file_to_path(file, path, file.name, True)

    # check if file exists
    assert os.path.exists(os.path.join(path, file.name))

    media_info = get_media_info_by_file_path(os.path.join(path, file.name))

    assert media_info is not None
