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


# KEPT AS LEGACY FOR NICE DISPLAY
@status_api.route("/orders/statistics")
def status_order_stats():
    # TODO: pull data from DB to feed this endpoint
    sample_res = {"total": "1", "last24h": "1", "saleVelocityPerSecon": "0"}

    return jsonify(sample_res)
