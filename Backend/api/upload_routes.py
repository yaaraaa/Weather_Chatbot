from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from Backend.services.indexing.parser import DataExtractor
from Backend.services.indexing.indexer import DocumentIndexer
from Backend.services import app_state
from Backend import config

UPLOAD_DIR = config.INPUT_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)

OUTPUT_DIR = config.OUTPUT_DIR
os.makedirs(OUTPUT_DIR, exist_ok=True)

upload_bp = Blueprint("upload_api", __name__)


@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    """Handles file upload, extracts content, indexes it into the vector database, and returns the session ID."""

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)

    session_id = "_" + str(uuid.uuid4()).replace("-", "_")
    output_json = os.path.join(OUTPUT_DIR, f"{session_id}.json")
    agent_name = "weather-agent"

    try:
        extractor = DataExtractor(agent_name, file_path, output_json)
        extractor.extract_and_save()

        app_state.collection_name = session_id
        indexer = DocumentIndexer(output_json)
        load_state = indexer.index(session_id)

        return (
            jsonify(
                {
                    "message": "File indexed successfully",
                    "session_id": session_id,
                    "load_state": load_state,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
