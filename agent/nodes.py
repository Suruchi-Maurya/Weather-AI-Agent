import re

from agent.state import AgentState
from tools.weather_api import get_weather


def extract_city(state: AgentState) -> AgentState:
    query = state["query"].strip()
    city = "Unknown"

    preposition_match = re.search(
        r"\b(?:in|for|at)\s+([A-Z][A-Za-z]*(?:[\s-]+[A-Z][A-Za-z]*)*)",
        query,
    )
    if preposition_match:
        city = preposition_match.group(1).strip()
    else:
        capitalized_matches = re.findall(
            r"\b([A-Z][A-Za-z]*(?:[\s-]+[A-Z][A-Za-z]*)*)\b",
            query,
        )
        if capitalized_matches:
            city = capitalized_matches[-1].strip()

    state["city"] = city
    return state


def fetch_weather(state: AgentState) -> AgentState:
    state["weather_data"] = get_weather(state["city"])
    return state


def generate_response(state: AgentState) -> AgentState:
    weather_code_map = {
        0: "clear skies",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "foggy",
        51: "light drizzle",
        61: "light rain",
        63: "moderate rain",
        71: "light snow",
        80: "rain showers",
        95: "thunderstorm",
    }

    weather_data = state["weather_data"]
    city = state["city"]

    if "error" in weather_data:
        state["response"] = f"Sorry, could not find weather data for {city}."
        return state

    description = weather_code_map.get(weather_data["weather_code"], "unknown conditions")
    state["response"] = (
        f"{city} is currently {weather_data['temperature']}°C "
        f"(feels like {weather_data['apparent_temperature']}°C) with {description}. "
        f"Wind: {weather_data['wind_speed']} km/h | "
        f"Humidity: {weather_data['humidity']}%."
    )
    return state
