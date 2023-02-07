"""Tests for the /file endpoint."""
# project/tests/test_metadata.py


from tests.conftest import get_settings_override

settings = get_settings_override()


def test_file_user(test_app, box_client_user):
    """should update the metadata file for the user"""
    as_user_id = settings.MEDIA_FOLDER_USER_ID
    file_id = settings.MEDIA_FILE_ID

    # create template
    response = test_app.post("/metadata?force=true")
    assert response.status_code == 201

    response = test_app.post(f"/file/{file_id}/{as_user_id}")
    assert response.status_code == 201

    # delete template
    response = test_app.delete("/metadata")
    assert response.status_code == 200


def test_file_user_download(test_app, box_client_user):
    """should update the metadata file for the user"""
    as_user_id = settings.MEDIA_FOLDER_USER_ID
    file_id = settings.SMALL_MEDIA_FILE_ID

    # create template
    response = test_app.post("/metadata?force=true")
    assert response.status_code == 201

    response = test_app.post(f"/file_local/{file_id}/{as_user_id}")
    assert response.status_code == 201

    # delete template
    response = test_app.delete("/metadata")
    assert response.status_code == 200
