""" Test the metadata module """
import json
import os

from app.box_metadata import (metadata_template_check_by_name,
                              metadata_template_delete,
                              metadata_template_from_dict)
from tests.conftest import get_settings_override

settings = get_settings_override()


def test_metadata_template_list(test_box_client):
    """should return a list of existing templates"""
    # client = jwt_check_client(settings)
    templates = test_box_client.get_metadata_templates()
    assert templates is not None
    for template in templates:
        print(f"Template: {template.id}\t{template.displayName}")
        assert template is not None


def test_metadata_template_from_json(test_box_client):
    """should create a metadata template from a json file"""
    with open(
        os.path.join(os.path.dirname(__file__), "samples/json/BigBuckBunny.mp4.json"),
        "r",
        encoding="utf-8",
    ) as file:
        bunny_dict = json.load(file)

    assert bunny_dict is not None

    # client = jwt_check_client(settings)

    track_generic = bunny_dict["tracks"][0].items()
    track_name = "TEST Media Track " + bunny_dict["tracks"][0]["track_type"]

    template = metadata_template_check_by_name(test_box_client, track_name)

    if template is not None:
        metadata_template_delete(test_box_client, track_name)

    template = metadata_template_from_dict(test_box_client, track_name, track_generic)

    assert template is not None

    # should raise an exception if trying to create a template that already exists
    try:
        metadata_template_from_dict(test_box_client, track_name, track_generic)
        assert False
    except ValueError as error:
        assert error is not None

    # try to delete a teamplate that does not exist
    try:
        metadata_template_delete(test_box_client, "Non Existent Template")
        assert False
    except ValueError as error:
        assert error is not None

    # delete and existing template
    metadata_template_delete(test_box_client, track_name)
