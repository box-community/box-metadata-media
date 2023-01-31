"""Pytest configuration file."""
# project/tests/conftest.py

import pytest
from starlette.testclient import TestClient

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
