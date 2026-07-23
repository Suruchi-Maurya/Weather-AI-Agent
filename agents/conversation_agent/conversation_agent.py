from typing import Dict, Any

class ConversationAgent:
    """
    ConversationAgent manages the dialogue flow and maintains the context of the user interaction.
    It ensures that the conversation remains coherent and goal-oriented.
    """
    
    def __init__(self):
        self.context_window = 10
        print("ConversationAgent initialized.")

    async def generate_response(self, user_input: str, history: list) -> str:
        """
        Generates a conversational response based on user input and previous dialogue history.
        """
        print(f"Processing conversation input: {user_input}")
        # TODO: Integrate with an LLM for natural language generation
        response = f"I understand you're asking about '{user_input}'. Let me help you with that."
        return response

    async def maintain_context(self, new_turn: Dict[str, Any], history: list) -> list:
        """
        Updates the conversation history and prunes it to fit within the context window.
        """
        history.append(new_turn)
        if len(history) > self.context_window:
            history = history[-self.context_window:]
        return history

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = ConversationAgent()
        history = []
        user_msg = "What's the weather like in London?"
        response = await agent.generate_response(user_msg, history)
        print(f"User: {user_msg}\nAgent: {response}")
        history = await agent.maintain_context({"user": user_msg, "agent": response}, history)
        print(f"History size: {len(history)}")
    
    asyncio.run(test())
