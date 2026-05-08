"""
Logging Configuration
"""

import logging
from pathlib import Path
from src.config import settings

# Create logs directory
Path(settings.logs_dir).mkdir(parents=True, exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    """Setup logger for module"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.log_level))
    
    # File handler
    file_handler = logging.FileHandler(
        Path(settings.logs_dir) / "agent.log"
    )
    file_handler.setLevel(getattr(logging, settings.log_level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
