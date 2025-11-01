"""
Analyzeshorts

This module provides functionality for analyzeshorts.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
from openai import OpenAI
import sys
import logging
from dotenv import load_dotenv
from tqdm import tqdm
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor
import time

# Constants
CONSTANT_1000 = 1000


env_path = Path("/Users/steven/.env")
load_dotenv(dotenv_path=env_path)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to transcribe audio using OpenAI Whisper
def transcribe_audio(file_path):
    """transcribe_audio function."""

    with open(file_path, "rb") as audio_file:
        # Use OpenAI directly instead of 'client'
        transcript_data = client.audio.transcribe(model="whisper-1", file=audio_file, response_format="verbose_json")

        # Build the transcript with timestamps
        transcript_with_timestamps = []
        for segment in transcript_data.segments:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            transcript_with_timestamps.append(f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}")

        return Path("\n").join(transcript_with_timestamps)

    # Helper function to format timestamps
    """format_timestamp function."""


def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{int(seconds):02d}"

    """analyze_text_for_section function."""


# Function to analyze text for YouTube Shorts using OpenAI GPT
def analyze_text_for_section(text, section_number):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in multimedia analysis and storytelling. Your task is to deeply analyze the content to provide a detailed and structured analysis of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact"
                    "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
                    "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers."
                    "considering the synergy between audio and visual elements. Focus on identifying central themes, emotional tones, "
                    "narrative progression, and the creator's artistic intent. Highlight how visual elements such as imagery, colors, "
                    "transitions interact with audio elements like dialogue, music, and sound effects to convey meaning and evoke emotions."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following transcript and associated content for Section {text}. Provide a detailed analysis covering:\n\n"
                    "1. **Central Themes and Messages**: What are the main ideas or messages being conveyed in this section?\n"
                    "2. **Emotional Tone**: What emotions are evoked by the combination of audio and visuals?\n"
                    "3. **Narrative Arc**: How does this section contribute to the overall narrative or story being told?\n"
                    "4. **Significant Metaphors, Symbols, and Imagery**: Are there any standout elements in the visuals or audio that enhance meaning?\n"
                    "5. **Interplay Between Visuals and Audio**: How do the visuals (e.g., imagery, lighting, colors) and audio (e.g., dialogue, sound effects, music) work together to deliver the creator's intent?\n"
                    "6. **Overall Impact**: How do these elements combine to create an immersive and cohesive viewer experience?"
                ),
            },
        ],
        max_tokens=CONSTANT_1000,
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"].strip()

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
                transcript_file_path = os.path.join(TRANSCRIPT_DIR, f"{filename_no_ext}_transcript.txt")
                with open(transcript_file_path, "w") as f:
                    f.write(transcript)
                print(f"Transcription saved for {filename_no_ext} at {transcript_file_path}")

                # Step 2: Analyze the segment's transcript
                analysis = analyze_text_for_section(transcript, filename_no_ext)
                analysis_file_path = os.path.join(ANALYSIS_DIR, f"{filename_no_ext}_analysis.txt")
                with open(analysis_file_path, "w") as f:
                    f.write(analysis)
                logger.info(f"Analysis saved for {filename_no_ext} at {analysis_file_path}")


if __name__ == "__main__":
    process_audio_directory(AUDIO_DIR)
