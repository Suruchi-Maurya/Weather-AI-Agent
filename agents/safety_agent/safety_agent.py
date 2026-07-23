from typing import Dict, Any

class SafetyAgent:
    """
    SafetyAgent ensures that the agent's responses are safe, unbiased, and compliant.
    It filters both user inputs and agent outputs for harmful content.
    """
    
    def __init__(self):
        self.blocked_keywords = ["harmful", "offensive", "dangerous", "illegal"]
        print("SafetyAgent initialized.")

    async def validate_input(self, user_input: str) -> Dict[str, Any]:
        """
        Checks if the user input contains any prohibited content.
        """
        input_lower = user_input.lower()
        for word in self.blocked_keywords:
            if word in input_lower:
                print(f"Safety violation detected in input: {word}")
                return {"is_safe": False, "reason": f"Input contains prohibited word: {word}"}
        
        return {"is_safe": True, "reason": None}

    async def validate_output(self, agent_output: str) -> Dict[str, Any]:
        """
        Checks if the generated response is safe to be sent to the user.
        """
        output_lower = agent_output.lower()
        for word in self.blocked_keywords:
            if word in output_lower:
                print(f"Safety violation detected in output: {word}")
                return {"is_safe": False, "reason": f"Output contains prohibited word: {word}"}
        
        return {"is_safe": True, "reason": None}

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = SafetyAgent()
        
        # Test safe input
        res1 = await agent.validate_input("What is the weather in London?")
        print(f"Input 1 safe: {res1['is_safe']}")
        
        # Test unsafe input
        res2 = await agent.validate_input("How to do something illegal?")
        print(f"Input 2 safe: {res2['is_safe']} - Reason: {res2['reason']}")
    
    asyncio.run(test())
