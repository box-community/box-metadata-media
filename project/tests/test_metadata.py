import os
import json
# from boxsdk import Client, JWTAuth
from tests.conftest import get_settings_override
from app.box_auth import jwt_auth, jwt_client, jwt_check_client

# from app.config import Settings, get_settings

from app.box_metadata import metadata_template_from_dict, metadata_template_delete

settings = get_settings_override()


def test_jwt_auth() -> None:
    """Test the JWT auth"""
    auth = jwt_auth(settings)
    assert auth is not None


def test_jwt_client() -> None:
    """Test the JWT client"""
    auth = jwt_auth(settings)

    client = jwt_client(auth)
    assert client is not None

    me = client.user().get()
    assert me is not None


def test_metadata_template_list():
    """should return a list of existing templates"""
    client = jwt_check_client(settings)
    templates = client.get_metadata_templates()
    assert templates is not None
    for template in templates:
        print(f"Template: {template.id}\t{template.displayName}")
        assert template is not None


def test_metadata_template_from_json():
    """should create a metadata template from a json file"""
    with open(
        os.path.join(os.path.dirname(__file__), "samples/Video/BigBuckBunny.mp4.json"),
        "r",
        encoding="utf-8",
    ) as file:
        bunny_dict = json.load(file)

    assert bunny_dict is not None

    client = jwt_check_client(settings)

    track_generic = bunny_dict["tracks"][0].items()
    track_name = 'TEST Media Track '+bunny_dict["tracks"][0]["track_type"]

    metadata_template_delete(client, track_name)

    template = metadata_template_from_dict(client, track_name, track_generic)

    assert template is not None
