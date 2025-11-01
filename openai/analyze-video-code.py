"""
Mp4 Mp3 Analyze Code

This module provides functionality for mp4 mp3 analyze code.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import logging
import os
import subprocess
import sys

import openai
from dotenv import load_dotenv

# Constants
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000


# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load environment variables from .env (ensure your OPENAI_API_KEY is stored here)
env_path = Path("/Users/steven/.env")
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Maximum allowed file size (25 MB)
MAX_SIZE = 25 * CONSTANT_1024 * CONSTANT_1024  # 25 MB in bytes

# Determine base directory from command-line argument or prompt
if len(sys.argv) > 1:
    base_dir = sys.argv[1]
else:
    base_dir = (
        input(
            "Enter the base directory containing your media files (leave blank to use current directory): "
        ).strip()
        or os.getcwd()
    )

if not os.path.isdir(base_dir):
    logging.error(f"Directory '{base_dir}' does not exist. Exiting.")
    sys.exit(1)

BASE_DIR = os.path.abspath(base_dir)
logging.info(f"Processing directory: {BASE_DIR}")

# Define output directories relative to BASE_DIR
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "trans")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Helper function to format timestamps (MM:SS)
def format_timestamp(seconds):
    """format_timestamp function."""

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

    # Function to transcribe audio from an MP4 file using OpenAI's Whisper API
    """transcribe_audio function."""


def transcribe_audio(file_path):
    # If file exceeds the MAX_SIZE limit, convert it to a lower-bitrate version
    if os.path.getsize(file_path) > MAX_SIZE:
        logging.info(
            f"File {file_path} exceeds {MAX_SIZE} bytes. Converting to lower bitrate."
        )
        filename_no_ext = os.path.splitext(os.path.basename(file_path))[0]
        converted_file = os.path.join(
            os.path.dirname(file_path), f"{filename_no_ext}_converted.mp4"
        )
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    file_path,
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "64k",
                    converted_file,
                ],
                check=True,
            )
            file_path = converted_file
            logging.info(f"Converted file created: {converted_file}")
        except Exception as e:
            logging.error(f"Conversion failed for {file_path}: {e}")
            return None

    with open(file_path, "rb") as audio_file:
        transcript_data = openai.Audio.transcribe(
            "whisper-1", audio_file, response_format="verbose_json"
        )
    transcript_lines = []
    for segment in transcript_data.segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        transcript_lines.append(
            f"{format_timestamp(start)} -- {format_timestamp(end)}: {text}"
        )
    return Path("\n").join(transcript_lines)

    """analyze_text_for_section function."""


# Function to analyze the transcript using ChatGPT with a detailed prompt
def analyze_text_for_section(text, section_number):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in multimedia analysis and storytelling. Provide a highly detailed analysis of video and audio content. "
                    "Examine themes, emotional tone, narrative structure, technical production, artistic intent, and audience impact."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Provide an in-depth analysis for {section_number}. Address the following aspects:\n"
                    "1. Central Themes and Messages: What are the primary themes and how complex are the underlying messages?\n"
                    "2. Emotional Tone: Describe how the audio and visuals interact to evoke emotions.\n"
                    "3. Narrative Structure: Explain how this segment fits into the overall narrative and identify key turning points.\n"
                    "4. Creator's Intent: What deeper message or vision is being conveyed?\n"
                    "5. Technical & Artistic Elements: Evaluate the cinematography, editing, sound design, and special effects.\n"
                    "6. Audience Impact: How engaging is the content and what makes it compelling?\n"
                    "\nTranscript:\n" + text
                ),
            },
        ],
        max_tokens=CONSTANT_2000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

    """process_media_directory function."""


# Function to process all MP4 files recursively within the base directory
def process_media_directory(media_dir):
    for root, _, files in os.walk(media_dir):
        for filename in files:
            if filename.lower().endswith(".mp4"):
                file_path = os.path.join(root, filename)
                logging.info(f"Processing file: {file_path}")
                transcript = transcribe_audio(file_path)
                if transcript is None:
                    logging.error(f"Transcription failed for {file_path}. Skipping.")
                    continue

                # Save transcript file (using the file's base name)
                filename_no_ext = os.path.splitext(filename)[0]
                transcript_file_path = os.path.join(
                    TRANSCRIPT_DIR, f"{filename_no_ext}_transcript.txt"
                )
                with open(transcript_file_path, "w") as f:
                    f.write(transcript)
                logging.info(f"Transcript saved: {transcript_file_path}")

                # Analyze transcript
                analysis = analyze_text_for_section(transcript, filename_no_ext)
                analysis_file_path = os.path.join(
                    ANALYSIS_DIR, f"{filename_no_ext}_analysis.txt"
                )
                with open(analysis_file_path, "w") as f:
                    f.write(analysis)
                logging.info(f"Analysis saved: {analysis_file_path}")


if __name__ == "__main__":
    process_media_directory(BASE_DIR)
