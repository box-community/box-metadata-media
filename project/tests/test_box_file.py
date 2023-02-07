""" Tests for box file api"""
import os

from app.box_file import download_file_to_path, get_file_by_id
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_get_file_by_id(box_client_user):
    """should return a box file object"""

    file_id = settings.MEDIA_FILE_ID

    file = get_file_by_id(box_client_user, file_id)
    assert file is not None
    assert file.id == file_id
    assert file.object_type == "file"


def test_download_file_to_path(box_client_user):
    """should download a file to a path"""

    file_id = settings.SMALL_MEDIA_FILE_ID
    file = get_file_by_id(box_client_user, file_id)

    # get current path
    path = os.path.join(os.getcwd(), "tmp")

    download_file_to_path(file, path, file.name, True)

    # check if file exists
    assert os.path.exists(os.path.join(path, file.name))
