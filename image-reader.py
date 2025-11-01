"""
Analyze Image Reader

This module provides functionality for analyze image reader.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import csv
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import backoff
from PIL import Image, UnidentifiedImageError
import openai
from env_d_loader import load_dotenv
from tqdm import tqdm

# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# --- CONFIGURATION ---
load_dotenv(Path.home() / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "No OpenAI API key found! Please set it in ~/.env as OPENAI_API_KEY=..."
    )

openai.api_key = OPENAI_API_KEY

# Allowed image extensions (lowercase)
VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# Retry mechanism for API calls
@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def analyze_image_gpt4o(image_path: Path) -> Dict[str, Any]:
    """
    Calls GPT-4o Vision API to analyze the image at image_path.
    Returns a dict with keys:
      - main_subject (str)
      - style (str)
      - color_palette (str)
      - tags (List[str])
      - orientation (str)
      - suggested_products (str or List[str])
      - SEO_title (str)
      - SEO_description (str)
      - emotion (str)
      - safety_rating (str: "G"/"PG"/"NSFW")
      - dominant_keyword (str)
    If parsing fails, returns an empty dict.
    """
    image_url = f"file://{image_path.resolve()}"
    text_prompt = (
        "Analyze this image for print-on-demand use. "
        "Return a single JSON object with keys: "
        "main_subject, style, color_palette, tags (list), orientation, "
        "suggested_products, SEO_title, SEO_description, emotion, "
        "safety_rating (G/PG/NSFW), dominant_keyword."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": {"type": "image_url", "image_url": image_url},
                },
                {"role": "user", "content": text_prompt},
            ],
            max_tokens=CONSTANT_1024,
            temperature=0.7,
        )
    except Exception as exc:
        logger.error(f"API error for '{image_path.name}': {exc}")
        return {}

    content = response.choices[0].message.content
    try:
        start_idx = content.index("{")
        end_idx = content.rindex("}") + 1
        json_str = content[start_idx:end_idx]
        return json.loads(json_str)
    except Exception as exc:
        logger.error(f"Error parsing GPT-4o output for '{image_path.name}': {exc}")
        logger.debug("Raw output:", content)
        return {}


def get_image_tech_meta(image_path: Path) -> Dict[str, Optional[Any]]:
    """
    Returns basic technical metadata for the image:
      - filename (str)
      - width (int)
      - height (int)
      - dpi (int)
      - format (str)
      - file_size (int, bytes)
      - created_date (str, 'YYYY-MM-DD HH:MM:SS')
    If reading fails, values may be None.
    """
    try:
        im = Image.open(image_path)
        width, height = im.width, im.height
        dpi_info = im.info.get("dpi", (CONSTANT_300, CONSTANT_300))
        dpi_val = dpi_info[0] if isinstance(dpi_info, tuple) else dpi_info
        file_size = image_path.stat().st_size
        created_ts = image_path.stat().st_ctime
        created_date = datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "filename": image_path.name,
            "width": width,
            "height": height,
            "dpi": dpi_val,
            "format": im.format,
            "file_size": file_size,
            "created_date": created_date,
        }
    except UnidentifiedImageError:
        logger.warning(f"Could not identify or open image '{image_path.name}'.")
    except Exception as exc:
        logger.error(f"Error reading metadata for '{image_path.name}': {exc}")
    return {
        "filename": image_path.name,
        "width": None,
        "height": None,
        "dpi": None,
        "format": None,
        "file_size": None,
        "created_date": None,
    }


def discover_images(input_folder: Path) -> List[Path]:
    """
    Recursively walk through input_folder and return a list of image file paths.
    Only files with extensions in VALID_EXTS are included. Maintains original discovery order.
    """
    image_files: List[Path] = []
    for root, _, files in os.walk(input_folder):
        root_path = Path(root)
        for fname in files:
            if root_path.joinpath(fname).suffix.lower() in VALID_EXTS:
                image_files.append(root_path / fname)
    return image_files


def build_source_tag(image_path: Path, base_folder: Path, date_str: str) -> str:
    """
    Constructs a "source" tag of the form:
      folder-subfolder{-sub-subfolder}-YYYYMMDD
    If the image is directly under base_folder, uses base_folder name instead of folder-subfolder.
    """
    rel = image_path.relative_to(base_folder)
    parent_parts = rel.parent.parts  # tuple of subfolder names
    folder_id = "-".join(parent_parts) if parent_parts else base_folder.name
    return f"{folder_id}-{date_str}"


def parse_args() -> argparse.Namespace:
    """parse_args function."""

    parser = argparse.ArgumentParser(
        description="Analyze images and output metadata to CSV."
    )
    parser.add_argument(
        "input_folder",
        type=Path,
        help="Full path to the folder containing image files.",
    )
    parser.add_argument(
        "-o",
        "--output_csv",
        type=Path,
        default=Path("analyzed_images.csv"),
        help="Path to output CSV file.",
    )
    return parser.parse_args()

    """main function."""


def main():
    args = parse_args()
    input_path = args.input_folder.resolve()
    output_csv = args.output_csv.resolve()

    if not input_path.is_dir():
        logger.error(f"Error: '{input_path}' is not a valid directory.")
        return

    date_str = datetime.now().strftime("%Y%m%d")

    image_paths = discover_images(input_path)
    if not image_paths:
        logger.warning(
            "No image files found in the specified directory or its subdirectories."
        )
        return

    fieldnames = [
        "filename",
        "width",
        "height",
        "dpi",
        "format",
        "file_size",
        "created_date",
        "main_subject",
        "style",
        "color_palette",
        "tags",
        "orientation",
        "suggested_products",
        "SEO_title",
        "SEO_description",
        "emotion",
        "safety_rating",
        "dominant_keyword",
        "source",
    ]

    with output_csv.open(mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for image_path in tqdm(image_paths, desc="Analyzing images", unit="image"):
            tech_meta = get_image_tech_meta(image_path)
            gpt_meta = analyze_image_gpt4o(image_path)
            source_tag = build_source_tag(image_path, input_path, date_str)

            record: Dict[str, Any] = {
                "filename": tech_meta["filename"],
                "width": tech_meta["width"],
                "height": tech_meta["height"],
                "dpi": tech_meta["dpi"],
                "format": tech_meta["format"],
                "file_size": tech_meta["file_size"],
                "created_date": tech_meta["created_date"],
                "main_subject": gpt_meta.get("main_subject"),
                "style": gpt_meta.get("style"),
                "color_palette": gpt_meta.get("color_palette"),
                "tags": json.dumps(gpt_meta.get("tags", [])),
                "orientation": gpt_meta.get("orientation"),
                "suggested_products": json.dumps(
                    gpt_meta.get("suggested_products", [])
                ),
                "SEO_title": gpt_meta.get("SEO_title"),
                "SEO_description": gpt_meta.get("SEO_description"),
                "emotion": gpt_meta.get("emotion"),
                "safety_rating": gpt_meta.get("safety_rating"),
                "dominant_keyword": gpt_meta.get("dominant_keyword"),
                "source": source_tag,
            }

            writer.writerow(record)

    logger.info(f"Completed analysis! CSV saved at: {output_csv.resolve()}")


if __name__ == "__main__":
    main()
