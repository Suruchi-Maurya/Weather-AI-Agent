from graph.state import WeatherState
from schemas.weather import LocationData, MapData


WMO_CODE_MAP = {
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


def build_map_data(state: WeatherState) -> dict:
    location_data = state.get("location_data", {})
    if not location_data or "error" in location_data:
        return {}

    location = LocationData.model_validate(location_data)

    weather_data = state.get("weather_data", {})
    forecast_data = state.get("forecast_data", {})
    aqi_data = state.get("aqi_data", {})
    weather_code = weather_data.get("weather_code", 0)
    rain_probability = (
        forecast_data.get("days", [{}])[0].get("rain_probability", "")
        if forecast_data.get("days")
        else ""
    )

    return MapData(
        city=location.city,
        lat=location.latitude,
        lon=location.longitude,
        temperature=weather_data.get("temperature", ""),
        aqi_label=aqi_data.get("aqi_label", ""),
        description=WMO_CODE_MAP.get(weather_code, "unknown conditions"),
        rain_probability=rain_probability,
    ).model_dump()
