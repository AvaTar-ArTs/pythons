#!/usr/bin/env python3
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

import os
import sys
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load API keys from ~/.env.d/
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)

# Load .env first
load_dotenv(os.path.expanduser("~/.env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ OPENAI_API_KEY missing. Ensure ~/.env or environment has it.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

# Path to a small MP3 file for testing
# User has "Music/nocTurneMeLoDieS/imperfection313.mp3"
# Or a smaller one for quick test: Music/nocTurneMeLoDieS/Chamber_of_Silence013.mp3 (0:13)
TEST_AUDIO_FILE = Path("/Users/steven/Music/nocTurneMeLoDieS/Chamber_of_Silence013.mp3")

def run_test_transcription():
    print(f"Testing transcription with: {TEST_AUDIO_FILE}")

    if not TEST_AUDIO_FILE.exists():
        print(f"Test file not found: {TEST_AUDIO_FILE}. Please ensure it exists.")
        sys.exit(1)

    try:
        # Check client.audio attributes
        print("\n--- Inspecting client.audio ---")
        print(f"Type of client.audio: {type(client.audio)}")
        print(f"Attributes of client.audio: {dir(client.audio)}")
        print("-----------------------------")

        with open(TEST_AUDIO_FILE, "rb") as audio_file:
            print("Attempting client.audio.transcriptions.create...")
            # Use client.audio.transcriptions.create for speech-to-text
            # and client.audio.speech.create for text-to-speech
            # The original script used client.audio.transcribe which is wrong.
            # It should be client.audio.transcriptions.create for OpenAI API v1.x
            transcript_data = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
            print("\n✅ Transcription successful in test script!")
            print("Partial Transcript:", transcript_data.text[:100], "...")
            print("Full response type:", type(transcript_data))

    except AttributeError as e:
        print(f"❌ AttributeError during transcription: {e}")
        print("This indicates a problem with the OpenAI client object or its version.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_test_transcription()
