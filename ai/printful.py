"""
Printful

This module provides functionality for printful.

Author: Auto-generated
Date: 2025-11-01
"""

import base64
import os

import pandas as pd
import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_480 = 480
CONSTANT_3999 = 3999
CONSTANT_71689 = 71689


# Set your API credentials
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImVjYjNlYTBlMDk0OWIzZDA1Y2ZiODk4N2EwYzU5NzU5ZTE0NzBmMjIzYzQ0ODViN2M0OWU0YWFkNTY5MGMxODM4MTc5N2Y4Y2RkZDE0MzBjIiwiaWF0IjoxNzM4MTk4MTA4LjkwNDQxMiwibmJmIjoxNzM4MTk4MTA4LjkwNDQxNCwiZXhwIjoxNzY5NzM0MTA4Ljg5NzE0Nywic3ViIjoiMTEzMjQxNTMiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIiwidXNlci5pbmZvIl19.AHO8pARL74uPg4bASasg_De9T9X50a29R014NE7TwFkPpT2R58TfeCA2Ygsyj4TQSXhg0g54cou2uY0ifJg"

# Find your shop ID by running this: curl -X GET https://api.printify.com/v1/catalog/blueprints.json --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImVjYjNlYTBlMDk0OWIzZDA1Y2ZiODk4N2EwYzU5NzU5ZTE0NzBmMjIzYzQ0ODViN2M0OWU0YWFkNTY5MGMxODM4MTc5N2Y4Y2RkZDE0MzBjIiwiaWF0IjoxNzM4MTk4MTA4LjkwNDQxMiwibmJmIjoxNzM4MTk4MTA4LjkwNDQxNCwiZXhwIjoxNzY5NzM0MTA4Ljg5NzE0Nywic3ViIjoiMTEzMjQxNTMiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIiwidXNlci5pbmZvIl19.AHO8pARL74uPg4bASasg_De9T9X50a29R014NE7TwFkPpT2R58TfeCA2Ygsyj4TQSXhg0g54cou2uY0ifJg"

shop_id = "19528660"

# Set the URL for the API endpoints
base_url = "https://api.printify.com/v1"
upload_url = f"{base_url}/uploads/images.json"
product_url = f"{base_url}/shops/{shop_id}/products.json"

# Load the CSV file
csv_path = "product_information.csv"  # Update this to your CSV file path
image_df = pd.read_csv(csv_path)

# Set headers for requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

for idx, row in image_df.iterrows():
    # Convert the image to Base64
    with open(row["local_path"], "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    # Upload the image to the Printify media library
    data = {"file_name": row["file_name"], "contents": img_b64}
    response = requests.post(upload_url, headers=headers, json=data)
    image_id = response.json()["id"]

    # To change the print object, use this to find the variant id curl -X GET "https://api.printify.com/v1/catalog/blueprints/852/print_providers/73/variants.json" -H "Authorization: Bearer YOUR_PRINTIFY_KEY"

    # Current settings are for cork art

    # Create the product with the uploaded image
    data = {
        "title": row["title"],
        "description": row["description"],
        "tags": row["tags"].split(", "),  # Assuming tags are comma-separated in the CSV
        "blueprint_id": CONSTANT_480,  # Replace with the actual blueprint ID
        "print_provider_id": 70,
        "variants": [
            {
                "id": CONSTANT_71689,  # Replace with the actual variant ID
                "price": CONSTANT_3999,
                "is_enabled": True,
            }
        ],
        "print_areas": [
            {
                "variant_ids": [CONSTANT_71689],  # Replace with the actual variant ID
                "placeholders": [
                    {
                        "position": "front",
                        "images": [
                            {
                                "id": image_id,
                                "x": 0.5,
                                "y": 0.5,
                                "scale": 1.0,
                                "angle": 0,
                            }
                        ],
                    }
                ],
            }
        ],
    }
    response = requests.post(product_url, headers=headers, json=data)
    if response.status_code >= CONSTANT_200 and response.status_code < CONSTANT_300:
        logger.info(f"Product {idx+1} created successfully!")
    else:
        print(f"Failed to create product {idx+1}. Server responded with: {response.text}")
