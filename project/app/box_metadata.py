"""Box metadata template functions"""
from boxsdk import Client
from boxsdk.object.metadata_template import (
    MetadataField,
    MetadataFieldType,
    MetadataTemplate,
)


def metadata_template_from_dict(
    client: Client, name: str, track_dict: dict
) -> MetadataTemplate:
    """create a metadata template from a dict"""

    # check if template exists
    template = metadata_template_check_by_name(client, name)
    if template is not None:
        raise Exception(f"Metadata template {name} already exists")

    fields = []
    for key, __ in track_dict:
        print(f"item: {key}")
        fields.append(MetadataField(MetadataFieldType.STRING, key))

    template = client.create_metadata_template(name, fields, hidden=False)

    return template


def metadata_template_check_by_name(client: Client, name: str) -> MetadataTemplate:
    """check if a metadata template exists by name"""

    templates = client.get_metadata_templates()
    for template in templates:
        if name == template.displayName:
            return template
    return None


def metadata_template_delete(client: Client, name: str) -> None:
    """delete a metadata template"""
    template = metadata_template_check_by_name(client, name)
    if template is not None:
        template.delete()
