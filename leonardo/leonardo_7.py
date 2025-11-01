"""
Leonardo 7

This module provides functionality for leonardo 7.

Author: Auto-generated
Date: 2025-11-01
"""

import json
import os
import sys
import time

import requests
from PIL import Image

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_204 = 204
CONSTANT_400 = 400


api_key = "de7c9cb8-022f-42f8-8bf7-a8f9caadfaee"
authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Styles to apply
styles = ["GENERAL", "CINEMATIC", "2D_ART_ILLUSTRATION", "PHOTOREALISTIC"]


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
    """process_images function."""

        return None


def process_images(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith((".jpg", ".jpeg", ".png", ".tiff", ".webp")):
            full_path = os.path.join(directory_path, filename)

            if not filename.endswith(".jpg"):
                converted_path = full_path.rsplit(".", 1)[0] + ".jpg"
                convert_image_to_jpeg(full_path, converted_path)
                full_path = converted_path
                logger.info(f"Converted {filename} to {full_path}")

            presigned_data = get_presigned_url()
            if not presigned_data:
                continue

            fields = json.loads(presigned_data["fields"])
            presigned_url = presigned_data["url"]
            init_image_id = presigned_data["id"]

            if upload_image(fields, presigned_url, full_path):
                logger.info(f"Uploaded image '{filename}'")

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.info("Usage: python script.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        process_images(directory_path)
