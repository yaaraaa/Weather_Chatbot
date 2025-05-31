from Backend.services.assistant.llm import llm
from Backend.services.assistant.state import AppState
from langchain_core.messages import HumanMessage


def check_or_extract_location(state: AppState):
    """Extracts or verifies the country from the user's query; updates flags accordingly to determine if weather data should be re-fetched."""

    # Check if query contains a new country (or any location)
    location_detection_prompt = (
        "Does this query mention a country or city? If yes, return its corresponding country name.\n"
        "If the query uses words like 'there', assume the same country as before and return 'same'.\n"
        "If the location is unknown, return 'unknown'.\n"
        "Only output one word: the country, 'same', or 'unknown'.\n\n"
        f"Query: {state['query']}\n"
        "Output:"
    )
    response = llm.invoke([HumanMessage(content=location_detection_prompt)])
    extracted = response.content.strip().lower()

    if extracted == "unknown":
        # No location, no history
        if not state.get("location"):
            state["location"] = "unknown"
            state["fetch_weather_flag"] = False
        else:
            # Reuse existing location
            state["fetch_weather_flag"] = False
    elif extracted == "same":
        # User referred to previous location (e.g. "there")
        state["fetch_weather_flag"] = False
    else:
        # New location detected
        prev = state.get("location")
        if extracted != prev:
            state["previous_location"] = prev
            state["location"] = extracted
            state["fetch_weather_flag"] = True
        else:
            state["fetch_weather_flag"] = False

    return state
