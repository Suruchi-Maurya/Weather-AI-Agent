from graph.state import WeatherState
from schemas.weather import AQISummary, LocationData, ServiceError
from services.openweather import get_air_quality


def fetch_air_quality_node(state: WeatherState) -> WeatherState:
    city = state.get("city", "Unknown")
    location_data = state.get("location_data", {})
    if "error" in location_data:
        result = ServiceError.model_validate(location_data)
    else:
        location = LocationData.model_validate(location_data)
        result = get_air_quality(
            location.city,
            location.latitude,
            location.longitude,
        )
    result_data = result.model_dump()

    if isinstance(result, ServiceError):
        return {
            "aqi_data": result_data,
            "aqi_summary": AQISummary(city=city, error=result.error).model_dump(),
        }

    summary = AQISummary(
        city=city,
        aqi_index=result.aqi_index,
        aqi_label=result.aqi_label,
        pm2_5=result.pm2_5,
        pm10=result.pm10,
    ).model_dump()
    return {"aqi_data": result_data, "aqi_summary": summary}
