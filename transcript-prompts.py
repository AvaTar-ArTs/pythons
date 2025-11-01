"""
Analyze Mp3 Transcript Prompts Code

This module provides functionality for analyze mp3 transcript prompts code.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1000 = 1000


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

from dotenv import load_dotenv

# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
env_path = Path("/Users/steven/.env")
load_dotenv(dotenv_path=env_path)

# Directory pathsp
AUDIO_DIR = Path(
    "/Users/steven/Music/NocTurnE-meLoDieS/mp3"
)  # Directory containing MP3 files
TRANSCRIPT_DIR = Path(
    "/Users/steven/Music/NocTurnE-meLoDieS/song-video/analysis-transcript"
)  # Directory to save transcripts
ANALYSIS_DIR = Path(
    "/Users/steven/Music/NocTurnE-meLoDieS/song-video/analysis-transcript"
)  # Directory to save the analysis files

# Create output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Function to transcribe audio using OpenAI's Whisper model
def transcribe_audio(file_path):
    """transcribe_audio function."""

    try:
        with open(file_path, "rb") as audio_file:
            transcript_data = client.audio.transcribe(
                "whisper-1", audio_file, response_format="verbose_json"
            )

            # Build the transcript with timestamps
            transcript_with_timestamps = []
            for segment in transcript_data.segments:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]
                transcript_with_timestamps.append(
                    f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
                )

            return Path("\n").join(transcript_with_timestamps)
    except Exception as e:
        logger.info(f"Error transcribing {file_path}: {e}")
        return None

    # Helper function to format timestamps
    """format_timestamp function."""


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

    """analyze_text_for_section function."""


# Function to analyze the text using OpenAI's GPT model
def analyze_text_for_section(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a language and music expert. Your goal is to deeply analyze song lyrics to identify the core context, emotional content, and meaning. Pay attention to the emotional tone, the narrative arc, and any underlying themes or messages that the artist is conveying.",
                },
                {
                    "role": "user",
                    "content": f"Analyze the following song transcript and provide a detailed analysis of: (1) the central themes and meaning, (2) the emotional tone of the song, (3) the intent of the artist, (4) any significant metaphors, symbols, or imagery used, and (5) how these elements come together to create an overall emotional and narrative experience: {text}",
                },
            ],
            max_tokens=CONSTANT_1000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.info(f"Error analyzing text: {e}")
        return None

    """process_audio_directory function."""


# Main function to process audio files in the directory
def process_audio_directory(audio_dir):
    for root, _, files in os.walk(audio_dir):
        for filename in files:
            if filename.lower().endswith(".mp3"):
                audio_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]

                # Step 1: Transcribe the audio file
                transcript = transcribe_audio(audio_file)
                if transcript:
                    transcript_file_path = os.path.join(
                        TRANSCRIPT_DIR, f"{filename_no_ext}_transcript.txt"
                    )
                    with open(transcript_file_path, "w") as f:
                        f.write(transcript)
                    print(
                        f"Transcription saved for {filename_no_ext} at {transcript_file_path}"
                    )

                    # Step 2: Analyze the transcript
                    analysis = analyze_text_for_section(transcript)
                    if analysis:
                        analysis_file_path = os.path.join(
                            ANALYSIS_DIR, f"{filename_no_ext}_analysis.txt"
                        )
                        with open(analysis_file_path, "w") as f:
                            f.write(analysis)
                        print(
                            f"Analysis saved for {filename_no_ext} at {analysis_file_path}"
                        )
                else:
                    logger.info(
                        f"Skipping {filename_no_ext} due to transcription error."
                    )


if __name__ == "__main__":
    process_audio_directory(AUDIO_DIR)
