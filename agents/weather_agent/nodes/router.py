import logging

from langchain_core.messages import HumanMessage

from graph.state import WeatherState
from persistence import database
from prompts.routing import ROUTER_PROMPT
from schemas.routing import RouterDecision

logger = logging.getLogger(__name__)


VALID_INTENTS = {"weather", "forecast", "aqi", "combined", "chat", "memory"}

INTENT_TO_NODES = {
    "weather": ["weather"],
    "forecast": ["forecast"],
    "aqi": ["air_quality"],
    "combined": ["weather", "forecast", "air_quality"],
    "chat": ["conversation"],
    "memory": ["memory"],
}

MEMORY_KEYWORDS = [
    "favorite city",
    "favourite city",
    "my city",
    "remember",
    "save my city",
    "what city",
    "my history",
    "what did i ask",
    "show history",
]


def _safe_fallback_decision() -> RouterDecision:
    return RouterDecision(
        thought="The LLM router was unavailable, so the safest route is normal conversation.",
        intent="chat",
        city="",
        required_nodes=["conversation"],
    )


def _keyword_memory_decision(query: str) -> RouterDecision | None:
    normalized_query = query.lower()
    if any(keyword in normalized_query for keyword in MEMORY_KEYWORDS):
        return RouterDecision(
            thought="The query asks about saved preferences or conversation memory.",
            intent="memory",
            city="",
            required_nodes=["memory"],
        )
    return None


def _format_recent_messages(state: WeatherState) -> str:
    messages = state.get("messages", [])[-4:]
    if not messages:
        return "None"
    return "\n".join(
        f"{message.get('role', 'unknown')}: {message.get('content', '')}"
        for message in messages
    )


def _normalize_decision(decision: RouterDecision, previous_city: str) -> RouterDecision:
    intent = decision.intent if decision.intent in VALID_INTENTS else "chat"
    city = decision.city.strip()

    if intent == "chat":
        city = ""
    elif not city:
        city = previous_city or "Unknown"

    return RouterDecision(
        thought=decision.thought,
        intent=intent,
        city=city.title() if city and city != "Unknown" else city,
        required_nodes=INTENT_TO_NODES[intent],
    )


def route_request_node(state: WeatherState) -> WeatherState:
    query = state["user_query"]
    user_id = state.get("user_id", "default_user")
    prefs = database.get_preference(user_id)
    state["memory_context"] = prefs
    if not state.get("city") and prefs.get("last_city"):
        state["city"] = prefs["last_city"]

    recent = database.get_recent_messages(user_id, limit=6)
    state["conversation_context"] = recent

    previous_city = state.get("previous_city", "") or prefs.get("last_city", "")
    recent_messages = _format_recent_messages(state)

    decision = _keyword_memory_decision(query)
    if decision is None:
        try:
            from core.llm import llm

            structured_llm = llm.with_structured_output(RouterDecision)
            prompt = (
                f"{ROUTER_PROMPT}\n\n"
                "Return a JSON-compatible object that matches the RouterDecision schema.\n"
                f"Recent conversation:\n{recent_messages}\n"
                f"User query: {query}\n"
                f"Previous city: {previous_city or 'None'}"
            )
            decision = structured_llm.invoke([HumanMessage(content=prompt)])
        except Exception:
            logger.exception("Router LLM call failed; falling back to chat intent.")
            decision = _safe_fallback_decision()

    decision = _normalize_decision(decision, previous_city)

    state["intent"] = decision.intent
    state["city"] = decision.city
    state["required_nodes"] = decision.required_nodes
    state["reasoning_trace"] = [
        *state.get("reasoning_trace", []),
        {
            "thought": decision.thought,
            "action": f"route_to:{','.join(decision.required_nodes)}",
            "observation": f"intent={decision.intent}, city={decision.city or 'none'}",
        },
    ]

    if decision.city and decision.city != "Unknown":
        state["previous_city"] = decision.city
    return state
