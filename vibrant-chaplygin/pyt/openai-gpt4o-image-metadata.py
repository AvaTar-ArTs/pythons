import os
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image, UnidentifiedImageError
import openai
from dotenv import load_dotenv
from tqdm import tqdm

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib
from dotenv import load_dotenv

env_dir = PathLib.home() / ".env.d"
if env_dir.exists():
    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# --- CONFIGURATION ---
# Load environment variables from ~/.env
load_dotenv(Path.home() / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found! Please set it in ~/.env as OPENAI_API_KEY=...")

openai.api_key = OPENAI_API_KEY

# Allowed image extensions (lowercase)
VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}


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
        content = response.choices[0].message.content
        start_idx = content.index("{")
        end_idx = content.rindex("}") + 1
        json_str = content[start_idx:end_idx]
        return json.loads(json_str)
    except Exception as exc:
        logger.info(f"❌ Error processing image '{image_path.name}': {exc}")
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
        with Image.open(image_path) as im:
            width, height = im.size
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
        logger.info(f"❌ Could not identify or open image '{image_path.name}'.")
    except Exception as exc:
        logger.info(f"❌ Error reading metadata for '{image_path.name}': {exc}")
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
    return [
        root_path / fname
        for root, _, files in os.walk(input_folder)
        for root_path in [Path(root)]
        for fname in files
        if root_path.joinpath(fname).suffix.lower() in VALID_EXTS
    ]


def build_source_tag(image_path: Path, base_folder: Path, date_str: str) -> str:
    """
    Constructs a "source" tag of the form:
      folder-subfolder{-sub-subfolder}-YYYYMMDD
    If the image is directly under base_folder, uses base_folder name instead of folder-subfolder.
    """
    rel = image_path.relative_to(base_folder)
    folder_id = "-".join(rel.parent.parts) if rel.parent.parts else base_folder.name
    return f"{folder_id}-{date_str}"


def main():
    """main function."""

    input_path = Path(input("📂 Enter the full path to the folder containing image files: ").strip())
    if not input_path.is_dir():
        logger.info(f"❌ Error: '{input_path}' is not a valid directory.")
        return

    output_csv = Path("analyzed_images.csv")
    date_str = datetime.now().strftime("%Y%m%d")

    image_paths = discover_images(input_path)
    if not image_paths:
        logger.info("⚠️ No image files found in the specified directory or its subdirectories.")
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
                "suggested_products": json.dumps(gpt_meta.get("suggested_products", [])),
                "SEO_title": gpt_meta.get("SEO_title"),
                "SEO_description": gpt_meta.get("SEO_description"),
                "emotion": gpt_meta.get("emotion"),
                "safety_rating": gpt_meta.get("safety_rating"),
                "dominant_keyword": gpt_meta.get("dominant_keyword"),
                "source": source_tag,
            }

            writer.writerow(record)

    logger.info(f"\n✅ Completed analysis! CSV saved at: {output_csv.resolve()}")


if __name__ == "__main__":
    main()
