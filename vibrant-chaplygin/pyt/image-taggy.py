import os
import zipfile
import tempfile
import csv
import requests
import boto3
import subprocess
import cv2
from clarifai.client.model import Model
from dotenv import load_dotenv
from PIL import Image

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


load_dotenv(os.path.expanduser("~/.env"))

# API keys
CLARIFAI_PAT = os.getenv("CLARIFAI_PAT")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
IMAGGA_API_KEY = os.getenv("IMAGGA_API_KEY")
IMAGGA_API_SECRET = os.getenv("IMAGGA_API_SECRET")

clarifai_model = Model(model_id="general-image-recognition", pat=CLARIFAI_PAT)
rekognition = boto3.client(
    "rekognition",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def get_clarifai_tags(image_path):
    try:
        with open(image_path, "rb") as f:
            response = clarifai_model.predict_by_bytes(f.read(), input_type="image")
        return [c["name"] for c in response["outputs"][0]["data"]["concepts"]]
    except Exception as e:
        logger.info(f"❌ Clarifai error: {e}")
        return ["ERROR"]
def get_rekognition_tags(image_path):
    try:
        with open(image_path, "rb") as f:
            response = rekognition.detect_labels(Image={"Bytes": f.read()})
        return [l["Name"] for l in response["Labels"]]
    except Exception as e:
        logger.info(f"❌ Rekognition error: {e}")
        return ["ERROR"]

def get_imagga_tags(image_path):
    try:
        with open(image_path, "rb") as img:
            response = requests.post(
                "https://api.imagga.com/v2/tags",
                auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET),
                files={"image": img},
            )
        tags = response.json().get("result", {}).get("tags", [])
        return [tag["tag"]["en"] for tag in tags[:10]]
    except Exception as e:
        logger.info(f"❌ Imagga error: {e}")
        return ["ERROR"]


def extract_video_frame(video_path):
    try:
        vidcap = cv2.VideoCapture(video_path)
        frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        mid_frame = frame_count // 2
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
        success, image = vidcap.read()
        if success:
            frame_file = video_path + "_frame.jpg"
            cv2.imwrite(frame_file, image)
            return frame_file
        else:
            logger.info(f"⚠️ Could not read frame from {video_path}")
            return None
    except Exception as e:
        logger.info(f"❌ Video frame extract error: {e}")
        return None


def extract_and_tag(zip_folder, output_csv):
    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "ZIP File",
                "Media File",
                "Clarifai Tags",
                "Rekognition Tags",
                "Imagga Tags",
            ]
        )

        for fname in os.listdir(zip_folder):
            if not fname.lower().endswith(".zip"):
                continue

            zip_path = os.path.join(zip_folder, fname)
            logger.info(f"🔍 Processing: {fname}")

            try:
                with zipfile.ZipFile(zip_path, "r") as archive:
                    for item in archive.namelist():
                        ext = item.lower()
                        if ext.endswith((".jpg", ".jpeg", ".png", ".webp")):
                            with tempfile.NamedTemporaryFile(
                                delete=False, suffix=os.path.splitext(item)[-1]
                            ) as tmp:
                                tmp.write(archive.read(item))
                                tmp_path = tmp.name
                        elif ext.endswith((".mp4", ".mov")):
                            with tempfile.NamedTemporaryFile(
                                delete=False, suffix=".mp4"
                            ) as tmp:
                                tmp.write(archive.read(item))
                                tmp.flush()
                                tmp_path = extract_video_frame(tmp.name)
                                if not tmp_path:
                                    continue
                        else:
                            continue

                        clarifai = get_clarifai_tags(tmp_path)
                        rekog = get_rekognition_tags(tmp_path)
                        imagga = get_imagga_tags(tmp_path)

                        writer.writerow(
                            [
                                fname,
                                item,
                                ", ".join(clarifai),
                                ", ".join(rekog),
                                ", ".join(imagga),
                            ]
                        )
                        os.unlink(tmp_path)
            except zipfile.BadZipFile:
                logger.info(f"⚠️ Skipping invalid ZIP: {zip_path}")

    # Auto-open the CSV file (macOS)
    subprocess.run(["open", output_csv])


if __name__ == "__main__":
    zip_folder = input("📂 Enter path to folder containing ZIPs: ").strip()
    output_csv = "zip_ai_tags.csv"
    extract_and_tag(zip_folder, output_csv)
    logger.info(f"\n✅ Done. Tags saved to {output_csv}")
