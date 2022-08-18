from uuid import uuid4

from flask import Blueprint, jsonify, request

from utils.dbutils import (
    get_uuid_from_username,
    register_user,
    verify_login,
    get_user_remoteid,
)
from utils.secretsutil import encode_auth_jwt, check_auth_jwt
from utils.playerutil import generate_login_dict, generate_user_profile

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

    res = generate_login_dict(username, auth_jwt, client_token)

    return jsonify(res), 200


@user_api.get("/minecraft/profile")
def userapi_minecraft_profile():
    data = request.headers.get("Authorization")

    if not data:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "Incorrect login or password",
        }
        return jsonify(res), 400

    token = data.replace("Bearer ", "")

    jwt_check = check_auth_jwt(token, None)

    if not jwt_check:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "Incorrect login or password",
        }
        return jsonify(res), 400

    username = jwt_check["sub"]

    res = generate_user_profile(username)

    return jsonify(res), 200


@user_api.post("/refresh")
def userapi_refresh():
    data = request.json
    if not data:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "No data found in request",
        }
        return jsonify(res), 400

    token = data.get("accessToken")
    client_token = data.get("clientToken")

    if not token or not client_token:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "No data found in request",
        }
        return jsonify(res), 400

    jwt_auth_ok = check_auth_jwt(token, client_token)

    if not jwt_auth_ok:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "Invalid token",
        }
        return jsonify(res), 400

    auth_jwt = encode_auth_jwt(jwt_auth_ok, client_token)
    res = generate_login_dict(jwt_auth_ok, auth_jwt, client_token)

    return jsonify(res), 200
