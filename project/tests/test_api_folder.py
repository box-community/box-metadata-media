"""Tests for the /file endpoint."""
# project/tests/test_metadata.py


from tests.conftest import get_settings_override

settings = get_settings_override()


def test_folder_user(test_app, box_client_user):
    """should update the metadata file for the user"""
    as_user_id = settings.MEDIA_FOLDER_USER_ID
    folder_id = settings.VIDEO_FOLDER_ID

    # create template
    response = test_app.post("/metadata?force=true")
    assert response.status_code == 201

    response = test_app.post(f"/folder/{folder_id}/{as_user_id}")
    assert response.status_code == 201

    # delete template
    response = test_app.delete("/metadata")
    assert response.status_code == 200
