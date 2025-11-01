"""
Analyze Csv Reader

This module provides functionality for analyze csv reader.

Author: Auto-generated
Date: 2025-11-01
"""

#!/usr/bin/env python3
import os
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from PIL import Image, UnidentifiedImageError
import openai
from env_d_loader import load_dotenv
from tqdm import tqdm

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024


# ─── CONFIGURATION ───
# 1) Path to your existing CSV file (prompted at runtime)
# 2) Output CSV file name
# 3) Base directory for building “source” tags (optional; default = parent folder of CSV)
load_dotenv(Path.home() / ".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "No OpenAI API key found! Please set it in ~/.env as OPENAI_API_KEY=..."
    )

openai.api_key = OPENAI_API_KEY

# Allowed image extensions (for fallback tech‐meta if needed)
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
      - suggested_products (List[str] or str)
      - SEO_title (str)
      - SEO_description (str)
      - emotion (str)
      - safety_rating (str: "G"/"PG"/"NSFW")
      - dominant_keyword (str)

    If parsing fails or API error occurs, returns an empty dict.
    """
    if not image_path.exists():
        logger.info(f"⚠️  File not found for GPT analysis: {image_path}")
        return {}

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
    except Exception as e:
        logger.info(f"❌ GPT-4o API error for '{image_path.name}': {e}")
        return {}

    content = response.choices[0].message.content
    try:
        start_idx = content.index("{")
        end_idx = content.rindex("}") + 1
        json_str = content[start_idx:end_idx]
        return json.loads(json_str)
    except Exception as e:
        logger.info(f"❌ Error parsing GPT-4o output for '{image_path.name}': {e}")
        logger.info("Raw output:", content)
        return {}


def get_image_tech_meta(image_path: Path) -> Dict[str, Optional[Any]]:
    """
    Returns basic technical metadata for the image, if it exists:
      - filename (str)
      - width (int)
      - height (int)
      - dpi (int)
      - format (str)
      - file_size (int, bytes)
      - created_date (str, 'YYYY-MM-DD HH:MM:SS')

    If PIL fails to open the file, returns keys with None values (except filename).
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


def build_source_tag_from_csv_row(
    original_path: str, base_folder: Path, date_str: str
) -> str:
    """
    Given an 'Original Path' string from the CSV, constructs a source tag:
      folder-subfolder{-sub-subfolder}-YYYYMMDD.

    If original_path is absolute or relative, we attempt to make it relative to base_folder;
    if that fails, we simply take the parent folder name from original_path.
    """
    try:
        img_path = Path(original_path)
        rel = img_path
        # If the image path is under base_folder, make it relative
        try:
            rel = img_path.relative_to(base_folder)
        except Exception:
            # If not under base_folder, keep the absolute/relative structure
            rel = img_path

        parent_parts = rel.parent.parts  # tuple of subfolder names
        if parent_parts:
            folder_id = "-".join(parent_parts)
        else:
            # Fallback: use the folder name containing the CSV itself
            folder_id = base_folder.name
    except Exception:
        folder_id = base_folder.name

    return f"{folder_id}-{date_str}"


def main():
    """main function."""

    # ── Prompt for CSV file path ──
    csv_input = input(
        "🗄️ Enter the full path to your CSV (e.g., /Users/steven/image_data-04-29-07-31.csv): "
    ).strip()
    csv_path = Path(csv_input)
    if not csv_path.is_file():
        logger.info(f"❌ Error: '{csv_path}' is not a valid file path.")
        return

    # Define output CSV (same directory as input, prefixed with 'enhanced_')
    output_csv = csv_path.parent / f"enhanced_{csv_path.stem}.csv"
    date_str = datetime.now().strftime("%Y%m%d")

    # Determine base folder for building "source" tags (default = parent folder of CSV)
    base_folder = csv_path.parent

    # ── Read existing CSV into memory ──
    with csv_path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        original_fieldnames = reader.fieldnames or []
        rows = list(reader)

    if not rows:
        logger.info("⚠️ CSV has no data rows to process.")
        return

    # ── Prepare new fieldnames ──
    # Keep all original columns, then append the GPT-4o fields + 'source'
    gpt_fields = [
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
    fieldnames = original_fieldnames + gpt_fields

    # ── Open output CSV for writing ──
    with output_csv.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # ── Process each row one by one ──
        for row in tqdm(rows, desc="Enhancing CSV rows", unit="row"):
            original_path_str = row.get("Original Path", "").strip()
            image_path = Path(original_path_str) if original_path_str else None

            # 1) Attempt to collect technical metadata if not already present
            tech_meta: Dict[str, Any] = {}
            if (
                image_path
                and image_path.exists()
                and image_path.suffix.lower() in VALID_EXTS
            ):
                tech_meta = get_image_tech_meta(image_path)
            else:
                # If the CSV already has Width/Height/DPI/etc., skip tech-meta
                tech_meta = {}

            # 2) Call GPT-4o only if the image file actually exists locally
            gpt_meta: Dict[str, Any] = {}
            if (
                image_path
                and image_path.exists()
                and image_path.suffix.lower() in VALID_EXTS
            ):
                gpt_meta = analyze_image_gpt4o(image_path)
            else:
                # Fill keys with None/empty defaults if image not found
                for key in [
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
                ]:
                    gpt_meta[key] = None

            # 3) Build "source" tag based on Original Path and date_str
            source_tag = build_source_tag_from_csv_row(
                original_path_str, base_folder, date_str
            )

            # 4) Construct the output record
            output_row: Dict[str, Any] = {}

            # Copy all original CSV columns verbatim
            for col in original_fieldnames:
                output_row[col] = row.get(col, "")

            # Overwrite/attach any tech_meta fields if needed (optional)
            # e.g., if you want to update Width/Height in CSV based on actual file:
            # output_row["Width"] = tech_meta.get("width", row.get("Width", ""))
            # But by default, we keep existing CSV values intact.

            # Append GPT-4o fields
            output_row["main_subject"] = gpt_meta.get("main_subject")
            output_row["style"] = gpt_meta.get("style")
            output_row["color_palette"] = gpt_meta.get("color_palette")
            # Store lists as JSON strings
            output_row["tags"] = (
                json.dumps(gpt_meta.get("tags", []))
                if isinstance(gpt_meta.get("tags"), list)
                else ""
            )
            output_row["orientation"] = gpt_meta.get("orientation")
            output_row["suggested_products"] = (
                json.dumps(gpt_meta.get("suggested_products", []))
                if isinstance(gpt_meta.get("suggested_products"), list)
                else ""
            )
            output_row["SEO_title"] = gpt_meta.get("SEO_title")
            output_row["SEO_description"] = gpt_meta.get("SEO_description")
            output_row["emotion"] = gpt_meta.get("emotion")
            output_row["safety_rating"] = gpt_meta.get("safety_rating")
            output_row["dominant_keyword"] = gpt_meta.get("dominant_keyword")

            # Append source tag
            output_row["source"] = source_tag

            # 5) Write the combined row to the new CSV
            writer.writerow(output_row)

    logger.info(f"\n✅ Completed enhancement! New CSV saved at: {output_csv.resolve()}")


if __name__ == "__main__":
    main()
