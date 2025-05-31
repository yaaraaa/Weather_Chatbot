def append_to_history(state, role, content):
    """Appends a conversation turn (role, content) to the chat history within the state."""

    if state.get("history") is None:
        state["history"] = []
    state["history"].append({"role": role, "content": content})
