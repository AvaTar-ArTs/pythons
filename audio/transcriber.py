"""
Transcriber

This module provides functionality for transcriber.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_300 = 300
CONSTANT_1000 = 1000

#!/usr/bin/env python3
"""
Advanced Transcriber - Consolidated Transcription Script

This script consolidates all transcription functionality from multiple transcription scripts
into a comprehensive, feature-rich transcription tool.
"""

import os
import sys
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor
import time

from dotenv import load_dotenv
from openai import OpenAI
from termcolor import colored
from tqdm import tqdm

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("transcription.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AdvancedTranscriber:
    """Comprehensive transcription tool with multiple processing modes."""

    def __init__(self):
        """__init__ function."""

        self.client = client
        self.supported_formats = [".mp3", ".mp4", ".wav", ".m4a", ".flac"]

    def format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def transcribe_audio(
        self, file_path: Path, model: str = "whisper-1", response_format: str = "verbose_json"
    ) -> Optional[Dict]:
        """Transcribe audio file using OpenAI Whisper."""
        try:
            with open(file_path, "rb") as audio_file:
                logger.info(f"Transcribing {file_path.name}...")
                transcript_data = client.audio.transcribe(model=model, file=audio_file, response_format=response_format)
                return transcript_data
        except Exception as e:
            logger.error(f"Error transcribing {file_path}: {e}")
            return None

    def transcribe_with_timestamps(self, file_path: Path) -> Optional[str]:
        """Transcribe audio with detailed timestamps."""
        transcript_data = self.transcribe_audio(file_path)
        if not transcript_data:
            return None

        transcript_with_timestamps = []
        for segment in transcript_data.segments:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            transcript_with_timestamps.append(
                f"{self.format_timestamp(start_time)} -- {self.format_timestamp(end_time)}: {text}"
            )

        return Path("\n").join(transcript_with_timestamps)

    def convert_mp4_to_mp3(self, mp4_path: Path) -> Optional[Path]:
        """Convert MP4 to MP3 using ffmpeg."""
        mp3_path = mp4_path.with_suffix(".mp3")
        if mp3_path.exists():
            return mp3_path

        try:
            subprocess.run(
                ["ffmpeg", "-i", str(mp4_path), "-q:a", "0", "-map", "a", str(mp3_path)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(f"Converted {mp4_path.name} to MP3")
            return mp3_path
        except Exception as e:
            logger.error(f"Error converting {mp4_path}: {e}")
            return None

    def split_audio(self, file_path: Path, segment_length: int = CONSTANT_300) -> List[Path]:
        """Split audio into smaller segments."""
        output_dir = file_path.parent / "segments"
        output_dir.mkdir(exist_ok=True)

        file_name_no_ext = file_path.stem
        command = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-f",
            "segment",
            "-segment_time",
            str(segment_length),
            "-c",
            "copy",
            str(output_dir / f"{file_name_no_ext}_%03d.mp3"),
        ]

        try:
            subprocess.run(command, check=True)
            return sorted(list(output_dir.glob("*.mp3")))
        except Exception as e:
            logger.error(f"Error splitting {file_path}: {e}")
            return []

    def batch_transcribe(self, input_dir: Path, output_dir: Optional[Path] = None) -> Dict[Path, str]:
        """Transcribe all audio files in a directory."""
        if not output_dir:
            output_dir = input_dir / "transcripts"
        output_dir.mkdir(exist_ok=True)

        results = {}
        audio_files = []

        # Find all audio files
        for ext in self.supported_formats:
            audio_files.extend(input_dir.rglob(f"*{ext}"))

        for file_path in tqdm(audio_files, desc="Transcribing files"):
            try:
                # Convert MP4 to MP3 if needed
                if file_path.suffix.lower() == ".mp4":
                    mp3_path = self.convert_mp4_to_mp3(file_path)
                    if mp3_path:
                        file_path = mp3_path

                # Transcribe
                transcript = self.transcribe_with_timestamps(file_path)
                if transcript:
                    output_file = output_dir / f"{file_path.stem}_transcript.txt"
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(transcript)
                    results[file_path] = transcript
                    logger.info(f"Transcribed {file_path.name}")

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                results[file_path] = f"Error: {str(e)}"

        return results

    def generate_quiz_from_transcript(self, transcript: str, num_questions: int = 5) -> str:
        """Generate quiz questions from transcript."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"Generate {num_questions} quiz questions based on the following transcript. Make questions that test comprehension and key concepts.",
                    },
                    {"role": "user", "content": f"Transcript:\n{transcript}"},
                ],
                max_tokens=CONSTANT_1000,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return f"Quiz generation failed: {str(e)}"


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced Transcriber")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("--convert", action="store_true", help="Convert MP4 to MP3 first")
    parser.add_argument("--split", type=int, help="Split audio into segments of specified length")
    parser.add_argument("--quiz", type=int, help="Generate quiz with specified number of questions")

    args = parser.parse_args()

    transcriber = AdvancedTranscriber()
    input_path = Path(args.input)

    if input_path.is_file():
        if args.convert and input_path.suffix.lower() == ".mp4":
            mp3_path = transcriber.convert_mp4_to_mp3(input_path)
            if mp3_path:
                input_path = mp3_path

        if args.split:
            segments = transcriber.split_audio(input_path, args.split)
            logger.info(f"Split into {len(segments)} segments")
            for segment in segments:
                logger.info(f"  {segment}")

        transcript = transcriber.transcribe_with_timestamps(input_path)
        if transcript:
            logger.info(transcript)

            if args.quiz:
                quiz = transcriber.generate_quiz_from_transcript(transcript, args.quiz)
                logger.info(Path("\n") + "=" * 50)
                logger.info("QUIZ QUESTIONS:")
                logger.info("=" * 50)
                logger.info(quiz)

    elif input_path.is_dir():
        output_dir = Path(args.output) if args.output else input_path / "transcripts"
        results = transcriber.batch_transcribe(input_path, output_dir)
        logger.info(f"Transcribed {len(results)} files. Results saved to {output_dir}")

    else:
        logger.info(f"Invalid input: {input_path}")


if __name__ == "__main__":
    main()
