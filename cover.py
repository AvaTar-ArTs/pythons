from openai import OpenAI

import logging

logger = logging.getLogger(__name__)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import glob
import os
from io import BytesIO

import requests
from moviepy.editor import AudioFileClip, ImageClip
from PIL import Image


def generate_cover_image_with_dalle(file_name, output_path):
    """generate_cover_image_with_dalle function."""

    prompt = f"lets create a series of typography cover image for '{file_name}' in the Font and style and contexts to tell the story'"
    response = client.images.generate(prompt=prompt, n=1, size="1024x1024")
    image_url = response.data[0].url
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(output_path)

    """convert_mp3_to_mp4 function."""


def convert_mp3_to_mp4(mp3_file, cover_image, output_file):
    audio = AudioFileClip(mp3_file)
    clip = ImageClip(cover_image)
    clip = clip.set_duration(audio.duration)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_file, fps=24)

    """process_directory function."""


def process_directory(directory):
    mp3_files = glob.glob(os.path.join(directory, "*.mp3"))

    for mp3_file in mp3_files:
        filename = os.path.basename(mp3_file)
        name, ext = os.path.splitext(filename)

        cover_image = os.path.join(directory, f"{name}.jpg")
        output_file = os.path.join(directory, f"{name}.mp4")

        generate_cover_image_with_dalle(name, cover_image)
        convert_mp3_to_mp4(mp3_file, cover_image, output_file)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        process_directory(sys.argv[1])
    else:
        logger.info("Please provide the directory containing MP3 files as an argument.")
