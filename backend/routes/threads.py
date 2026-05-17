from flask import Blueprint, request, jsonify

threads_bp = Blueprint("threads", __name__)

@threads_bp.route("", methods=["POST"])
def create_thread():
    data = request.json
    return jsonify({
        "message": "Thread created",
        "data": data
    }), 201