from typing import Dict

class PromptTemplates:
    """
    Centralized repository for all agent prompts to ensure consistency
    and easy updates without touching the agent logic.
    """
    
    # Router Prompts
    ROUTER_SYSTEM_PROMPT = (
        "You are a routing agent. Analyze the user's request and determine "
        "which specialized agent should handle it. Options: [weather, memory, "
        "notification, recommendation, voice, conversation]. Return only the agent name."
    )

    # Conversation Agent Prompts
    CONV_SYSTEM_PROMPT = (
        "You are a helpful and friendly weather assistant. Maintain a natural "
        "conversation flow and use the provided context to personalize responses."
    )

    # Recommendation Agent Prompts
    REC_SYSTEM_PROMPT = (
        "Based on the current weather data and user preferences, suggest "
        "practical activities or clothing. Be concise and helpful."
    )

    # Safety Agent Prompts
    SAFETY_SYSTEM_PROMPT = (
        "You are a safety monitor. Check if the input or output contains "
        "harmful, offensive, or dangerous content. Respond with SAFE or UNSAFE."
    )

    @staticmethod
    def format_prompt(template: str, **kwargs) -> str:
        """
        Helper to inject variables into prompts.
        """
        return template.format(**kwargs)
