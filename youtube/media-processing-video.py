"""
Media Processing Video Deep 13

This module provides functionality for media processing video deep 13.

Author: Auto-generated
Date: 2025-11-01
"""

import logging
import os
import sys
from pathlib import Path
import openai
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

# Constants
CONSTANT_300 = 300
CONSTANT_1800 = 1800


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load environment variables
env_path = Path("~/.env")
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Base config
config = {"base_dir": ""}
if not config.get("base_dir"):
    base_dir_input = input("Enter base directory (leave blank for current): ").strip()
    config["base_dir"] = base_dir_input or os.getcwd()

BASE_DIR = Path(config["base_dir"]).resolve()
if not BASE_DIR.is_dir():
    logging.error(f"Directory '{BASE_DIR}' does not exist. Exiting.")
    sys.exit(1)

# Output directories
TRANSCRIPT_DIR = BASE_DIR / "trans"
ANALYSIS_DIR = BASE_DIR / "analysis"
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


def format_timestamp(seconds: float) -> str:
    """format_timestamp function."""

    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def get_video_duration(file_path: Path) -> float:
    """Get the duration of the video in seconds."""
    with VideoFileClip(str(file_path)) as video:
        return video.duration


def transcribe_audio(file_path: Path, start_time: float, end_time: float) -> str:
    """Transcribe a section of MP4 using Whisper."""
    with open(file_path, "rb") as audio_file:
        transcript_data = openai.Audio.transcribe(
            "whisper-1",
            audio_file,
            response_format="verbose_json",
            start_time=start_time,
            end_time=end_time,
        )
    return Path("\n").join(
        f"{format_timestamp(seg['start'])} -- {format_timestamp(seg['end'])}: {seg['text']}"
        for seg in transcript_data.segments
    )


def analyze_text(text: str, section_number: str) -> str:
    """Perform a detailed analysis of multimedia content using ChatGPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # upgrade model
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
        max_tokens=CONSTANT_1800,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def process_media_directory(media_dir: Path):
    """Process MP4s: transcribe and analyze in sections."""
    section_duration = CONSTANT_300  # 5 minutes per section
    for file_path in media_dir.rglob("*.mp4"):
        filename_no_ext = file_path.stem
        video_duration = get_video_duration(file_path)

        for start_time in range(0, int(video_duration), section_duration):
            end_time = min(start_time + section_duration, video_duration)

            logging.info(
                f"Transcribing {file_path.name} from {format_timestamp(start_time)} to {format_timestamp(end_time)}..."
            )
            transcript = transcribe_audio(file_path, start_time, end_time)
            (
                TRANSCRIPT_DIR
                / f"{filename_no_ext}_transcript_{start_time}_{end_time}.txt"
            ).write_text(transcript)

            logging.info(
                f"Analyzing {file_path.name} from {format_timestamp(start_time)} to {format_timestamp(end_time)}..."
            )
            analysis = analyze_text(
                transcript, f"{filename_no_ext}_{start_time}_{end_time}"
            )
            (
                ANALYSIS_DIR / f"{filename_no_ext}_analysis_{start_time}_{end_time}.txt"
            ).write_text(analysis)

            logging.info(
                f"Completed section {format_timestamp(start_time)} to {format_timestamp(end_time)} of {file_path.name}"
            )


if __name__ == "__main__":
    process_media_directory(BASE_DIR)
