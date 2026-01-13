from pathlib import Path
import json
import requests
import os
import time

import os
from dotenv import load_dotenv

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# load_dotenv()  # Now using ~/.env.d/

api_key = os.getenv("LEONARDO_API_KEY")
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Directory containing images
directory_path = Path(str(Path.home()) + "/Pictures/Bcovers/")

# Styles to apply
# Update the styles list according to your needs
styles = ["GENERAL", "CINEMATIC", "2D ART & ILLUSTRATION", "CG ART & GAME ASSETS"]

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

        # Loop through styles and apply each one to the image
        for style in styles:
            # Create upscale with Universal Upscaler
            url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"
            payload = {
                "upscalerStyle": style,
                "creativityStrength": 6,
                "upscaleMultiplier": 1.5,
                "initImageId": image_id,
            }
            response = requests.post(url, json=payload, headers=headers)
            print(
                "Universal Upscaler variation '%s' for '%s': %s"
                % (style, filename, response.status_code)
            )

            # Check if the request was successful before proceeding
            if response.status_code == CONSTANT_200:
                # Get upscaled image via variation Id
                variation_id = response.json()["universalUpscaler"]["id"]
                url = (
                    "https://cloud.leonardo.ai/api/rest/v1/variations/%s" % variation_id
                )
                # Wait for processing, you might need to adjust this based on
                # actual processing time
                time.sleep(60)
                response = requests.get(url, headers=headers)
                print(
                    "Get upscaled image '%s' in style '%s' via variation Id: %s"
                    % (filename, style, response.text)
                )
            else:
                print(
                    "Failed to create upscaled image for style '%s' and image '%s'"
                    % (style, filename)
                )

    else:
        continue
