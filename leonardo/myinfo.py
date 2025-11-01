"""
Myinfo

This module provides functionality for myinfo.

Author: Auto-generated
Date: 2025-11-01
"""

import json

import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


url = "https://cloud.leonardo.ai/api/rest/v1/generations/user/f7bb8476-e3f0-4f1f-9a06-4600866cc49c?offset=0&limit=1000"
headers = {
    "accept": "application/json",
    "authorization": "Bearer de7c9cb8-022f-42f8-8bf7-a8f9caadfaee",
}

response = requests.get(url, headers=headers)
if response.status_code == CONSTANT_200:
    data = response.json()
    logger.info(json.dumps(data, indent=4))  # Pretty print the JSON data
else:
    logger.info(f"Failed to fetch data: {response.status_code}")
