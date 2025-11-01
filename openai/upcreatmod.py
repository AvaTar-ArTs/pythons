"""
Upcreatmod

This module provides functionality for upcreatmod.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import openai
import pandas as pd
from tqdm import tqdm
from PIL import Image
import requests
import io

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_150 = 150


# Set OpenAI and Stability API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
stability_ai_key = os.getenv("STABILITY_API_KEY")


# Function to generate a clickable title
def generate_clickable_title(detail):
    """generate_clickable_title function."""

    prompt = f"Generate a catchy and clickable title for a 3D Breakthrough Grinch Round Christmas ORnament with the theme: '{detail}'. Maximum 30 characters. At the end of each title write Cork Back Coaster"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    clickable_title = response["choices"][0]["message"]["content"].strip()
    clickable_title = clickable_title.replace('"', "")  # Remove double quotes
    return clickable_title

    # Function to generate a description
    """generate_description function."""


def generate_description(detail):
    prompt = f"Generate a compelling description for a 3D Breakthrough Grinch Round Christmas ORnament with the theme: '{detail}'. Maximum CONSTANT_150 characters."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    description = response["choices"][0]["message"]["content"].strip()
    description = description.replace('"', "")  # Remove double quotes
    description += " 3D Breakthrough Grinch Round Christmas ORnament"
    return description

    """generate_tags function."""


# Function to generate tags
def generate_tags(detail):
    prompt = f"Generate relevant tags for a 3D Breakthrough Grinch Round Christmas ORnament with the theme: '{detail}'. Separate the tags with commas."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    tag = response["choices"][0]["message"]["content"].strip()
    tag = tag.replace('"', "")  # Remove double quotes
    return tag


# Read input file and process data
csv_path = "input.csv"
df = pd.read_csv(csv_path)
file_names = []
local_paths = []
titles = []
descriptions = []
tags = []

for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
    detail = row["details"]
    title = generate_clickable_title(detail)
    description = generate_description(detail)
    tag = generate_tags(detail)

    # Generate the image using DALL-E
    try:
        response = openai.Image.create(prompt=detail, n=1, size="1024x1024")
        image_data = requests.get(response["data"][0]["url"]).content
        image = Image.open(io.BytesIO(image_data))
        ### Generates File in Numerical Order Based on Files Generated -- NO OVERWRITING
        idx = 0
        while True:
            file_name = f"Dalle_{idx}.png"  ## Rename Dalle_ To whatever
            if not os.path.exists(file_name):
                break
            idx += 1
        local_path = file_name
        image.save(local_path)
        local_paths.append(local_path)
    except Exception as e:
        logger.info(f"Error in generating image for {detail}: {e}")
        continue

    file_names.append(file_name)
    titles.append(title)
    descriptions.append(description)
    tags.append(tag)

# Create output dataframe and save to CSV
output_df = pd.DataFrame(
    {
        "file_name": file_names,
        "local_path": local_paths,
        "title": titles,
        "description": descriptions,
        "tags": tags,
    }
)
output_df.to_csv("product_information.csv", index=False)
