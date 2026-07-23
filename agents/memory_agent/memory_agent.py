from typing import Dict, Any, List, Optional

class MemoryAgent:
    """
    MemoryAgent handles the storage and retrieval of user preferences and historical data.
    It allows the weather agent to remember user-specific details like favorite cities.
    """
    
    def __init__(self):
        # In-memory storage for demonstration; would be a database in production
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        print("MemoryAgent initialized.")

    async def store_preference(self, user_id: str, key: str, value: Any) -> bool:
        """
        Stores a specific preference for a user.
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        
        self.user_profiles[user_id][key] = value
        print(f"Stored preference for {user_id}: {key} = {value}")
        return True

    async def retrieve_preference(self, user_id: str, key: str) -> Optional[Any]:
        """
        Retrieves a stored preference for a user.
        """
        user_data = self.user_profiles.get(user_id, {})
        value = user_data.get(key)
        print(f"Retrieved preference for {user_id}: {key} = {value}")
        return value

    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Returns all stored information for a specific user.
        """
        return self.user_profiles.get(user_id, {})

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = MemoryAgent()
        user_id = "user_123"
        await agent.store_preference(user_id, "favorite_city", "New York")
        await agent.store_preference(user_id, "unit", "Celsius")
        
        city = await agent.retrieve_preference(user_id, "favorite_city")
        print(f"User's favorite city: {city}")
        
        context = await agent.get_user_context(user_id)
        print(f"Full user context: {context}")
    
    asyncio.run(test())
