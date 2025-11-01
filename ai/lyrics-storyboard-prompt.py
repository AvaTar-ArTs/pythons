"""
Lyrics Storyboard Prompt Cli

This module provides functionality for lyrics storyboard prompt cli.

Author: Auto-generated
Date: 2025-11-01
"""

from openai import OpenAI

# Constants
CONSTANT_300 = 300


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# Function to analyze the transcript using GPT
def analyze_text(text):
    """analyze_text function."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI expert in narrative-driven image generation for DALL-E. Your goal is to analyze song transcripts to extract themes, emotions, key objects, and visual styles that will help create dynamic, vibrant images for visual storytelling.",
            },
            {
                "role": "user",
                "content": f"Analyze the following song transcript to extract: (1) main themes, (2) emotions, (3) key objects or characters for the images, (4) suggested lighting and color schemes, and (5) a recommended transition from one image to the next: {text}",
            },
        ],
        max_tokens=CONSTANT_300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    import sys

    transcript_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(transcript_file, "r") as f:
        transcript = f.read()

    analysis = analyze_text(transcript)
    with open(output_file, "w") as f:
        f.write(analysis)
