"""Pytest configuration file."""
# project/tests/conftest.py

import pytest
from starlette.testclient import TestClient

from app.box_auth import jwt_check_client
from app.box_client import get_box_client
from app.config import Settings, get_settings
from app.main import create_application


def get_settings_override():
    """Override get_settings to return test settings."""
    return Settings(
        testing=True,
        environment="dev",
        FERNET_KEY="FERNET_KEY",
        JWT_PATH="app/.jwt.config.json",
        JWT_PUBLIC_KEY_ID="JWT_PUBLIC_KEY_ID",
        JWT_EXPIRATION_SECONDS=3300,
        MEDIA_METADATA_TEMPLATE_NAME="TEST Media Metadata",
        MEDIA_FOLDER_ID="191494027812",
        MEDIA_FOLDER_USER_ID="18622116055",
        MEDIA_FILE_ID="1121082178302",
        SMALL_MEDIA_FILE_ID="1127033309244",
        AUDIO_FOLDER_ID="192444166451",
        IMAGE_FOLDER_ID="192444586290",
        VIDEO_FOLDER_ID="192442970500",
    )


@pytest.fixture(scope="module")
def test_app():
    """Create test application fixture for the tests."""
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_template():
    """Create test application fixture for the tests."""
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    # create a test template

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_real_settings():
    """Create test application fixture for the tests."""
    # set up
    app = create_application()
    # app.dependency_overrides[get_settings] = get_settings
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def box_client():
    """Create test box client fixture for the tests."""
    # set up
    client = jwt_check_client(get_settings_override())

    # testing
    yield client

    # tear down


@pytest.fixture(scope="module")
def box_client_user():
    """Create test box client fixture for the tests impersonating the user."""
    # set up
    settings = get_settings_override()
    client = get_box_client(settings, settings.MEDIA_FOLDER_USER_ID)

    # testing
    yield client

    # tear down
