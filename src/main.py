"""
Main Entry Point for AI Agent System
"""

import argparse
import sys
from typing import Optional
from src.chat.chat_engine import ChatEngine
from src.voice_engine import MicrophoneInput, SpeakerOutput
from src.stt import SpeechToTextEngine
from src.tts import TextToSpeechEngine
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class AIAgentSystem:
    """Main AI Agent System"""
    
    def __init__(self):
        """Initialize system"""
        self.chat_engine = ChatEngine()
        self.mic = MicrophoneInput()
        self.speaker = SpeakerOutput()
        self.stt = SpeechToTextEngine(model_size=settings.whisper_model)
        self.tts = TextToSpeechEngine()
        
        logger.info("AI Agent System initialized")
    
    def run_chat_mode(self) -> None:
        """
        Run in text chat mode
        """
        print(f"\n{'='*60}")
        print(f"AI Agent System - Chat Mode")
        print(f"Current Agent: {self.chat_engine.orchestrator.current_agent_name.upper()}")
        print(f"{'='*60}")
        print("Commands:")
        print("  /agent <name>  - Switch agent (jarvis, friday, edith, karen, veronica)")
        print("  /agents        - List all agents")
        print("  /clear         - Clear history")
        print("  /quit          - Exit")
        print(f"{'='*60}\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    self._handle_command(user_input)
                    continue
                
                # Process message
                result = self.chat_engine.process_message(user_input)
                
                if result["success"]:
                    agent_name = result["agent"].upper()
                    response = result["response"]
                    print(f"\n{agent_name}: {response}\n")
                else:
                    print(f"\nError: {result.get('error')}\n")
            
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                logger.error(f"Chat error: {e}")
                print(f"Error: {e}\n")
    
    def run_voice_mode(self) -> None:
        """
        Run in voice mode
        """
        print(f"\n{'='*60}")
        print(f"AI Agent System - Voice Mode")
        print(f"Current Agent: {self.chat_engine.orchestrator.current_agent_name.upper()}")
        print(f"{'='*60}")
        print("Listening for voice input...")
        print("Press Ctrl+C to exit\n")
        
        while True:
            try:
                # Record audio
                print("\nListening...", end="", flush=True)
                audio = self.mic.record_until_silence(
                    silence_duration=1.0,
                    max_duration=30.0,
                )
                
                if audio is None:
                    print(" No audio detected")
                    continue
                
                print(" Processing...")
                
                # Convert to text
                stt_result = self.stt.transcribe(audio)
                
                if not stt_result.get("text"):
                    print(f"Error: {stt_result.get('error')}")
                    continue
                
                user_text = stt_result["text"]
                print(f"\nYou: {user_text}")
                
                # Process message
                result = self.chat_engine.process_message(user_text)
                
                if result["success"]:
                    response = result["response"]
                    agent_name = result["agent"].upper()
                    print(f"{agent_name}: {response}")
                    
                    # Convert response to speech
                    print("\nSpeaking...", end="", flush=True)
                    audio_response = self.tts.synthesize_text(response)
                    
                    if audio_response is not None:
                        self.speaker.play(audio_response)
                        print(" Done")
                    else:
                        print(" (TTS failed)")
                else:
                    print(f"Error: {result.get('error')}")
            
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                logger.error(f"Voice error: {e}")
                print(f"Error: {e}")
    
    def _handle_command(self, command: str) -> None:
        """
        Handle special commands
        
        Args:
            command: Command string
        """
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == "/quit" or cmd == "/exit":
            print("\nExiting...")
            sys.exit(0)
        
        elif cmd == "/agent" and len(parts) > 1:
            agent_name = parts[1].lower()
            result = self.chat_engine.switch_agent(agent_name)
            if result["success"]:
                print(f"\nSwitched to: {agent_name.upper()}\n")
            else:
                print(f"\nError: {result['error']}\n")
        
        elif cmd == "/agents":
            agents = self.chat_engine.list_agents()
            print("\nAvailable Agents:")
            for name, info in agents.items():
                marker = "*" if name == self.chat_engine.orchestrator.current_agent_name else " "
                print(f"{marker} {name.upper()}: {info['description']}")
            print()
        
        elif cmd == "/clear":
            result = self.chat_engine.clear_history()
            print(f"\n{result['message']}\n")
        
        else:
            print("\nUnknown command\n")

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser(
        description="AI Agent System - JARVIS-like Personal AI Assistant"
    )
    
    parser.add_argument(
        "--mode",
        choices=["chat", "voice", "api"],
        default="chat",
        help="Run mode (default: chat)",
    )
    
    parser.add_argument(
        "--agent",
        choices=["jarvis", "friday", "edith", "karen", "veronica"],
        help="Default agent",
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API port (for API mode)",
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting AI Agent System - mode: {args.mode}")
    
    if args.mode == "api":
        # Run API server
        print(f"\nStarting API server on {settings.api_host}:{args.port}")
        print(f"Swagger UI: http://localhost:{args.port}/docs\n")
        
        import uvicorn
        from src.api.agent_api import app
        
        uvicorn.run(
            app,
            host=settings.api_host,
            port=args.port,
            log_level="info",
        )
    else:
        # Run chat or voice mode
        system = AIAgentSystem()
        
        if args.agent:
            system.chat_engine.switch_agent(args.agent)
        
        if args.mode == "voice":
            system.run_voice_mode()
        else:  # chat mode
            system.run_chat_mode()

if __name__ == "__main__":
    main()
