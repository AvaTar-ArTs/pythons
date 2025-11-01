"""
Analyze Shorts Code

This module provides functionality for analyze shorts code.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import logging
import os

import openai
from dotenv import load_dotenv
from termcolor import colored
from tqdm import tqdm

# Constants
CONSTANT_1700 = 1700


# Load environment variables from .env
env_path = os.path.expanduser("~/.env")
load_dotenv(dotenv_path=env_path)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")


def format_timestamp(seconds):
    """format_timestamp function."""

    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{int(seconds):02d}"

    """transcribe_audio function."""


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript_data = openai.Audio.transcribe(
            model="whisper-1", file=audio_file, response_format="verbose_json"
        )
        transcript_with_timestamps = []
        for segment in transcript_data["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            transcript_with_timestamps.append(
                f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
            )
        return Path("\n").join(transcript_with_timestamps)

    """analyze_text_for_section function."""


# Function to analyze text for YouTube Shorts using OpenAI GPT
def analyze_text_for_section(text, section_number):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in multimedia analysis and storytelling. Your task is to deeply analyze video content, "
                "considering the synergy between audio and visual elements. Focus on identifying central themes, emotional tones, "
                "narrative progression, and the creator's artistic intent. Highlight how visual elements such as imagery, colors, and "
                "transitions interact with audio elements like dialogue, music, and sound effects to convey meaning and evoke emotions.",
            },
            {
                "role": "user",
                "content": f"Analyze the following transcript and associated content for Section {section_number}. Provide a detailed analysis covering:\n\n"
                "1. **Central Themes and Messages**: What are the main ideas or messages being conveyed in this section?\n"
                "2. **Emotional Tone**: What emotions are evoked by the combination of audio and visuals?\n"
                "3. **Narrative Arc**: How does this section contribute to the overall narrative or story being told?\n"
                "4. **Significant Metaphors, Symbols, and Imagery**: Are there any standout elements in the visuals or audio that enhance meaning?\n"
                "5. **Interplay Between Visuals and Audio**: How do the visuals (e.g., imagery, lighting, colors) and audio (e.g., dialogue, sound effects, music) work together to deliver the creator's intent?\n"
                "6. **Overall Impact**: How do these elements combine to create an immersive and cohesive viewer experience:{prompt}",
            },
        ],
        max_tokens=CONSTANT_1700,
        temperature=0.8,
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
    # Prompt for the media directory
    media_dir = input(
        "Enter the path to the directory containing MP3/MP4 files: "
    ).strip()
    if not os.path.isdir(media_dir):
        logger.info(f"Invalid directory: {media_dir}")
        exit(1)

    # Process the media files in the provided directory
    process_media_directory(media_dir)
