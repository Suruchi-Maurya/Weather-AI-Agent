# Weather AI Agent - LangGraph Architecture

## Overview

Weather AI Agent is an LLM-orchestrated weather application built with
LangGraph and Streamlit. It combines current weather, a seven-day forecast,
air quality, persistent user preferences, conversation history, and a live map.

The application uses specialized LangGraph nodes rather than autonomous agents.
Each node has one explicit responsibility, while the graph controls execution.

## Architecture

```text
Streamlit UI
    |
    v
Router node (Groq + structured output)
    |
    +-- conversation --> Conversation node ------------------------+
    +-- memory -------> Memory node -------------------------------+
    +-- weather/forecast/aqi/combined                              |
            |                                                       |
            v                                                       |
       Location node (one geocode)                                  |
            |                                                       |
            +-- Weather node --+                                    |
            +-- Forecast node -+--> Alert node --> Recommendation --+
            +-- Air-quality ---+                                    |
                                                                    v
                                                            Persistence node
                                                            (SQLite + map data)
```

## Project Structure

```text
weather_intelligence/
|-- app.py                         # Streamlit entry point
|-- core/
|   |-- config.py                  # Project paths, environment loading, API keys
|   `-- llm.py                     # Shared Groq client
|-- graph/
|   |-- state.py                   # WeatherState shared by all nodes
|   |-- routing.py                 # Conditional route selection
|   `-- workflow.py                # Node registration, edges, graph compilation
|-- nodes/
|   |-- router.py                  # Classifies intent and selects required nodes
|   |-- location.py                # Resolves one shared location per query
|   |-- conversation.py            # Handles general conversation
|   |-- weather.py                 # Fetches and normalizes current weather
|   |-- forecast.py                # Fetches the seven-day forecast
|   |-- air_quality.py             # Fetches and normalizes air quality
|   |-- alerts.py                  # Deterministic environmental safety rules
|   |-- memory.py                  # Handles saved city and history requests
|   |-- recommendation.py          # Synthesizes weather guidance with Groq
|   `-- persistence.py             # Saves responses and builds map data
|-- services/
|   |-- geocoding.py               # Resolves cities to coordinates
|   |-- cache.py                    # Thread-safe in-memory TTL caching
|   |-- http.py                     # Shared HTTP session with retries/backoff
|   |-- open_meteo.py              # Current weather and forecast client
|   |-- openweather.py             # Air-quality client
|   `-- map_builder.py             # Builds the map payload
|-- persistence/
|   `-- database.py                # SQLite repository functions
|-- prompts/                       # LLM prompt definitions
|-- schemas/                       # Pydantic structured-output models
|-- ui/
|   |-- chat.py                    # Scrollable chat and graph invocation
|   |-- sidebar.py                 # User preferences and quick actions
|   `-- map_view.py                # Folium map rendering
|-- data/
|   `-- weather_memory.db          # Auto-created local SQLite database
|-- tests/
|   |-- test_graph.py              # Location-first routing and node contracts
|   |-- test_services.py           # Typed services, caching, and retries
|   `-- test_alerts_and_sessions.py # Safety alerts and session behavior
|-- .env.example
|-- requirements.txt
`-- README.md
```

## Why Nodes?

A LangGraph node is any function registered with `workflow.add_node`. The
weather, forecast, and air-quality nodes call predetermined services and update
state; they do not choose tools or run reasoning loops. The LLM-powered router,
conversation, memory, and recommendation components are also bounded nodes with
fixed responsibilities.

An autonomous agent would independently choose among tools, repeat actions, and
decide when its task is complete. This application intentionally uses the more
predictable node-based workflow.

## Data Flow

1. The router loads user memory and classifies the query.
2. Weather-related routes resolve the city once in the location node.
3. Selected data nodes reuse the shared coordinates and typed Pydantic models.
4. The alert node calculates deterministic heat, wind, storm, rain, and AQI risk.
5. The recommendation node explains the data without lowering deterministic risk.
6. The persistence node stores the exchange and creates map data.
7. Streamlit renders the response and updates the map.

## Reliability and Caching

All provider calls use a shared HTTP session with retries, exponential backoff,
and explicit timeouts. Successful responses are cached in memory:

| Data | Cache duration |
| --- | --- |
| City coordinates | 30 days |
| Current weather | 10 minutes |
| Forecast | 30 minutes |
| Air quality | 15 minutes |

Provider failures are represented by typed `ServiceError` objects and are not
cached, allowing later requests to retry normally.

## Safety Alerts

Safety alerts are generated by deterministic Python rules rather than the LLM.
Current rules cover extreme heat, strong wind, thunderstorms, likely rain, and
moderate-to-poor air quality. The LLM turns those facts into natural guidance,
but cannot lower the calculated risk level.

## Persistent Data

SQLite is always stored at `data/weather_memory.db`. The path is derived from
the project root, so running the application from another working directory
cannot create duplicate databases.

The database contains:

- User preferences and last city
- Conversation history
- Session activity

Changing the sidebar user ID resets visible session state before loading that
user's history. **New chat** starts a blank session without deleting saved
history; **Clear history** explicitly deletes that user's conversation history.

## Setup

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add `GROQ_API_KEY` and `OPENWEATHER_API_KEY` to `.env`.

## Run

```powershell
streamlit run app.py
```

Then open `http://localhost:8501`.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Technology

| Area | Technology |
| --- | --- |
| Workflow | LangGraph |
| LLM | Groq through LangChain |
| Structured output | Pydantic |
| Weather and forecast | Open-Meteo |
| Air quality | OpenWeather |
| Persistence | SQLite |
| UI | Streamlit |
| Map | Folium and streamlit-folium |
