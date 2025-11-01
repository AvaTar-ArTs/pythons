
# Constants
CONSTANT_1000 = 1000

cimport openai

from pathlib import Path
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from termcolor import colored
from tqdm import tqdm

# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
env_path = '/Users/steven/.env'  # Update this path if necessary
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Error checking for OpenAI API key
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

# Directory paths
AUDIO_DIR = Path("/Users/steven/Movies/HeKaTe-saLome/")  # Directory containing MP3 files
TRANSCRIPT_DIR = Path("/Users/steven/Movies/HeKaTe-saLome/transcript")  # Directory to save transcripts
ANALYSIS_DIR = Path("/Users/steven/Movies/HeKaTe-saLome/analysis")  # Directory to save the analysis files

# Create output directories if they don't exist
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Function to transcribe audio using OpenAI Whisper
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        # Use OpenAI directly instead of 'client'
        transcript_data = openai.Audio.transcribe(
            model="whisper-1", file=audio_file, response_format="verbose_json"
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
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{int(seconds):02d}"

# Function to analyze text for YouTube Shorts using OpenAI GPT
def analyze_text_for_section(text, section_number):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a social media and content analysis expert. "
                    "Your goal is to analyze YouTube Shorts for their core message, emotional tone, "
                    "and effectiveness in engaging viewers. Consider factors such as brevity, "
                    "narrative structure, visual and audio elements, and overall impact."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following YouTube Short transcript and provide a detailed analysis of: "
                    f"(1) the core message or theme, "
                    f"(2) the emotional tone conveyed, "
                    f"(3) the intent of the creator, "
                    f"(4) any notable storytelling or editing techniques used (e.g., cuts, pacing, effects), "
                    f"and (5) how effectively it engages and resonates with viewers: {text}"
                ),
            },
        ],
        max_tokens=CONSTANT_1000,
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"].strip()


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
                logger.info(f"Analysis saved for {filename_no_ext} at {analysis_file_path}")

if __name__ == "__main__":
    process_audio_directory(AUDIO_DIR)
