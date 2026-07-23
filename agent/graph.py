from langgraph.graph import END, START, StateGraph  # Import graph primitives: start marker, end marker, and graph builder.

from agent.nodes import extract_city, fetch_weather, generate_response  # Import node functions that transform shared state.
from agent.state import AgentState  # Import the typed state schema used by every graph node.

graph = StateGraph(AgentState)  # Create a LangGraph StateGraph whose state shape is AgentState.
graph.add_node("extract_city", extract_city)  # Register the city extraction function as a named graph node.
graph.add_node("fetch_weather", fetch_weather)  # Register the weather API function as the next graph node.
graph.add_node("generate_response", generate_response)  # Register the response formatter as the final graph node.
graph.add_edge(START, "extract_city")  # Connect LangGraph's START marker to the first executable node.
graph.add_edge("extract_city", "fetch_weather")  # Route state from city extraction into weather fetching.
graph.add_edge("fetch_weather", "generate_response")  # Route fetched weather data into response generation.
graph.add_edge("generate_response", END)  # Connect the final node to LangGraph's END marker.
app = graph.compile()  # Compile the declarative graph into an invokable LangGraph app.
