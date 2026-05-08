"""
Speech-to-Text Engine
Convert audio to text using Whisper
"""

import whisper
import numpy as np
from typing import Optional, Dict, Any
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class SpeechToTextEngine:
    """Convert speech to text using Whisper"""
    
    def __init__(
        self,
        model_size: str = "base",
        language: str = "en",
    ):
        """
        Initialize STT engine
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            language: Language code
        """
        self.model_size = model_size
        self.language = language
        
        try:
            logger.info(f"Loading Whisper model: {model_size}")
            self.model = whisper.load_model(model_size)
            logger.info(f"Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.model = None
    
    def transcribe(
        self,
        audio_data: np.ndarray,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Audio data as numpy array
            language: Language code (uses default if not provided)
        
        Returns:
            Dictionary with transcription and metadata
        """
        if self.model is None:
            logger.error("Whisper model not loaded")
            return {"text": "", "language": "", "error": "Model not loaded"}
        
        if audio_data is None or len(audio_data) == 0:
            logger.warning("Empty audio data provided")
            return {"text": "", "language": "", "error": "Empty audio"}
        
        try:
            logger.info(f"Transcribing audio - {len(audio_data)} samples")
            
            # Convert to float32 if needed
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio
            max_val = np.abs(audio_data).max()
            if max_val > 0:
                audio_data = audio_data / max_val
            
            # Transcribe
            lang = language or self.language
            result = self.model.transcribe(
                audio_data,
                language=lang,
                verbose=False,
            )
            
            logger.info(f"Transcription: {result['text']}")
            
            return {
                "text": result["text"],
                "language": result["language"],
                "confidence": 0.95,  # Whisper doesn't return confidence
            }
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return {"text": "", "language": "", "error": str(e)}
    
    def transcribe_file(
        self,
        audio_file: str,
        language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transcribe audio file
        
        Args:
            audio_file: Path to audio file
            language: Language code
        
        Returns:
            Dictionary with transcription
        """
        if self.model is None:
            logger.error("Whisper model not loaded")
            return {"text": "", "error": "Model not loaded"}
        
        try:
            logger.info(f"Transcribing file: {audio_file}")
            
            lang = language or self.language
            result = self.model.transcribe(
                audio_file,
                language=lang,
                verbose=False,
            )
            
            logger.info(f"File transcription: {result['text']}")
            
            return {
                "text": result["text"],
                "language": result["language"],
            }
        except Exception as e:
            logger.error(f"File transcription failed: {e}")
            return {"text": "", "error": str(e)}
