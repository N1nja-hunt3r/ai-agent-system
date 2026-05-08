"""
FRIDAY Agent - Casual, Fun, Friendly
"""

from src.agents.base_agent import BaseAgent

class FridayAgent(BaseAgent):
    """FRIDAY: Casual, fun, and friendly AI assistant"""
    
    def __init__(self):
        super().__init__(
            name="FRIDAY",
            description="Casual and friendly AI assistant with fun personality",
            personality="casual_fun",
        )
    
    def get_system_prompt(self) -> str:
        """Get FRIDAY system prompt"""
        return """You are FRIDAY, a casual and friendly AI assistant. Your characteristics:
- Be conversational and engaging
- Use humor and friendly tone
- Explain things in simple, accessible language
- Show enthusiasm for helping
- Use emojis occasionally when appropriate
- Be approachable and warm
- Make interactions enjoyable

Maintain this fun and friendly personality in all interactions."""
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input as FRIDAY"""
        # Understand intent
        intent_info = self.understand_intent(user_input)
        
        # Generate response
        response = self.generate_response(
            prompt=user_input,
            temperature=0.8,  # Higher temperature for more creative responses
        )
        
        return response
