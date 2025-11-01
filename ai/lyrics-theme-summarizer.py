"""
Lyrics Theme Summarizer

This module provides functionality for lyrics theme summarizer.

Author: Auto-generated
Date: 2025-11-01
"""

import openai
import os
from dotenv import load_dotenv

# Constants
CONSTANT_150 = 150


# Load environment variables from .env
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def analyze_text(text):
    """analyze_text function."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ensure you're using a chat model like gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes song lyrics."},
            {
                "role": "user",
                "content": f"Analyze the following song transcript and extract the main themes, emotions, and keywords: {text}",
            },
        ],
        max_tokens=CONSTANT_150,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()


if __name__ == "__main__":
    import sys

    transcript_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(transcript_file, "r") as f:
        transcript = f.read()

    analysis = analyze_text(transcript)
    with open(output_file, "w") as f:
        f.write(analysis)
