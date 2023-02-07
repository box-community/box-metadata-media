"""Handles the box client api"""

from boxsdk import Client

from app.box_auth import jwt_check_client
from app.config import Settings


def get_box_client(settings: Settings, as_user: str | None = None) -> Client:
    """Returns a box client, optionally impersonating a user"""

    client = jwt_check_client(settings)

    if as_user is not None:
        user = client.user(user_id=as_user).get()
        client = client.as_user(user)

    return client
