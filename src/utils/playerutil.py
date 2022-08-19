from os import environ

from utils.dbutils import get_uuid_from_username, get_user_remoteid
from utils.mediautil import get_player_skin, get_player_cape

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

    # SKIN HANDLER
    skin_hash, variant = get_player_skin(user_uuid)
    if not skin_hash:
        skin_hash = "default"
        variant = "SLIM"

    final_skin_uri = f"{STORAGE_BASEURL}/skin/{skin_hash}.png"

    # CAPE HANDLER
    cape_hash = get_player_cape(user_uuid)
    id_cape = "default"
    url_cape = f"{STORAGE_BASEURL}/cape/default.png"

    if cape_hash:
        id_cape = cape_hash
        url_cape = f"{STORAGE_BASEURL}/cape/{cape_hash}.png"

    cape_res = {
        "id": id_cape,
        "state": "ACTIVE",
        "url": url_cape,
    }

    res = {
        "id": user_uuid,
        "name": username,
        "skins": [
            {
                "id": skin_hash,
                "state": "ACTIVE",
                "url": final_skin_uri,
                "variant": variant,
            }
        ],
        "CAPES": [cape_res],
    }

    return res
