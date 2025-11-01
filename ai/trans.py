"""
Ana Trans

This module provides functionality for ana trans.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import openai
import os
import subprocess
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1500 = 1500


# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
load_dotenv(Path("/Users/steven/.env"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for directory paths
project_root = input("Please enter the project root directory path: ").strip()

# Directory paths based on user input
MEDIA_DIR = os.path.join(project_root, "Media")  # Directory containing media files
TRANSCRIPT_DIR = os.path.join(MEDIA_DIR, "transcript")  # Directory to save transcripts
ANALYSIS_DIR = os.path.join(MEDIA_DIR, "analysis")  # Directory to save the analysis files

# Create output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Function to split the media into sections using ffmpeg
def split_media_to_segments(media_path, segment_length=CONSTANT_300):
    """Split the media into smaller segments."""
    media_name, media_ext = os.path.splitext(os.path.basename(media_path))
    output_dir = os.path.join(MEDIA_DIR, media_name + "_segments")
    os.makedirs(output_dir, exist_ok=True)

    # Using ffmpeg to split the media into smaller segments
    command = [
        "ffmpeg",
        "-i",
        media_path,
        "-c",
        "copy",
        "-map",
        "0",
        "-segment_time",
        str(segment_length),
        "-f",
        "segment",
        "-reset_timestamps",
        "1",
        os.path.join(output_dir, media_name + "_%03d" + media_ext),
    ]
    subprocess.run(command)

    # List the generated segments
    segments = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(media_ext)])
    return segments


# Function to transcribe media segments using Whisper
def transcribe_media_segment(file_path):
    """transcribe_media_segment function."""

    with open(file_path, "rb") as media_file:
        transcript_data = openai.Audio.transcribe("whisper-1", media_file, response_format="verbose_json")

        # Build the transcript with timestamps
        transcript_with_timestamps = []
        for segment in transcript_data["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            transcript_with_timestamps.append(f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}")

        return Path("\n").join(transcript_with_timestamps)

    # Helper function to format timestamps
    """format_timestamp function."""


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

    """analyze_text_for_section function."""


# Function to analyze the transcript for a section
def analyze_text_for_section(text, section_number):
    prompt = (
        f"Analyze the following transcript and associated content for section {section_number}. "
        "Provide a comprehensive analysis covering:\n"
        "1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed. "
        "How do they connect to the broader narrative?\n"
        "2. **Emotional Tone**: What emotions are evoked, and how are they conveyed through the combination of audio and visuals?\n"
        "3. **Narrative Arc**: Describe how this section contributes to the overall story or progression. "
        "Are there key turning points or developments?\n"
        "4. **Creator’s Intent**: What is the likely purpose or message the creator is trying to communicate? "
        "Is it to entertain, inform, inspire, or persuade?\n"
        "5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable metaphors, symbols, or visual/audio motifs "
        "that enhance the narrative or emotional impact.\n"
        "6. **Storytelling Techniques**: Identify specific techniques used, such as pacing, transitions, visual effects, or sound design. "
        "How do they contribute to the overall experience?\n"
        "7. **Interplay Between Visuals and Audio**: Analyze how visuals and audio work together to create meaning and impact. "
        "Are there any standout moments?\n"
        "8. **Audience Engagement and Impact**: Evaluate how effectively the content captures and holds attention. "
        "How well does it resonate with its intended audience?\n"
        "9. **Overall Effectiveness**: Summarize how these elements combine to create a cohesive, immersive, and impactful experience for the viewer.\n\n"
        f"Transcript:\n{text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=CONSTANT_1500,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()

    """process_media_by_section function."""


# Main function to process large media files in sections
def process_media_by_section(media_file, segment_length=CONSTANT_300):
    # Split media into smaller segments
    segments = split_media_to_segments(media_file, segment_length)

    # Process each segment
    for index, segment in enumerate(segments):
        section_number = index + 1
        logger.info(f"Processing Section {section_number}: {segment}")

        # Step 1: Transcribe the segment
        transcript = transcribe_media_segment(segment)
        transcript_file_path = os.path.join(TRANSCRIPT_DIR, f"section_{section_number}_transcript.txt")
        with open(transcript_file_path, "w") as f:
            f.write(transcript)
        logger.info(f"Transcription saved for Section {section_number} at {transcript_file_path}")

        # Step 2: Analyze the segment's transcript
        analysis = analyze_text_for_section(transcript, section_number)
        analysis_file_path = os.path.join(ANALYSIS_DIR, f"section_{section_number}_analysis.txt")
        with open(analysis_file_path, "w") as f:
            f.write(analysis)
        logger.info(f"Analysis saved for Section {section_number} at {analysis_file_path}")


if __name__ == "__main__":
    import sys

# Suggested Improvements:
# 1. Error Handling: Add try-except blocks around file operations and subprocess calls to handle potential errors gracefully.
# 2. Logging: Implement logging instead of print statements for better control over output and debugging.
# 3. Configuration: Consider using a configuration file or command-line arguments for setting paths and parameters, making the script more flexible.
# 4. Parallel Processing: Use concurrent processing for transcribing and analyzing segments to improve performance.
# 5. Code Reusability: Extract repeated code patterns into separate functions to enhance code reusability and readability.
# 6. API Key Security: Ensure the API key is securely managed and not hardcoded or exposed in the code.
