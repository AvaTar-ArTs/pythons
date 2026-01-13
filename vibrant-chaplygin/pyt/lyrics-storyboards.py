from openai import OpenAI

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

from dotenv import load_dotenv

# Load environment variables from .env
# load_dotenv()  # Now using ~/.env.d/


# Function to transcribe audio using OpenAI Whisper
def transcribe_audio(file_path):
    """transcribe_audio function."""

    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcribe("whisper-1", audio_file)
        return transcript.text

    # Function to analyze the transcript using GPT
    """analyze_text function."""


def analyze_text(text):
    response = client.chat.completions.create(
        model="gpt-4o",
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

    audio_file_path = sys.argv[1]
    output_transcript_path = sys.argv[2]
    output_analysis_path = sys.argv[3]

    # Step 1: Transcribe the audio file
    transcript = transcribe_audio(audio_file_path)
    with open(output_transcript_path, "w") as f:
        f.write(transcript)
    logger.info(f"Transcription completed and saved to: {output_transcript_path}")

    # Step 2: Analyze the transcription
    analysis = analyze_text(transcript)
    with open(output_analysis_path, "w") as f:
        f.write(analysis)
    logger.info(f"Analysis completed and saved to: {output_analysis_path}")
