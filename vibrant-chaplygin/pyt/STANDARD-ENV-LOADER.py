#!/usr/bin/env python3
"""
STANDARD ENV LOADER FOR ~/.env.d/
Add this code to the top of your Python scripts
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load all .env files from ~/.env.d/
env_dir = Path.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)
