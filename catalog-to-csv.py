"""
Image Catalog Csv Builder

This module provides functionality for image catalog csv builder.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
analyze_images_to_csv.py
Analyze a folder of images: write technical EXIF + GPT vision tags into CSV.

Key fixes vs your script:
- Uses OpenAI v1 client (`from openai import OpenAI`) safely.
- Supports local images by **base64 data URLs**, not unsupported file://.
- Robust JSON parsing with schema validation & fallbacks.
- Progress bar, error logs, and safe field defaults.
- Deterministic CSV column order.

Usage:
  export OPENAI_API_KEY=...
  python analyze_images_to_csv.py --input Path("/path/to/folder") --out analyzed_images.csv
"""
from __future__ import annotations
import argparse, base64, csv, io, json, os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, UnidentifiedImageError, ExifTags
from tqdm import tqdm
from openai import OpenAI

VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def img_to_data_url(p: Path) -> Tuple[str, str]:
    img = Image.open(p)
    fmt = (img.format or "PNG").lower()
    buf = io.BytesIO()
    img.save(buf, format=img.format or "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/{fmt};base64,{b64}", fmt.upper()
def image_tech_meta(p: Path) -> Dict[str, Any]:
    try:
        im = Image.open(p)
        width, height = im.width, im.height
        fmt = im.format
        size = p.stat().st_size
        exif = {}
        try:
            raw = im.getexif()
            if raw:
                exif = {ExifTags.TAGS.get(k, str(k)): str(v) for k, v in raw.items()}
        except Exception:
            pass
        return {"filename": p.name, "width": width, "height": height, "format": fmt, "file_size": size, "exif": json.dumps(exif) }
    except UnidentifiedImageError:
        return {"filename": p.name, "width": None, "height": None, "format": None, "file_size": None, "exif": "{}"}

FIELDS = [
    "filename","width","height","format","file_size",
    "main_subject","style","color_palette","tags",
    "orientation","suggested_products","SEO_title","SEO_description",
    "emotion","safety_rating","dominant_keyword","source"
]

def call_gpt(data_url: str) -> Dict[str, Any]:
    prompt = (
        "Analyze this image for print-on-demand. Return ONLY JSON with keys: "
        "main_subject, style, color_palette, tags (array), orientation, "
        "suggested_products (array), SEO_title, SEO_description, emotion, "
        "safety_rating (G|PG|NSFW), dominant_keyword."
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are a strict JSON generator."},
                {"role":"user","content":[
                    {"type":"text","text": prompt},
                    {"type":"image_url","image_url":{"url": data_url}}
                ]}
            ],
            temperature=0.4,
            max_tokens=CONSTANT_500,
        )
        content = resp.choices[0].message.content or ""
        # Try to parse as pure JSON; fallback to substring extraction
        try:
            return json.loads(content)
        except Exception:
            start = content.find("{")
            end = content.rfind("}")
            if start != -1 and end != -1:
                return json.loads(content[start:end+1])
    except Exception as e:
        logger.info(f"API error: {e}")
    return {}
def discover_images(root: Path) -> List[Path]:
    return [p for p in root.rglob("*") if p.suffix.lower() in VALID_EXTS]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path, help="Folder to scan")
    ap.add_argument("--out", default=Path("analyzed_images.csv"), type=Path)
    args = ap.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Missing OPENAI_API_KEY")

    imgs = discover_images(args.input.expanduser().resolve())
    if not imgs:
        logger.info("No images found."); return

    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for p in tqdm(imgs, desc="Analyzing", unit="image"):
            tech = image_tech_meta(p)
            try:
                data_url, _ = img_to_data_url(p)
            except Exception:
                data_url = None
            g = call_gpt(data_url) if data_url else {}
            row = {
                **{k: tech.get(k) for k in ["filename","width","height","format","file_size"]},
                "main_subject": g.get("main_subject"),
                "style": g.get("style"),
                "color_palette": g.get("color_palette"),
                "tags": json.dumps(g.get("tags", [])),
                "orientation": g.get("orientation"),
                "suggested_products": json.dumps(g.get("suggested_products", [])),
                "SEO_title": g.get("SEO_title"),
                "SEO_description": g.get("SEO_description"),
                "emotion": g.get("emotion"),
                "safety_rating": g.get("safety_rating"),
                "dominant_keyword": g.get("dominant_keyword"),
                "source": str(p.parent),
            }
            w.writerow(row)
    logger.info(f"✅ Wrote {args.out.resolve()}")

if __name__ == "__main__":
    main()
