"""
Configuration Management
Load and manage environment variables and settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import os

class Settings(BaseSettings):
    """Application Settings"""
    
    # LLM Configuration
    primary_llm_provider: str = "deepseek"
    fallback_llm_providers: str = "nemotron,glm,gemma,gpt-oss"
    
    # DeepSeek
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    deepseek_flash_model: str = "deepseek-v4-flash"
    deepseek_pro_model: str = "deepseek-v4-pro"
    deepseek_reasoning_model: str = "deepseek-v4-pro"
    deepseek_coding_model: str = "deepseek-v4-flash"
    deepseek_chat_model: str = "deepseek-v4-flash"
    
    # Nemotron
    nemotron_api_key: Optional[str] = None
    nemotron_base_url: str = "https://api.nvidia.com/v1/nemotron"
    nemotron_omni_model: str = "nemotron-3-nano-omni-30b-a3b-reasoning"
    nemotron_safety_model: str = "nemotron-3-content-safety"
    nemotron_multimodal_model: str = "nemotron-3-nano-omni-30b-a3b-reasoning"
    nemotron_safety_check_model: str = "nemotron-3-content-safety"
    
    # GLM
    glm_api_key: Optional[str] = None
    glm_base_url: str = "https://api.chatglm.cn/v1"
    glm_5_1_model: str = "glm-5.1"
    glm_4_7_model: str = "glm-4.7"
    glm_reasoning_model: str = "glm-5.1"
    glm_coding_model: str = "glm-4.7"
    glm_agentic_model: str = "glm-5.1"
    
    # Gemma
    gemma_api_key: Optional[str] = None
    gemma_base_url: str = "https://api.gemma.ai/v1"
    gemma_31b_model: str = "gemma-4-31b-it"
    gemma_reasoning_model: str = "gemma-4-31b-it"
    gemma_coding_model: str = "gemma-4-31b-it"
    
    # GPT-OSS
    gpt_oss_api_key: Optional[str] = None
    gpt_oss_base_url: str = "https://api.gpt-oss.com/v1"
    gpt_oss_20b_model: str = "gpt-oss-20b"
    gpt_oss_reasoning_model: str = "gpt-oss-20b"
    gpt_oss_efficient_model: str = "gpt-oss-20b"
    
    # FLUX
    flux_api_key: Optional[str] = None
    flux_base_url: str = "https://api.flux.ai/v1"
    flux_image_model: str = "flux.2-klein-4b"
    
    # Speech-to-Text
    stt_provider: str = "whisper"
    whisper_model: str = "base"
    whisper_language: str = "en"
    
    # Text-to-Speech
    tts_provider: str = "gtts"
    tts_language: str = "en"
    tts_speed: float = 1.0
    
    # Agent Configuration
    default_agent: str = "friday"
    agent_memory_size: int = 100
    agent_context_length: int = 2000
    agent_response_timeout: int = 30
    enable_multi_agent: bool = True
    max_concurrent_agents: int = 3
    agent_collaboration_enabled: bool = True
    
    # System Configuration
    app_name: str = "AI Agent System"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Data Storage
    data_dir: str = "./data"
    logs_dir: str = "./logs"
    models_dir: str = "./models"
    
    # Voice Settings
    voice_enabled: bool = True
    microphone_device: str = "default"
    speaker_device: str = "default"
    voice_timeout: int = 30
    
    # Chat Settings
    chat_history_size: int = 50
    chat_context_length: int = 4000
    chat_max_tokens: int = 2000
    
    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_reload: bool = False
    
    # WebSocket
    websocket_enabled: bool = True
    websocket_heartbeat: int = 30
    
    # Database
    database_url: str = "sqlite:///./data/agent.db"
    redis_enabled: bool = False
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    api_key_enabled: bool = False
    api_key: str = "your_api_key_here"
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60
    
    # File Operations
    file_operations_enabled: bool = True
    file_base_path: str = "./data/files"
    max_file_size_mb: int = 100
    
    # Monitoring
    metrics_enabled: bool = False
    metrics_port: int = 9090
    
    # Feature Flags
    feature_voice: bool = True
    feature_chat: bool = True
    feature_file_ops: bool = True
    feature_device_access: bool = False
    feature_learning: bool = True
    feature_multimodal: bool = True
    feature_image_gen: bool = False
    
    # Advanced Settings
    use_quantization: bool = False
    use_flash_attention: bool = True
    batch_size: int = 1
    max_context_tokens: int = 128000
    max_output_tokens: int = 4096
    enable_reasoning: bool = True
    reasoning_timeout: int = 60
    reasoning_cost_limit: float = 5.0
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_llm_provider(self) -> str:
        """Get primary LLM provider"""
        return self.primary_llm_provider
    
    def get_fallback_providers(self) -> List[str]:
        """Get fallback LLM providers"""
        return [p.strip() for p in self.fallback_llm_providers.split(",")]
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for provider"""
        provider = provider.lower()
        if provider == "deepseek":
            return self.deepseek_api_key
        elif provider == "nemotron":
            return self.nemotron_api_key
        elif provider == "glm":
            return self.glm_api_key
        elif provider == "gemma":
            return self.gemma_api_key
        elif provider == "gpt_oss":
            return self.gpt_oss_api_key
        elif provider == "flux":
            return self.flux_api_key
        return None

# Create settings instance
settings = Settings()
