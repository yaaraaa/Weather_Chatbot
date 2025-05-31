from Backend.services.assistant.state import AppState
from Backend.services.assistant.tools.retriever import search_knowledge_base


def retrieve_documents(state: AppState):
    """Fetches relevant documents from the knowledge base using the query, weather, and location."""

    docs = search_knowledge_base.invoke(
        {
            "query": state["query"],
            "weather": state["weather_category"],
            "country": state["location"],
        }
    )
    state["documents"] = docs
    return state
