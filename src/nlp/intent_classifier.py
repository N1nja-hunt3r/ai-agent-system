"""
Intent Classification Module
Classify user intent from text
"""

from typing import Dict, List, Tuple, Optional
import json
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class IntentClassifier:
    """Classify user intents"""
    
    INTENT_PATTERNS = {
        "greeting": ["hello", "hi", "hey", "greetings", "good morning", "good evening"],
        "farewell": ["bye", "goodbye", "see you", "take care", "farewell"],
        "help": ["help", "assist", "support", "how do i", "can you help"],
        "file_create": ["create file", "new file", "make file", "write file"],
        "file_delete": ["delete file", "remove file", "erase file"],
        "file_read": ["read file", "open file", "show file", "read me"],
        "information": ["what is", "tell me", "information", "explain", "how does"],
        "time": ["what time", "current time", "what's the time", "what hour"],
        "weather": ["weather", "forecast", "temperature", "rain"],
        "reminder": ["remind me", "set reminder", "remember", "note"],
        "call": ["call", "phone", "dial", "contact"],
        "message": ["message", "text", "send message", "sms"],
        "search": ["search", "find", "look for", "google"],
        "thank": ["thank", "thanks", "appreciate", "grateful"],
        "unknown": [],
    }
    
    def __init__(self):
        """Initialize intent classifier"""
        logger.info("IntentClassifier initialized")
    
    def classify(self, text: str) -> Dict[str, any]:
        """
        Classify intent from text
        
        Args:
            text: User text
        
        Returns:
            Dictionary with intent, confidence, and entities
        """
        text_lower = text.lower().strip()
        
        if not text_lower:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": [],
                "text": text,
            }
        
        # Find matching intent
        intent = "unknown"
        confidence = 0.0
        
        for intent_name, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern in text_lower:
                    intent = intent_name
                    confidence = 0.95  # High confidence for pattern match
                    break
            if confidence > 0.5:
                break
        
        # Extract entities
        entities = self._extract_entities(text_lower)
        
        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "text": text,
        }
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract entities from text
        
        Args:
            text: Lowercased text
        
        Returns:
            List of entities
        """
        entities = []
        
        # Simple entity extraction
        if "file" in text:
            # Extract filename if present
            words = text.split()
            for i, word in enumerate(words):
                if word == "file" and i + 1 < len(words):
                    filename = words[i + 1]
                    entities.append({
                        "type": "file",
                        "value": filename,
                    })
        
        if "remind" in text or "reminder" in text:
            # Extract reminder content
            if "in" in text:
                entities.append({
                    "type": "time_reference",
                    "value": text,
                })
        
        return entities
    
    def get_intent_description(self, intent: str) -> str:
        """Get human-readable description of intent"""
        descriptions = {
            "greeting": "User is greeting",
            "farewell": "User is saying goodbye",
            "help": "User is asking for help",
            "file_create": "User wants to create a file",
            "file_delete": "User wants to delete a file",
            "file_read": "User wants to read a file",
            "information": "User is requesting information",
            "time": "User is asking for time",
            "weather": "User is asking about weather",
            "reminder": "User is setting a reminder",
            "call": "User is initiating a call",
            "message": "User is sending a message",
            "search": "User is searching for something",
            "thank": "User is expressing gratitude",
            "unknown": "Intent is unclear",
        }
        return descriptions.get(intent, "Unknown intent")
