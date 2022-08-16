from flask import Flask, jsonify

from api.statusapi import status_api

app = Flask(__name__)

app.register_blueprint(status_api)


@app.route("/")
def index_route():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()
