from flask import Blueprint, jsonify

health_routes = Blueprint('health_routes', __name__)

@health_routes.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"}), 200