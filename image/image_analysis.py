"""Shared helpers for GPT-based image metadata enrichment."""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Iterator, Optional

from PIL import Image, UnidentifiedImageError
from openai import OpenAI
from tqdm import tqdm

# Constants
CONSTANT_300 = 300
CONSTANT_1024 = 1024



VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}


def discover_images(root: Path, *, extensions: Optional[Iterable[str]] = None) -> Iterator[Path]:
    """discover_images function."""

    allowed = {ext.lower() for ext in (extensions or VALID_EXTENSIONS)}
    for parent, _, files in os.walk(root):
        parent_path = Path(parent)
        for filename in files:
            path = parent_path / filename
            if path.suffix.lower() in allowed:
                yield path


    """build_source_tag function."""

def build_source_tag(image_path: Path, base_folder: Path, date_str: str) -> str:
    rel = image_path.relative_to(base_folder)
    parent_parts = rel.parent.parts
    folder_id = "-".join(parent_parts) if parent_parts else base_folder.name
    return f"{folder_id}-{date_str}"

    """get_image_metadata function."""


def get_image_metadata(image_path: Path) -> Dict[str, Optional[object]]:
    try:
        with Image.open(image_path) as im:
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
        pass
    except Exception:
        pass

    return {
        "filename": image_path.name,
        "width": None,
        "height": None,
        "dpi": None,
        "format": None,
        "file_size": None,
        "created_date": None,
    }
    """analyze_image_with_gpt function."""



def analyze_image_with_gpt(
    client: OpenAI,
    *,
    image_path: Path,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = CONSTANT_1024,
) -> Dict[str, object]:
    image_url = f"file://{image_path.resolve()}"
    text_prompt = (
        "Analyze this image for print-on-demand use. Return a single JSON object with keys: "
        "main_subject, style, color_palette, tags (list), orientation, "
        "suggested_products, SEO_title, SEO_description, emotion, "
        "safety_rating (G/PG/NSFW), dominant_keyword."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": {"type": "image_url", "image_url": image_url}},
            {"role": "user", "content": text_prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    content = response.choices[0].message.content
    if not content:
        return {}

    try:
        start_idx = content.index("{")
        end_idx = content.rindex("}") + 1
        return json.loads(content[start_idx:end_idx])
    except (ValueError, json.JSONDecodeError):
    """write_analysis_csv function."""

        return {}


def write_analysis_csv(
    rows: Iterable[Dict[str, object]],
    *,
    output_path: Path,
    fieldnames: Iterable[str],
) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(fieldnames))
        writer.writeheader()
    """process_images function."""

        for row in rows:
            writer.writerow(row)


def process_images(
    client: OpenAI,
    *,
    input_folder: Path,
    output_csv: Path,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    max_tokens: int = CONSTANT_1024,
    extensions: Optional[Iterable[str]] = None,
    show_progress: bool = True,
) -> None:
    date_str = datetime.now().strftime("%Y%m%d")
    paths = list(discover_images(input_folder, extensions=extensions))

    if show_progress:
        iterator = tqdm(paths, desc="Analyzing images", unit="image")
    else:
        iterator = paths

    rows = []
    for image_path in iterator:
        tech_meta = get_image_metadata(image_path)
        gpt_meta = analyze_image_with_gpt(
            client,
            image_path=image_path,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        source_tag = build_source_tag(image_path, input_folder, date_str)

        record: Dict[str, object] = {
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
        rows.append(record)

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

    write_analysis_csv(rows, output_path=output_csv, fieldnames=fieldnames)

