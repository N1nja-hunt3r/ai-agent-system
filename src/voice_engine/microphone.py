"""
Microphone Input Module
Captures audio from microphone
"""

import sounddevice as sd
import numpy as np
from typing import Optional
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class MicrophoneInput:
    """Capture audio from microphone"""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        device: Optional[int] = None,
    ):
        """
        Initialize microphone input
        
        Args:
            sample_rate: Audio sample rate (Hz)
            channels: Number of audio channels
            device: Device index (None for default)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device
        
        logger.info(f"MicrophoneInput initialized - sample_rate: {sample_rate}Hz, channels: {channels}")
    
    def record(
        self,
        duration: float,
        dtype: str = "float32",
    ) -> Optional[np.ndarray]:
        """
        Record audio for specified duration
        
        Args:
            duration: Recording duration in seconds
            dtype: Data type (float32, int16, etc.)
        
        Returns:
            Audio data as numpy array, or None if failed
        """
        try:
            logger.info(f"Recording for {duration} seconds...")
            audio = sd.rec(
                int(self.sample_rate * duration),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device,
                dtype=dtype,
            )
            sd.wait()  # Wait for recording to complete
            logger.info(f"Recording completed - {len(audio)} samples")
            return audio
        except Exception as e:
            logger.error(f"Microphone recording failed: {e}")
            return None
    
    def record_until_silence(
        self,
        silence_threshold: float = 0.01,
        silence_duration: float = 1.0,
        max_duration: float = 30.0,
        dtype: str = "float32",
    ) -> Optional[np.ndarray]:
        """
        Record until silence detected
        
        Args:
            silence_threshold: Audio level threshold for silence
            silence_duration: Duration of silence to detect (seconds)
            max_duration: Maximum recording duration (seconds)
            dtype: Data type
        
        Returns:
            Audio data as numpy array
        """
        try:
            logger.info("Recording until silence detected...")
            
            chunk_duration = 0.5  # 500ms chunks
            silence_samples = int(self.sample_rate * silence_duration / chunk_duration)
            consecutive_silence = 0
            max_samples = int(self.sample_rate * max_duration)
            
            audio_chunks = []
            
            while len(np.concatenate(audio_chunks or [[]])) < max_samples:
                chunk = sd.rec(
                    int(self.sample_rate * chunk_duration),
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    device=self.device,
                    dtype=dtype,
                )
                sd.wait()
                
                # Check if chunk is silent
                if np.max(np.abs(chunk)) < silence_threshold:
                    consecutive_silence += 1
                else:
                    consecutive_silence = 0
                    audio_chunks.append(chunk)
                
                if consecutive_silence >= silence_samples:
                    break
            
            if audio_chunks:
                audio = np.concatenate(audio_chunks)
                logger.info(f"Recording completed - {len(audio)} samples")
                return audio
            else:
                logger.warning("No audio recorded")
                return None
        except Exception as e:
            logger.error(f"Record until silence failed: {e}")
            return None
    
    def list_devices(self) -> str:
        """List available audio devices"""
        try:
            return str(sd.query_devices())
        except Exception as e:
            logger.error(f"Failed to query devices: {e}")
            return "Unable to list devices"
