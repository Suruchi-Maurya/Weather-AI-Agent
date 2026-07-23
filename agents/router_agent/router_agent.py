from typing import Dict, Any

class RouterAgent:
    """
    RouterAgent determines which specialized agent should handle a given request.
    It acts as the traffic controller for the multi-agent system.
    """
    
    def __init__(self):
        self.agent_map = {
            "weather": "WeatherService",
            "memory": "MemoryAgent",
            "notification": "NotificationAgent",
            "recommendation": "RecommendationAgent",
            "voice": "VoiceAgent"
        }
        print("RouterAgent initialized.")

    async def route_request(self, user_input: str) -> str:
        """
        Analyzes the user input and routes it to the appropriate agent.
        """
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["weather", "temperature", "forecast"]):
            return "weather"
        if any(word in input_lower for word in ["remember", "favorite", "my profile"]):
            return "memory"
        if any(word in input_lower for word in ["alert", "notify", "reminder"]):
            return "notification"
        if any(word in input_lower for word in ["suggest", "recommend", "what should i wear"]):
            return "recommendation"
        
        print(f"Routing request: '{user_input}' -> Default: conversation")
        return "conversation"

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = RouterAgent()
        queries = [
            "What is the weather in Tokyo?",
            "Remember that I love Paris",
            "Set an alert for rain",
            "What should I wear today?",
            "Hello there!"
        ]
        for q in queries:
            route = await agent.route_request(q)
            print(f"Query: {q} => Route: {route}")
    
    asyncio.run(test())
