"""Shared utilities for transcribe scripts."""

import os
from pathlib import Path


def load_env_d() -> None:
    """Load all .env files from ~/.env.d and ~/.env into os.environ."""
    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                print(f"Warning: Error loading {env_file}: {e}")
    try:
        from dotenv import load_dotenv

        load_dotenv(Path.home() / ".env")
    except ImportError:
        pass


def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format for plain-text transcripts."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def format_timestamp_srt(seconds: float) -> str:
    """Convert seconds to SRT/VTT format HH:MM:SS,mmm."""
    ms = int(seconds * 1000)
    hours = ms // 3600000
    minutes = (ms % 3600000) // 60000
    secs = (ms % 60000) // 1000
    ms = ms % 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"
