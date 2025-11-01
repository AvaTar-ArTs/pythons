"""
Convert Loop 6

This module provides functionality for convert loop 6.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import json
import os
import time

import requests
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_204 = 204
CONSTANT_400 = 400


# Load environment variables from ~/.env.d
def load_env_d():
    """Load all .env files from ~/.env.d directory"""
    from pathlib import Path

    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if not key.startswith("source") and not key.startswith(
                            "export"
                        ):
                            os.environ[key] = value


load_env_d()

api_key = os.getenv("LEONARDO_API_KEY")
authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Directory containing images
directory_path = Path(str(Path.home()) + "/Music/trashCaTs/in-this-alley-where-i-hide")

# Styles to apply
# Update the styles list according to your needs
styles = ["GENERAL", "CINEMATIC", "2D ART & ILLUSTRATION", "CG ART & GAME ASSETS"]


def convert_image_to_jpeg(input_path, output_path, dpi=CONSTANT_400):
    """Convert an image to JPEG format with specified DPI."""
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, "JPEG", dpi=(dpi, dpi))


def get_presigned_url():
    """get_presigned_url function."""

    url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
    payload = {"extension": "jpg"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == CONSTANT_200:
        return response.json()["uploadInitImage"]
    else:
        logger.info(f"Failed to get presigned URL: {response.status_code}")
        return None

    """upload_image function."""


def upload_image(fields, presigned_url, image_path):
    files = {"file": open(image_path, "rb")}
    response = requests.post(presigned_url, data=fields, files=files)
    return response.status_code == CONSTANT_204

    """upscale_image function."""


def upscale_image(
    init_image_id, style, creativity_strength, upscale_multiplier, prompt
):
    url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"
    payload = {
        "initImageId": init_image_id,
        "generatedImageId": None,
        "variationId": None,
        "upscalerStyle": style,
        "creativityStrength": creativity_strength,
        "upscaleMultiplier": upscale_multiplier,
        "prompt": prompt,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == CONSTANT_200:
        return response.json()["universalUpscaler"]["id"]
    else:
        print(
            f"Failed to upscale image: {
                response.status_code} {
                response.text}"
        )
        return None
    """get_upscaled_image function."""


def get_upscaled_image(variation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/variations/{variation_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == CONSTANT_200:
        return response.json()
    else:
        logger.info(f"Failed to get upscaled image: {response.status_code}")
        return None


# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(
        (".jpg", ".jpeg", ".png", ".tiff", ".webp")
    ):  # Check for supported image formats
        full_path = os.path.join(directory_path, filename)

        # Convert image to JPEG format if necessary
        if not filename.endswith(".jpg"):
            converted_path = full_path.rsplit(".", 1)[0] + ".jpg"
            convert_image_to_jpeg(full_path, converted_path)
            full_path = converted_path
            logger.info(f"Converted {filename} to {full_path}")

        # Get a presigned URL for uploading an image
        presigned_data = get_presigned_url()
        if not presigned_data:
            continue

        fields = json.loads(presigned_data["fields"])
        presigned_url = presigned_data["url"]
        init_image_id = presigned_data["id"]

        # Upload the image
        if upload_image(fields, presigned_url, full_path):
            logger.info(f"Uploaded image '{filename}'")

            # Loop through styles and apply each one to the image
            for style in styles:
                variation_id = upscale_image(
                    init_image_id,
                    style,
                    5,
                    1.5,
                    "Example prompt for universal upscaler",
                )
                if variation_id:
                    logger.info(f"Upscaled image '{filename}' with style '{style}'")
                    # Wait for processing, adjust this based on actual
                    # processing time
                    time.sleep(60)
                    upscaled_image_data = get_upscaled_image(variation_id)
                    if upscaled_image_data:
                        print(
                            f"Retrieved upscaled image for '{filename}' with style '{style}': {
                                upscaled_image_data.get(
                                    'imageUrl', 'No URL available')}"
                        )
    else:
        continue
