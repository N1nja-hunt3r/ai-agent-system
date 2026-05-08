"""
LLM Bridge - Multi-Provider LLM Integration
Supports: DeepSeek, Nemotron, GLM, Gemma, GPT-OSS, and others
"""

import requests
from typing import Optional, Dict, Any, List
from src.config import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class LLMBridge:
    """Multi-provider LLM interface"""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize LLM bridge
        
        Args:
            provider: LLM provider (deepseek, nemotron, glm, gemma, gpt-oss)
            model: Model name
        """
        self.provider = provider or settings.primary_llm_provider
        self.model = model
        self.fallback_providers = settings.get_fallback_providers()
        
        logger.info(f"LLMBridge initialized - provider: {self.provider}, model: {self.model}")
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            system_prompt: System message
        
        Returns:
            Dictionary with response and metadata
        """
        try:
            # Try primary provider
            result = self._generate_with_provider(
                self.provider,
                prompt,
                max_tokens,
                temperature,
                top_p,
                system_prompt,
            )
            
            if result and "text" in result:
                return result
            
            # Try fallback providers
            for fallback_provider in self.fallback_providers:
                logger.info(f"Trying fallback provider: {fallback_provider}")
                result = self._generate_with_provider(
                    fallback_provider,
                    prompt,
                    max_tokens,
                    temperature,
                    top_p,
                    system_prompt,
                )
                if result and "text" in result:
                    return result
            
            return {"text": "", "error": "All providers failed"}
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {"text": "", "error": str(e)}
    
    def _generate_with_provider(
        self,
        provider: str,
        prompt: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        system_prompt: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Generate with specific provider
        
        Args:
            provider: Provider name
            prompt: User prompt
            max_tokens: Maximum tokens
            temperature: Temperature
            top_p: Top-p parameter
            system_prompt: System prompt
        
        Returns:
            Response dictionary or None
        """
        api_key = settings.get_api_key(provider)
        
        if not api_key:
            logger.warning(f"No API key for provider: {provider}")
            return None
        
        try:
            if provider.lower() == "deepseek":
                return self._generate_deepseek(
                    api_key, prompt, max_tokens, temperature, top_p, system_prompt
                )
            elif provider.lower() == "nemotron":
                return self._generate_nemotron(
                    api_key, prompt, max_tokens, temperature, top_p, system_prompt
                )
            elif provider.lower() == "glm":
                return self._generate_glm(
                    api_key, prompt, max_tokens, temperature, top_p, system_prompt
                )
            elif provider.lower() == "gemma":
                return self._generate_gemma(
                    api_key, prompt, max_tokens, temperature, top_p, system_prompt
                )
            elif provider.lower() == "gpt_oss":
                return self._generate_gpt_oss(
                    api_key, prompt, max_tokens, temperature, top_p, system_prompt
                )
            else:
                logger.error(f"Unknown provider: {provider}")
                return None
        except Exception as e:
            logger.error(f"Provider {provider} failed: {e}")
            return None
    
    def _generate_deepseek(
        self, api_key: str, prompt: str, max_tokens: int,
        temperature: float, top_p: float, system_prompt: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Generate with DeepSeek"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": settings.deepseek_chat_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            }
            
            response = requests.post(
                f"{settings.deepseek_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "provider": "deepseek",
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                }
            else:
                logger.error(f"DeepSeek API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"DeepSeek generation failed: {e}")
            return None
    
    def _generate_nemotron(
        self, api_key: str, prompt: str, max_tokens: int,
        temperature: float, top_p: float, system_prompt: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Generate with Nemotron"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": settings.nemotron_omni_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            }
            
            response = requests.post(
                f"{settings.nemotron_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "provider": "nemotron",
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                }
            else:
                logger.error(f"Nemotron API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Nemotron generation failed: {e}")
            return None
    
    def _generate_glm(
        self, api_key: str, prompt: str, max_tokens: int,
        temperature: float, top_p: float, system_prompt: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Generate with GLM"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": settings.glm_agentic_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            }
            
            response = requests.post(
                f"{settings.glm_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "provider": "glm",
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                }
            else:
                logger.error(f"GLM API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"GLM generation failed: {e}")
            return None
    
    def _generate_gemma(
        self, api_key: str, prompt: str, max_tokens: int,
        temperature: float, top_p: float, system_prompt: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Generate with Gemma"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": settings.gemma_reasoning_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            }
            
            response = requests.post(
                f"{settings.gemma_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "provider": "gemma",
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                }
            else:
                logger.error(f"Gemma API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Gemma generation failed: {e}")
            return None
    
    def _generate_gpt_oss(
        self, api_key: str, prompt: str, max_tokens: int,
        temperature: float, top_p: float, system_prompt: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """Generate with GPT-OSS"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": settings.gpt_oss_reasoning_model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            }
            
            response = requests.post(
                f"{settings.gpt_oss_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result["choices"][0]["message"]["content"],
                    "provider": "gpt_oss",
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0),
                }
            else:
                logger.error(f"GPT-OSS API error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"GPT-OSS generation failed: {e}")
            return None
