import os
import requests


def send_chat_to_backend(session_id, query):
    """Sends a chat query to the backend API and returns the JSON response or error."""

    payload = {"session_id": session_id, "query": query}
    try:
        response = requests.post(f"{os.getenv('API_URL')}/chat", json=payload)
        try:
            return response.json(), response.status_code
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Invalid JSON returned",
                "raw_response": response.text,
            }, response.status_code
    except Exception as e:
        return {"error": str(e)}, 500
