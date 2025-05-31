from Backend.services.assistant.llm import llm
from langchain_core.messages import HumanMessage
from Backend.services.assistant.state import AppState


def classify_intent(state: AppState):
    """Classifies user intent as either 'weather' or 'recommendation' based on chat history and current query."""

    conversation = state.get("history", [])
    print(conversation)
    formatted_history = ""
    for turn in conversation:
        role = turn["role"]
        content = turn["content"]
        formatted_history += f"{role.capitalize()}: {content}\n"

    prompt = (
        "You are a classification assistant.\n"
        "Classify the user’s **current intent** based on the conversation context below, pay more attention to recent messages.\n"
        "Choose from:\n"
        "- 'weather': if the user is just asking about the weather.\n"
        "- 'recommendation': if the user wants clothing or activity suggestions based on the weather.\n\n"
        "Respond with **only one word**: 'weather' or 'recommendation'.\n\n"
        f"{formatted_history}"
        f"User: {state['query']}\n"
        "Intent:"
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    intent = response.content.strip().lower()
    if intent not in ["weather", "recommendation"]:
        intent = "recommendation"
    state["intent"] = intent
    return state
