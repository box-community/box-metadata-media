from boxsdk import Client, JWTAuth

from app.config import Settings


def jwt_auth(settings: Settings) -> JWTAuth:
    """
    Get the auth for the JWT app user
    """
    # access_token = jwt_access_token_get(db, settings)

    auth = JWTAuth.from_settings_file(
        settings.JWT_PATH,
        # store_tokens=jwt_store_token,
        # access_token=access_token
    )

    return auth


def jwt_client(auth: JWTAuth) -> Client:
    """
    Get the client for the JWT app user
    """
    client = Client(auth)

    return client


def jwt_check_client(settings: Settings) -> Client:
    """ Get a Client object for the JWT app user"""
    auth = jwt_auth(settings)
    client = jwt_client(auth)
    return client

