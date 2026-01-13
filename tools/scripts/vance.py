import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def upscale_image(api_token, image_path, scale):
    try:
        url = "https://api-service.vanceai.com/web_api/v1/enlarge3"
        headers = {"Authorization": f"Bearer {api_token}"}

        with open(image_path, "rb") as image_file:
            files = {"image": image_file}
            params = {
                "model_name": (
                    "EnlargeStandard_2x_Stable"
                    if scale == 2
                    else "EnlargeStandard_4x_Stable"
                ),
                "suppress_noise": 40,
                "remove_blur": 60,
                "scale": scale,
            }

            response = requests.post(url, headers=headers, files=files, data=params)
            response.raise_for_status()  # Check if request was successful
            response_data = response.json()
            trans_id = response_data["data"]["trans_id"]

            while True:
                progress_response = requests.get(
                    f"https://api-service.vanceai.com/web_api/v1/progress?trans_id={trans_id}&api_token={api_token}"
                )
                progress_response.raise_for_status()
                progress_data = progress_response.json()
                status = progress_data["data"]["status"]

                if status == "finish":
                    image_url = progress_data["data"]["image_url"]
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    output_path = os.path.join("output", os.path.basename(image_path))
                    with open(output_path, "wb") as output_file:
                        output_file.write(image_response.content)
                    logging.info(f"Image processing finished for {image_path}")
                    return output_path, "success"
                elif status == "fatal":
                    logging.error(f"Image processing failed for {image_path}")
                    return None, "processing failed"
                else:
                    time.sleep(2)
        logging.error(
            f"Initial request failed for {image_path}: {response.status_code}"
        )
        return None, f"initial request failed: {response.status_code}"
    except requests.RequestException as e:
        logging.error(f"Request error for {image_path}: {e}")
        return None, f"request error: {e}"
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")
        return None, f"error: {e}"


def process_image(api_token, image_path, scale):
    output_path, status = upscale_image(api_token, image_path, scale)
    return {
        "input_image": image_path,
        "output_image": output_path,
        "status": status,
        "action": f"upscale {scale}x",
    }


def process_directory(api_token, input_dir, scale, max_workers=4):
    results = []
    os.makedirs("output", exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_image = {
            executor.submit(
                process_image, api_token, os.path.join(input_dir, image_filename), scale
            ): image_filename
            for image_filename in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, image_filename))
        }
        for future in as_completed(future_to_image):
            image_filename = future_to_image[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logging.error(f"Error processing {image_filename}: {e}")

    results_df = pd.DataFrame(results)
    results_df.to_csv("image_upscaling_results.csv", index=False)
    logging.info("Processing completed. Results saved to image_upscaling_results.csv")


# Usage example
api_token = os.getenv("VANCEAI_API_TOKEN")
input_directory = "/Users/steven/Pictures/City"
scale_factor = 2  # Set the desired scale factor (2, 4, 6, 8)
process_directory(api_token, input_directory, scale_factor)
