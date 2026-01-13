#!/usr/bin/env python3
"""
AI Agent Environment Loader
===========================
Integrates with ~/.env.d modular environment system
Loads all API keys and configurations for the AI agent stack
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgentEnvLoader:
    """Loads environment variables from ~/.env.d for AI agent system"""
    
    def __init__(self):
        self.env_d_path = Path.home() / ".env.d"
        self.loaded_vars = {}
        self.loaded_categories = []
        self.validation_errors = []
        
    def load_all_categories(self) -> Dict[str, Any]:
        """Load all environment categories from ~/.env.d"""
        logger.info("🔄 Loading all environment categories from ~/.env.d")
        
        # Load all .env files
        for env_file in self.env_d_path.glob("*.env"):
            category = env_file.stem
            self.load_category(category)
        
        # Load aliases if available
        aliases_file = self.env_d_path / "aliases.sh"
        if aliases_file.exists():
            self.load_aliases()
        
        return {
            "loaded_vars": self.loaded_vars,
            "loaded_categories": self.loaded_categories,
            "validation_errors": self.validation_errors,
            "total_vars": len(self.loaded_vars)
        }
    
    def load_category(self, category: str) -> bool:
        """Load a specific environment category"""
        env_file = self.env_d_path / f"{category}.env"
        
        if not env_file.exists():
            logger.warning(f"⚠️  Environment file not found: {env_file}")
            return False
        
        try:
            # Use bash to source the file and capture environment
            # Handle special characters by escaping the command
            cmd = f"set -e; source {env_file} 2>/dev/null || true; env"
            result = subprocess.run(
                ['bash', '-c', cmd],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse environment variables
            new_vars = {}
            for line in result.stdout.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    new_vars[key] = value
                    self.loaded_vars[key] = value
            
            self.loaded_categories.append(category)
            logger.info(f"✅ Loaded {category}: {len(new_vars)} variables")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to load {category}: {e}")
            self.validation_errors.append(f"Failed to load {category}: {e}")
            return False
    
    def load_aliases(self) -> bool:
        """Load aliases from aliases.sh"""
        aliases_file = self.env_d_path / "aliases.sh"
        
        if not aliases_file.exists():
            return False
        
        try:
            # Source aliases and capture environment
            cmd = f"source {aliases_file} && env"
            result = subprocess.run(
                ['bash', '-c', cmd],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse aliases and functions
            aliases = {}
            for line in result.stdout.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    if key.startswith('alias_') or key.startswith('function_'):
                        aliases[key] = value
                        self.loaded_vars[key] = value
            
            if aliases:
                self.loaded_categories.append("aliases")
                logger.info(f"✅ Loaded aliases: {len(aliases)} items")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to load aliases: {e}")
            return False
    
    def validate_api_keys(self) -> Dict[str, List[str]]:
        """Validate API keys using the existing validation logic"""
        validation_results = {
            "valid": [],
            "invalid": [],
            "missing": []
        }
        
        # API key validation patterns
        validation_patterns = {
            "OPENAI_API_KEY": r"^sk-",
            "ANTHROPIC_API_KEY": r"^sk-ant-",
            "GROQ_API_KEY": r"^gsk_",
            "XAI_API_KEY": r"^xai-",
            "DEEPSEEK_API_KEY": r"^sk-",
            "ELEVENLABS_API_KEY": r"^[a-f0-9]{32}$",
            "STABILITY_API_KEY": r"^sk-",
            "REPLICATE_API_TOKEN": r"^r8_",
            "PINECONE_API_KEY": r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$",
            "NOTION_TOKEN": r"^secret_",
            "SERPAPI_KEY": r"^[a-f0-9]{16}$",
            "NEWSAPI_KEY": r"^[a-f0-9]{32}$"
        }
        
        import re
        
        for key, pattern in validation_patterns.items():
            value = self.loaded_vars.get(key)
            
            if not value:
                validation_results["missing"].append(key)
            elif value in ["your_key_here", "your_*_here", ""]:
                validation_results["invalid"].append(key)
            elif not re.match(pattern, value):
                validation_results["invalid"].append(key)
            else:
                validation_results["valid"].append(key)
        
        return validation_results
    
    def generate_docker_env(self) -> str:
        """Generate Docker environment file from loaded variables"""
        docker_env = []
        
        # Core configuration
        docker_env.extend([
            "# AI Agent Docker Environment",
            "# Generated from ~/.env.d",
            "",
            "# Database Configuration",
            f"POSTGRES_DB={self.loaded_vars.get('POSTGRES_DB', 'n8n')}",
            f"POSTGRES_USER={self.loaded_vars.get('POSTGRES_USER', 'n8n')}",
            f"POSTGRES_PASSWORD={self.loaded_vars.get('POSTGRES_PASSWORD', 'your_secure_postgres_password_here')}",
            "",
            "# n8n Configuration",
            f"N8N_ENCRYPTION_KEY={self.loaded_vars.get('N8N_ENCRYPTION_KEY', 'your_n8n_encryption_key_here')}",
            f"TZ={self.loaded_vars.get('TZ', 'America/New_York')}",
            f"GENERIC_TIMEZONE={self.loaded_vars.get('GENERIC_TIMEZONE', 'America/New_York')}",
            "",
            "# AI API Keys - Core LLMs"
        ])
        
        # Core LLM APIs
        llm_keys = [
            "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GROQ_API_KEY", 
            "XAI_API_KEY", "DEEPSEEK_API_KEY"
        ]
        for key in llm_keys:
            value = self.loaded_vars.get(key, f"your_{key.lower()}_here")
            docker_env.append(f"{key}={value}")
        
        docker_env.extend(["", "# Audio & Music APIs"])
        
        # Audio & Music APIs
        audio_keys = [
            "ELEVENLABS_API_KEY", "SUNO_COOKIE", "ASSEMBLYAI_API_KEY", "DEEPGRAM_API_KEY"
        ]
        for key in audio_keys:
            value = self.loaded_vars.get(key, f"your_{key.lower()}_here")
            docker_env.append(f"{key}={value}")
        
        docker_env.extend(["", "# Art & Vision APIs"])
        
        # Art & Vision APIs
        art_keys = [
            "STABILITY_API_KEY", "REPLICATE_API_TOKEN", "RUNWAY_API_KEY", "LEONARDO_API_KEY"
        ]
        for key in art_keys:
            value = self.loaded_vars.get(key, f"your_{key.lower()}_here")
            docker_env.append(f"{key}={value}")
        
        docker_env.extend(["", "# Automation & Agents APIs"])
        
        # Automation & Agents APIs
        automation_keys = [
            "PINECONE_API_KEY", "OPENROUTER_API_KEY", "COHERE_API_KEY", 
            "FIREWORKS_API_KEY", "LANGSMITH_API_KEY"
        ]
        for key in automation_keys:
            value = self.loaded_vars.get(key, f"your_{key.lower()}_here")
            docker_env.append(f"{key}={value}")
        
        docker_env.extend(["", "# Documents & Knowledge APIs"])
        
        # Documents & Knowledge APIs
        doc_keys = ["NOTION_TOKEN"]
        for key in doc_keys:
            value = self.loaded_vars.get(key, f"your_{key.lower()}_here")
            docker_env.append(f"{key}={value}")
        
        docker_env.extend(["", "# SEO & Analytics APIs"])
        
        # SEO & Analytics APIs
        seo_keys = ["SERPAPI_KEY", "NEWSAPI_KEY"]
        for key in seo_keys:
            value = self.loaded_vars.get(key, f"your_{key.lower()}_here")
            docker_env.append(f"{key}={value}")
        
        docker_env.extend([
            "",
            "# Server Configuration",
            "FLASK_ENV=production",
            "FLASK_DEBUG=false",
            "LOG_LEVEL=INFO",
            "",
            "# Webhook URLs",
            "N8N_WEBHOOK_URL=http://n8n:5678",
            "AI_AGENT_URL=http://ai-agent:5000",
            "CONTENT_RESEARCH_URL=http://content-research:5001"
        ])
        
        return "\n".join(docker_env)
    
    def save_docker_env(self, output_file: str = ".env") -> bool:
        """Save generated Docker environment to file"""
        try:
            docker_env_content = self.generate_docker_env()
            
            with open(output_file, 'w') as f:
                f.write(docker_env_content)
            
            # Set secure permissions
            os.chmod(output_file, 0o600)
            
            logger.info(f"✅ Docker environment saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save Docker environment: {e}")
            return False
    
    def get_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report"""
        validation = self.validate_api_keys()
        
        return {
            "loaded_categories": self.loaded_categories,
            "total_variables": len(self.loaded_vars),
            "validation": validation,
            "ai_services_ready": len(validation["valid"]),
            "ai_services_missing": len(validation["missing"]),
            "ai_services_invalid": len(validation["invalid"]),
            "ready_for_deployment": len(validation["missing"]) == 0 and len(validation["invalid"]) == 0
        }

def main():
    """Main function"""
    print("🤖 AI Agent Environment Loader")
    print("==============================")
    
    loader = AIAgentEnvLoader()
    
    # Load all categories
    result = loader.load_all_categories()
    
    print(f"\n📊 Loaded {result['total_vars']} variables from {len(result['loaded_categories'])} categories")
    print(f"Categories: {', '.join(result['loaded_categories'])}")
    
    # Validate API keys
    validation = loader.validate_api_keys()
    
    print(f"\n🔍 API Key Validation:")
    print(f"  ✅ Valid: {len(validation['valid'])}")
    print(f"  ❌ Invalid: {len(validation['invalid'])}")
    print(f"  ⚠️  Missing: {len(validation['missing'])}")
    
    if validation['valid']:
        print(f"\n✅ Valid API Keys: {', '.join(validation['valid'])}")
    
    if validation['invalid']:
        print(f"\n❌ Invalid API Keys: {', '.join(validation['invalid'])}")
    
    if validation['missing']:
        print(f"\n⚠️  Missing API Keys: {', '.join(validation['missing'])}")
    
    # Generate Docker environment
    print(f"\n🐳 Generating Docker environment file...")
    if loader.save_docker_env():
        print("✅ Docker environment file created: .env")
    else:
        print("❌ Failed to create Docker environment file")
        return 1
    
    # Status report
    status = loader.get_status_report()
    
    print(f"\n📈 Deployment Readiness:")
    if status['ready_for_deployment']:
        print("🎉 Ready for deployment! All required API keys are configured.")
    else:
        print("⚠️  Not ready for deployment. Please configure missing API keys.")
        print(f"   Missing: {len(validation['missing'])} keys")
        print(f"   Invalid: {len(validation['invalid'])} keys")
    
    return 0 if status['ready_for_deployment'] else 1

if __name__ == "__main__":
    sys.exit(main())