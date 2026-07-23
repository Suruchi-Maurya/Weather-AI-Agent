from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class UserRequest:
    """
    Schema for the initial user request.
    """
    user_id: str
    text: str
    audio_data: Optional[bytes] = None
    session_id: str = "default_session"

@dataclass
class AgentTask:
    """
    Schema for a task assigned to a specific agent.
    """
    task_id: str
    agent_id: str
    payload: Dict[str, Any]
    priority: int = 1

@dataclass
class SystemState:
    """
    Schema for the global state managed by the Orchestrator.
    """
    session_id: str
    user_context: Dict[str, Any] = field(default_factory=dict)
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    current_agent: Optional[str] = None
    final_response: Optional[str] = None
