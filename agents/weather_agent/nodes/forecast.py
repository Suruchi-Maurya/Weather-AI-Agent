from graph.state import WeatherState
from schemas.weather import LocationData, ServiceError
from services.open_meteo import get_forecast


def fetch_forecast_node(state: WeatherState) -> WeatherState:
    location_data = state.get("location_data", {})
    if "error" in location_data:
        result = ServiceError.model_validate(location_data)
    else:
        location = LocationData.model_validate(location_data)
        result = get_forecast(
            location.city,
            location.latitude,
            location.longitude,
        )
    return {"forecast_data": result.model_dump()}
