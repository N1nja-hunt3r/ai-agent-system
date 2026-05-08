"""
JARVIS Agent - Formal, Technical, Professional
"""

from src.agents.base_agent import BaseAgent

class JarvisAgent(BaseAgent):
    """JARVIS: Formal, technical, and professional AI assistant"""
    
    def __init__(self):
        super().__init__(
            name="JARVIS",
            description="Formal and technical AI assistant with professional demeanor",
            personality="formal_technical",
        )
    
    def get_system_prompt(self) -> str:
        """Get JARVIS system prompt"""
        return """You are JARVIS, a formal and highly technical AI assistant. Your characteristics:
- Speak in a formal, professional manner
- Provide detailed technical explanations
- Focus on accuracy and precision
- Use technical terminology appropriately
- Be analytical and logical
- Address the user respectfully
- Provide comprehensive information

Maintain this personality in all interactions."""
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input as JARVIS"""
        # Understand intent
        intent_info = self.understand_intent(user_input)
        
        # Generate response
        response = self.generate_response(
            prompt=user_input,
            temperature=0.3,  # Lower temperature for more formal responses
        )
        
        return response
