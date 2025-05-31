from typing import TypedDict, Optional


class AppState(TypedDict):
    """Defines the structure of the application state shared across components."""
    
    query: str
    location: Optional[str]
    previous_location: Optional[str]
    weather_data: Optional[dict]
    weather_category: Optional[str]
    fetch_weather_flag: Optional[bool]
    documents: Optional[str]
    final_response: Optional[str]
    intent: Optional[str]
    history: Optional[list]
