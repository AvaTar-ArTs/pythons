"""
Youtube Format Timestamp

This module provides functionality for youtube format timestamp.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import openai
import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1500 = 1500


# Load environment variables from ~/.env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

def format_timestamp(seconds):
    """Format seconds into MM:SS timestamp."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{int(seconds):02d}"

def transcribe_audio(file_path):
    """Transcribe audio file using OpenAI's Whisper API."""
    with open(file_path, "rb") as audio_file:
        transcript_data = openai.Audio.transcribe(
            model="whisper-1", 
            file=audio_file, 
            response_format="verbose_json"
        )
        return Path("\n").join(
            f"{format_timestamp(segment['start'])} -- {format_timestamp(segment['end'])}: {segment['text']}"
            for segment in transcript_data["segments"]
        )

def analyze_text_for_section(text, section_name):
    """Analyze transcript text using OpenAI GPT."""
    prompt = (
        f"Analyze the following transcript and associated content for {section_name}. "
        "Provide a comprehensive analysis covering:\n"
        "1. Central Themes and Messages: Identify the primary ideas or messages conveyed. "
        "How do they connect to the broader narrative?\n"
        "2. Emotional Tone: What emotions are evoked, and how are they conveyed through the "
        "combination of audio and visuals?\n"
        "3. Narrative Arc: Describe how this section contributes to the overall story or progression. "
        "Are there key turning points or developments?\n"
        "4. Creator’s Intent: What is the likely purpose or message the creator is trying to communicate? "
        "Is it to entertain, inform, inspire, or persuade?\n"
        "5. Significant Metaphors, Symbols, and Imagery: Highlight notable metaphors, symbols, or "
        "visual/audio motifs that enhance the narrative or emotional impact.\n"
        "6. Storytelling Techniques: Identify specific techniques used, such as pacing, transitions, "
        "visual effects, or sound design. How do they contribute to the overall experience?\n"
        "7. Interplay Between Visuals and Audio: Analyze how visuals and audio work together to create "
        "meaning and impact. Are there any standout moments?\n"
        "8. Audience Engagement and Impact: Evaluate how effectively the content captures and holds attention. "
        "How well does it resonate with its intended audience?\n"
        "9. Overall Effectiveness: Summarize how these elements combine to create a cohesive, immersive, "
        "and impactful experience for the viewer.\n\n"
        f"Transcript:\n{text}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in multimedia analysis and storytelling. Your task is to provide a detailed and structured analysis of video and audio content, focusing on themes, emotional tone, narrative structure, artistic intent, and audience impact."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=CONSTANT_1500,
        temperature=0.8
    )
    return response.choices[0].message["content"]

def process_audio_file(file_path):
    """Process a single audio file: Transcribe and Analyze."""
    base_dir, file_name = os.path.dirname(file_path), os.path.basename(file_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    
    # Transcription
    logger.info(f"Processing transcription for {file_name}...")
    transcript = transcribe_audio(file_path)
    transcript_path = os.path.join(base_dir, f"{file_name_no_ext}_transcript.txt")
    with open(transcript_path, "w") as f:
        f.write(transcript)
    logger.info(f"Transcript saved to {transcript_path}")
    
    # Analysis
    logger.info(f"Processing analysis for {file_name}...")
    analysis = analyze_text_for_section(transcript, file_name_no_ext)
    analysis_path = os.path.join(base_dir, f"{file_name_no_ext}_analysis.txt")
    with open(analysis_path, "w") as f:
        f.write(analysis)
    logger.info(f"Analysis saved to {analysis_path}")

def process_audio_directory():
    """Prompt user for directory and process all audio files."""
    audio_dir = input("Enter the main directory path containing MP3 files: ").strip()
    
    if not os.path.isdir(audio_dir):
        raise NotADirectoryError(f"The directory {audio_dir} does not exist.")
    
    logger.info(f"Scanning directory {audio_dir} for audio files...")
    for root, _, files in os.walk(audio_dir):
        for file in files:
            if file.lower().endswith(".mp3"):
                file_path = os.path.join(root, file)
                logger.info(f"Found audio file: {file_path}")
                process_audio_file(file_path)

if __name__ == "__main__":
    process_audio_directory()
