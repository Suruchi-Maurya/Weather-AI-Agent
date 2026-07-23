from typing import List, Dict, Any

class RecommendationAgent:
    """
    RecommendationAgent provides personalized suggestions based on weather data.
    Example: Suggesting an umbrella if rain is predicted.
    """
    
    def __init__(self):
        print("RecommendationAgent initialized.")

    async def get_recommendations(self, weather_data: Dict[str, Any], user_preferences: Dict[str, Any]) -> List[str]:
        """
        Analyzes weather and user preferences to generate a list of recommendations.
        """
        recommendations = []
        temp = weather_data.get("temperature", 20)
        condition = weather_data.get("condition", "Clear")

        if "rain" in condition.lower() or "storm" in condition.lower():
            recommendations.append("It looks like rain. I recommend taking an umbrella!")
        
        if temp < 10:
            recommendations.append("It's quite chilly. Don't forget a warm jacket.")
        elif temp > 30:
            recommendations.append("It's very hot outside. Stay hydrated and use sunscreen.")

        # Personalization based on preferences
        if user_preferences.get("activity") == "running" and "Clear" in condition:
            recommendations.append("The weather is perfect for your morning run!")

        print(f"Generated {len(recommendations)} recommendations.")
        return recommendations

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = RecommendationAgent()
        weather = {"temperature": 8, "condition": "Rainy"}
        prefs = {"activity": "running"}
        recs = await agent.get_recommendations(weather, prefs)
        for r in recs:
            print(f"Rec: {r}")
    
    asyncio.run(test())
