"""
Story Section Gpt 2

This module provides functionality for story section gpt 2.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_2000 = 2000

#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/core_analysis/story-section-gpt.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/core_analysis/story-section-gpt.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load environment variables from .env (ensure your OPENAI_API_KEY is stored here)
env_path = Path("/Users/steven/.env")
load_dotenv(dotenv_path=env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define a simple config dictionary. You can expand this as needed.
config = {"base_dir": ""}  # Leave blank to prompt for base directory

# Prompt for base directory if not set in config; default to current directory if input is empty
if not config.get("base_dir"):
    base_dir_input = input(
        "Enter the base directory containing your media files (leave blank to use current directory): "
    ).strip()
    config["base_dir"] = base_dir_input if base_dir_input else os.getcwd()

# Verify that the directory exists
if not os.path.isdir(config["base_dir"]):
    logging.error(f"Directory '{config['base_dir']}' does not exist. Exiting.")
    sys.exit(1)

# Define BASE_DIR using the config value
BASE_DIR = os.path.abspath(config["base_dir"])

# Define output directories relative to BASE_DIR
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transscript")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")

# Auto-create the output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Helper function to format timestamps
def format_timestamp(seconds):
    """format_timestamp function."""

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

    # Function to transcribe audio from a file using Whisper
    """transcribe_audio function."""


def transcribe_audio(file_path):
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

    """analyze_text_for_section function."""


# Function to analyze the transcript using ChatGPT with a more in-depth prompt
def analyze_text_for_section(text, section_number):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in multimedia analysis and storytelling. Your task is to provide a highly detailed and in-depth analysis of video and audio content. Your analysis should examine themes, emotional tone, narrative structure, technical production, artistic intent, and audience impact. Consider every nuance and provide insights into how audio and visual elements, editing, and special effects contribute to the overall experience."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Provide an in-depth analysis for {section_number}. Please address the following aspects:\n"
                    "1. **Central Themes and Messages**: What are the primary themes, and how complex are the underlying messages?\n"
                    "2. **Emotional Tone**: Describe the range of emotions conveyed. How do the audio and visual elements interact to evoke these emotions?\n"
                    "3. **Narrative Arc and Structure**: Explain how this section fits into the overall narrative. Identify key turning points and their significance.\n"
                    "4. **Creator’s Intent and Vision**: What deeper message or purpose might the creator be conveying? How do multimedia elements support this intent?\n"
                    "5. **Technical and Artistic Elements**: Analyze the use of cinematography, editing, sound design, and any special effects. How do these technical choices enhance the storytelling?\n"
                    "6. **Audience Impact and Engagement**: Evaluate how effectively the content captures and maintains audience attention. What makes it engaging?\n"
                    "\nTranscript:\n" + text
                ),
            },
        ],
        max_tokens=CONSTANT_2000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

    """process_media_directory function."""


# Main function to process MP4 files in the directory
def process_media_directory(media_dir):
    for root, _, files in os.walk(media_dir):
        for filename in files:
            if filename.lower().endswith(".mp4"):
                file_path = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]

                # Step 1: Transcribe the media file (MP4)
                logger.info(f"Transcribing {filename}...")
                transcript = transcribe_audio(file_path)
                transcript_file_path = os.path.join(
                    TRANSCRIPT_DIR, f"{filename_no_ext}_transcript.txt"
                )
                with open(transcript_file_path, "w") as f:
                    f.write(transcript)
                print(
                    f"Transcription saved for {filename_no_ext} at {transcript_file_path}"
                )

                # Step 2: Analyze the transcript
                logger.info(f"Analyzing transcript for {filename}...")
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
    process_media_directory(BASE_DIR)
