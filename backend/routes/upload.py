from flask import Blueprint, request, jsonify, current_app
import os

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    return jsonify({
        "message": "Image uploaded successfully",
        "filename": file.filename
    })