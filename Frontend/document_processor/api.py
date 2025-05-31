import requests
import os


def upload_file_to_backend(file):
    """Uploads a document file to the backend for processing and returns the server response."""

    file.seek(0)  # Reset pointer to the start just in case
    files = {"file": (file.name, file, "multipart/form-data")}
    try:
        response = requests.post(f"{os.getenv('API_URL')}/upload", files=files)
        try:
            return response.json(), response.status_code
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Invalid JSON returned from server",
                "raw_response": response.text,
            }, response.status_code
    except Exception as e:
        return {"error": str(e)}, 500
