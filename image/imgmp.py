"""
Imgmp

This module provides functionality for imgmp.

Author: Auto-generated
Date: 2025-11-01
"""

from PIL import Image
from moviepy.editor import AudioFileClip, ImageSequenceClip
import glob
import os

import logging

logger = logging.getLogger(__name__)


def get_cover_images(file_name, cover_image_directory):
    """get_cover_images function."""

    # Check for both JPG and PNG extensions
    images = []
    jpg_paths = glob.glob(os.path.join(cover_image_directory, f"{file_name}*.jpg"))
    png_paths = glob.glob(os.path.join(cover_image_directory, f"{file_name}*.png"))

    images.extend(jpg_paths)
    images.extend(png_paths)

    if images:
        return images
    else:
        print(f"Cover images not found for {file_name}. Please ensure the cover images exist.")
        return None

    """convert_mp3_to_mp4_with_images function."""


def convert_mp3_to_mp4_with_images(mp3_file, cover_images, output_file):
    audio = AudioFileClip(mp3_file)
    clips = [ImageClip(image).set_duration(audio.duration / len(cover_images)) for image in cover_images]
    video = ImageSequenceClip(clips, fps=1)  # 1 fps as each image is a frame
    video = video.set_duration(audio.duration)
    video = video.set_audio(audio)
    video.write_videofile(output_file, fps=24)

    """process_directory function."""


def process_directory(mp3_directory, cover_image_directory):
    mp3_files = glob.glob(os.path.join(mp3_directory, "*.mp3"))

    for mp3_file in mp3_files:
        filename = os.path.basename(mp3_file)
        name, ext = os.path.splitext(filename)

        cover_images = get_cover_images(name, cover_image_directory)
        if cover_images:
            output_file = os.path.join(mp3_directory, f"{name}.mp4")
            convert_mp3_to_mp4_with_images(mp3_file, cover_images, output_file)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2:
        mp3_directory = sys.argv[1]
        cover_image_directory = sys.argv[2]
        process_directory(mp3_directory, cover_image_directory)
    else:
        print("Please provide the directories containing MP3 files and cover images as arguments.")
        print("Usage: python imgmp4.py /path/to/mp3_directory /path/to/cover_image_directory")
