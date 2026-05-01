from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint("auth_bp", __name__)

ADMIN_PASSWORD = "admin123"  # change later


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    password = data.get("password")

    if password == ADMIN_PASSWORD:
        session["admin"] = True
        return jsonify({"success": True})

    return jsonify({"success": False}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("admin", None)
    return jsonify({"success": True})