from time import time

from flask import Blueprint, jsonify

from utils.playerutil import generate_user_profile
from utils.mediautil import (
    remove_skin_from_player,
    is_file_allowed,
    check_temp_folder,
    upload_file,
)

media_api = Blueprint("media_api", __name__)

TEMP_UPLOAD_FOLDER = "/tmp/mc/"


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


@media_api.post("/minecraft/profile/skins")
def media_api_minecraft_profile_skins_upload():
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

    if "file" not in request.files:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "No file",
        }
        return jsonify(res), 400

    file = request.files["file"]

    if not is_file_allowed:
        res = {
            "error": "ForbiddenOperationException",
            "errorMessage": "Invalid file",
        }
        return jsonify(res), 400

    filename = secure_filename(file.filename)
    current_time = int(time())
    check_temp_folder()
    final_temp_file = f"{TEMP_UPLOAD_FOLDER}/SKINS/{current_time}_{filename}"
    file.save(final_temp_file)

    # UPLOAD TO S3
    upload_file(final_temp_file, "SKIN", jwt_check)

    # RESPONSE OR FLASK WILL SCREAM
    res = {"status": "ok"}
    return jsonify(res), 200
