import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/processing/over3.py
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/processing/imgmp4.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/mp3-mp4-coverimg_1.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/process_variants_mp3-mp4-coverimg copy.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/Mp3toMp4ximg_1.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/process_variants_imgmp4.py
- /Users/steven/Music/nocTurneMeLoDieS/python/DUPLICATES_ARCHIVE/over3_1.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
import glob
import os
import sys

from moviepy.editor import AudioFileClip, ImageClip, ImageSequenceClip


def get_cover_images(file_name, cover_image_directory):
    # Check for both JPG and PNG extensions
    images = []
    jpg_paths = glob.glob(os.path.join(cover_image_directory, f"{file_name}*.jpg"))
    png_paths = glob.glob(os.path.join(cover_image_directory, f"{file_name}*.png"))

    images.extend(jpg_paths)
    images.extend(png_paths)

    if images:
        return images
    else:
        print(
            f"Cover images not found for {file_name}. Please ensure the cover images exist."
        )
        return None


def convert_mp3_to_mp4_with_images(mp3_file, cover_images, output_file):
    audio = AudioFileClip(mp3_file)
    clips = [
        ImageClip(image).set_duration(audio.duration / len(cover_images))
        for image in cover_images
    ]
    video = ImageSequenceClip(clips, fps=1)  # 1 fps as each image is a frame
    video = video.set_duration(audio.duration)
    video = video.set_audio(audio)
    video.write_videofile(output_file, fps=24)


def process_directory(mp3_directory, cover_image_directory):
    mp3_files = glob.glob(os.path.join(mp3_directory, "*.mp3"))

    for mp3_file in mp3_files:
        filename = os.path.basename(mp3_file)
        name, ext = os.path.splitext(filename)

        cover_images = get_cover_images(name, cover_image_directory)
        if cover_images:
            output_file = os.path.join(mp3_directory, f"{name}.mp4")
            convert_mp3_to_mp4_with_images(mp3_file, cover_images, output_file)


try:
        import sys
        if len(sys.argv) > 2:
            mp3_directory = sys.argv[1]
            cover_image_directory = sys.argv[2]
            process_directory(mp3_directory, cover_image_directory)
        else:
            print(
                "Please provide the directories containing MP3 files and cover images as arguments."
            )
            print(
                "Usage: python imgmp4.py /path/to/mp3_directory /path/to/cover_image_directory"
            )
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)