from uuid import uuid4

from flask import Blueprint, jsonify, request

from utils.dbutils import (
    get_uuid_from_username,
    register_user,
    verify_login,
    get_user_remoteid,
)
from utils.secretsutil import encode_auth_jwt

user_api = Blueprint("user_api", __name__)


@user_api.route("/users/profiles/minecraft/<username>")
def userapi_profiles_minecraft(username: str):
    uuid = get_uuid_from_username(username)
    return jsonify({"uuid": uuid, "username": username})


# NONSTANDARD FOR MOJANG API AS YOU CAN'T REGISTER FROM LAUNCHER
@user_api.post("/api/v1/register")
def api_v1_register():
    data = request.json

    if not data:
        return jsonify({"status": "ko", "err": "No data"})

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "ko", "err": "No data"})

    if (
        len(username) < 3
        or len(username) > 255
        or len(password) < 8
        or len(password) > 255
    ):
        return jsonify({"status": "ko", "err": "Invalid data was provided"})

    uuid = register_user(username, password)

    if not uuid:
        return jsonify(
            {"status": "ko", "err": "User already exists or an error happened"}
        )

    return jsonify({"status": "ok", "uuid": uuid})


@user_api.post("/authenticate")
def userapi_auth():
    data = request.json

    if not data:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "No data found in request",
        }
        return jsonify(res), 400

    # PARSE DATA
    # WE WILL IGNORE THE "AGENT" PART BECAUSE WHO CARES ABOUT "SCROLLS"
    username = data.get("username")
    password = data.get("password")
    client_token = data.get("clientToken")  # OPTIONAL

    if not username or not password:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "Missing username or password",
        }
        return jsonify(res), 400

    print(data)

    # VERIFY LOGIN
    if not verify_login(username, password):
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "Incorrect login or password",
        }
        return jsonify(res), 400

    # CLIENT TOKEN & RES GENERATION LOGIC
    if not client_token:
        client_token = str(uuid4())

    auth_jwt = encode_auth_jwt(username, client_token)
    user_uuid = get_uuid_from_username(username)
    remoteid = get_user_remoteid(username)

    res = {
        "user": {
            "username": username,
            "properties": [
                {"name": "preferredLanguage", "value": "en-us"},
                {"name": "registrationCountry", "value": "SAV"},
            ],
            "id": 1,
        },
        "clientToken": client_token,
        "accessToken": auth_jwt,
        "availableProfiles": [{"name": username, "id": user_uuid}],
        "selectedProfile": {"name": username, "id": user_uuid},
    }

    print(res)

    return jsonify(res), 200
