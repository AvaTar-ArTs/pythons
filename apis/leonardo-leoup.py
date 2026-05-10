# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip("'").strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import json
import os
import time

import requests

import logging

logger = logging.getLogger(__name__)


api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError(
        "API key is not set. Please ensure the API_KEY environment variable is configured correctly."
    )

authorization = f"Bearer {api_key}"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Get a presigned URL for uploading an image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

payload = {"extension": "jpg"}

response = requests.post(url, json=payload, headers=headers)

logger.info(response.text)

logger.info("Get a presigned URL for uploading an image: %s" % response.status_code)

# Upload image via presigned URL
fields = json.loads(response.json()["uploadInitImage"]["fields"])

url = response.json()["uploadInitImage"]["url"]

logger.info("Presigned URL: %s" % url)

# For getting the image later
image_id = response.json()["uploadInitImage"]["id"]

image_file_path = ""
files = {"file": open(image_file_path, "rb")}

response = requests.post(url, data=fields, files=files)  # Header is not needed

logger.info("Upload image via presigned URL: %s" % response.status_code)


# Create upscale with Universal Upscaler
url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"

payload = {
    "upscalerStyle": "2D ART & ILLUSTRATION",
    "creativityStrength": 6,
    "upscaleMultiplier": 1.5,
    "initImageId": image_id,
}


response = requests.post(url, json=payload, headers=headers)

logger.info(response.text)
logger.info("Universal Upscaler variation: %s" % response.status_code)

# Get upscaled image via variation Id
variation_id = response.json()["universalUpscaler"]["id"]

url = "https://cloud.leonardo.ai/api/rest/v1/variations/%s" % variation_id

time.sleep(60)

response = requests.get(url, headers=headers)

logger.info(response.text)
