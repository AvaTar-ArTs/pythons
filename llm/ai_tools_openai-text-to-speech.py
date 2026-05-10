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

import csv
import os
import subprocess

import logging

logger = logging.getLogger(__name__)


def generate_speech_with_curl(question_text, question_number, api_key):
    """generate_speech_with_curl function."""

    curl_command = [
        "curl",
        "https://api.openai.com/v1/audio/speech",
        "-H",
        f"Authorization: Bearer {api_key}",
        "-H",
        "Content-Type: application/json",
        "-d",
        f"""{{
            "model": "tts-1",
            "input": "{question_text}",
            "voice": "alloy"
        }}""",
        "--output",
        f"speech/question_{question_number}.mp3",
    ]

    subprocess.run(curl_command)

    """main function."""


def main(csv_path, api_key):
    # Ensure the output directory exists
    os.makedirs("speech", exist_ok=True)

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            question_text = row["Question"].replace('"', '\\"')  # Escape double quotes
            logger.info(f"Generating speech for question {i}")
            generate_speech_with_curl(question_text, i, api_key)
            logger.info(f"Generated speech for question {i}")


if __name__ == "__main__":
    csv_path = str(Path.home()) + "/Music/quiz-talk/Gtrivia - Sheet1.csv"  # Update this to the path of your CSV file
    api_key = os.getenv("OPENAI_API_KEY")  # Get API key from environment
    main(csv_path, api_key)
