"""Tests for the /metadata endpoint."""
# project/tests/test_metadata.py

from app.box_metadata import metadata_template_check_by_name
from tests.conftest import get_settings_override


def test_metadata(test_app, test_box_client):
    """Should return a 404 if it does not exist or the matadata template details"""
    response = test_app.get("/metadata")

    template = metadata_template_check_by_name(
        test_box_client, get_settings_override().MEDIA_METADATA_TEMPLATE_NAME
    )
    if template is None:
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Demo template not found, goto /metadata/create to create it"
        }
    else:
        assert response.status_code == 200


def test_metadata_create(test_app, test_box_client):
    """Should create a metadata template"""
    template = metadata_template_check_by_name(
        test_box_client, get_settings_override().MEDIA_METADATA_TEMPLATE_NAME
    )
    if template is not None:
        template.delete()

    response = test_app.post("/metadata/create?force=true")
    assert response.status_code == 201

    template = metadata_template_check_by_name(
        test_box_client, get_settings_override().MEDIA_METADATA_TEMPLATE_NAME
    )
    assert template is not None

    result = template.response_object
    assert response.json() == {"status": "success", "data": result}
