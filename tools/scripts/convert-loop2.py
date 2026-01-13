import csv
import json
import os
import time
from datetime import datetime

import requests
from PIL import Image

api_key = "de7c9cb8-022f-42f8-8bf7-a8f9caadfaee"
authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Directory containing images
directory_path = "/Users/steven/Pictures/TrashCaT/trashy-heartbreak"
output_csv = "upscaled_images_log.csv"

# Styles to apply
styles = ["GENERAL", "CINEMATIC", "2D ART & ILLUSTRATION", "CG ART & GAME ASSETS"]


def convert_image_to_jpeg(input_path, output_path, dpi=400):
    """Convert an image to JPEG format with specified DPI."""
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, "JPEG", dpi=(dpi, dpi))


def get_presigned_url():
    url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
    payload = {"extension": "jpg"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["uploadInitImage"]
    else:
        print(f"Failed to get presigned URL: {response.status_code}")
        return None


def upload_image(fields, presigned_url, image_path):
    files = {"file": open(image_path, "rb")}
    response = requests.post(presigned_url, data=fields, files=files)
    return response.status_code == 204


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
    if response.status_code == 200:
        return response.json()["universalUpscaler"]["id"]
    else:
        print(
            f"Failed to upscale image: {
                response.status_code} {
                response.text}"
        )
        return None


def get_upscaled_image(variation_id):
    url = f"https://cloud.leonardo.ai/api/rest/v1/variations/{variation_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get upscaled image: {response.status_code}")
        return None


# Initialize CSV file
with open(output_csv, mode="w", newline="") as file:
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
            print(f"Converted {filename} to {full_path}")

        # Get a presigned URL for uploading an image
        presigned_data = get_presigned_url()
        if not presigned_data:
            continue

        fields = json.loads(presigned_data["fields"])
        presigned_url = presigned_data["url"]
        init_image_id = presigned_data["id"]

        # Upload the image
        if upload_image(fields, presigned_url, full_path):
            print(f"Uploaded image '{filename}'")

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
                    print(f"Upscaled image '{filename}' with style '{style}'")
                    # Wait for processing, adjust this based on actual
                    # processing time
                    time.sleep(60)
                    upscaled_image_data = get_upscaled_image(variation_id)
                    if upscaled_image_data:
                        generation_data = [
                            init_image_id,
                            datetime.now().isoformat(),
                            False,
                            0,
                            "COMPLETE",
                            init_image_id,
                            variation_id,
                            upscaled_image_data.get("imageUrl", "No URL available"),
                            "COMPLETE",
                            "UPSCALE",
                        ]
                        with open(output_csv, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow(generation_data)
                        print(
                            f"Logged upscaled image data for '{filename}' with style '{style}'"
                        )

            # Pause before processing the next image
            time.sleep(120)  # Wait to avoid spamming the server

    else:
        continue
