from pathlib import Path
import os
import subprocess

import openai
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1500 = 1500


# Load environment variables from .env (make sure your OPENAI_API_KEY is stored here)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Directory paths
VIDEO_DIR = (
    Path("/Users/steven/Movies/j2025")  # Directory containing MP4 files
)
TRANSCRIPT_DIR = Path("/Users/steven/Movies/j2025/transcript")  # Directory to save transcripts
ANALYSIS_DIR = Path("/Users/steven/Movies/j2025/analysis")  # Directory to save the analysis files

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
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


# Function to analyze multimedia content using GPT-4o
def analyze_text_for_section(transcript, section_number=1):
    try:
        response = openai.ChatCompletion.create(
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
            max_tokens=CONSTANT_1500,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    



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
        print(
            f"Transcription saved for Section {section_number} at {transcript_file_path}"
        )

        # Step 2: Analyze the segment's transcript
        analysis = analyze_text_for_section(transcript, section_number)
        analysis_file_path = os.path.join(
            ANALYSIS_DIR, f"section_{section_number}_analysis.txt"
        )
        with open(analysis_file_path, "w") as f:
            f.write(analysis)
        logger.info(f"Analysis saved for Section {section_number} at {analysis_file_path}")


if __name__ == "__main__":
    import sys

    video_file = sys.argv[1]  # Path to the MP4 file
    process_video_by_section(
        video_file, segment_length=CONSTANT_300
    )  # Break into 5-minute sections
