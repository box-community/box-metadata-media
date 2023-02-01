"""Tests for the /metadata/user/folder endpoint."""
# project/tests/test_metadata.py

from pymediainfo import MediaInfo
from tests.conftest import get_settings_override
from app.box_metadata import file_metadata_update
from app.box_metadata_template import metadata_template_check_by_name


def test_single_file_metadata(test_app, test_box_client):
    """should grab the files from the folder under the user security context,
    process them with media info and store the metadata in box file"""

    settings = get_settings_override()

    service_user = test_box_client.user().get()
    assert service_user is not None

    user = test_box_client.user(user_id=settings.MEDIA_FOLDER_USER_ID).get()

    client = test_box_client.as_user(user)
    assert client is not None

    # get the folder
    folder = client.folder(folder_id=settings.MEDIA_FOLDER_ID).get()
    assert folder is not None

    file = client.file(file_id=settings.MEDIA_FILE_ID).get()
    assert file is not None

    file_download_url = file.get_download_url()
    assert file_download_url is not None

    data = MediaInfo.parse(file_download_url)
    assert data is not None


def test_should_update_file_metadata(test_app, test_box_client):
    """should update the file metadata"""
    settings = get_settings_override()
    user_id = settings.MEDIA_FOLDER_USER_ID
    file_id = settings.MEDIA_FILE_ID
    template_name = settings.MEDIA_METADATA_TEMPLATE_NAME

    # response = test_app.post("/metadata?force=true")
    # assert response.status_code == 201

    template = metadata_template_check_by_name(test_box_client, template_name)
    assert template is not None

    template_key = template["templateKey"]

    file_metadata_update(test_box_client, file_id, user_id, template_name)

    # check if the file metadata was updated
    user = test_box_client.user(user_id).get()
    client = test_box_client.as_user(user)
    file = client.file(file_id).get()
    metadata = file.get_all_metadata()
    assert metadata is not None
