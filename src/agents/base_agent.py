"""
Base Agent Class
Provides foundation for all agent personalities
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
from datetime import datetime
from src.memory.memory_manager import MemoryManager
from src.nlp.intent_classifier import IntentClassifier
from src.nlp.entity_extractor import EntityExtractor
from src.llm.llm_bridge import LLMBridge
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseAgent(ABC):
    """Base class for all agent personalities"""
    
    def __init__(
        self,
        name: str,
        description: str,
        personality: str = "neutral",
    ):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            description: Agent description
            personality: Personality type
        """
        self.name = name
        self.description = description
        self.personality = personality
        self.created_at = datetime.utcnow()
        
        # Initialize components
        self.memory = MemoryManager()
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.llm = LLMBridge()
        
        logger.info(f"Agent initialized: {name} ({personality})")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get system prompt for this agent"""
        pass
    
    @abstractmethod
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return response"""
        pass
    
    def understand_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Understand user intent from input
        
        Args:
            user_input: User input text
        
        Returns:
            Intent classification result
        """
        intent_result = self.intent_classifier.classify(user_input)
        entities = self.entity_extractor.extract(user_input)
        
        result = {
            **intent_result,
            "entities": entities,
        }
        
        # Store in memory
        self.memory.add_short_term_memory(
            content=user_input,
            memory_type="user_input",
            metadata=result,
        )
        
        return result
    
    def generate_response(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate response using LLM
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens
            temperature: Sampling temperature
        
        Returns:
            Generated response
        """
        system_prompt = self.get_system_prompt()
        
        result = self.llm.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            system_prompt=system_prompt,
        )
        
        response = result.get("text", "I couldn't generate a response.")
        
        # Store in memory
        self.memory.add_short_term_memory(
            content=response,
            memory_type="agent_response",
            metadata={
                "prompt": prompt,
                "provider": result.get("provider"),
            },
        )
        
        return response
    
    def get_memory(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent memories"""
        return self.memory.get_long_term_memory(limit=limit)
    
    def add_memory(self, content: str, importance: float = 0.5) -> bool:
        """Add to memory"""
        return self.memory.add_long_term_memory(
            content=content,
            importance=importance,
        )
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "description": self.description,
            "personality": self.personality,
            "created_at": self.created_at.isoformat(),
        }
