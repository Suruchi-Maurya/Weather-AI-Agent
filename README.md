# Phase 1 — Basic Weather Agent

## Overview
Single LangGraph agent that fetches real-time weather and replies in natural language.

## Architecture
User Query → extract_city → fetch_weather → generate_response → Output

## Tech Stack
| Category | Technology |
| --- | --- |
| Agent Framework | LangGraph |
| Weather API | Open-Meteo, free |
| City Extraction | Regex |
| Language | Python 3.10+ |

## Project Structure
```text
phase1_weather_agent/
├── agent/
│   ├── __init__.py        # Marks the agent directory as a Python package
│   ├── state.py           # Defines the shared AgentState TypedDict
│   ├── nodes.py           # Contains extract_city, fetch_weather, and generate_response nodes
│   └── graph.py           # Wires LangGraph nodes and compiles the app
├── tools/
│   ├── __init__.py        # Marks the tools directory as a Python package
│   └── weather_api.py     # Calls Open-Meteo geocoding and weather APIs
├── main.py                # Runs the interactive command-line weather agent
├── requirements.txt       # Lists Python package dependencies
└── README.md              # Project documentation
```

## Setup & Run
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Example
You: What is the weather in Bangalore?
Agent: Bangalore is currently 27°C (feels like 29°C) with partly cloudy skies. Wind: 14 km/h | Humidity: 68%.

## Key Concepts
- LangGraph StateGraph and node wiring
- TypedDict AgentState shared across nodes
- External API calls inside agent nodes
- Sequential edge flow: START → nodes → END

## Notes
- Open-Meteo is used — no API key required
- Each query is stateless (no memory between runs)
