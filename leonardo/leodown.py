"""
Leodown

This module provides functionality for leodown.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import json

import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# Base URL for API
base_url = "https://cloud.leonardo.ai/api/rest/v1/generations/user/f7bb8476-e3f0-4f1f-9a06-4600866cc49c"
headers = {
    "accept": "application/json",
    "authorization": "Bearer f7bb8476-e3f0-4f1f-9a06-4600866cc49c",  # Replace with your actual token
}

# Output file
output_file = Path("/Users/steven/Pictures/leonardo_library.json")

# Pagination parameters
offset = 0
limit = 10  # Maximum number of items per request
all_generations = []

while True:
    # Request URL with pagination
    url = f"{base_url}?offset={offset}&limit={limit}"
    response = requests.get(url, headers=headers)

    # Check response status
    if response.status_code != CONSTANT_200:
        logger.info(f"Failed to fetch data: {response.status_code}, {response.text}")
        break

    # Parse JSON response
    data = response.json()
    generations = data.get("generations", [])

    # Add to the master list
    all_generations.extend(generations)

    # Check if there are more items to fetch
    if len(generations) < limit:
        break  # No more items to fetch

    # Update offset
    offset += limit

# Save all data to a JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(all_generations, file, indent=4)

logger.info(f"Library downloaded and saved to {output_file}")
