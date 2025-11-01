"""
Parse 13

This module provides functionality for parse 13.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored
from tqdm import tqdm

# Constants
CONSTANT_1500 = 1500


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
env_path = os.path.expanduser("~/.env")
load_dotenv(dotenv_path=env_path)

# Configure logging for error reporting
logging.basicConfig(
    filename="transcription_analysis_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Prompt the user for the main directory path with emoji and color feedback
AUDIO_DIR = input(
    "🎵 Please enter the full path to the main directory containing your MP3 files (including subfolders): "
)
if not os.path.isdir(AUDIO_DIR):
    logger.info(colored("❌ Invalid directory path. Please check and try again.", "red"))
    sys.exit(1)

# Define paths for transcript and analysis subdirectories within the main directory
TRANSCRIPT_DIR = os.path.join(AUDIO_DIR, "transcript")
ANALYSIS_DIR = os.path.join(AUDIO_DIR, "analysis")

# Create the transcript and analysis directories with feedback
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

logger.info(colored(f"📁 Directories set up successfully!", "green"))
logger.info(f"🔍 AUDIO_DIR: {colored(AUDIO_DIR, 'cyan')}")
logger.info(f"📝 TRANSCRIPT_DIR: {colored(TRANSCRIPT_DIR, 'cyan')}")
logger.info(f"🔬 ANALYSIS_DIR: {colored(ANALYSIS_DIR, 'cyan')}")


# Helper function to format timestamps
def format_timestamp(seconds):
    """format_timestamp function."""

    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


# Function to parse the transcript into segments
    """parse_transcript function."""

def parse_transcript(transcript_text):
    segments = []
    for line in transcript_text.split(Path("\n")):
        if "--" in line:
            parts = line.split(": ")
            if len(parts) == 2:
                timestamp, text = parts[0], parts[1]
                segments.append({"timestamp": timestamp, "text": text})
    return segments


    """transcribe_audio function."""

# Function to transcribe audio using OpenAI's Whisper model with retry mechanism
def transcribe_audio(file_path, max_attempts=3):
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        logger.info(colored(f"❌ {os.path.basename(file_path)} is invalid or empty.", "red"))
        return None

    for attempt in range(max_attempts):
        try:
            with open(file_path, "rb") as audio_file:
                transcript_data = client.audio.transcribe(
                    "whisper-1", audio_file, response_format="verbose_json"
                )
                transcript_with_timestamps = []
                for segment in transcript_data.segments:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"]
                    transcript_with_timestamps.append(
                        f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
                    )
                return Path("\n").join(transcript_with_timestamps)
        except Exception as e:
            logging.error(f"🚨 Attempt {attempt + 1}: Error transcribing {file_path}: {e}")
            print(
                colored(
                    f"🚨 Attempt {attempt + 1}: Error transcribing {os.path.basename(file_path)}. Retrying...",
                    "yellow",
                )
            )
            time.sleep(2)  # Wait before retrying
    print(
        colored(
            f"❌ Failed to transcribe {os.path.basename(file_path)} after {max_attempts} attempts.",
            "red",
        )
    )
    return None

    """analyze_text_for_section function."""


# Function to analyze the text using OpenAI's GPT model with retry mechanism
def analyze_text_for_section(text, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an experienced language and music expert. Your role is to provide an in-depth, structured analysis of song lyrics."
                            "Focus on uncovering the central context, emotional nuances, narrative arc, and deeper meanings. Analyze the emotional tone,"
                            "narrative journey, and underlying themes, while highlighting any significant metaphors, symbols, and imagery."
                            "Explain how these elements interconnect and contribute to the overall emotional and narrative impact."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Please provide a thorough analysis of the following song transcript, structured as follows: "
                            f"(1) **Central Themes and Meaning**: Describe the main themes and the message conveyed by the song. "
                            f"(2) **Emotional Tone**: Highlight the emotional tone and any shifts throughout the lyrics. "
                            f"(3) **Artist's Intent**: Discuss what the artist might be aiming to express or achieve with these lyrics. "
                            f"(4) **Metaphors, Symbols, and Imagery**: Identify and explain notable metaphors, symbols, or imagery, and their significance. "
                            f"(5) **Overall Emotional and Narrative Experience**: Summarize how these elements create an impactful experience for the listener. "
                            f"(5) **Overall Emotional and Narrative Experience**: Summarize how these elements create an impactful experience for the listener. "
                            f"Structure your response in clear, detailed bullet points for better readability, : {text}"
                        ),
                    },
                ],
                max_tokens=CONSTANT_1500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"⚠️ Attempt {attempt + 1}: Error analyzing text: {e}")
            print(
                colored(
                    f"⚠️ Attempt {attempt + 1}: Error analyzing the transcript. Retrying...",
                    "yellow",
                )
            )
            time.sleep(2)  # Wait before retrying
    logger.info(colored(f"❌ Failed to analyze the transcript after {max_attempts} attempts.", "red"))
    return None
    """link_timestamps_to_analysis function."""



# Function to link timestamps from the transcript to the analysis
def link_timestamps_to_analysis(transcript_segments, analysis_text):
    linked_analysis = analysis_text
    for segment in transcript_segments:
        if any(word in analysis_text for word in segment["text"].split()):
            linked_analysis = linked_analysis.replace(
                segment["text"], f"{segment['text']} [{segment['timestamp']}]"
            )
    """process_audio_file function."""

    return linked_analysis


# Main function to process audio files in the directory
def process_audio_file(audio_file):
    filename_no_ext = os.path.splitext(os.path.basename(audio_file))[0]
    logger.info(colored(f"🔄 Processing {filename_no_ext}...", "blue"))

    # Transcribe the audio file
    transcript = transcribe_audio(audio_file)
    if transcript:
        transcript_file_path = os.path.join(TRANSCRIPT_DIR, f"{filename_no_ext}_transcript.txt")
        with open(transcript_file_path, "w") as f:
            f.write(transcript)
        logger.info(f"✅ Transcription saved for {filename_no_ext} at {transcript_file_path}")

        # Parse transcript for segments
        transcript_segments = parse_transcript(transcript)

        # Analyze the transcript
        analysis = analyze_text_for_section(transcript)
        if analysis:
            # Link timestamps to analysis
            linked_analysis = link_timestamps_to_analysis(transcript_segments, analysis)

            analysis_file_path = os.path.join(ANALYSIS_DIR, f"{filename_no_ext}_analysis.txt")
            with open(analysis_file_path, "w") as f:
                f.write("# Analysis of " + filename_no_ext + Path("\n\n") + linked_analysis)
            print(
                f"📝 Analysis with timestamps saved for {filename_no_ext} at {analysis_file_path}"
            )
        else:
    """process_audio_directory function."""

            logger.info(colored(f"⚠️ Skipping analysis for {filename_no_ext} due to error.", "yellow"))
    else:
        logger.info(colored(f"⚠️ Skipping {filename_no_ext} due to transcription error.", "yellow"))


def process_audio_directory(audio_dir):
    audio_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(audio_dir)
        for f in files
        if f.lower().endswith(".mp3")
    ]
    if not audio_files:
        logger.info(colored("📂 No MP3 files found in the directory. Please check your path.", "red"))
        return

    logger.info(colored(f"🎶 Found {len(audio_files)} audio files. Starting processing...", "green"))

    with ThreadPoolExecutor() as executor:
        list(
            tqdm(
                executor.map(process_audio_file, audio_files),
                total=len(audio_files),
                desc="Processing MP3 files",
            )
        )


if __name__ == "__main__":
    process_audio_directory(AUDIO_DIR)
