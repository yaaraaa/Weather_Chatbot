from Backend.services.assistant.llm import llm
from Backend.services.assistant.state import AppState
from Backend.services.assistant.nodes.utils import append_to_history
from langchain_core.messages import HumanMessage


def generate_weather_only_response(state: AppState):
    """Generates a simple weather report if the user only asked about the weather."""

    if state.get("location") == "unknown" or not state.get("location"):
        append_to_history(state, "user", state["query"])
        state["final_response"] = "I'm not sure which location you're asking about..."
        append_to_history(state, "assistant", state["final_response"])
        return state

    append_to_history(state, "user", state["query"])
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that reports current weather.",
        },
        *state["history"],
        {
            "role": "user",
            "content": f"The user asked about the weather. Here is the current weather JSON: {state['weather_data']}\nGenerate a clear, user-friendly weather report.",
        },
    ]
    response = llm.invoke([HumanMessage(**msg) for msg in messages])

    final_answer = response.content.strip()
    state["documents"] = ""
    state["final_response"] = final_answer
    append_to_history(state, "assistant", final_answer)
    return state


def generate_final_response(state: AppState):
    """Generates a contextual response including weather, category, and retrieved documents."""

    if state["location"] == "unknown":
        append_to_history(state, "user", state["query"])
        state["final_response"] = "I'm not sure which location you're asking about..."
        append_to_history(state, "assistant", state["final_response"])
        return state

    append_to_history(state, "user", state["query"])

    doc_snippets = state["documents"]
    weather_data = state["weather_data"]
    category = state["weather_category"]

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that gives weather-based recommendations.",
        },
        *state["history"],
        {
            "role": "user",
            "content": f"Weather: {weather_data}\nCategory: {category}\nAdditional Context: {doc_snippets}\nAnswer the query based on this, answer in a way that is friendly and relevant to the user query.",
        },
    ]
    response = llm.invoke([HumanMessage(**msg) for msg in messages])

    final_answer = response.content.strip()
    state["final_response"] = final_answer

    append_to_history(state, "assistant", final_answer)
    return state
