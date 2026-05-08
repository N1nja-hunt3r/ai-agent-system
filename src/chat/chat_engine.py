"""
Chat Engine - Manages conversations and interaction
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from src.agents.agent_orchestrator import AgentOrchestrator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class ChatEngine:
    """Manage chat conversations"""
    
    def __init__(self):
        """Initialize chat engine"""
        self.orchestrator = AgentOrchestrator()
        self.conversation_history: List[Dict[str, Any]] = []
        self.session_start = datetime.utcnow()
        
        logger.info("ChatEngine initialized")
    
    def process_message(self, user_input: str) -> Dict[str, Any]:
        """
        Process user message and get response
        
        Args:
            user_input: User message
        
        Returns:
            Response with metadata
        """
        if not user_input or not user_input.strip():
            logger.warning("Empty user input")
            return {
                "success": False,
                "error": "Empty input",
            }
        
        try:
            # Get response from current agent
            response = self.orchestrator.process(user_input)
            
            # Add to conversation history
            timestamp = datetime.utcnow()
            
            self.conversation_history.append({
                "timestamp": timestamp.isoformat(),
                "role": "user",
                "content": user_input,
                "agent": self.orchestrator.current_agent_name,
            })
            
            self.conversation_history.append({
                "timestamp": datetime.utcnow().isoformat(),
                "role": "assistant",
                "content": response,
                "agent": self.orchestrator.current_agent_name,
            })
            
            logger.info(f"Message processed - agent: {self.orchestrator.current_agent_name}")
            
            return {
                "success": True,
                "response": response,
                "agent": self.orchestrator.current_agent_name,
                "timestamp": datetime.utcnow().isoformat(),
            }
        except Exception as e:
            logger.error(f"Message processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
            }
    
    def switch_agent(self, agent_name: str) -> Dict[str, Any]:
        """
        Switch to different agent
        
        Args:
            agent_name: Agent name
        
        Returns:
            Status dictionary
        """
        success = self.orchestrator.switch_agent(agent_name)
        
        if success:
            return {
                "success": True,
                "message": f"Switched to {agent_name}",
                "agent_info": self.orchestrator.get_current_agent_info(),
            }
        else:
            return {
                "success": False,
                "error": f"Agent {agent_name} not found",
            }
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get conversation history
        
        Args:
            limit: Maximum number of messages
        
        Returns:
            Conversation history
        """
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def clear_history(self) -> Dict[str, Any]:
        """Clear conversation history"""
        count = len(self.conversation_history)
        self.conversation_history = []
        logger.info(f"Conversation history cleared - {count} messages")
        return {
            "success": True,
            "message": f"Cleared {count} messages",
        }
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get session information"""
        duration = (datetime.utcnow() - self.session_start).total_seconds()
        
        return {
            "session_start": self.session_start.isoformat(),
            "duration_seconds": duration,
            "messages_count": len(self.conversation_history),
            "current_agent": self.orchestrator.current_agent_name,
            "agent_info": self.orchestrator.get_current_agent_info(),
        }
    
    def list_agents(self) -> Dict[str, Any]:
        """List all available agents"""
        return self.orchestrator.list_agents()
