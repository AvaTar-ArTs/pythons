import os
import time

import requests

# Get the API key from the environment variable
API_KEY = os.getenv("VANCEAI_API_KEY")
API_URL = "https://api-service.vanceai.com/web_api/v1/removebg"
PROGRESS_URL = "https://api-service.vanceai.com/web_api/v1/progress"


def remove_background(input_path, output_path):
    with open(input_path, "rb") as file:
        response = requests.post(
            API_URL, files={"image_file": file}, headers={"api_key": API_KEY}
        )

    if response.status_code == 200:
        result = response.json()
        trans_id = result["trans_id"]
        download_result(trans_id, output_path)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def download_result(trans_id, output_path):
    while True:
        response = requests.get(
            f"{PROGRESS_URL}?trans_id={trans_id}&api_token={API_KEY}"
        )

        if response.status_code == 200:
            progress_result = response.json()
            status = progress_result["data"]["status"]
            if status == "finish":
                image_url = progress_result["data"]["image_url"]
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    with open(output_path, "wb") as out_file:
                        out_file.write(image_response.content)
                    print(f"Background removed and saved to {output_path}")
                else:
                    print(f"Error downloading image: {image_response.status_code}")
                break
            elif status == "fatal":
                print("Image processing failed.")
                break
            else:
                print(f"Current status: {status}. Checking again in 2 seconds.")
                time.sleep(2)
        else:
            print(f"Request failed: {response.status_code}")
            break


def process_directory(input_dir):
    output_dir = os.path.join(input_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, f"{os.path.splitext(filename)[0]}.png"
            )
            remove_background(input_path, output_path)


if __name__ == "__main__":
    input_directory = input("Enter the path to the source directory: ")
    if os.path.isdir(input_directory):
        process_directory(input_directory)
    else:
        print("The specified directory does not exist.")
