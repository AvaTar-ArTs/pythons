"""
Motion Upload 2

This module provides functionality for motion upload 2.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import json
import time

import requests

import logging

logger = logging.getLogger(__name__)


api_key = "<YOUR_API_KEY>"
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Get a presigned URL for uploading an image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

payload = {"extension": "jpg"}

response = requests.post(url, json=payload, headers=headers)

logger.info("Get a presigned URL for uploading an image: %s" % response.status_code)

# Upload image via presigned URL
fields = json.loads(response.json()["uploadInitImage"]["fields"])

url = response.json()["uploadInitImage"]["url"]

image_id = response.json()["uploadInitImage"]["id"]  # For getting the image later

image_file_path = Path("/Users/steven/Pictures/zombot/default_a_detailed_photograph_of_a_serious_cyberpunk_zombot_cy_0_fb6f4194-86a6-4f09-be49-57de04fc667a_unzoom.jpg")
files = {"file": open(image_file_path, "rb")}

response = requests.post(url, data=fields, files=files)  # Header is not needed

logger.info("Upload image via presigned URL: %s" % response.status_code)

# Generate video with an init image
url = "https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd"

payload = {"imageId": image_id, "isInitImage": True, "motionStrength": 5}

response = requests.post(url, json=payload, headers=headers)

logger.info("Generate video with an init image: %s" % response.status_code)

# Get the generated video
generation_id = response.json()["motionSvdGenerationJob"]["generationId"]

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

time.sleep(60)

response = requests.get(url, headers=headers)

logger.info(response.text)
