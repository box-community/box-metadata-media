"""Tests the handling of a box client"""

from app.box_client import get_box_client
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_get_client():
    """should get a box client"""

    # get jwt client
    client_jwt = get_box_client(settings)
    assert client_jwt is not None

    # get client impersonating a user
    client_user = get_box_client(settings, settings.MEDIA_FOLDER_USER_ID)
    assert client_user is not None

    user_jwt = client_jwt.user().get()
    assert user_jwt is not None

    user_user = client_user.user().get()
    assert user_user is not None

    assert user_jwt.id != user_user.id
