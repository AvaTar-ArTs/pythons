from pathlib import Path
import json
import time

import requests

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_204 = 204



def upload_image(api_key, image_file_path):
 headers = {
 "accept": "application/json",
 "content-type": "application/json",
 "authorization": f"Bearer {api_key}"
 }
 
 # Get a presigned URL for uploading an image
 url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

 payload = {"extension": "jpg"}
 response = requests.post(url, json=payload, headers=headers)

 if response.status_code != CONSTANT_200:
 logger.info(f"Failed to get presigned URL: {response.status_code} {response.text}")
 return None

 presigned_data = response.json()['uploadInitImage']
 fields = presigned_data['fields']
 presigned_url = presigned_data['url']
 image_id = presigned_data['id']
 
 files = {'file': open(image_file_path, 'rb')}
 response = requests.post(presigned_url, data=fields, files=files)

 if response.status_code != CONSTANT_204:
 logger.info(f"Failed to upload image: {response.status_code} {response.text}")
 return None

 logger.info("Image uploaded successfully")

 return image_id

def upscale_image(api_key, image_id):
 url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"
 headers = {
 "accept": "application/json",
 "content-type": "application/json",
 "authorization": f"Bearer {api_key}"
 }

 payload = {
 "upscalerStyle": "Cinematic",
 "creativityStrength": 6,
 "upscaleMultiplier": 1.5,
 "initImageId": image_id
 }

 response = requests.post(url, json=payload, headers=headers)

 if response.status_code != CONSTANT_200:
 logger.info(f"Failed to create upscale: {response.status_code} {response.text}")
 return None

 variation_id = response.json()['universalUpscaler']['id']

 return variation_id

def get_upscaled_image(api_key, variation_id):
 headers = {
 "accept": "application/json",
 "authorization": f"Bearer {api_key}"
 }

 url = f"https://cloud.leonardo.ai/api/rest/v1/variations/{variation_id}"

 time.sleep(60) # Wait for processing

 response = requests.get(url, headers=headers)

 if response.status_code != CONSTANT_200:
 logger.info(f"Failed to get upscaled image: {response.status_code} {response.text}")
 return None

 return response.json()

def main():
 api_key = "<YOUR_API_KEY>"
 image_file_path = Path("/path/to/your/image.jpg")

 image_id = upload_image(api_key, image_file_path)
 
 if not image_id:
 return

 variation_id = upscale_image(api_key, image_id)

 if not variation_id:
 return

 upscaled_image_data = get_upscaled_image(api_key, variation_id)

 if upscaled_image_data:
 # Process the upscaled image data as needed
 pass

if __name__ == "__main__":
 main()
