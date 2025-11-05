from pathlib import Path
import json
import os
import time

import requests

from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


load_dotenv()

api_key = os.getenv("LEONARDO_API_KEY")
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Directory containing images
directory_path = Path(str(Path.home()) + "/Pictures/CookiMonster/1")

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".jpg"):  # Check if the file is a JPEG image
        full_path = os.path.join(directory_path, filename)

        # Get a presigned URL for uploading an image
        url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
        payload = {"extension": "jpg"}
        response = requests.post(url, json=payload, headers=headers)
        print(
            "Get a presigned URL for uploading image '%s': %s"
            % (filename, response.status_code)
        )

        # Upload image via presigned URL
        fields = json.loads(response.json()["uploadInitImage"]["fields"])
        url = response.json()["uploadInitImage"]["url"]
        image_id = response.json()["uploadInitImage"]["id"]
        files = {"file": open(full_path, "rb")}
        response = requests.post(url, data=fields, files=files)  # Header is not needed
        print(
            "Upload image '%s' via presigned URL: %s" % (filename, response.status_code)
        )

        # Create upscale with Universal Upscaler
        url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"
        payload = {
            "upscalerStyle": "2D ART & ILLUSTRATION",
            "creativityStrength": 8,
            "upscaleMultiplier": 1.5,
            "initImageId": image_id,
        }
        response = requests.post(url, json=payload, headers=headers)
        print(
            "Universal Upscaler variation for '%s': %s"
            % (filename, response.status_code)
        )

        # Get upscaled image via variation Id
        variation_id = response.json()["universalUpscaler"]["id"]
        url = "https://cloud.leonardo.ai/api/rest/v1/variations/%s" % variation_id
        time.sleep(60)
        response = requests.get(url, headers=headers)
        print(
            "Get upscaled image '%s' via variation Id: %s" % (filename, response.text)
        )

    else:
        continue
