#!/usr/bin/env python3
"""
Configuration Manager - Loads API keys and settings from ~/env.d
"""

from pathlib import Path
from typing import Dict, Optional
import os
import json


class ConfigManager:
    """Manage configuration and API keys"""
    
    def __init__(self, env_dir: Optional[Path] = None):
        self.env_dir = env_dir or Path.home() / '.env.d'
        self.config = {}
        self.api_keys = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from env.d directory"""
        if not self.env_dir.exists():
            print(f"Note: {self.env_dir} not found, using defaults")
            return
        
        # Load all .env files
        for env_file in self.env_dir.glob('*.env'):
            self._load_env_file(env_file)
        
        # Load JSON config if exists
        config_json = self.env_dir / 'config.json'
        if config_json.exists():
            with open(config_json) as f:
                self.config.update(json.load(f))
        
        print(f"Loaded config from {self.env_dir}")
    
    def _load_env_file(self, env_file: Path):
        """Load environment variables from .env file"""
        try:
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        
                        # Store API keys separately
                        if 'API_KEY' in key or 'TOKEN' in key or 'SECRET' in key:
                            self.api_keys[key] = value
                        else:
                            self.config[key] = value
        except Exception as e:
            print(f"Warning: Could not load {env_file}: {e}")
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        # Try various naming conventions
        possible_keys = [
            f'{service.upper()}_API_KEY',
            f'{service.upper()}_KEY',
            f'{service.upper()}_TOKEN',
            service.upper()
        ]
        
        for key in possible_keys:
            if key in self.api_keys:
                return self.api_keys[key]
        
        return None
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def has_api_key(self, service: str) -> bool:
        """Check if API key exists for service"""
        return self.get_api_key(service) is not None
    
    def list_available_services(self) -> list:
        """List services with configured API keys"""
        services = set()
        for key in self.api_keys.keys():
            # Extract service name from key
            service = key.split('_')[0].lower()
            services.add(service)
        return sorted(services)


# Global config instance
_config = None

def get_config() -> ConfigManager:
    """Get global config instance"""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config
