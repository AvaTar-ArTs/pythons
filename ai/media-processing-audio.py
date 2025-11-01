"""
Media Processing Audio Openai Analyzer

This module provides functionality for media processing audio openai analyzer.

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
CONSTANT_1500 = 1500


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv

# Load environment variables from .env
env_path = os.path.expanduser("~/.env")
# Update the path if needed
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key

# Error checking for OpenAI API key
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")


# Helper to format timestamps
def format_timestamp(seconds):
    """Convert seconds into the format MM:SS."""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{int(seconds):02d}"


# Function to transcribe audio or video
def transcribe_file(file_path):
    """Transcribe audio or video using OpenAI Whisper."""
    with open(file_path, "rb") as media_file:
        transcript_data = client.audio.transcribe(model="whisper-1", file=media_file, response_format="verbose_json")

    # Build the transcript with timestamps
    transcript_with_timestamps = []
    for segment in transcript_data.segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        transcript_with_timestamps.append(f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}")

    return Path("\n").join(transcript_with_timestamps)


# Function to analyze text
def analyze_text_for_section(text, section_name):
    """Analyze the transcribed text using OpenAI GPT."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis "
                    "of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. "
                    "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
                    "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following transcript and associated content for {text}. Provide a comprehensive analysis covering:\n\n"
                    "1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed. How do they connect to the broader narrative?\n"
                    "2. **Emotional Tone**: What emotions are evoked, and how are they conveyed through the combination of audio and visuals?\n"
                    "3. **Narrative Arc**: Describe how this section contributes to the overall story or progression. Are there key turning points or developments?\n"
                    "4. **Creator's Intent**: What is the likely purpose or message the creator is trying to communicate? Is it to entertain, inform, inspire, or persuade?\n"
                    "5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable metaphors, symbols, or visual/audio motifs that enhance the narrative or emotional impact.\n"
                    "6. **Storytelling Techniques**: Identify specific techniques used, such as pacing, transitions, visual effects, or sound design. How do they contribute to the overall experience?\n"
                    "7. **Interplay Between Visuals and Audio**: Analyze how visuals and audio work together to create meaning and impact. Are there any standout moments?\n"
                    "8. **Audience Engagement and Impact**: Evaluate how effectively the content captures and holds attention. How well does it resonate with its intended audience?\n"
                    "9. **Overall Effectiveness**: Summarize how these elements combine to create a cohesive, immersive, and impactful experience for the viewer.\n\n"
                    f"Transcript:\n{text}"
                ),
            },
        ],
        max_tokens=CONSTANT_1500,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# Function to process audio and video files
def process_media_directory(media_dir):
    """Process MP3 and MP4 files in the specified directory."""
    # Auto-create transcript and analysis folders within the source directory
    transcript_dir = os.path.join(media_dir, "transcript")
    analysis_dir = os.path.join(media_dir, "analysis")
    os.makedirs(transcript_dir, exist_ok=True)
    os.makedirs(analysis_dir, exist_ok=True)

    # Process media files in the directory
    for root, _, files in os.walk(media_dir):
        for filename in files:
            if filename.lower().endswith((".mp3", ".mp4")):
                media_file = os.path.join(root, filename)
                file_name_no_ext = os.path.splitext(filename)[0]

                logger.info(f"Processing file: {filename}")

                # Step 1: Transcribe the media file
                try:
                    transcript = transcribe_file(media_file)
                    transcript_file_path = os.path.join(transcript_dir, f"{file_name_no_ext}_transcript.txt")
                    with open(transcript_file_path, "w") as f:
                        f.write(transcript)
                    logger.info(f"Transcription saved at {transcript_file_path}")
                except Exception as e:
                    logger.info(f"Error transcribing {filename}: {e}")
                    continue

                # Step 2: Analyze the transcript
                try:
                    analysis = analyze_text_for_section(transcript, file_name_no_ext)
                    analysis_file_path = os.path.join(analysis_dir, f"{file_name_no_ext}_analysis.txt")
                    with open(analysis_file_path, "w") as f:
                        f.write(analysis)
                    logger.info(f"Analysis saved at {analysis_file_path}")
                except Exception as e:
                    logger.info(f"Error analyzing {filename}: {e}")


if __name__ == "__main__":
    # Prompt for the media directory
    media_dir = input("Enter the path to the directory containing MP3/MP4 files: ").strip()
    if not os.path.isdir(media_dir):
        logger.info(f"Invalid directory: {media_dir}")
        exit(1)

    # Process the media files in the provided directory
    process_media_directory(media_dir)
