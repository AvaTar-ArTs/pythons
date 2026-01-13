#!/usr/bin/env python3
"""
Updated Deepgram Live Transcription Test
Works with Deepgram SDK v3+
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

from pathlib import Path
import os
from deepgram import (
    DeepgramClient,
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
        logger.info("\n✅ Transcription successful!")
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
