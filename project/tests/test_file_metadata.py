"""Tests for the /metadata/user/folder endpoint."""
# project/tests/test_metadata.py

from app.box_file import get_file_by_id
from app.box_metadata import file_metadata_set
from app.box_metadata_template import get_metadata_template_by_name
from app.media_info import get_media_info_by_url
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_should_update_file_metadata(test_app, box_client_user):
    """should update the file metadata"""

    file_id = settings.MEDIA_FILE_ID
    template_name = settings.MEDIA_METADATA_TEMPLATE_NAME

    # create the default test template
    response = test_app.post("/metadata?force=true")
    assert response.status_code == 201

    template = get_metadata_template_by_name(box_client_user, template_name)
    assert template is not None

    file = get_file_by_id(box_client_user, file_id)

    file_download_url = file.get_download_url()

    media_info = get_media_info_by_url(file_download_url)
    file_metadata = file_metadata_set(file, template, media_info)
    assert file_metadata is not None

    # check if the file metadata was updated
    file = box_client_user.file(file_id).get()
    metadata = file.metadata(template["scope"], template["templateKey"]).get()
    assert metadata is not None
    assert metadata == file_metadata

    # delete the default test template
    response = test_app.delete("/metadata")
    assert response.status_code == 200
