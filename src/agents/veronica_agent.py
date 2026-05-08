"""
VERONICA Agent - Curious, Technical Explorer, Experimental
"""

from src.agents.base_agent import BaseAgent

class VeronicaAgent(BaseAgent):
    """VERONICA: Curious and technically adventurous AI assistant"""
    
    def __init__(self):
        super().__init__(
            name="VERONICA",
            description="Curious and exploratory AI assistant focused on technical discovery",
            personality="curious_explorer",
        )
    
    def get_system_prompt(self) -> str:
        """Get VERONICA system prompt"""
        return """You are VERONICA, a curious and explorative AI assistant. Your characteristics:
- Be curious about every topic
- Dive deep into technical details
- Suggest novel approaches and experiments
- Think outside the box
- Ask clarifying questions
- Explore edge cases and possibilities
- Embrace technical challenges

Maintain this curious and exploratory personality in all interactions."""
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input as VERONICA"""
        # Understand intent
        intent_info = self.understand_intent(user_input)
        
        # Generate creative and exploratory response
        response = self.generate_response(
            prompt=user_input,
            temperature=0.85,  # Higher temperature for creative exploration
        )
        
        return response
