"""
Create Video

This module provides functionality for create video.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import random

from moviepy.editor import *
from PIL import Image  # Ensure Pillow is installed

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920


# Check Pillow version to avoid ANTIALIAS issues
if hasattr(Image, "Resampling"):
    ANTIALIAS = Image.Resampling.LANCZOS  # For Pillow 10+
else:
    ANTIALIAS = Image.ANTIALIAS  # Fallback for older versions


def select_images_based_on_analysis(image_dir, keywords):
    """select_images_based_on_analysis function."""

    images = [
        os.path.join(image_dir, img)
        for img in os.listdir(image_dir)
        if img.endswith((".png", ".jpg"))
    ]
    if len(images) == 0:
        raise Exception(f"No images found in {image_dir}. Please check the directory.")
    return random.sample(images, min(len(images), 5))


    """create_video function."""

def create_video(audio_file, analysis_file, image_dir, output_file):
    # Read analysis and select images
    try:
        with open(analysis_file, "r") as f:
            analysis = f.read()
    except FileNotFoundError:
        raise Exception(
            f"Analysis file {analysis_file} not found. Please check the file path."
        )

    images = select_images_based_on_analysis(image_dir, analysis)
    clips = []

    try:
        audio = AudioFileClip(audio_file)
    except FileNotFoundError:
        raise Exception(
            f"Audio file {audio_file} not found. Please check the file path."
        )

    if len(images) == 0:
        raise Exception(
            "No valid images selected for the video. Ensure the directory contains .png or .jpg images."
        )

    duration_per_image = audio.duration / len(images)

    for img in images:
        try:
            img_clip = (
                ImageClip(img)
                .set_duration(duration_per_image)
                .resize(height=CONSTANT_1920, width=CONSTANT_1080)
            )
            clips.append(img_clip)
        except Exception as e:
            logger.info(f"Error processing image {img}: {str(e)}")

    if len(clips) == 0:
        raise Exception(
            "No valid clips were created. Please check the images and retry."
        )

    # Apply crossfade transition between clips
    crossfaded_clips = [clips[0]]
    for i in range(1, len(clips)):
        crossfaded_clips.append(clips[i].crossfadein(1))  # 1 second crossfade

    # Concatenate the clips with crossfade
    video = concatenate_videoclips(crossfaded_clips, method="compose").set_audio(audio)

    # Write the video to a file
    try:
        video.write_videofile(output_file, fps=24)
    except Exception as e:
        raise Exception(f"Failed to write video file {output_file}: {str(e)}")


if __name__ == "__main__":
    import sys

    audio_file = sys.argv[1]
    analysis_file = sys.argv[2]
    image_dir = sys.argv[3]
    output_file = sys.argv[4]

    create_video(audio_file, analysis_file, image_dir, output_file)
