from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Abstract Base Class for all agents in the system.
    Ensures a consistent interface across different specialized agents.
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        print(f"{self.agent_name} initialized.")

    @abstractmethod
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for the agent to process a request.
        """
        pass

class AgentResponse:
    """
    Standardized response object for inter-agent communication.
    """
    def __init__(self, agent_name: str, content: Any, status: str = "success", metadata: Dict = None):
        self.agent_name = agent_name
        self.content = content
        self.status = status
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent_name,
            "content": self.content,
            "status": self.status,
            "metadata": self.metadata
        }
