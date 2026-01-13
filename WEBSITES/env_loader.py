#!/usr/bin/env python3
"""
Simple Environment Loader
=========================
Loads environment variables from ~/.env.d for the AI agent
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Any

class AIAgentEnvLoader:
    """Simple environment loader for AI agent"""
    
    def __init__(self):
        self.env_d_path = Path.home() / ".env.d"
        self.loaded_vars = {}
        self.loaded_categories = []
        
    def load_all_categories(self) -> Dict[str, Any]:
        """Load all environment categories from ~/.env.d"""
        # Load all .env files
        for env_file in self.env_d_path.glob("*.env"):
            category = env_file.stem
            self.load_category(category)
        
        return {
            "loaded_vars": self.loaded_vars,
            "loaded_categories": self.loaded_categories,
            "total_vars": len(self.loaded_vars)
        }
    
    def load_category(self, category: str) -> bool:
        """Load a specific environment category"""
        env_file = self.env_d_path / f"{category}.env"
        
        if not env_file.exists():
            return False
        
        try:
            # Read the file directly
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.loaded_vars[key] = value
            
            self.loaded_categories.append(category)
            return True
            
        except Exception as e:
            return False