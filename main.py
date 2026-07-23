from multi_agent.agents.weather_agent_v1.graph import app


def main() -> None:
    print("Weather agent ready. Type exit, quit, or q to stop.")

    while True:
        query = input("You: ").strip()
        if query.lower() in ["exit", "quit", "q"]:
            break

        try:
            result = app.invoke(
                {
                    "query": query,
                    "city": "",
                    "weather_data": {},
                    "response": "",
                }
            )
            print(f"Agent: {result['response']}")
        except Exception as exc:
            print(f"Agent: Sorry, something went wrong while handling your request: {exc}")


if __name__ == "__main__":
    main()
