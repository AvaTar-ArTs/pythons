"""
Youtube Generate Content

This module provides functionality for youtube generate content.

Author: Auto-generated
Date: 2025-11-01
"""

import os
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
from PIL import Image
import requests
import io
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
stability_ai_key = os.getenv("STABILITY_API_KEY")


# Function to generate content based on a prompt
def generate_content(prompt):
    """generate_content function."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    generated_content = response.choices[0].message.content.strip()
    generated_content = generated_content.replace('"', "")  # Remove double quotes
    return generated_content


# Read input file and process data
csv_path = "test.csv"
df = pd.read_csv(csv_path)

file_names = []
local_paths = []
titles = []
descriptions = []
tags = []

for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
    prompt = row["prompt"]
    detail = row["detail"]

    # Check and generate title, description, and tags as necessary
    title = row["title"] if row["title"] != "-" else generate_content(prompt)
    description = (
        row["description"] if row["description"] != "-" else generate_content(prompt)
    )
    tag = row["tags"] if row["tags"] != "-" else generate_content(prompt)

    # Generate the image using DALL-E
    try:
        response = client.images.generate(prompt=detail, n=1, size="1024x1024")
        image_data = requests.get(response.data[0].url).content
        image = Image.open(io.BytesIO(image_data))

        # Generate file in numerical order, avoiding overwriting
        image_idx = 0
        while True:
            file_name = f"Dall-ME_{image_idx}.png"
            if not os.path.exists(file_name):
                break
            image_idx += 1
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
