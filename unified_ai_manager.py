
#!/usr/bin/env python3
"""
Unified AI Manager
Consolidates AI integration functionality from multiple scripts into one system.
"""

import os
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

# Load API keys from ~/.env.d/
def load_env_d():
    """Load all .env files from ~/.env.d directory"""
    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                print(f"Warning: Error loading {env_file}: {e}")


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def initialize_client(self):
        """Initialize the AI client."""
        pass
    
    @abstractmethod
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get chat completion from the AI."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        if not self.api_key:
            raise ValueError("OpenAI API key not found")
    
    def initialize_client(self):
        """Initialize OpenAI client."""
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get chat completion from OpenAI."""
        if not self.client:
            self.initialize_client()
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content


class AnthropicProvider(AIProvider):
    """Anthropic provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.client = None
        if not self.api_key:
            raise ValueError("Anthropic API key not found")
    
    def initialize_client(self):
        """Initialize Anthropic client."""
        from anthropic import Anthropic
        self.client = Anthropic(api_key=self.api_key)
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get chat completion from Anthropic."""
        if not self.client:
            self.initialize_client()
        
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 4000),
            messages=anthropic_messages,
            **{k: v for k, v in kwargs.items() if k not in ["max_tokens"]}
        )
        return response.content[0].text


class GroqProvider(AIProvider):
    """Groq provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        self.client = None
        if not self.api_key:
            raise ValueError("Groq API key not found")
    
    def initialize_client(self):
        """Initialize Groq client."""
        from groq import Groq
        self.client = Groq(api_key=self.api_key)
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Get chat completion from Groq."""
        if not self.client:
            self.initialize_client()
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content


class UnifiedAIManager:
    """Unified manager for all AI providers."""
    
    def __init__(self):
        load_env_d()
        self.providers: Dict[str, AIProvider] = {}
        self.active_provider: Optional[AIProvider] = None
        self.logger = logging.getLogger(__name__)
    
    def register_provider(self, name: str, provider: AIProvider):
        """Register an AI provider."""
        self.providers[name] = provider
        self.logger.info(f"Registered AI provider: {name}")
    
    def set_active_provider(self, provider_name: str):
        """Set the active AI provider."""
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not registered")
        self.active_provider = self.providers[provider_name]
        self.logger.info(f"Set active provider to: {provider_name}")
    
    def chat(self, messages: List[Dict[str, str]], provider: Optional[str] = None, **kwargs) -> str:
        """Get chat completion using the active or specified provider."""
        if provider:
            if provider not in self.providers:
                raise ValueError(f"Provider {provider} not registered")
            provider_instance = self.providers[provider]
        elif self.active_provider:
            provider_instance = self.active_provider
        else:
            raise ValueError("No provider specified or active")
        
        return provider_instance.chat_completion(messages, **kwargs)
    
    def list_providers(self) -> List[str]:
        """List available providers."""
        return list(self.providers.keys())


# Initialize the manager with common providers
ai_manager = UnifiedAIManager()

# Register providers if their API keys are available
if os.getenv("OPENAI_API_KEY"):
    ai_manager.register_provider("openai", OpenAIProvider())
if os.getenv("ANTHROPIC_API_KEY"):
    ai_manager.register_provider("anthropic", AnthropicProvider())
if os.getenv("GROQ_API_KEY"):
    ai_manager.register_provider("groq", GroqProvider())

# Set a default provider if available
if ai_manager.providers:
    default_provider = next(iter(ai_manager.providers))
    ai_manager.set_active_provider(default_provider)
    print(f"Initialized AI manager with default provider: {default_provider}")
else:
    print("Warning: No AI providers configured. Please set API keys in ~/.env.d/")
