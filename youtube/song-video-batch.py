"""
Song Video Batch Analyzer

This module provides functionality for song video batch analyzer.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import openai
from dotenv import load_dotenv
from termcolor import colored
from tqdm import tqdm

# Constants
CONSTANT_1000 = 1000


# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
env_path = "~/.env"
load_dotenv(dotenv_path=env_path)

# Directory paths
AUDIO_DIR = Path(
    "/Users/steven/Music/NocTurnE-meLoDieS/song-video/mp3"
)  # Directory containing MP3 files
TRANSCRIPT_DIR = Path(
    "/Users/steven/Music/NocTurnE-meLoDieS/Discography/Audio/transcript"
)  # Directory to save transcripts
ANALYSIS_DIR = Path(
    "/Users/steven/Music/NocTurnE-meLoDieS/Discography/Audio/analysis"
)  # Directory to save the analysis files

# Create output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    """transcribe_audio function."""

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

    # Helper function to format timestamps
    """format_timestamp function."""


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

    """analyze_text_for_section function."""


def analyze_text_for_section(text, section_number):
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
                transcript_file_path = os.path.join(
                    TRANSCRIPT_DIR, f"{filename_no_ext}_transcript.txt"
                )
                with open(transcript_file_path, "w") as f:
                    f.write(transcript)
                print(
                    f"Transcription saved for {filename_no_ext} at {transcript_file_path}"
                )

                # Step 2: Analyze the segment's transcript
                analysis = analyze_text_for_section(transcript, filename_no_ext)
                analysis_file_path = os.path.join(
                    ANALYSIS_DIR, f"{filename_no_ext}_analysis.txt"
                )
                with open(analysis_file_path, "w") as f:
                    f.write(analysis)
                logger.info(
                    f"Analysis saved for {filename_no_ext} at {analysis_file_path}"
                )


if __name__ == "__main__":
    process_audio_directory(AUDIO_DIR)
