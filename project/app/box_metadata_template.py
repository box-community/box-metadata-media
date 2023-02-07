"""Box metadata template functions"""
import json
import os

from boxsdk import Client
from boxsdk.object.metadata_template import (
    MetadataField,
    MetadataFieldType,
    MetadataTemplate,
)


def get_sample_dictionary() -> dict:
    """loads a sample output of a media file to use as the template fo rthe metadata"""
    with open(
        os.path.join(
            os.path.dirname(__file__), "sample_template/BigBuckBunny.mp4.json"
        ),
        "r",
        encoding="utf-8",
    ) as file:
        media_info_raw = json.load(file)

    media_info = media_info_raw["tracks"][0]

    return media_info


def create_metadata_template_from_dict(
    client: Client, name: str, media_info: dict
) -> MetadataTemplate:
    """create a metadata template from a dict"""

    # check if template exists
    template = get_metadata_template_by_name(client, name)
    if template is not None:
        raise ValueError(f"Metadata template {name} already exists")

    fields = []
    for key in media_info:
        fields.append(MetadataField(MetadataFieldType.STRING, key))

    template = client.create_metadata_template(name, fields, hidden=False)

    return template


def get_metadata_template_by_name(client: Client, name: str) -> MetadataTemplate:
    """check if a metadata template exists by name"""

    templates = client.get_metadata_templates()
    for template in templates:
        if name == template.displayName:
            return template
    return None


def delete_metadata_template(client: Client, name: str) -> None:
    """delete a metadata template"""
    template = get_metadata_template_by_name(client, name)
    if template is None:
        raise ValueError(f"Metadata template {name} does not exist")
    template.delete()
