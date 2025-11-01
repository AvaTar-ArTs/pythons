"""
Yt Dalle Prompt

This module provides functionality for yt dalle prompt.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import csv
from io import BytesIO

import requests
from openai import OpenAI
from PIL import Image
import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_150 = 150
CONSTANT_300 = 300


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set your OpenAI API key here


def upscale_image(image_url):
    """upscale_image function."""

    # Fetch the image
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Calculate the new size, doubling the width and height
    new_size = (image.width * 2, image.height * 2)

    # Resize the image to the new size
    upscaled_image = image.resize(new_size, Image.ANTIALIAS)

    # Set the DPI to CONSTANT_300
    upscaled_image.save("upscaled_image.png", dpi=(CONSTANT_300, CONSTANT_300))
    logger.info("Image has been upscaled and saved with CONSTANT_300 DPI.")

    """generate_youtube_content function."""


def generate_youtube_content(image_description, question, image_url):
    # Generate YouTube title, description, and SEO keywords using GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Based on the image description: '{image_description}', generate a YouTube video title, description, and SEO keywords.",
            },
        ],
        max_tokens=CONSTANT_150,
    )
    youtube_content = response.choices[0].message.content.strip()

    # Split the content into title, description, and keywords
    content_lines = youtube_content.split(Path("\n"))
    title = content_lines[0].strip()
    description = content_lines[1].strip()
    keywords = content_lines[2].strip()

    # Write to CSV
    with open("youtube_content.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Question", "Image URL", "Title", "Description", "Keywords"])
        writer.writerow([question, image_url, title, description, keywords])

    logger.info("YouTube content generated and saved to CSV.")

    """analyze_and_generate function."""


def analyze_and_generate():
    question = "Describe a futuristic cityscape."

    # Step 1: Generate a detailed descriptive prompt
    prompt_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
        max_tokens=CONSTANT_100,
    )
    detailed_prompt = prompt_response.choices[0].message.content.strip()

    # Step 2: Use the detailed prompt to create an image with DALL·E
    image_response = client.images.generate(
        model="dalle-3", prompt=detailed_prompt, n=1
    )
    image_url = image_response.data[0].url

    # Upscale the image
    upscale_image(image_url)

    # Generate YouTube content based on the detailed prompt and image URL
    generate_youtube_content(detailed_prompt, question, image_url)


# Run the analysis and generation process
analyze_and_generate()
