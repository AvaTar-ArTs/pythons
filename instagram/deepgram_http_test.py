
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_401 = 401
CONSTANT_402 = 402

#!/usr/bin/env python3
"""
Deepgram API Test using direct HTTP requests
Tests if the API key is valid
"""

from pathlib import Path
import os
import sys
import json

try:
    import requests
except ImportError:
    logger.info("❌ requests library not found")
    logger.info("   Install: pip install requests")
    sys.exit(1)

# Get API key from environment
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

if not DEEPGRAM_API_KEY:
    logger.info("❌ DEEPGRAM_API_KEY not found in environment")
    logger.info("   Run: source ~/.env.d/loader.sh")
    sys.exit(1)

logger.info("╔════════════════════════════════════════════════════════════╗")
logger.info("║        Deepgram API Key Test (HTTP)                       ║")
logger.info("╚════════════════════════════════════════════════════════════╝\n")
logger.info(f"Testing API key: {DEEPGRAM_API_KEY[:10]}...\n")

# Test 1: Check API key with projects endpoint
logger.info("Test 1: Checking API key validity...")
headers = {
    "Authorization": f"Bearer {DEEPGRAM_API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.get(
        "https://api.deepgram.com/v1/projects",
        headers=headers,
        timeout=10
    )

    if response.status_code == CONSTANT_200:
        logger.info("✅ API key is VALID!\n")
        projects = response.json()
        logger.info(f"Projects found: {len(projects.get('projects', []))}")

    elif response.status_code == CONSTANT_401:
        logger.info("❌ API key is INVALID (CONSTANT_401 Unauthorized)\n")
        logger.info(f"Response: {response.text}\n")
        logger.info("Get a new key at: https://console.deepgram.com/")
        sys.exit(1)

    else:
        logger.info(f"⚠️  Unexpected response: HTTP {response.status_code}")
        logger.info(f"Response: {response.text}")

except requests.exceptions.RequestException as e:
    logger.info(f"❌ Network error: {e}")
    sys.exit(1)

# Test 2: Try a simple transcription
logger.info("\nTest 2: Testing transcription...")

audio_url = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"

payload = {
    "url": audio_url
}

params = {
    "model": "nova-2",
    "smart_format": "true"
}

try:
    response = requests.post(
        "https://api.deepgram.com/v1/listen",
        headers=headers,
        params=params,
        json=payload,
        timeout=30
    )

    if response.status_code == CONSTANT_200:
        result = response.json()
        transcript = result["results"]["channels"][0]["alternatives"][0]["transcript"]

        logger.info("✅ Transcription SUCCESSFUL!\n")
        logger.info(f"Transcript: \"{transcript}\Path("\n"))
        logger.info("="*60)
        logger.info("🎉 Your Deepgram API key is fully functional!")
        logger.info("="*60)

    elif response.status_code == CONSTANT_401:
        logger.info("❌ Authentication failed")
        logger.info("   Your API key may have limited permissions")

    elif response.status_code == CONSTANT_402:
        logger.info("⚠️  Payment required")
        logger.info("   Your account may need credits")
        logger.info("   Check: https://console.deepgram.com/billing")

    else:
        logger.info(f"❌ Transcription failed: HTTP {response.status_code}")
        logger.info(f"Response: {response.text}")

except requests.exceptions.RequestException as e:
    logger.info(f"❌ Network error: {e}")
    sys.exit(1)
except KeyError as e:
    logger.info(f"❌ Unexpected response format: {e}")
    logger.info(f"Response: {response.text}")
    sys.exit(1)
