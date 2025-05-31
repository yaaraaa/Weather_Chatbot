from flask import Blueprint, request, jsonify
from Backend.services.assistant.graph.builder import build_graph

chat_bp = Blueprint("chat_api", __name__)

chat_app = build_graph()
chat_state_store = {}


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """Processes a user query through the LangGraph assistant and returns the response and updated state."""

    data = request.get_json()
    session_id = data.get("session_id")
    new_query = data.get("query")

    if not session_id or not new_query:
        return jsonify({"error": "Missing session_id or query"}), 400

    state = chat_state_store.get(session_id, {"history": []})
    state["query"] = new_query

    result = chat_app.invoke(state)

    for key in [
        "history",
        "previous_location",
        "location",
        "weather_data",
        "weather_category",
        "intent",
        "documents",
    ]:
        state[key] = result.get(key)

    chat_state_store[session_id] = state

    return jsonify({"response": result["final_response"], "state": state}), 200
