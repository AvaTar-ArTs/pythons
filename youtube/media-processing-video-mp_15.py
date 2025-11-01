"""
Media Processing Video Mp 15

This module provides functionality for media processing video mp 15.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import logging
import os
import subprocess
import sys

import openai
from dotenv import load_dotenv

# Constants
CONSTANT_1024 = 1024
CONSTANT_2000 = 2000


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

env_path = Path("/Users/steven/.env")
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_SIZE = 25 * CONSTANT_1024 * CONSTANT_1024  # 25 MB hard limit

# ----- helpers -----
def format_timestamp(seconds: float) -> str:
    """format_timestamp function."""

    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

    """run_ffmpeg function."""

def run_ffmpeg(cmd: list) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def extract_small_audio(src_path: str) -> str:
    """
    Extract mono, low-bitrate AAC to keep well under 25 MB.
    Try 32 kbps first; if still too big, retry at 24 kbps.
    Returns the path to the audio file.
    """
    base, _ = os.path.splitext(src_path)
    out_path = f"{base}__audio.m4a"
        """attempt function."""


    def attempt(bitrate_kbps: int) -> str:
        # -vn: no video, -ac 1: mono, -ar 16000: 16 kHz
        cmd = [
            "ffmpeg", "-y", "-i", src_path,
            "-vn",
            "-ac", "1",
            "-ar", "16000",
            "-c:a", "aac",
            "-b:a", f"{bitrate_kbps}k",
            out_path,
        ]
        run_ffmpeg(cmd)
        return out_path

    logging.info("Extracting audio at 32 kbps AAC …")
    attempt(32)
    if os.path.getsize(out_path) > MAX_SIZE:
        logging.info("Audio still >25MB; retrying at 24 kbps …")
        attempt(24)

    size = os.path.getsize(out_path)
    if size > MAX_SIZE:
        raise RuntimeError(
            f"Audio file still exceeds 25MB after down-bitrate (size={size} bytes). "
            "Consider segmenting the input."
        )
    logging.info(f"Audio ready: {out_path} ({size} bytes)")
    return out_path

def transcribe_audio(file_path: str) -> str | None:
    """
    Sends a small audio-only file to Whisper. If input is MP4, extract audio first.
    """
    path = file_path
    if file_path.lower().endswith(".mp4"):
        path = extract_small_audio(file_path)
    elif os.path.getsize(file_path) > MAX_SIZE:
        # If a raw .mp3 is too big (unlikely at low bitrates), re-encode smaller
        logging.info("MP3 exceeds limit; down-encoding …")
        path = extract_small_audio(file_path)

    with open(path, "rb") as audio_file:
        # Old SDK call signature, keeping consistent with your env
        data = openai.Audio.transcribe("whisper-1", audio_file, response_format="verbose_json")

    transcript_lines = []
    # Use dict-style access consistently
    for seg in data.get("segments", []) or []:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"]
        transcript_lines.append(f"{format_timestamp(start)} -- {format_timestamp(end)}: {text}")

    return Path("\n").join(transcript_lines)
    """analyze_text_for_section function."""


def analyze_text_for_section(text: str, section_name: str) -> str:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in multimedia analysis and storytelling. "
                    "Provide a detailed analysis of themes, tone, structure, intent, and audience impact."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following transcript for {section_name}:\n\n{text}\n\n"
                    "Cover: themes/messages; emotional tone; narrative structure; creator intent; "
                    "technical/artistic elements; and audience impact."
                ),
            },
        ],
        max_tokens=CONSTANT_2000,
        temperature=0.7,
    )
    """process_media_directory function."""

    return resp.choices[0].message.content.strip()

def process_media_directory(media_dir: str) -> None:
    for root, _, files in os.walk(media_dir):
        for filename in files:
            if not (filename.lower().endswith(".mp4") or filename.lower().endswith(".mp3")):
                continue

            file_path = os.path.join(root, filename)
            logging.info(f"Processing file: {file_path}")

            try:
                transcript = transcribe_audio(file_path)
            except subprocess.CalledProcessError as e:
                logging.error(f"ffmpeg failed for {file_path}: {e}")
                continue
            except Exception as e:
                logging.error(f"Transcription failed for {file_path}: {e}")
                continue

            if not transcript:
                logging.error(f"No transcript produced for {file_path}")
                continue

            # Save transcript
            filename_no_ext = os.path.splitext(filename)[0]
            transcript_dir = os.path.join(BASE_DIR, "trans")
            analysis_dir = os.path.join(BASE_DIR, "analysis")
            os.makedirs(transcript_dir, exist_ok=True)
            os.makedirs(analysis_dir, exist_ok=True)

            transcript_file_path = os.path.join(transcript_dir, f"{filename_no_ext}_transcript.txt")
            with open(transcript_file_path, "w") as f:
                f.write(transcript)
            logging.info(f"Transcript saved: {transcript_file_path}")

            # Analyze transcript
            analysis = analyze_text_for_section(transcript, filename_no_ext)
            analysis_file_path = os.path.join(analysis_dir, f"{filename_no_ext}_analysis.txt")
            with open(analysis_file_path, "w") as f:
                f.write(analysis)
            logging.info(f"Analysis saved: {analysis_file_path}")

# ----- entrypoint -----
if len(sys.argv) > 1:
    base_dir = sys.argv[1]
else:
    base_dir = (input("Enter the base directory containing your media files (leave blank to use current directory): ").strip() or os.getcwd())

if not os.path.isdir(base_dir):
    logging.error(f"Directory '{base_dir}' does not exist. Exiting.")
    sys.exit(1)

BASE_DIR = os.path.abspath(base_dir)
logging.info(f"Processing directory: {BASE_DIR}")

process_media_directory(BASE_DIR)
