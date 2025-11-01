"""
Batch Image Seo Gpt4 Pipeline

This module provides functionality for batch image seo gpt4 pipeline.

Author: Auto-generated
Date: 2025-11-01
"""

import os
import sys
import csv
import json
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import backoff  # pip install backoff
from PIL import Image, UnidentifiedImageError
from dotenv import load_dotenv
from openai import OpenAI, OpenAIAPIError
from tqdm import tqdm

# Constants
CONSTANT_300 = 300
CONSTANT_400 = 400
CONSTANT_500 = 500
CONSTANT_1024 = 1024


# ───────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────────────────────────

# 1) Logging: both to console and to a file
LOG_FILE = "batch_image_seo_pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# 2) Allowed image extensions (lowercase)
VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

# 3) GPT-4o Vision mult i modal prompts
SYSTEM_PROMPT = (
    "You are an expert in multimedia analysis and storytelling. Your task is to provide "
    "a detailed and structured analysis of the visual content. Focus on themes, style, "
    "color palette, emotion, composition, and potential product fit. Return a single JSON "
    "object with keys: main_subject, style, color_palette, tags (list), orientation, "
    "suggested_products, SEO_title, SEO_description, emotion, safety_rating (G/PG/NSFW), "
    "dominant_keyword."
)
USER_TEXT_PROMPT = (
    "Analyze this image and return the requested JSON fields. The image is provided above under 'image_url'."
)

# 4) “Top 5% SEO Analytics” template—these will be COMBINED into each row.
#    (In a real setup, you’d replace these dummy values with real analytics data per product.)
SEO_TEMPLATE = {
    "SEO Keywords": "",  # e.g. "Retro Gaming Merch, Pixel Art Hoodie"
    "Traffic Source": "",  # e.g. "70% Google, 20% TikTok Shop, 10% Direct"
    "CRO Tactic": "",  # e.g. "Added 'Limited Edition' badge"
    "Backlink Source": "",  # e.g. "Featured on GeekCultureBlog.com (DA 65)"
    "Engagement Rate": "",  # e.g. "7.2%"
}

# 5) Niche design prompts (Geeky, Dark Humor, Anime) to be embedded in CSV
NUANCED_PROMPTS = {
    "Geeky": "Design a RGB-lit gaming mousepad with a cyberpunk cityscape and glowing neon gridlines. Include hidden Easter eggs like 'Level Up' in binary code.",
    "Dark Humour": "Create a minimalist tee with the phrase 'I’m Not Lazy, I’m in Energy-Saving Mode' in glitchy retro font. Add a pixelated coffee cup icon.",
    "Anime": "Illustrate a Studio Ghibli-inspired poster with a flying cat bus soaring over a magical forest. Use soft watercolor gradients and hidden Totoro silhouettes.",
}


# ───────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────────────────────────────────────────────


def load_openai_client(env_path: Path) -> OpenAI:
    """
    Load OpenAI API key from .env and return a configured OpenAI client.
    Raises an error if key is missing.
    """
    if not env_path.is_file():
        raise FileNotFoundError(f".env file not found at {env_path}")
    load_dotenv(dotenv_path=str(env_path))
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in .env")
    return OpenAI(api_key=api_key)


def retry_on_api_error(exception: Exception) -> bool:
    """
    Return True if we should retry on this exception (e.g., OpenAIAPIError with 5xx or rate limit).
    We give up on 4xx (invalid request).
    """
    if isinstance(exception, OpenAIAPIError):
        status = getattr(exception, "status_code", None)
        if status and CONSTANT_400 <= status < CONSTANT_500:
            return False
        return True
    return False


@backoff.on_exception(
    backoff.expo,
    OpenAIAPIError,
    max_tries=4,
    jitter=backoff.full_jitter,
    giveup=lambda e: not retry_on_api_error(e),
)
def call_gpt4o(messages: List[Dict[str, Any]], model: str, max_tokens: int, temperature: float) -> str:
    """
    Wrapper around the OpenAI chat completion call with retry logic.
    Returns the raw text content from the model.
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content


def get_image_tech_meta(image_path: Path) -> Dict[str, Optional[Any]]:
    """
    Extracts technical metadata from an image file:
      filename, width, height, dpi, format, file_size (bytes), created_date (YYYY-MM-DD HH:MM:SS)
    If reading fails, returns None for everything except filename.
    """
    meta = {
        "filename": image_path.name,
        "width": None,
        "height": None,
        "dpi": None,
        "format": None,
        "file_size": None,
        "created_date": None,
    }
    try:
        im = Image.open(image_path)
        width, height = im.width, im.height
        dpi_info = im.info.get("dpi", (CONSTANT_300, CONSTANT_300))
        dpi_val = dpi_info[0] if isinstance(dpi_info, tuple) else dpi_info
        file_size = image_path.stat().st_size
        created_ts = image_path.stat().st_ctime
        created_date = datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d %H:%M:%S")
        meta.update(
            {
                "width": width,
                "height": height,
                "dpi": dpi_val,
                "format": im.format,
                "file_size": file_size,
                "created_date": created_date,
            }
        )
    except UnidentifiedImageError:
        logger.warning(f"Could not identify/open image: {image_path.name}")
    except Exception as e:
        logger.error(f"Error reading metadata for {image_path.name}: {e}")
    return meta


def build_source_tag(image_path: Path, base_folder: Path, date_str: str) -> str:
    """
    Constructs a source tag:
      folder-subfolder{-sub-subfolder}-YYYYMMDD
    If the image is directly under base_folder, uses base_folder.name instead.
    """
    try:
        rel = image_path.relative_to(base_folder)
        parts = rel.parent.parts
        folder_id = "-".join(parts) if parts else base_folder.name
    except Exception:
        folder_id = base_folder.name
    return f"{folder_id}-{date_str}"


def discover_images(input_folder: Path) -> List[Path]:
    """
    Recursively find all image files under input_folder that match VALID_EXTS.
    """
    image_files: List[Path] = []
    for root, _, files in os.walk(input_folder):
        for fname in files:
            if Path(fname).suffix.lower() in VALID_EXTS:
                image_files.append(Path(root) / fname)
    return image_files


def build_gpt_messages(image_path: Path) -> List[Dict[str, Any]]:
    """
    Build the list of messages for GPT-4o:
      1) System role with multimedia analysis instructions
      2) User role with multimodal content array (image_url + text prompt)
    """
    image_url = f"file://{image_path.resolve()}"
    multimodal_content = [{"type": "image_url", "image_url": image_url}, {"type": "text", "text": USER_TEXT_PROMPT}]
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": multimodal_content}]


# ───────────────────────────────────────────────────────────────────────────────
# ARGPARSE
# ───────────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    """parse_args function."""

    parser = argparse.ArgumentParser(
        description="Batch analyze images with GPT-4o Vision, enrich with SEO metrics, and output a final CSV."
    )
    parser.add_argument("input_folder", type=Path, help="Full path to the folder containing image files.")
    parser.add_argument(
        "-o",
        "--output_csv",
        type=Path,
        default=Path("enhanced_image_seo_data.csv"),
        help="Path to output CSV file. (default: enhanced_image_seo_data.csv)",
    )
    parser.add_argument("-m", "--model", type=str, default="gpt-4o", help="OpenAI model to use (default: gpt-4o).")
    parser.add_argument(
        "--max_tokens", type=int, default=CONSTANT_1024, help="Max tokens for GPT-4o (default: CONSTANT_1024)."
    )
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for GPT-4o (default: 0.7).")
    return parser.parse_args()

    # ───────────────────────────────────────────────────────────────────────────────
    # MAIN
    # ───────────────────────────────────────────────────────────────────────────────

    """main function."""


def main():
    args = parse_args()
    input_folder: Path = args.input_folder.resolve()
    output_csv: Path = args.output_csv.resolve()

    if not input_folder.is_dir():
        logger.error(f"Input folder '{input_folder}' does not exist or is not a directory.")
        sys.exit(1)

    # Load OpenAI client
    try:
        global client
        client = load_openai_client(Path.home() / ".env")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        sys.exit(1)

    # Discover images
    image_paths = discover_images(input_folder)
    if not image_paths:
        logger.info(f"No image files found in '{input_folder}'. Exiting.")
        sys.exit(0)

    # Prepare CSV fieldnames (including SEO and design prompts)
    date_str = datetime.now().strftime("%Y%m%d")
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
        # SEO Columns (Top 5% Analytics)
        "SEO Keywords",
        "Traffic Source",
        "CRO Tactic",
        "Backlink Source",
        "Engagement Rate",
        # Niche Design Prompts
        "Design Prompt - Geeky",
        "Design Prompt - Dark Humor",
        "Design Prompt - Anime",
    ]

    # Open CSV for writing
    try:
        with output_csv.open("w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for image_path in tqdm(image_paths, desc="Analyzing images", unit="image"):
                # 1) Technical metadata
                tech_meta = get_image_tech_meta(image_path)

                # 2) Build GPT messages & call GPT-4o Vision
                messages = build_gpt_messages(image_path)
                try:
                    raw_response = call_gpt4o(
                        messages=messages, model=args.model, max_tokens=args.max_tokens, temperature=args.temperature
                    )
                except OpenAIAPIError as e:
                    logger.error(f"API error for '{image_path.name}': {e}")
                    gpt_meta = {}
                except Exception as e:
                    logger.error(f"Unexpected error for '{image_path.name}': {e}")
                    gpt_meta = {}
                else:
                    # 3) Parse JSON
                    try:
                        start = raw_response.index("{")
                        end = raw_response.rindex("}") + 1
                        json_str = raw_response[start:end]
                        gpt_meta = json.loads(json_str)
                    except Exception as e:
                        logger.error(f"JSON parse error for '{image_path.name}': {e}")
                        logger.debug(f"Raw response: {raw_response}")
                        gpt_meta = {}

                # 4) Build “source” tag
                source_tag = build_source_tag(image_path, input_folder, date_str)

                # 5) Build SEO fields (dummy values or placeholders—edit as needed)
                seo_data = {
                    "SEO Keywords": SEO_TEMPLATE["SEO Keywords"],
                    "Traffic Source": SEO_TEMPLATE["Traffic Source"],
                    "CRO Tactic": SEO_TEMPLATE["CRO Tactic"],
                    "Backlink Source": SEO_TEMPLATE["Backlink Source"],
                    "Engagement Rate": SEO_TEMPLATE["Engagement Rate"],
                }

                # 6) Build final record
                record: Dict[str, Any] = {
                    # Technical metadata
                    "filename": tech_meta["filename"],
                    "width": tech_meta["width"],
                    "height": tech_meta["height"],
                    "dpi": tech_meta["dpi"],
                    "format": tech_meta["format"],
                    "file_size": tech_meta["file_size"],
                    "created_date": tech_meta["created_date"],
                    # GPT-4o fields
                    "main_subject": gpt_meta.get("main_subject"),
                    "style": gpt_meta.get("style"),
                    "color_palette": (
                        json.dumps(gpt_meta.get("color_palette", []))
                        if isinstance(gpt_meta.get("color_palette"), list)
                        else gpt_meta.get("color_palette")
                    ),
                    "tags": (
                        json.dumps(gpt_meta.get("tags", []))
                        if isinstance(gpt_meta.get("tags"), list)
                        else gpt_meta.get("tags")
                    ),
                    "orientation": gpt_meta.get("orientation"),
                    "suggested_products": (
                        json.dumps(gpt_meta.get("suggested_products", []))
                        if isinstance(gpt_meta.get("suggested_products"), list)
                        else gpt_meta.get("suggested_products")
                    ),
                    "SEO_title": gpt_meta.get("SEO_title"),
                    "SEO_description": gpt_meta.get("SEO_description"),
                    "emotion": gpt_meta.get("emotion"),
                    "safety_rating": gpt_meta.get("safety_rating"),
                    "dominant_keyword": gpt_meta.get("dominant_keyword"),
                    # Source tag
                    "source": source_tag,
                    # SEO (Top 5% Analytics) placeholders
                    "SEO Keywords": seo_data["SEO Keywords"],
                    "Traffic Source": seo_data["Traffic Source"],
                    "CRO Tactic": seo_data["CRO Tactic"],
                    "Backlink Source": seo_data["Backlink Source"],
                    "Engagement Rate": seo_data["Engagement Rate"],
                    # Niche design prompts
                    "Design Prompt - Geeky": NUANCED_PROMPTS["Geeky"],
                    "Design Prompt - Dark Humor": NUANCED_PROMPTS["Dark Humour"],
                    "Design Prompt - Anime": NUANCED_PROMPTS["Anime"],
                }

                writer.writerow(record)

    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting gracefully.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error writing CSV: {e}")
        sys.exit(1)

    logger.info(f"✅ Batch pipeline complete! CSV saved at: {output_csv.resolve()}")


if __name__ == "__main__":
    main()
