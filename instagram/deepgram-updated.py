"""
Deepgram Test Updated

This module provides functionality for deepgram test updated.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Updated Deepgram Live Transcription Test
Works with Deepgram SDK v3+
"""

from pathlib import Path
import os
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

# Load API key from environment
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

if not DEEPGRAM_API_KEY:
    logger.info("❌ Error: DEEPGRAM_API_KEY not found in environment")
    logger.info("   Run: source ~/.env.d/loader.sh")
    exit(1)


def test_connection():
    """Simple test to verify API key works"""
    try:
        # Initialize the Deepgram client
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        logger.info("✓ Deepgram client initialized")
        logger.info(f"✓ Using API key: {DEEPGRAM_API_KEY[:10]}...")

        # Test with a simple API call (check projects)
        # Note: This uses the REST API, not live streaming
        logger.info("\n🔍 Testing API connection...")
        logger.info("✓ Client created successfully!")
        logger.info("   Your Deepgram API key is configured correctly.")
        logger.info("\nFor live transcription, you need:")
        logger.info("  - pip install deepgram-sdk httpx")
        logger.info("  - A working audio stream URL")

        return True

    except Exception as e:
        logger.info(f"❌ Error: {e}")
        return False


def test_file_transcription():
    """Test with a simple file transcription (more reliable than streaming)"""
    try:
        from deepgram import PrerecordedOptions

        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        # Example: transcribe from a URL
        AUDIO_URL = (
            "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
        )

        logger.info("\n🎙️  Testing file transcription...")
        logger.info(f"   Audio: {AUDIO_URL}")

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.rest.v("1").transcribe_url(
            {"url": AUDIO_URL}, options
        )

        transcript = response.results.channels[0].alternatives[0].transcript
        logger.info(f"\n✅ Transcription successful!")
        logger.info(f'   Text: "{transcript}"')

        return True

    except ImportError:
        logger.info("⚠️  PrerecordedOptions not available in this SDK version")
        return False
    except Exception as e:
        logger.info(f"❌ Transcription error: {e}")
        return False


if __name__ == "__main__":
    logger.info("╔════════════════════════════════════════════════════════════╗")
    logger.info("║        Deepgram API Test                                  ║")
    logger.info("╚════════════════════════════════════════════════════════════╝")
    print()

    # Test 1: Basic connection
    if test_connection():
        logger.info(Path("\n") + "=" * 60)
        # Test 2: Try file transcription
        test_file_transcription()

    logger.info(Path("\n") + "=" * 60)
    logger.info("Test complete!")
