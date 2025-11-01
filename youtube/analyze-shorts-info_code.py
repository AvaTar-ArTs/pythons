
# Constants
CONSTANT_1500 = 1500

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

# Error checking for OpenAI API key
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

# Load environment variables from .env
env_path = os.path.expanduser("~/.env")
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI API key

if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

# Directory paths
AUDIO_DIR = Path("/Users/steven/Movies/poject2025/mp4")  # Directory containing MP3 files
TRANSCRIPT_DIR = Path("/Users/steven/Movies/poject2025/mp4/transcript")  # Directory to save transcripts
ANALYSIS_DIR = Path("/Users/steven/Movies/poject2025/mp4/analysis")  # Directory to save the analysis files

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

# Function to analyze text
def analyze_text_for_section(text, section_name):
    """Analyze the transcribed text using OpenAI GPT."""
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": (
                       "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis "
                    "of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact. "
                    "Analyze how visual elements (e.g., imagery, colors, transitions) interact with audio elements (e.g., dialogue, music, sound effects) "
                    "to convey meaning and evoke emotions. Highlight storytelling techniques and assess their effectiveness in engaging viewers."
                )
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
                )
            }
        ],
        max_tokens=CONSTANT_1500,
        temperature=0.7)

    return response.choices[0].message.content.strip()


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
