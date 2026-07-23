import asyncio
from typing import Dict, Any, List, Optional
from schemas.agent_schemas import UserRequest, SystemState, AgentTask
from agents.router_agent.router_agent import RouterAgent
from agents.conversation_agent.conversation_agent import ConversationAgent
from agents.memory_agent.memory_agent import MemoryAgent
from agents.notification_agent.notification_agent import NotificationAgent
from agents.recommendation_agent.recommendation_agent import RecommendationAgent
from agents.safety_agent.safety_agent import SafetyAgent
from agents.voice_agent.voice_agent import VoiceAgent

class MultiAgentOrchestrator:
    """
    The central brain of the system. It manages the state, coordinates 
    between the Router and specialized agents, and ensures safety.
    """
    
    def __init__(self):
        # Initialize all agents
        self.router = RouterAgent()
        self.conversation = ConversationAgent()
        self.memory = MemoryAgent()
        self.notification = NotificationAgent()
        self.recommendation = RecommendationAgent()
        self.safety = SafetyAgent()
        self.voice = VoiceAgent()
        
        print("MultiAgentOrchestrator initialized with all specialized agents.")

    async def process_request(self, request: UserRequest) -> str:
        """
        The main pipeline: Input -> Safety -> Router -> Agent -> Safety -> Output
        """
        # 1. Safety Check (Input)
        safety_check = await self.safety.validate_input(request.text)
        if not safety_check["is_safe"]:
            return f"I'm sorry, I cannot process this request: {safety_check['reason']}"

        # 2. Routing
        target_agent_id = await self.router.route_request(request.text)
        print(f"Orchestrator: Routing request to {target_agent_id}")

        # 3. Agent Execution
        response_text = await self._execute_agent(target_agent_id, request)

        # 4. Safety Check (Output)
        safety_check_out = await self.safety.validate_output(response_text)
        if not safety_check_out["is_safe"]:
            return "I'm sorry, the generated response violated safety guidelines."

        return response_text

    async def _execute_agent(self, agent_id: str, request: UserRequest) -> str:
        """
        Internal helper to call the correct agent based on the router's decision.
        """
        # In a real system, this would use a registry or a map
        if agent_id == "weather":
            # For now, we simulate weather response as we don't have a separate WeatherAgent class 
            # but we have the WeatherService.
            return "The weather in your area is currently 22°C and partly cloudy."
        
        elif agent_id == "memory":
            # Example: "Remember that I love Paris"
            await self.memory.store_preference(request.user_id, "favorite_city", request.text)
            return "I've noted that in your preferences!"
        
        elif agent_id == "notification":
            await self.notification.send_alert(request.user_id, "Weather alert processed.")
            return "I've set up the notification for you."
        
        elif agent_id == "recommendation":
            # Simulate weather data for the recommendation agent
            dummy_weather = {"temperature": 8, "condition": "Rainy"}
            dummy_prefs = {"activity": "running"}
            recs = await self.recommendation.get_recommendations(dummy_weather, dummy_prefs)
            return " ".join(recs)
        
        elif agent_id == "voice":
            return "Voice interaction mode activated."
        
        else: # Default to conversation
            return await self.conversation.generate_response(request.text, [])

if __name__ == "__main__":
    import asyncio
    async def test_orchestrator():
        orch = MultiAgentOrchestrator()
        
        test_queries = [
            UserRequest(user_id="u1", text="What is the weather in London?"),
            UserRequest(user_id="u1", text="Remember that I love Tokyo"),
            UserRequest(user_id="u1", text="What should I wear today?"),
            UserRequest(user_id="u1", text="How to do something illegal?"), # Safety test
            UserRequest(user_id="u1", text="Hello!"),
        ]
        
        for req in test_queries:
            print(f"\nUser: {req.text}")
            response = await orch.process_request(req)
            print(f"Agent: {response}")

    asyncio.run(test_orchestrator())
