from graph.state import WeatherState
from services.geocoding import geocode_city


def resolve_location_node(state: WeatherState) -> WeatherState:
    """Resolve the requested city once for all downstream services."""
    result = geocode_city(state.get("city", "Unknown"))
    return {"location_data": result.model_dump()}
