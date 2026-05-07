"""
Entity Extraction Module
Extract named entities from text
"""

from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class EntityExtractor:
    """Extract entities from text"""
    
    ENTITY_TYPES = {
        "person": ["person", "name", "user", "guy", "girl", "man", "woman"],
        "location": ["location", "place", "city", "country", "home", "office"],
        "time": ["time", "date", "moment", "hour", "minute", "second"],
        "quantity": ["number", "amount", "count", "quantity"],
        "action": ["action", "verb", "operation", "task"],
        "file": ["file", "document", "image", "video", "audio"],
    }
    
    def __init__(self):
        """Initialize entity extractor"""
        logger.info("EntityExtractor initialized")
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities from text
        
        Args:
            text: Input text
        
        Returns:
            List of extracted entities
        """
        entities = []
        text_lower = text.lower()
        words = text_lower.split()
        
        # Simple pattern-based entity extraction
        for i, word in enumerate(words):
            entity = self._identify_entity(word, words, i, text_lower)
            if entity:
                entities.append(entity)
        
        # Remove duplicates
        unique_entities = []
        seen = set()
        for entity in entities:
            key = (entity["type"], entity["value"])
            if key not in seen:
                unique_entities.append(entity)
                seen.add(key)
        
        return unique_entities
    
    def _identify_entity(
        self,
        word: str,
        words: List[str],
        index: int,
        full_text: str,
    ) -> Dict[str, Any]:
        """
        Identify if a word is an entity
        
        Args:
            word: Current word
            words: All words
            index: Word index
            full_text: Full text
        
        Returns:
            Entity dictionary or None
        """
        # Check for keywords
        if any(kw in word for kw in self.ENTITY_TYPES["file"]):
            # Get next word as value
            if index + 1 < len(words):
                value = words[index + 1]
                return {
                    "type": "file",
                    "value": value,
                    "position": index,
                }
        
        if any(kw in word for kw in self.ENTITY_TYPES["time"]):
            return {
                "type": "time",
                "value": word,
                "position": index,
            }
        
        if any(kw in word for kw in self.ENTITY_TYPES["location"]):
            # Try to get full location
            if index + 1 < len(words):
                value = f"{word} {words[index + 1]}"
            else:
                value = word
            return {
                "type": "location",
                "value": value,
                "position": index,
            }
        
        return None
    
    def extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract date references from text"""
        dates = []
        date_keywords = ["today", "tomorrow", "yesterday", "next", "last"]
        
        text_lower = text.lower()
        for keyword in date_keywords:
            if keyword in text_lower:
                dates.append({
                    "type": "date",
                    "value": keyword,
                })
        
        return dates
    
    def extract_numbers(self, text: str) -> List[Dict[str, Any]]:
        """Extract numbers from text"""
        numbers = []
        words = text.split()
        
        for word in words:
            try:
                num = float(word)
                numbers.append({
                    "type": "number",
                    "value": num,
                    "text": word,
                })
            except ValueError:
                pass
        
        return numbers
