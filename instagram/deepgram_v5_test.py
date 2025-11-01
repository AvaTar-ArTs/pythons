
import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""Deepgram SDK v5 Test - Uses current API"""

import os
import sys
from pathlib import Path

# Get API key from environment
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

if not DEEPGRAM_API_KEY:
    logger.info("❌ DEEPGRAM_API_KEY not found in environment")
    logger.info("   Run: source ~/.env.d/loader.sh")
    sys.exit(1)

logger.info("╔════════════════════════════════════════════════════════════╗")
logger.info("║        Deepgram API Key Test (SDK v5.x)                   ║")
logger.info("╚════════════════════════════════════════════════════════════╝\n")
logger.info(f"Testing API key: {DEEPGRAM_API_KEY[:10]}...\n")

try:
    from deepgram import DeepgramClient, PrerecordedOptions

    # Initialize client with API key from environment
    client = DeepgramClient(api_key=DEEPGRAM_API_KEY)

    logger.info("✓ DeepgramClient initialized\n")

    # Test with a remote audio file
    logger.info("🎙️  Testing transcription with sample audio...")

    AUDIO_URL = {
        "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
    }

    # Configure transcription options
    options = PrerecordedOptions(
        model="nova-2",
        smart_format=True,
    )

    logger.info("   Sending request to Deepgram...")

    # Perform transcription
    response = client.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)

    # Extract transcript
    transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]

    logger.info(f"\n✅ SUCCESS!\n")
    logger.info(f"Transcript: \"{transcript}\Path("\n"))
    logger.info("="*60)
    logger.info("🎉 Your Deepgram API key is working correctly!")
    logger.info("="*60)

except ImportError as e:
    logger.info(f"❌ Import error: {e}")
    logger.info("\n📦 Install required package:")
    logger.info("   pip install --upgrade deepgram-sdk")
    sys.exit(1)

except KeyError as e:
    logger.info(f"❌ Response format error: {e}")
    logger.info("\n⚠️  API returned unexpected format. Response:")
    logger.info(response)
    sys.exit(1)

except Exception as e:
    logger.info(f"❌ API Error: {e}\n")
    logger.info("This could mean:")
    logger.info("  1. ❌ API key is invalid or expired")
    logger.info("  2. 🔑 Get new key: https://console.deepgram.com/")
    logger.info("  3. 💳 Account may need credits or verification")
    logger.info("  4. 🌐 Network/connectivity issue")
    sys.exit(1)
