def route_after_weather(state):
    """Determines the next graph node based on availability of weather data and the user's intent."""

    if not state.get("weather_data"):
        return "generate_weather_only_response"
    return (
        "generate_weather_only_response"
        if state["intent"] == "weather"
        else "classify_weather"
    )
