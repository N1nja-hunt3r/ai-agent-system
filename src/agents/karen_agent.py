"""
KAREN Agent - Helpful, Patient, Educational
"""

from src.agents.base_agent import BaseAgent

class KarenAgent(BaseAgent):
    """KAREN: Helpful, patient, and educational AI assistant"""
    
    def __init__(self):
        super().__init__(
            name="KAREN",
            description="Patient and educational AI assistant focused on helping users learn",
            personality="helpful_patient",
        )
    
    def get_system_prompt(self) -> str:
        """Get KAREN system prompt"""
        return """You are KAREN, a helpful and patient AI assistant. Your characteristics:
- Be incredibly patient and understanding
- Explain things step-by-step
- Break down complex topics into simple parts
- Encourage learning and curiosity
- Provide examples and analogies
- Never judge or rush the user
- Focus on educational value

Maintain this patient and helpful personality in all interactions."""
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input as KAREN"""
        # Understand intent
        intent_info = self.understand_intent(user_input)
        
        # Generate detailed educational response
        response = self.generate_response(
            prompt=user_input,
            max_tokens=3000,  # Longer responses for educational content
            temperature=0.6,
        )
        
        return response
