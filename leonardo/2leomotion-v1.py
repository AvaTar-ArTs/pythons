"""
2Leomotion 5

This module provides functionality for 2leomotion 5.

Author: Auto-generated
Date: 2025-11-01
"""

import requests
import time

import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_544 = 544
CONSTANT_960 = 960
CONSTANT_1082 = 1082


load_dotenv()

api_key = os.getenv("LEONARDO_API_KEY")
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization,
}

# Generate an image
url = "https://cloud.leonardo.ai/api/rest/v1/generations"

payload = {
    "height": CONSTANT_960,
    "modelId": "ac614f96-CONSTANT_1082-45bf-be9d-757f2d31c174",
    "prompt": "A detailed photograph of a serious cyberpunk Hacker Cyborg transhumanist the past looking directly at the camera, standing straight, hands relaxed, square jaws, masculine face, dark scruff and no wrinkles, slightly buff looking, wearing a dark graphic t-shirt, detailed clothing texture realistic skin texture, black background, sharp focus, front view, waist up shot, high contrast, strong backlighting, action film dark color lut, cinematic luts",
    "negative_prompt": "black and white, grainy, extra limbs, bad anatomy, airbrush, portrait, zoomed, soft light,smooth skin, closeup, vignette, out of shot, out of focus, portrait, statue, white statue, hands, bad anatomy, badhands, extra fingers, extra limbs, colored background, side profile, 3/4 view, 3/4 face, side view, 3/4 angle,detailed background, scenery, brownish background",
    "width": CONSTANT_544,
    "num_images": 1,
    "alchemy": True,
    "public": True,
}

response = requests.post(url, json=payload, headers=headers)

logger.info("Generate an image: %s" % response.status_code)

# Get the generation of images
generation_id = response.json()["sdGenerationJob"]["generationId"]

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

time.sleep(60)

response = requests.get(url, headers=headers)

logger.info("Get the generation of images: %s" % response.status_code)

image_id = response.json()["generations_by_pk"]["generated_images"][0]["id"]

# Create a variation of image (upscale variation)
url = "https://cloud.leonardo.ai/api/rest/v1/variations/upscale"

payload = {"id": image_id}

response = requests.post(url, json=payload, headers=headers)

variation_id = response.json()["sdUpscaleJob"]["id"]

logger.info("Create a variation of image: %s" % response.status_code)

# Get the image variation
url = "https://cloud.leonardo.ai/api/rest/v1/variations/%s" % variation_id

time.sleep(60)

response = requests.get(url, headers=headers)

logger.info("Get the image variation: %s" % response.status_code)

image_variation_id = response.json(
)["generated_image_variation_generic"][0]["id"]

# Generate video with a generated image
url = "https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd"

payload = {
    "imageId": image_variation_id,
    "motionStrength": 5,
    "isVariation": True,
}

response = requests.post(url, json=payload, headers=headers)

logger.info("Generate video with a generated image: %s" % response.status_code)

# Get the generation of images
generation_id = response.json()["motionSvdGenerationJob"]["generationId"]

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

time.sleep(60)

response = requests.get(url, headers=headers)

logger.info(response.text)
