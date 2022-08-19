from flask import Blueprint, jsonify

from utils.playerutil import generate_user_profile
from utils.mediautil import remove_skin_from_player

media_api = Blueprint("media_api", __name__)


@media_api.put("/minecraft/profile/capes/active")
def media_api_minecraft_profile_capes_active():
    data = request.header.get("Authorization")

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


@media_api.delete("/minecraft/profile/skins/active")
def media_api_minecraft_profile_skins_delete():
    data = request.header.get("Authorization")

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
    remove_skin_from_player(username)

    # ADD RES OTHERWISE FLASK WILL SCREAM
    res = {"status": "ok"}
    return jsonify(res), 200
