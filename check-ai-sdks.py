#!/usr/bin/env python3
"""
AI Services Setup Verification Tool
Checks installation and configuration of all AI service SDKs
"""

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
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
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import os
import sys
from importlib.util import find_spec

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def check_package(package_name, display_name=None):
    """Check if a Python package is installed"""
    if display_name is None:
        display_name = package_name
    
    try:
        spec = find_spec(package_name)
        if spec is not None:
            try:
                mod = __import__(package_name)
                version = getattr(mod, '__version__', 'unknown')
                print(f"{GREEN}✅{RESET} {display_name:30} {BLUE}v{version}{RESET}")
                return True
            except:
                print(f"{GREEN}✅{RESET} {display_name:30} {YELLOW}(installed){RESET}")
                return True
    except:
        pass
    
    print(f"{RED}❌{RESET} {display_name:30} {RED}NOT INSTALLED{RESET}")
    return False

def check_env_var(var_name, service_name=None, validate_func=None):
    """Check if an environment variable is set"""
    if service_name is None:
        service_name = var_name
    
    value = os.getenv(var_name)
    
    if value and value not in ['', 'your_key_here', 'your_xai_api_key_here']:
        # Mask the key for display
        if len(value) > 12:
            masked = value[:8] + '...' + value[-4:]
        else:
            masked = '***'
        
        # Validate format if function provided
        if validate_func and not validate_func(value):
            print(f"{YELLOW}⚠️{RESET}  {service_name:30} {YELLOW}Invalid format{RESET}")
            return False
        
        print(f"{GREEN}✅{RESET} {service_name:30} {masked}")
        return True
    else:
        print(f"{RED}❌{RESET} {service_name:30} {RED}NOT SET{RESET}")
        return False

def validate_openai_key(key):
    """Validate OpenAI key format"""
    return key.startswith('sk-proj-') or key.startswith('sk-')

def validate_anthropic_key(key):
    """Validate Anthropic key format"""
    return key.startswith('sk-ant-')

def validate_xai_key(key):
    """Validate XAI key format"""
    return key.startswith('xai-')

def validate_groq_key(key):
    """Validate Groq key format"""
    return key.startswith('gsk_')

def main():
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}🤖 AI Services Setup Verification{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    # Check Python SDKs
    print(f"{BOLD}📦 Python SDK Installation:{RESET}\n")
    
    sdks = {
        'openai': 'OpenAI',
        'anthropic': 'Anthropic (Claude)',
        'groq': 'Groq',
        'google.generativeai': 'Google Gemini',
        'cohere': 'Cohere',
    }
    
    installed = 0
    for pkg, name in sdks.items():
        if check_package(pkg, name):
            installed += 1
    
    print(f"\n{BOLD}📊 Installed: {installed}/{len(sdks)}{RESET}\n")
    
    # Additional packages that use OpenAI SDK
    print(f"{YELLOW}ℹ️  XAI/Grok: Uses OpenAI SDK (openai package){RESET}")
    print(f"{YELLOW}ℹ️  DeepSeek: Uses OpenAI SDK (openai package){RESET}")
    print(f"{YELLOW}ℹ️  Perplexity: Uses custom SDK or OpenAI SDK{RESET}\n")
    
    # Check environment variables
    print(f"\n{BOLD}🔐 Environment Variables:{RESET}\n")
    
    env_vars = [
        ('OPENAI_API_KEY', 'OpenAI', validate_openai_key),
        ('ANTHROPIC_API_KEY', 'Anthropic (Claude)', validate_anthropic_key),
        ('XAI_API_KEY', 'XAI (Grok)', validate_xai_key),
        ('GROQ_API_KEY', 'Groq', validate_groq_key),
        ('GEMINI_API_KEY', 'Google Gemini', None),
        ('PERPLEXITY_API_KEY', 'Perplexity', None),
        ('DEEPSEEK_API_KEY', 'DeepSeek', None),
        ('MISTRAL_API_KEY', 'Mistral', None),
        ('COHERE_API_KEY', 'Cohere', None),
        ('OPENROUTER_API_KEY', 'OpenRouter', None),
        ('TOGETHER_API_KEY', 'Together AI', None),
        ('CEREBRAS_API_KEY', 'Cerebras', None),
    ]
    
    configured = 0
    for var_name, service_name, validator in env_vars:
        if check_env_var(var_name, service_name, validator):
            configured += 1
    
    print(f"\n{BOLD}📊 Configured: {configured}/{len(env_vars)}{RESET}\n")
    
    # Additional checks
    print(f"\n{BOLD}🔧 Configuration Files:{RESET}\n")
    
    config_files = [
        '~/.env.d/llm-apis.env',
        '~/.env.d/MASTER_CONSOLIDATED.env',
        '~/.secrets/.ai-apis.env',
        '~/.codex/.env',
        '~/.env.d/.grok/settings.json',
    ]
    
    existing_configs = 0
    for config_file in config_files:
        expanded = os.path.expanduser(config_file)
        if os.path.exists(expanded):
            print(f"{GREEN}✅{RESET} {config_file}")
            existing_configs += 1
        else:
            print(f"{RED}❌{RESET} {config_file}")
    
    print(f"\n{BOLD}📊 Found: {existing_configs}/{len(config_files)}{RESET}\n")
    
    # Recommendations
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}💡 Recommendations:{RESET}\n")
    
    if configured < len(env_vars):
        print(f"{YELLOW}⚠️{RESET}  Some API keys are not loaded. Run: {BLUE}source ~/.env.d/loader.sh llm-apis{RESET}")
    
    if installed < len(sdks):
        missing = [name for pkg, name in sdks.items() if not find_spec(pkg)]
        if missing:
            print(f"{YELLOW}⚠️{RESET}  Missing SDKs: {', '.join(missing)}")
            print(f"   Install with: {BLUE}pip3 install openai anthropic groq google-generativeai cohere{RESET}")
    
    # Check XAI specifically
    xai_key = os.getenv('XAI_API_KEY')
    if not xai_key or xai_key == 'your_xai_api_key_here':
        print(f"{RED}🚨{RESET} XAI_API_KEY is not set in llm-apis.env!")
        print("   Add it from ~/.secrets/.ai-apis.env or ~/.codex/.env")
    
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    # Summary
    all_good = (installed == len(sdks)) and (configured == len(env_vars))
    if all_good:
        print(f"{GREEN}{BOLD}✅ All AI services are properly installed and configured!{RESET}\n")
        return 0
    else:
        print(f"{YELLOW}{BOLD}⚠️  Some services need attention. See recommendations above.{RESET}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())

