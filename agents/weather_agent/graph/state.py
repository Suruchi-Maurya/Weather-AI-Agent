from typing import TypedDict


class WeatherState(TypedDict, total=False):
    user_query: str
    user_id: str
    intent: str
    city: str
    required_nodes: list[str]
    location_data: dict
    weather_data: dict
    forecast_data: dict
    aqi_data: dict
    weather_summary: dict
    aqi_summary: dict
    environmental_alerts: list[dict]
    memory_context: dict
    conversation_context: list
    map_data: dict
    messages: list
    previous_city: str
    reasoning_trace: list[dict]
    risk_level: str
    final_response: str


# Backward-compatible alias for integrations that imported the Phase 2 name.
AgentState = WeatherState
