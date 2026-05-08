"""
Agent Orchestrator - Manages multiple agents
"""

from typing import Optional, Dict, Any
from src.agents.jarvis_agent import JarvisAgent
from src.agents.friday_agent import FridayAgent
from src.agents.edith_agent import EdithAgent
from src.agents.karen_agent import KarenAgent
from src.agents.veronica_agent import VeronicaAgent
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class AgentOrchestrator:
    """Manage and coordinate multiple agents"""
    
    def __init__(self):
        """Initialize agent orchestrator"""
        self.agents = {
            "jarvis": JarvisAgent(),
            "friday": FridayAgent(),
            "edith": EdithAgent(),
            "karen": KarenAgent(),
            "veronica": VeronicaAgent(),
        }
        
        self.current_agent_name = settings.default_agent.lower()
        self.current_agent = self.agents.get(self.current_agent_name)
        
        if not self.current_agent:
            logger.warning(f"Agent {self.current_agent_name} not found, using friday")
            self.current_agent_name = "friday"
            self.current_agent = self.agents["friday"]
        
        logger.info(f"AgentOrchestrator initialized - current agent: {self.current_agent_name}")
    
    def process(self, user_input: str) -> str:
        """Process input with current agent"""
        if not self.current_agent:
            logger.error("No agent selected")
            return "Agent not available"
        
        return self.current_agent.process_user_input(user_input)
    
    def switch_agent(self, agent_name: str) -> bool:
        """
        Switch to different agent
        
        Args:
            agent_name: Name of agent (jarvis, friday, edith, karen, veronica)
        
        Returns:
            True if successful
        """
        agent_name = agent_name.lower()
        
        if agent_name not in self.agents:
            logger.warning(f"Agent {agent_name} not found")
            return False
        
        self.current_agent_name = agent_name
        self.current_agent = self.agents[agent_name]
        logger.info(f"Switched to agent: {agent_name}")
        return True
    
    def get_current_agent_info(self) -> Dict[str, Any]:
        """Get information about current agent"""
        if not self.current_agent:
            return {}
        return self.current_agent.get_info()
    
    def list_agents(self) -> Dict[str, Dict[str, str]]:
        """List all available agents"""
        return {
            name: agent.get_info()
            for name, agent in self.agents.items()
        }
    
    def get_agent_memory(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get agent memory"""
        if agent_name:
            agent_name = agent_name.lower()
            agent = self.agents.get(agent_name)
        else:
            agent = self.current_agent
        
        if not agent:
            return {}
        
        return {
            "agent": agent.name,
            "memories": agent.get_memory(),
        }
