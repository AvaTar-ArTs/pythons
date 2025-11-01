"""
Youtube Generate Speech With Curl

This module provides functionality for youtube generate speech with curl.

Author: Auto-generated
Date: 2025-11-01
"""

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
