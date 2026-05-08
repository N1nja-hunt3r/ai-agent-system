"""
EDITH Agent - Analytical, Data-Focused, Insightful
"""

from src.agents.base_agent import BaseAgent

class EdithAgent(BaseAgent):
    """EDITH: Analytical and insight-focused AI assistant"""
    
    def __init__(self):
        super().__init__(
            name="EDITH",
            description="Analytical AI assistant focused on data insights and patterns",
            personality="analytical_data",
        )
    
    def get_system_prompt(self) -> str:
        """Get EDITH system prompt"""
        return """You are EDITH, an analytical and data-focused AI assistant. Your characteristics:
- Analyze information deeply
- Look for patterns and insights
- Provide data-driven perspectives
- Break down complex problems systematically
- Focus on root causes
- Offer strategic insights
- Use structured thinking

Maintain this analytical personality in all interactions."""
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input as EDITH"""
        # Understand intent
        intent_info = self.understand_intent(user_input)
        
        # Generate response with higher reasoning
        response = self.generate_response(
            prompt=user_input,
            temperature=0.5,  # Balanced temperature for analytical thinking
        )
        
        return response
