"""
Upscale

This module provides functionality for upscale.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import json
import requests
import time

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_8049 = 8049


api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API key is not set. Please ensure the API_KEY environment variable is configured correctly.")

authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# Get a presigned URL for uploading an image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

payload = {"extension": "jpg"}

response = requests.post(url, json=payload, headers=headers)

logger.info(response.text)

logger.info("Get a presigned URL for uploading an image: %s" % response.status_code)

# Upload image via presigned URL
fields = json.loads(response.json()['uploadInitImage']['fields'])

url = response.json()['uploadInitImage']['url']

logger.info("Presigned URL: %s" % url)

# For getting the image later
image_id = response.json()['uploadInitImage']['id']

image_file_path = Path("/Users/steven/Pictures/zombot/default_a_detailed_photograph_of_a_serious_cyberpunk_zombot_cy_0_bb72aa30-CONSTANT_8049-48da-ab22-c5306913a325_unzoom.jpg")
files = {'file': open(image_file_path, 'rb')}

response = requests.post(url, data=fields, files=files)  # Header is not needed

logger.info("Upload image via presigned URL: %s" % response.status_code)


# Create upscale with Universal Upscaler
url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"

payload = {

    "upscalerStyle": "Cinematic",
    "creativityStrength": 6,
    "upscaleMultiplier": 1.5,
    "initImageId": image_id

}


response = requests.post(url, json=payload, headers=headers)

logger.info(response.text)
logger.info("Universal Upscaler variation: %s" % response.status_code)

# Get upscaled image via variation Id
variation_id = response.json()['universalUpscaler']['id']

url = "https://cloud.leonardo.ai/api/rest/v1/variations/%s" % variation_id

time.sleep(60)

response = requests.get(url, headers=headers)

logger.info(response.text)
