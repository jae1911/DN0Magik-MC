from flask import Blueprint, jsonify

from utils.dbutils import get_uuid_from_username


user_api = Blueprint("user_api", __name__)


@user_api.route("/users/profiles/minecraft/<username>")
def userapi_profiles_minecraft(username: str):
    uuid = get_uuid_from_username(username)
    return jsonify({"uuid": uuid, "username": username})
