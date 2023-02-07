""" Test the metadata module """
import os

from app.box_metadata_template import (
    create_metadata_template_from_dict,
    delete_metadata_template,
    get_metadata_template_by_name,
)
from app.media_info import get_media_info_by_file_path
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_metadata_template_check_by_name(box_client):
    """should check if a metadata template exists by name"""

    template_name = "This template should not exists"
    template = get_metadata_template_by_name(box_client, template_name)
    assert template is None


def test_metadata_template_list(box_client):
    """should return a list of existing templates"""
    # client = jwt_check_client(settings)
    templates = box_client.get_metadata_templates()
    assert templates is not None
    for template in templates:
        print(f"Template: {template.id}\t{template.displayName}")
        assert template is not None


def test_metadata_template_from_json(box_client):
    """should create a metadata template from a json file"""

    media_info = get_media_info_by_file_path(
        os.path.join(os.path.dirname(__file__), "samples/json/BigBuckBunny.mp4.json")
    )
    template_name = "TEST Media Track " + media_info["track_type"]

    template = get_metadata_template_by_name(box_client, template_name)

    if template is not None:
        delete_metadata_template(box_client, template_name)

    template = create_metadata_template_from_dict(box_client, template_name, media_info)

    assert template is not None

    # should raise an exception if trying to create a template that already exists
    try:
        create_metadata_template_from_dict(box_client, template_name, media_info)
        assert False
    except ValueError as error:
        assert error is not None

    # try to delete a teamplate that does not exist
    try:
        delete_metadata_template(box_client, "Non Existent Template")
        assert False
    except ValueError as error:
        assert error is not None

    # delete and existing template
    delete_metadata_template(box_client, template_name)
