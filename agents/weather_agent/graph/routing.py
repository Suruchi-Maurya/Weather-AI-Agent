from graph.state import WeatherState


def route_after_router(state: WeatherState) -> str | list[str]:
    if state.get("intent") in {"weather", "forecast", "aqi", "combined"}:
        return "location"

    required_nodes = state.get("required_nodes", [])
    if required_nodes:
        return required_nodes[0]
    return "conversation"


def route_after_location(state: WeatherState) -> str | list[str]:
    required_nodes = state.get("required_nodes", [])
    if state.get("intent") == "combined":
        return required_nodes or ["weather", "forecast", "air_quality"]
    if required_nodes:
        return required_nodes[0]
    return "conversation"
