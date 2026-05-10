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
                            value = value.strip().strip("'").strip("'")
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
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# 🌟 Environment Variables
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
HF_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_MODEL = os.getenv("HF_TTS_MODEL", "suno/bark-small")

# 🎯 Preferred Models
PREFERRED_MODELS = ["gpt-4o-tts", "gpt-4o-audio", "gpt-4o-mini-tts"]


def choose_best_openai_model():
    """🔍 Choose the best available OpenAI model for TTS."""
    if not OPENAI_KEY:
        logger.info("⚠️ OpenAI API key is missing.")
        return None, None

    client = OpenAI(api_key=OPENAI_KEY)
    try:
        models = [m.id for m in client.models.list().data]
        logger.info(f"📜 Available models: {models}")
        for name in PREFERRED_MODELS:
            if name in models:
                logger.info(f"✅ Selected model: {name}")
                return client, name
        logger.info("❌ No preferred models available.")
    except Exception as e:
        logger.info(f"⚠️ Error accessing OpenAI models: {e}")
    return None, None


def can_use_hf():
    """🔍 Check if Hugging Face API can be used."""
    if HF_KEY:
        logger.info("✅ Hugging Face API key is available.")
    else:
        logger.info("⚠️ Hugging Face API key is missing.")
    return bool(HF_KEY)


def hf_params():
    """🔧 Get Hugging Face parameters."""
    logger.info(f"🔧 Hugging Face Model: {HF_MODEL}")
    return HF_KEY, HF_MODEL
