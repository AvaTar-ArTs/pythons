"""
Media Processing Video Mp4Tomp 2

This module provides functionality for media processing video mp4tomp 2.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import subprocess

import whisper

import logging

logger = logging.getLogger(__name__)



def convert_mp4_to_mp3(mp4_file, mp3_file):
    """convert_mp4_to_mp3 function."""

    # Use ffmpeg to convert mp4 to mp3
    subprocess.run(["ffmpeg", "-i", mp4_file, "-q:a", "0", "-map", "a", mp3_file])


    """transcribe_audio function."""

def transcribe_audio(file_path):
    # Load the Whisper model
    model = whisper.load_model("base")

    # Transcribe the audio file
    result = model.transcribe(file_path)

    return result["segments"]

    """save_transcription function."""


def save_transcription(segments, output_file):
    with open(output_file, "w") as f:
        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            f.write(f"[{start:.2f} - {end:.2f}] {text}\n")
    """process_directory function."""



def process_directory(source_directory):
    for root, _, files in os.walk(source_directory):
        for filename in files:
            if filename.lower().endswith(".mp4"):
                mp4_file = os.path.join(root, filename)
                filename_no_ext = os.path.splitext(filename)[0]
                mp3_file = os.path.join(root, f"{filename_no_ext}.mp3")
                transcription_file = os.path.join(
                    root, f"{filename_no_ext}_transcription.txt"
                )

                # Convert MP4 to MP3
                convert_mp4_to_mp3(mp4_file, mp3_file)
                logger.info(f"Converted {mp4_file} to {mp3_file}")

                # Transcribe the MP3
                segments = transcribe_audio(mp3_file)

                # Save the transcription
                save_transcription(segments, transcription_file)
    """main function."""

                logger.info(f"Transcription saved to {transcription_file}")


def main():
    source_directory = input("Enter the path to the source directory: ")
    process_directory(source_directory)


if __name__ == "__main__":
    main()
