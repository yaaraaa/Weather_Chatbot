from langgraph.graph import StateGraph, END
from Backend.services.assistant.state import AppState
from Backend.services.assistant.nodes import (
    intent,
    location,
    weather,
    documents,
    responses,
)
from Backend.services.assistant.graph.routes import route_after_weather


def build_graph():
    """Builds and compiles the assistant's state graph, defining the node flow and transitions."""

    graph = StateGraph(AppState)

    graph.set_entry_point("classify_intent")
    graph.add_node("classify_intent", intent.classify_intent)
    graph.add_node("check_or_extract_location", location.check_or_extract_location)
    graph.add_node("fetch_weather", weather.fetch_weather)
    graph.add_node("classify_weather", weather.classify_weather)
    graph.add_node("retrieve_documents", documents.retrieve_documents)
    graph.add_node(
        "generate_weather_only_response", responses.generate_weather_only_response
    )
    graph.add_node("generate_response", responses.generate_final_response)

    graph.add_edge("classify_intent", "check_or_extract_location")
    graph.add_edge("check_or_extract_location", "fetch_weather")
    graph.add_conditional_edges(
        "fetch_weather",
        route_after_weather,
        {
            "generate_weather_only_response": "generate_weather_only_response",
            "classify_weather": "classify_weather",
        },
    )
    graph.add_edge("classify_weather", "retrieve_documents")
    graph.add_edge("retrieve_documents", "generate_response")
    graph.add_edge("generate_weather_only_response", END)
    graph.add_edge("generate_response", END)

    return graph.compile()
