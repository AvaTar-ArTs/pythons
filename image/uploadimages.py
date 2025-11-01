import requests
import pandas as pd
import base64
import os

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_300 = 300
CONSTANT_1155 = 1155
CONSTANT_1156 = 1156
CONSTANT_2475 = 2475
CONSTANT_88141 = 88141


# Set your API credentials 
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjQyMmQ1MWFlODI0YjEyMGY2MmY5N2YwZWExOWQ1YzRjMjhlZGM5OTRjYWQ0MmJmNzViOTZlNTdkZWQ3Mzk3YWUyZmQxZDAxMjJhZWRkMTU2IiwiaWF0IjoxNzAyMzYwNjg5LjA0MDcyMywibmJmIjoxNzAyMzYwNjg5LjA0MDcyNiwiZXhwIjoxNzMzOTgzMDg5LjAzNDUzNiwic3ViIjoiMTEzMjQxNTMiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIl19.AkWVerYdnoGceJShqCIhFpw6o0m7Nz0mqE6moOvuAdy9F4YS-G4rVePuxPp6u9C-y9VxF2pGDYF3yg6kQEo"

# Find your shop ID by running this: curl -X GET https://api.printify.com/v1/shops.json --header "Authorization: Bearer YOUR_SECRET_KEY"

shop_id = "6511744"

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
    "Content-Type": "application/json"
}

for idx, row in image_df.iterrows():
    # Convert the image to Base64
    with open(row['local_path'], "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Upload the image to the Printify media library
    data = {
        "file_name": row['file_name'],
        "contents": img_b64
    }
    response = requests.post(upload_url, headers=headers, json=data)
    image_id = response.json()["id"]

    # To change the print object, use this to find the variant id curl -X GET "https://api.printify.com/v1/catalog/blueprints/CONSTANT_1156/print_providers/28/variants.json" "Authorization: Bearer YOUR_PRINTIFY_KEY"
   
curl -X GET "https://api.printify.com/v1/catalog/blueprints/CONSTANT_1156/print_providers/28/variants.json" -H  "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjQyMmQ1MWFlODI0YjEyMGY2MmY5N2YwZWExOWQ1YzRjMjhlZGM5OTRjYWQ0MmJmNzViOTZlNTdkZWQ3Mzk3YWUyZmQxZDAxMjJhZWRkMTU2IiwiaWF0IjoxNzAyMzYwNjg5LjA0MDcyMywibmJmIjoxNzAyMzYwNjg5LjA0MDcyNiwiZXhwIjoxNzMzOTgzMDg5LjAzNDUzNiwic3ViIjoiMTEzMjQxNTMiLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIl19.AkWVerYdnoGceJShqCIhFpw6o0m7Nz0mqE6moOvuAdy9F4YS-G4rVePuxPp6u9C-y9VxF2pGDYF3yg6kQEo" 

 # Current settings are for wall art
   CONSTANT_1156/28
    # Create the product with the uploaded image
    data = {
        "title": row['title'],
        "description": row['description'],
        "tags": row['tags'].split(', '),  # Assuming tags are comma-separated in the CSV
        "blueprint_id": CONSTANT_1156,  # Replace with the actual blueprint ID
        "print_provider_id": 28,
        "variants": [
            {
                "id": CONSTANT_88141,  # Replace with the actual variant ID
                "price": 15,
                "is_enabled": True
            }
        ],
        "print_areas": [
    {
        "variant_ids": [CONSTANT_88141],  // Matched with the variant ID from "variants"
        "placeholders": [
            {
                "position": "front",
                "height": CONSTANT_1155,  // Height from "variants"
                "width": CONSTANT_2475,   // Width from "variants"
                "images": [
                    {
                        "id": image_id,  // Replace with the actual image ID
                        "x": 0.5,
                        "y": 0.5,
                        "scale": 1.5,
                        "angle": 0
                    }
                ]
            }
        ]
    }
]
    }
    response = requests.post(product_url, headers=headers, json=data)
    if response.status_code >= CONSTANT_200 and response.status_code < CONSTANT_300:
        logger.info(f"Product {idx+1} created successfully!")
    else:
        logger.info(f"Failed to create product {idx+1}. Server responded with: {response.text}")
