""" Handle metadata fecthing and processing for box files"""
import os

from boxsdk import BoxAPIException, Client
from boxsdk.object.file import File
from boxsdk.object.metadata import Metadata
from pymediainfo import MediaInfo

from app.box_metadata_template import metadata_template_check_by_name


def get_file_url_by_id(client: Client, file_id: str) -> str:
    """get the file by id"""

    download_url = client.file(file_id).get_download_url()
    return download_url


def get_file_by_id(client: Client, file_id: str) -> File:
    """get the file by id"""

    file = client.file(file_id)
    return file


def file_metadata_set(
    client: Client, file_id: str, user_id: str | None, template_name: str
) -> Metadata:
    """update the file metadata"""

    # check if we need to switch user context
    if user_id is not None:
        user = client.user(user_id)
        client = client.as_user(user)

    file = get_file_by_id(client, file_id)
    download_url = get_file_url_by_id(client, file_id)

    media_info = MediaInfo.parse(download_url)
    track_general = media_info.general_tracks[0]
    metadata_media = track_general.to_data()

    template = metadata_template_check_by_name(client, template_name)
    template_fields = template["fields"]

    metadata_mapped = {}
    for field in template_fields:
        metadata_mapped[field["key"]] = metadata_media.get(field["displayName"])

    # convert values from list to strings
    for key, value in metadata_mapped.items():
        if isinstance(value, list):
            metadata_mapped[key] = ", ".join(value)

    # remove none values
    metadata_mapped = {k: v for k, v in metadata_mapped.items() if v is not None}

    # convert integers to strings
    for key, value in metadata_mapped.items():
        if isinstance(value, int):
            metadata_mapped[key] = str(value)

    # adjust some values directly from file
    file = file.get()
    metadata_mapped["fileName"] = file.name
    metadata_mapped["fileExtension"] = os.path.splitext(file.name)[1]

    # convert dict values into string
    metadata_mapped["folderName"] = ""
    for folder in file.path_collection["entries"]:
        metadata_mapped["folderName"] = (
            metadata_mapped.get("folderName", "") + "/" + folder["name"]
        )

    metadata_mapped["completeName"] = metadata_mapped["folderName"] + "/" + file.name

    applied_metadata = file.metadata(
        scope="enterprise", template=template.template_key
    ).set(metadata_mapped)

    return applied_metadata
