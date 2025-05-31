from langchain_core.tools import tool
from typing import Annotated
from langchain_community.utilities import OpenWeatherMapAPIWrapper


@tool
def get_weather_info(
    location: Annotated[str, "The location that the user has provided."],
) -> str:
    """Retrieves the current weather conditions for the given location"""

    weather = OpenWeatherMapAPIWrapper()
    return weather.run(location)
