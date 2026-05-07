"""
Text-to-Speech Engine
Converts text to speech using multiple TTS providers
"""

import numpy as np
from typing import Optional
from gtts import gTTS
import io
import scipy.io.wavfile as wavfile
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class TextToSpeechEngine:
    """Convert text to speech"""
    
    def __init__(
        self,
        engine: str = "gtts",
        language: str = "en",
        speed: float = 1.0,
    ):
        """
        Initialize TTS engine
        
        Args:
            engine: TTS engine (gtts, pyttsx3)
            language: Language code
            speed: Speech speed (0.5-2.0)
        """
        self.engine = engine
        self.language = language
        self.speed = max(0.5, min(2.0, speed))  # Clamp speed
        
        logger.info(f"TTS Engine initialized - engine: {engine}, language: {language}")
    
    def synthesize_text(
        self,
        text: str,
        language: Optional[str] = None,
    ) -> Optional[np.ndarray]:
        """
        Convert text to speech audio
        
        Args:
            text: Text to synthesize
            language: Language code (uses default if not provided)
        
        Returns:
            Audio data as numpy array, or None if failed
        """
        if language is None:
            language = self.language
        
        if not text or len(text.strip()) == 0:
            logger.warning("Empty text provided for synthesis")
            return None
        
        try:
            if self.engine == "gtts":
                return self._synthesize_gtts(text, language)
            else:
                logger.error(f"Unknown TTS engine: {self.engine}")
                return None
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return None
    
    def _synthesize_gtts(self, text: str, language: str) -> Optional[np.ndarray]:
        """
        Synthesize using Google Text-to-Speech
        
        Args:
            text: Text to synthesize
            language: Language code
        
        Returns:
            Audio data as numpy array
        """
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Write to bytes buffer
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            # Read WAV file from buffer
            sample_rate, audio_data = wavfile.read(fp)
            
            # Convert to float32 and normalize
            audio_data = audio_data.astype(np.float32)
            max_val = np.abs(audio_data).max()
            if max_val > 0:
                audio_data = audio_data / (max_val / 0.8)  # Normalize to 80% of max
            
            logger.info(f"TTS synthesis successful - {len(text)} chars")
            return audio_data
        except Exception as e:
            logger.error(f"gTTS synthesis failed: {e}")
            return None
    
    def synthesize_file(
        self,
        text: str,
        output_path: str,
        language: Optional[str] = None,
    ) -> bool:
        """
        Synthesize text and save to file
        
        Args:
            text: Text to synthesize
            output_path: Output file path
            language: Language code
        
        Returns:
            True if successful
        """
        if language is None:
            language = self.language
        
        try:
            if self.engine == "gtts":
                tts = gTTS(text=text, lang=language, slow=False)
                tts.save(output_path)
                logger.info(f"Audio saved to {output_path}")
                return True
            else:
                logger.error(f"Unknown TTS engine: {self.engine}")
                return False
        except Exception as e:
            logger.error(f"Failed to save TTS to file: {e}")
            return False
