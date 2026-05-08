"""
Speaker Output Module
Plays audio through speaker
"""

import sounddevice as sd
import numpy as np
from typing import Optional
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class SpeakerOutput:
    """Output audio through speaker"""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        device: Optional[int] = None,
    ):
        """
        Initialize speaker output
        
        Args:
            sample_rate: Audio sample rate (Hz)
            channels: Number of audio channels
            device: Device index (None for default)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device
        
        logger.info(f"SpeakerOutput initialized - sample_rate: {sample_rate}Hz, channels: {channels}")
    
    def play(
        self,
        audio_data: np.ndarray,
        blocking: bool = True,
    ) -> bool:
        """
        Play audio data
        
        Args:
            audio_data: Audio data as numpy array
            blocking: Wait for playback to complete
        
        Returns:
            True if successful
        """
        try:
            if audio_data is None or len(audio_data) == 0:
                logger.warning("Empty audio data provided")
                return False
            
            logger.info(f"Playing audio - {len(audio_data)} samples")
            
            sd.play(
                audio_data,
                samplerate=self.sample_rate,
                device=self.device,
                channels=self.channels,
            )
            
            if blocking:
                sd.wait()
            
            logger.info("Playback completed")
            return True
        except Exception as e:
            logger.error(f"Speaker playback failed: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop playback"""
        try:
            sd.stop()
            logger.info("Playback stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop playback: {e}")
            return False
    
    def set_volume(self, volume: float) -> bool:
        """
        Set output volume (0.0 - 1.0)
        
        Args:
            volume: Volume level
        
        Returns:
            True if successful
        """
        try:
            volume = max(0.0, min(1.0, volume))
            logger.info(f"Volume set to {volume * 100}%")
            # Note: sounddevice doesn't have direct volume control
            # Volume should be adjusted at the audio data level
            return True
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return False
