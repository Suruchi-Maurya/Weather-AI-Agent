from graph.state import WeatherState
from persistence import database
from services.map_builder import build_map_data


def persist_response_node(state: WeatherState) -> WeatherState:
    """Persist the exchange and prepare the UI map payload."""
    user_id = state.get("user_id", "default_user")

    if state.get("intent") != "memory":
        database.save_message(
            user_id,
            "user",
            state.get("user_query", ""),
            state.get("intent", ""),
            state.get("city", ""),
        )
        database.upsert_session(user_id)

    database.save_message(
        user_id,
        "assistant",
        state["final_response"],
        state.get("intent", ""),
        state.get("city", ""),
    )

    if state.get("city") and state["city"] != "Unknown":
        database.save_preference(user_id, last_city=state["city"])

    state["map_data"] = build_map_data(state)
    return state
