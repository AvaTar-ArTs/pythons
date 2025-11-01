"""
Youtube Api Client

This module provides functionality for youtube api client.

Author: Auto-generated
Date: 2025-11-01
"""

import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_512 = 512
CONSTANT_4334 = 4334


# API URL
url = "https://cloud.leonardo.ai/api/rest/v1/generations"

# Payload for the POST request
payload = {
    "height": CONSTANT_512,
    "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
    "prompt": "Create a vibrant and lively image featuring a front-facing, centered group of the CoTTonWooDs, the adorable inhabitants of Itchy Isle. These fluffy creatures should be depicted in a range of pastel colors, each exuding unique personality and joy. Imagine them with soft, cotton-like textures, big, sparkling eyes full of wonder, and wide, beaming smiles. They should have playful tufts of hair styled in whimsical ways, resembling colorful strands of yarn. The background should be a cheerful blur of Itchy Isle's signature landmarks - macrame houses, yarn trees, and a rainbow-streaked sky. The overall atmosphere of the image should be one of happiness, friendship, and the magical essence of a carefree, enchanting world.",
    "width": CONSTANT_512,
}

# Headers for the POST request
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer 7ccf0307-636e-CONSTANT_4334-9a61-814202374698",
}

# Sending the POST request and getting the response
response = requests.post(url, json=payload, headers=headers)

# Printing the response
logger.info(response.text)
