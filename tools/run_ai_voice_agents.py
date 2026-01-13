#!/usr/bin/env python3
"""
AI Voice Agents - Production Ready
Integrated with ~/.env.d environment management
"""

import os
import sys
from pathlib import Path

# Load environment from ~/.env.d
sys.path.insert(0, str(Path.home() / ".env.d"))
try:
    from loader import load_env

    load_env()
except ImportError:
    print("Warning: ~/.env.d loader not found. Using system environment variables.")

# Import the main application
from openai_voice_agent import main

if __name__ == "__main__":
    print("🎙️ Starting AI Voice Agents")
    main()
