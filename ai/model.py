"""
Model

This module provides functionality for model.

Author: Auto-generated
Date: 2025-11-01
"""

# utils/model_select.py
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
