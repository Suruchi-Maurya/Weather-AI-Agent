from langgraph.graph import END, START, StateGraph

from graph.routing import route_after_location, route_after_router
from graph.state import WeatherState
from nodes.air_quality import fetch_air_quality_node
from nodes.alerts import evaluate_alerts_node
from nodes.conversation import handle_conversation_node
from nodes.forecast import fetch_forecast_node
from nodes.memory import handle_memory_node
from nodes.location import resolve_location_node
from nodes.persistence import persist_response_node
from nodes.recommendation import generate_recommendation_node
from nodes.router import route_request_node
from nodes.weather import fetch_weather_node


workflow = StateGraph(WeatherState)
workflow.add_node("router", route_request_node)
workflow.add_node("location", resolve_location_node)
workflow.add_node("conversation", handle_conversation_node)
workflow.add_node("weather", fetch_weather_node)
workflow.add_node("forecast", fetch_forecast_node)
workflow.add_node("air_quality", fetch_air_quality_node)
workflow.add_node("memory", handle_memory_node)
workflow.add_node("alerts", evaluate_alerts_node)
workflow.add_node("recommendation", generate_recommendation_node)
workflow.add_node("persistence", persist_response_node)

workflow.add_edge(START, "router")
workflow.add_conditional_edges(
    "router",
    route_after_router,
    {
        "conversation": "conversation",
        "location": "location",
        "memory": "memory",
    },
)
workflow.add_conditional_edges(
    "location",
    route_after_location,
    {
        "weather": "weather",
        "forecast": "forecast",
        "air_quality": "air_quality",
    },
)
workflow.add_edge("memory", "persistence")
workflow.add_edge("conversation", "persistence")
workflow.add_edge("weather", "alerts")
workflow.add_edge("forecast", "alerts")
workflow.add_edge("air_quality", "alerts")
workflow.add_edge("alerts", "recommendation")
workflow.add_edge("recommendation", "persistence")
workflow.add_edge("persistence", END)

app = workflow.compile()
