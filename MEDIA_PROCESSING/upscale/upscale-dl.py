import os
import time

import requests

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

image_directory = "/Users/steven/Pictures/zombot"
# Directory to save upscaled images
download_directory = "/Users/steven/Pictures/zombot/upscaled"

# Ensure download directory exists
os.makedirs(download_directory, exist_ok=True)

for filename in os.listdir(image_directory):
    if filename.endswith(".jpg"):
        image_file_path = os.path.join(image_directory, filename)

        # Get a presigned URL for uploading an image
        url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
        payload = {"extension": "jpg"}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print(
                f""Get a presigned URL for uploading image '{filename}': {
                    response.status_code
                }"
            )
            fields = response.json()["uploadInitImage"]["fields"]
            url = response.json()["uploadInitImage"]["url"]
            image_id = response.json()["uploadInitImage"]["id"]

            with open(image_file_path, "rb") as f:
                files = {"file": f}
                response = requests.post(url, data=fields, files=files)

            # Handling image upload response
            if response.status_code == 200:
                print(
                    f""Uploaded image '{filename}' via presigned URL: {
                        response.status_code
                    }"
                )

                # Create upscale with Universal Upscaler
                url = "https://cloud.leonardo.ai/api/rest/v1/variations/universal-upscaler"
                payload = {
                    "upscalerStyle": "Cinematic",
                    "creativityStrength": 6,
                    "upscaleMultiplier": 1.5,
                    "initImageId": image_id,
                }
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    variation_id = response.json()["universalUpscaler"]["id"]

                    # Wait for the upscaling process to complete
                    time.sleep(120)

                    # Fetch the upscaled image
                    url = f"https://cloud.leonardo.ai/api/rest/v1/variations/{variation_id}"
                    response = requests.get(url, headers=headers)

                    if response.status_code == 200:
                        # Saving the image
                        upscaled_image_path = os.path.join(
                            download_directory, f"upscaled_{filename}"
                        )
                        with open(upscaled_image_path, "wb") as f:
                            f.write(response.content)
                        print(f"Upscaled image saved as '{upscaled_image_path}'")
                    else:
                        print(
                            f""Failed to download the upscaled image for '{
                                filename
                            }', status code: {response.status_code}"
                        )
                else:
                    print(
                        f""Failed to upscale image '{filename}', status code: {
                            response.status_code
                        }"
                    )
            else:
                print(
                    f""Failed to upload image '{filename}', status code: {
                        response.status_code
                    }"
                )
        else:
            print(
                f""Failed to get URL for '{filename}', status code: {
                    response.status_code
                }"
            )
    else:
        print(f"Skipping non-jpg file: {filename}")
