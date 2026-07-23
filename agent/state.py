from typing import TypedDict


class AgentState(TypedDict):
    query: str
    city: str
    weather_data: dict
    response: str
