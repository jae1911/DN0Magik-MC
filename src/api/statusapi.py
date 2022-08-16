from flask import Blueprint, jsonify

status_api = Blueprint("status_api", __name__)

# KEPT FOR NICE DISPLAY ON LEGACY LAUNCHERS
@status_api.route("/check")
def status_api_check():
    sample_res = [
        {"minecraft.net": "green"},
        {"session.minecraft.net": "green"},
        {"authserver.mojang.com": "green"},
        {"sessionserver.mojang.com": "green"},
        {"api.mojang.com": "green"},
        {"textures.minecraft.net": "green"},
        {"mojang.com": "green"},
    ]

    return jsonify(sample_res)
