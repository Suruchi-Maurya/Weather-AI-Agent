import logging

from graph.state import WeatherState
from schemas.weather import LocationData, ServiceError, WeatherSummary
from services.open_meteo import get_current_weather


logger = logging.getLogger(__name__)

WEATHER_CODE_MAP = {
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


def fetch_weather_node(state: WeatherState) -> WeatherState:
    city = state.get("city", "Unknown")
    location_data = state.get("location_data", {})
    if "error" in location_data:
        result = ServiceError.model_validate(location_data)
    else:
        location = LocationData.model_validate(location_data)
        result = get_current_weather(
            location.city,
            location.latitude,
            location.longitude,
        )
    result_data = result.model_dump()

    if isinstance(result, ServiceError):
        logger.warning("Weather lookup failed for %s: %s", city, result.error)
        return {
            "weather_data": result_data,
            "weather_summary": WeatherSummary(city=city, error=result.error).model_dump(),
        }

    summary = WeatherSummary(
        city=city,
        temperature=result.temperature,
        apparent_temperature=result.apparent_temperature,
        humidity=result.humidity,
        wind_speed=result.wind_speed,
        condition=WEATHER_CODE_MAP.get(result.weather_code, "unknown conditions"),
    ).model_dump()
    return {"weather_data": result_data, "weather_summary": summary}
