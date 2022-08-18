from os import environ

from utils.dbutils import get_uuid_from_username, get_user_remoteid
from utils.mediautil import get_player_skin

# ENV
STORAGE_BASEURL = environ.get("STORAGE_BASEURL")


def generate_login_dict(username: str, token: str, client_identifer: str):
    user_uuid = get_uuid_from_username(username)
    remoteid = get_user_remoteid(username)

    res = {
        "user": {
            "username": username,
            "properties": [
                {"name": "preferredLanguage", "value": "en-us"},
                {"name": "registrationCountry", "value": "SAV"},
            ],
            "id": remoteid,
        },
        "clientToken": client_identifer,
        "accessToken": token,
        "availableProfiles": [{"name": username, "id": user_uuid}],
        "selectedProfile": {"name": username, "id": user_uuid},
    }

    return res


def generate_user_profile(username: str):
    user_uuid = get_uuid_from_username(username)

    # TODO: SKINHANDLER
    skin_hash = get_player_skin(user_uuid)
    if not skin_hash:
        skin_hash = "default"

    final_skin_uri = f"{STORAGE_BASEURL}/skin/{skin_hash}.png"

    res = {
        "id": user_uuid,
        "name": username,
        "skins": [
            {
                "id": skin_hash,
                "state": "ACTIVE",
                "url": final_skin_uri,
                "variant": "SLIM",
            }
        ],
        "CAPES": [
            {
                "id": "8c94945e-d0b4-4df8-97d1-d8d397624f93",
                "state": "ACTIVE",
                "url": "https://bm.jae.fi/defaultcape.png",
            }
        ],
    }

    return res
