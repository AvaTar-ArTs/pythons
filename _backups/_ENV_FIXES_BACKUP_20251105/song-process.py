from pathlib import Path
import csv
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_2000 = 2000


# Load environment variables from .env file
load_dotenv(dotenv_path=Path(str(Path.home()) + "/.env"))

# Get API key and validate it
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("❌ OpenAI API key not found. Please check your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


# Helper function to format timestamps
def format_timestamp(seconds):
    """Convert seconds into MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


# Function to transcribe audio using OpenAI's Whisper
def transcribe_audio(file_path):
    """Transcribe an audio file using OpenAI's Whisper API."""
    with open(file_path, "rb") as audio_file:
        transcript_data = client.audio.transcribe(
            model="whisper-1", file=audio_file, response_format="verbose_json"
        )

    # Process transcript with timestamps
    transcript_with_timestamps = []
    for segment in transcript_data.segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        transcript_with_timestamps.append(
            f"{format_timestamp(start_time)} -- {format_timestamp(end_time)}: {text}"
        )

    return Path("\n").join(transcript_with_timestamps)


# Function to analyze multimedia content using GPT-4o
def analyze_text_for_section(transcript, section_number=1):
    """analyze_text_for_section function."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Upgraded to GPT-4o
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert multimedia analyst and storyteller. Your role is to deliver comprehensive, insightful, and "
                        "emotionally intelligent evaluations of audio-visual content. Your analyses should cover thematic depth, emotional tone, "
                        "narrative structure, artistic expression, technical execution, and audience engagement. Use vivid, descriptive language "
                        "and reference specific moments when necessary."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Please provide a thorough analysis of Section {section_number} of the following transcript. Break down key elements with depth and clarity:\n\n"
                        "### 1. Central Themes and Messages\n"
                        "- Identify and interpret the primary themes.\n"
                        "- Are there any hidden or layered meanings?\n\n"
                        "### 2. Emotional Tone\n"
                        "- Describe the mood and emotional shifts.\n"
                        "- How do sound, rhythm, or possible visuals contribute to the emotion?\n\n"
                        "### 3. Narrative Arc and Structure\n"
                        "- How does this section move the story forward?\n"
                        "- Mention key transitions or turning points.\n\n"
                        "### 4. Creator’s Intent and Vision\n"
                        "- What might the creator be trying to say or express?\n"
                        "- How do multimedia elements (e.g., sound, visuals, pacing) support this vision?\n\n"
                        "### 5. Technical and Artistic Elements\n"
                        "- Comment on production techniques: editing, sound design, transitions, or special effects.\n"
                        "- How do these enhance storytelling?\n\n"
                        "### 6. Audience Impact and Engagement\n"
                        "- How effectively does it capture and maintain attention?\n"
                        "- What makes this portion memorable or emotionally resonant?\n\n"
                        f"### Transcript\n{transcript}"
                    ),
                },
            ],
            max_tokens=CONSTANT_2000,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.info(colored(f"Error analyzing text: {e}", "red"))
        return None


# Function to process a single audio file
def process_audio_file(file_path, csv_data):
    """Process an audio file: Transcribe and Analyze."""
    base_dir = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    song_dir = os.path.join(base_dir, file_name_no_ext)

    # Create a folder for the song
    os.makedirs(song_dir, exist_ok=True)

    # Step 1: Transcribe the audio file
    logger.info(f"🎼 Transcribing {file_name}...")
    transcript = transcribe_audio(file_path)
    transcript_path = os.path.join(song_dir, f"{file_name_no_ext}_transcript.txt")
    with open(transcript_path, "w") as f:
        f.write(transcript)
    logger.info(f"✅ Transcript saved: {transcript_path}")

    # Step 2: Analyze the transcript
    logger.info(f"🎭 Analyzing {file_name}...")
    analysis = analyze_text_for_section(transcript, file_name_no_ext)
    analysis_path = os.path.join(song_dir, f"{file_name_no_ext}_analysis.txt")
    with open(analysis_path, "w") as f:
        f.write(analysis)
    logger.info(f"✅ Analysis saved: {analysis_path}")

    # Append info to CSV data list
    csv_data.append(
        [
            file_name_no_ext,
            file_path,
            transcript_path,
            analysis_path,
            transcript,
            analysis,
        ]
    )


# Function to process all audio files in a directory and save as CSV
def process_audio_directory():
    """Prompt user for directory and process all audio files."""
    audio_dir = input("Enter the directory containing MP3 files: ").strip()

    if not os.path.isdir(audio_dir):
        logger.info(f"❌ Invalid directory: {audio_dir}")
        sys.exit(1)

    logger.info(f"🔍 Scanning directory {audio_dir} for audio files...")
    csv_data = [
        [
            "Song Title",
            "MP3 File Path",
            "Transcript File",
            "Analysis File",
            "Transcript Content",
            "Analysis Content",
        ]
    ]

    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(root, file)
                logger.info(f"🎵 Found audio file: {file_path}")
                process_audio_file(file_path, csv_data)

    # Save CSV
    csv_path = os.path.join(
        audio_dir, Path(str(Path.home()) + "/Music/nocTurneMeLoDieS/mp4/song_data.csv")
    )
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    logger.info(f"📜 CSV file saved: {csv_path}")


if __name__ == "__main__":
    process_audio_directory()
