from flask import Blueprint, jsonify, request

from utils.dbutils import get_uuid_from_username, register_user


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
