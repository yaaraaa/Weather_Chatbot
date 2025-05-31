from Backend.services.assistant.llm import llm
from Backend.services.assistant.state import AppState
from langchain_core.messages import HumanMessage
from Backend.services.assistant.tools.weather import get_weather_info


def fetch_weather(state: AppState):
    """Fetches current weather information based on the state location, unless unnecessary."""

    # only skip fetching weather if they are asking about a recommendation and weather has been fetched before
    # if they are asking about the weather, fetch the weather information again
    if not state.get("fetch_weather_flag") and state.get("intent") == "recommendation":
        return state  # Skip API call
    try:
        weather = get_weather_info.invoke({"location": state["location"]})
        state["weather_data"] = weather
    except Exception as e:
        print(f"❌ Weather API Error: {e}")
        state["weather_data"] = None
    return state


def classify_weather(state: AppState):
    """Classifies the raw weather data into a weather category (e.g., sunny, rainy)."""

    prompt = (
        "You are a weather classification assistant. Classify the following weather report into ONE of these categories:\n"
        "- sunny: clear skies, low clouds, typically warm or mild.\n"
        "- rainy: any form of precipitation (light rain, heavy rain, showers, drizzle).\n"
        "- snowy: snow, sleet, or freezing conditions with snow.\n"
        "- windy: strong winds, noticeable gusts, often with other weather.\n"
        "- cloudy: mostly or completely covered sky, no significant precipitation.\n\n"
        "Return only one category from this list: sunny, rainy, snowy, windy, cloudy.\n\n"
        "Examples:\n"
        "Weather: Clear sky, 20°C, low wind.\n"
        "Output: sunny\n\n"
        "Weather: Light rain showers, 18°C, wind 5 m/s.\n"
        "Output: rainy\n\n"
        f"Weather: {state['weather_data']}\n"
        "Output:"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip().lower()
    valid_categories = {"sunny", "rainy", "snowy", "windy", "cloudy"}
    if category not in valid_categories:
        category = "cloudy"
    state["weather_category"] = category
    return state
