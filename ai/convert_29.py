"""
Convert 29

This module provides functionality for convert 29.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import subprocess

from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1500 = 1500


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv

# Load environment variables from .env
env_path = os.path.expanduser("~/.env")
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key

if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")


# Helper to format timestamps
def format_timestamp(seconds):
    """format_timestamp function."""

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


# Function to convert MP4 to MP3
    """convert_mp4_to_mp3 function."""

def convert_mp4_to_mp3(mp4_path):
    mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"
    if os.path.exists(mp3_path):
        return mp3_path  # Skip conversion if already exists

    try:
        subprocess.run(
            ["ffmpeg", "-i", mp4_path, "-q:a", "0", "-map", "a", mp3_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        logger.info(f"Converted {os.path.basename(mp4_path)} to MP3.")
        return mp3_path
    except Exception as e:
        logger.info(f"Error converting {mp4_path} to MP3: {e}")
        return None


    """split_audio function."""

# Function to split audio into smaller chunks
def split_audio(file_path, segment_length=CONSTANT_300):
    output_dir = os.path.join(os.path.dirname(file_path), "segments")
    os.makedirs(output_dir, exist_ok=True)
    file_name_no_ext = os.path.splitext(os.path.basename(file_path))[0]

    command = [
        "ffmpeg",
        "-i",
        file_path,
        "-f",
        "segment",
        "-segment_time",
        str(segment_length),
        "-c",
        "copy",
        os.path.join(output_dir, f"{file_name_no_ext}_%03d.mp3"),
    ]
    subprocess.run(command, check=True)
    return sorted(
        [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".mp3")
        ]
    )

    """transcribe_file function."""


# Function to transcribe audio or video
def transcribe_file(file_path):
    try:
        with open(file_path, "rb") as media_file:
            transcript_data = client.audio.transcribe(
                model="whisper-1", file=media_file, response_format="verbose_json"
            )
        transcript_with_timestamps = [
            f"{format_timestamp(segment['start'])} -- {format_timestamp(segment['end'])}: {segment['text']}"
            for segment in transcript_data.segments
        ]
        return Path("\n").join(transcript_with_timestamps)
    except Exception as e:
        logger.info(f"Error transcribing {file_path}: {e}")
        return None
    """analyze_text_for_section function."""



# Function to analyze text
def analyze_text_for_section(text, filename_no_ext):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed "
                        "and structured analysis of video and audio content, focusing on themes, emotional tone, narrative structure, "
                        "artistic intent, and audience impact. Analyze how visuals and audio interact to convey meaning and evoke emotions."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following transcript for {filename_no_ext}. Provide a detailed analysis covering:\n\n"
                        "1. **Central Themes and Messages**\n"
                        "2. **Emotional Tone**\n"
                        "3. **Narrative Arc**\n"
                        "4. **Creator's Intent**\n"
                        "5. **Storytelling Techniques**\n"
                        "6. **Audience Engagement and Impact**\n\n"
                        f"Transcript:\n{text}"
                    ),
                },
            ],
            max_tokens=CONSTANT_1500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.info(f"Error analyzing transcript for {filename_no_ext}: {e}")
    """process_media_directory function."""

        return None


# Main function to process audio and video files
def process_media_directory(media_dir):
    transcript_dir = os.path.join(media_dir, "transcript")
    analysis_dir = os.path.join(media_dir, "analysis")
    os.makedirs(transcript_dir, exist_ok=True)
    os.makedirs(analysis_dir, exist_ok=True)

    for root, _, files in os.walk(media_dir):
        for filename in files:
            if filename.lower().endswith((".mp3", ".mp4")):
                media_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]

                if filename.lower().endswith(".mp4"):
                    media_file = convert_mp4_to_mp3(media_file)
                    if not media_file:
                        continue

                # Split large files
                if os.path.getsize(media_file) > 25 * CONSTANT_1024 * CONSTANT_1024:
                    segments = split_audio(media_file)
                else:
                    segments = [media_file]

                full_transcript = ""
                for segment in segments:
                    transcript = transcribe_file(segment)
                    if transcript:
                        full_transcript += transcript + Path("\n")

                if full_transcript:
                    transcript_path = os.path.join(
                        transcript_dir, f"{filename_no_ext}_transcript.txt"
                    )
                    with open(transcript_path, "w") as f:
                        f.write(full_transcript)
                    logger.info(f"Transcription saved at {transcript_path}")

                    analysis = analyze_text_for_section(
                        full_transcript, filename_no_ext
                    )
                    if analysis:
                        analysis_path = os.path.join(
                            analysis_dir, f"{filename_no_ext}_analysis.txt"
                        )
                        with open(analysis_path, "w") as f:
                            f.write(analysis)
                        logger.info(f"Analysis saved at {analysis_path}")


if __name__ == "__main__":
    media_dir = input("Enter the directory path containing MP3/MP4 files: ").strip()
    if not os.path.isdir(media_dir):
        logger.info(f"Invalid directory: {media_dir}")
    else:
        process_media_directory(media_dir)
