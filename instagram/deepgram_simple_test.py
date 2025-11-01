
import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""Simple Deepgram API key test"""

from pathlib import Path
import os
import sys

# Get API key from environment
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

if not DEEPGRAM_API_KEY:
    logger.info("❌ DEEPGRAM_API_KEY not found in environment")
    logger.info("   Run: source ~/.env.d/loader.sh")
    sys.exit(1)

logger.info(f"Testing Deepgram API key: {DEEPGRAM_API_KEY[:10]}...\n")

try:
    from deepgram import DeepgramClient

    # Initialize client (automatically uses DEEPGRAM_API_KEY from env)
    client = DeepgramClient()

    logger.info("✓ DeepgramClient initialized successfully")
    logger.info("✓ API key is properly configured\n")

    # Try a simple transcription test
    logger.info("Testing with sample audio file...")

    AUDIO_URL = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"

    response = client.listen.rest.v("1").transcribe_url(
        {"url": AUDIO_URL},
        {"model": "nova-2", "smart_format": True}
    )

    transcript = response.results.channels[0].alternatives[0].transcript

    logger.info(f"✅ SUCCESS! Transcription result:")
    logger.info(f"   \"{transcript}\Path("\n"))
    logger.info("Your Deepgram API key is working correctly! 🎉")

except ImportError as e:
    logger.info(f"❌ Import error: {e}")
    logger.info("   Install: pip install deepgram-sdk")
    sys.exit(1)

except Exception as e:
    logger.info(f"❌ API Error: {e}")
    logger.info("\nThis could mean:")
    logger.info("  1. Your API key is invalid or expired")
    logger.info("  2. You need to create a new key at: https://console.deepgram.com/")
    logger.info("  3. Your account needs verification or credits")
    sys.exit(1)
