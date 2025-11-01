"""
Ai Tools Whisper Vid Mp3 Transcribe Analyze 1

This module provides functionality for ai tools whisper vid mp3 transcribe analyze 1.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import subprocess

import openai
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1000 = 1000


# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Directory paths
VIDEO_DIR = Path(
    "/Users/steven/Movies/poject2025/Media"
)  # Directory containing MP4 files
TRANSCRIPT_DIR = Path(
    "/Users/steven/Movies/poject2025/Media/Mp4/transcript"
)  # Directory to save transcripts
ANALYSIS_DIR = Path(
    "/Users/steven/Movies/poject2025/Media/Mp4/analysis"
)  # Directory to save the analysis files

# Create output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)


# Function to split the video into sections using ffmpeg
def split_video_to_segments(video_path, segment_length=CONSTANT_300):
    """Split the video into smaller segments."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(VIDEO_DIR, video_name + "_segments")
    os.makedirs(output_dir, exist_ok=True)

    # Using ffmpeg to split the video into smaller segments
    command = [
        "ffmpeg",
        "-i",
        video_path,
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
        os.path.join(output_dir, video_name + "_%03d.mp4"),
    ]
    subprocess.run(command)

    # List the generated segments
    segments = sorted(
        [
            os.path.join(output_dir, f)
            for f in os.listdir(output_dir)
            if f.endswith(".mp4")
        ]
    )
    return segments


# Function to transcribe video segments using Whisper
def transcribe_video_segment(file_path):
    """transcribe_video_segment function."""

    with open(file_path, "rb") as video_file:
        transcript_data = openai.Audio.transcribe(
            "whisper-1", video_file, response_format="verbose_json"
        )

        # Build the transcript with timestamps
        transcript_with_timestamps = []
        for segment in transcript_data["segments"]:
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


# Function to analyze the transcript for a section
def analyze_text_for_section(text, section_number):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers ",
            },
            {
                "role": "user",
                "content": f"Analyze the following song transcript to extract: (1) main themeAnalyze the following transcript and associated content for {text}. Provide a comprehensive analysis covering:1. **Central Themes and Messages**: Identify the primary ideas or messages conveyed. How do they connect to the broader narrative?2. **Emotional Tone**: What emotions are evoked, and how are they conveyed through the combination of audio and visuals? 3. **Narrative Arc**: Describe how this section contributes to the overall story or progression. Are there key turning points or developments?\n4. **Creator’s Intent**: What is the likely purpose or message the creator is trying to communicate? Is it to entertain, inform, inspire, or persuade?\n5. **Significant Metaphors, Symbols, and Imagery**: Highlight notable metaphors, symbols, or visual/audio motifs that enhance the narrative or emotional impact.\n6. **Storytelling Techniques**: Identify specific techniques used, such as pacing, transitions, visual effects, or sound design. How do they contribute to the overall experience?\n7. **Interplay Between Visuals and Audio**: Analyze how visuals and audio work together to create meaning and impact. Are there any standout moments?\n8. **Audience Engagement and Impact**: Evaluate how effectively the content captures and holds attention. How well does it resonate with its intended audience?\n9. **Overall Effectiveness**: Summarize how these elements combine to create a cohesive, immersive, and impactful experience for the viewer.\n\nTranscript:\n{text}",
            },
        ],
        max_tokens=CONSTANT_1000,
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()

    """process_video_by_section function."""


# Main function to process large videos in sections
def process_video_by_section(video_file, segment_length=CONSTANT_300):
    # Split video into smaller segments
    segments = split_video_to_segments(video_file, segment_length)

    # Process each segment
    for index, segment in enumerate(segments):
        section_number = index + 1
        logger.info(f"Processing Section {section_number}: {segment}")

        # Step 1: Transcribe the segment
        transcript = transcribe_video_segment(segment)
        transcript_file_path = os.path.join(
            TRANSCRIPT_DIR, f"section_{section_number}_transcript.txt"
        )
        with open(transcript_file_path, "w") as f:
            f.write(transcript)
        logger.info(
            f"Transcription saved for Section {section_number} at {transcript_file_path}"
        )

        # Step 2: Analyze the segment's transcript
        analysis = analyze_text_for_section(transcript, section_number)
        analysis_file_path = os.path.join(
            ANALYSIS_DIR, f"section_{section_number}_analysis.txt"
        )
        with open(analysis_file_path, "w") as f:
            f.write(analysis)
        logger.info(
            f"Analysis saved for Section {section_number} at {analysis_file_path}"
        )


if __name__ == "__main__":
    import sys

    video_file = sys.argv[1]  # Path to the MP4 file
    process_video_by_section(
        video_file, segment_length=CONSTANT_300
    )  # Break into 5-minute sections
