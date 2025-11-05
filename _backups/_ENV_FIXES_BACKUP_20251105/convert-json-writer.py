from pathlib import Path
import csv
import json
import os
import time
from datetime import datetime

import requests
from PIL import Image

import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_120 = 120
CONSTANT_200 = 200
CONSTANT_204 = 204
CONSTANT_400 = 400


load_dotenv()

api_key = os.getenv("LEONARDO_API_KEY")
authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Directory containing images
directory_path = Path(str(Path.home()) + "/Pictures/TrashCaT/trashy-heartbreak")
output_csv = "upscaled_images_log.csv"

# Styles to apply
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
    with open(image_path, "rb") as file:
        files = {"file": file}
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
        logger.info(f"Failed to upscale image: {response.status_code} {response.text}")
        return None
    """get_upscaled_image function."""


def get_upscaled_image(variation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/variations/{variation_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == CONSTANT_200:
        return response.json()
    else:
        logger.info(
            f"Failed to get upscaled image: {response.status_code} {response.text}"
        )
        return None


def initialize_csv(file_path):
    """Initialize the CSV file with headers."""
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "generation_id",
                "created_at",
                "nsfw",
                "like_count",
                "generation_status",
                "image_id",
                "variant_id",
                "variant_url",
                "variant_status",
                "variant_transformation",
            ]
        )


def log_to_csv(file_path, data):
    """Log data to the CSV file."""
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)


# Initialize CSV file
initialize_csv(output_csv)

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.lower().endswith(
        (".jpg", ".jpeg", ".png", ".tiff", ".webp")
    ):  # Check for supported image formats
        full_path = os.path.join(directory_path, filename)

        # Convert image to JPEG format if necessary
        if not filename.lower().endswith(".jpg"):
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
                    time.sleep(
                        60
                    )  # Wait for processing, adjust this based on actual processing time
                    upscaled_image_data = get_upscaled_image(variation_id)
                    if upscaled_image_data:
                        image_url = upscaled_image_data.get(
                            "imageUrl", "No URL available"
                        )
                        if image_url == "No URL available":
                            logger.info(
                                f"URL not available for variation ID: {variation_id}"
                            )

                        generation_data = [
                            init_image_id,
                            datetime.now().isoformat(),
                            False,
                            0,
                            "COMPLETE",
                            init_image_id,
                            variation_id,
                            image_url,
                            "COMPLETE",
                            "UPSCALE",
                        ]
                        log_to_csv(output_csv, generation_data)
                        print(
                            f"Logged upscaled image data for '{filename}' with style '{style}'"
                        )

            # Pause before processing the next image
            time.sleep(CONSTANT_120)  # Wait to avoid spamming the server

    else:
        continue
