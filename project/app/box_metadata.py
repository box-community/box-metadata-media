""" Handle metadata fecthing and processing for box files"""
import json
from boxsdk import Client
from pymediainfo import MediaInfo

from app.box_metadata_template import metadata_template_check_by_name


def get_file_url_by_id(client: Client, file_id: str) -> str:
    """get the file by id"""

    download_url = client.file(file_id).get_download_url()
    return download_url


def get_file_by_id(client: Client, file_id: str) -> str:
    """get the file by id"""

    file = client.file(file_id)
    return file


def file_metadata_update(
    client: Client, file_id: str, user_id: str | None, template_name: str
) -> None:
    """update the file metadata"""

    # check if we need to switch user context
    if user_id is not None:
        user = client.user(user_id)
        client = client.as_user(user)

    file = get_file_by_id(client, file_id)
    download_url = get_file_url_by_id(client, file_id)

    media_info = MediaInfo.parse(download_url)
    track_general = media_info.general_tracks[0]
    metadata = track_general.to_data()
    # metadata_json = json.dumps(metadata, indent=4)

    template = metadata_template_check_by_name(client, template_name)
    template_fields = template["fields"]

    metadata_mapped = {}
    for field in template_fields:
        metadata_mapped[field["displayName"]] = metadata.get(field["displayName"])

    metadata_json = json.dumps(metadata_mapped, indent=4)

    file.metadata(scope="enterprise", template=template.template_key)
    # {track_type: 'Genral'}
    applied_metadata = file.metadata().create({})

    # applied_metadata = file.metadata().create(metadata_json)

    print(applied_metadata)

    # file.metadata(scope="enterprise", template=template.template_key).set(metadata_json)
