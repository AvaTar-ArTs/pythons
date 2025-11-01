"""
Script 174

This module provides functionality for script 174.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import sys

import ffmpeg
import whisper

import logging

logger = logging.getLogger(__name__)



def convert_video_to_audio(video_file, output_dir):
    """convert_video_to_audio function."""

    try:
        base_name = os.path.basename(video_file)
        output_file = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}.mp3")

        ffmpeg.input(video_file).output(output_file).run(overwrite_output=True)
        logger.info(f"Converted {video_file} to {output_file}")
        return output_file
    except Exception as e:
        logger.info(f"An error occurred while converting {video_file}: {e}")
        return None


    """transcribe_audio function."""

def transcribe_audio(mp3_file):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(mp3_file)
        return result
    except Exception as e:
        logger.info(f"An error occurred while transcribing {mp3_file}: {e}")
        return None

    """save_transcription function."""


def save_transcription(result, output_dir, base_name):
    try:
        transcription_file = os.path.join(output_dir, f"{base_name}.txt")
        with open(transcription_file, "w") as f:
            for segment in result["segments"]:
                start_time = segment["start"]
                end_time = segment["end"]
                text = segment["text"]
                f.write(f"[{start_time:.2f} - {end_time:.2f}] {text}\n")
        logger.info(f"Saved transcription to {transcription_file}")
    except Exception as e:
        logger.info(f"An error occurred while saving the transcription: {e}")
    """process_directory function."""



def process_directory(source_directory):
    try:
        if not os.path.exists(source_directory):
            raise FileNotFoundError(f"The directory {source_directory} does not exist.")

        output_dir = os.path.join(source_directory, "processed_audio")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in os.listdir(source_directory):
            if filename.endswith(".mp4") or filename.endswith(".mov"):
                video_file = os.path.join(source_directory, filename)
                mp3_file = convert_video_to_audio(video_file, output_dir)
                if mp3_file:
                    result = transcribe_audio(mp3_file)
                    if result:
                        base_name = os.path.splitext(filename)[0]
                        save_transcription(result, output_dir, base_name)

    except Exception as e:
    """main function."""

        logger.info(f"An error occurred while processing the directory: {e}")


def main():
    source_directory = input("Enter the path to the source directory: ")
    process_directory(source_directory)


if __name__ == "__main__":
    main()
