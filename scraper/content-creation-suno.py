"""
Content Creation Suno Scrape 3

This module provides functionality for content creation suno scrape 3.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Scrape Suno-like grid HTML into CSV.

This script extracts song information from a Suno-like grid HTML and outputs it into a CSV file. It targets specific HTML structures to gather data such as song titles, URLs, cover images, and more.

Targets structures:
- Container: .react-aria-GridListItem
- Title: link text under a <span class="cursor-pointer ...">
- Song URL: <a href=Path("/song/...")>
- Cover URL: first <img> in the left block
- Time: overlay <span class="font-mono">mm:ss</span> within the image block
- Keys/Tags: all <span title="..."> inside the descriptor cluster (joined with ", ")

Usage:
  python scrape_suno_grid.py /path/to/songs.html --output songs_extracted.csv --base-url "https://suno.ai"
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import List
from urllib.parse import urljoin

import pandas as pd
from bs4 import BeautifulSoup


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Extract song rows from a Suno-like grid HTML into CSV.")
    parser.add_argument("html_file", type=Path, help="Path to songs.html")
    parser.add_argument("--output", "-o", type=Path, default=Path("songs_extracted.csv"), help="Output CSV file path")
    parser.add_argument("--base-url", type=str, default="", help="Join relative href/src with this base URL")
    return parser.parse_args()


def get_text(element) -> str:
    """Extract and return text from an HTML element."""
    return element.get_text(strip=True) if element else ""


def get_attr(element, attribute_name: str) -> str:
    """Extract and return an attribute value from an HTML element."""
    if element and element.has_attr(attribute_name):
        return element.get(attribute_name) or ""
    return ""


def absolutize(url: str, base: str) -> str:
    """Convert a relative URL to an absolute URL using the base URL."""
    if not url or not base:
        return url or ""
    return urljoin(base, url)


def extract_rows(soup: BeautifulSoup, base_url: str) -> List[dict]:
    """Extract song data rows from the parsed HTML soup."""
    rows = []
    for item in soup.select(".react-aria-GridListItem"):
        img = item.select_one("img")
        time_span = item.select_one("span.font-mono")
        anchor = item.select_one("a[href^='/song/']")
        title_span = item.select_one("span.cursor-pointer")
        key_spans = item.select("span[title]")

        cover_url = get_attr(img, "src")
        song_url = get_attr(anchor, "href")
        title = get_text(title_span) or get_text(anchor)

        keys = []
        for ks in key_spans:
            title_text = get_attr(ks, "title").strip()
            if not title_text:
                title_text = get_text(ks).strip()
            if title_text:
                keys.append(title_text)

        # De-duplicate keys while preserving order (case-insensitive)
        seen = set()
        dedup = []
        for key in keys:
            lower_key = key.lower()
            if lower_key not in seen:
                seen.add(lower_key)
                dedup.append(key)

        rows.append(
            {
                "CoverUrl": absolutize(cover_url, base_url),
                "SongTitle": title,
                "SongURL": absolutize(song_url, base_url),
                "Time": get_text(time_span),
                "Keys": ", ".join(dedup),
            }
        )
    return rows


def main():
    """Main function to execute the script."""
    args = parse_args()
    html_text = args.html_file.read_text(encoding="utf-8", errors="ignore")

    # Prefer lxml if available, else use html.parser
    soup = None
    for parser in ("lxml", "html.parser"):
        try:
            soup = BeautifulSoup(html_text, parser)
            break
        except Exception:
            continue

    if soup is None:
        raise RuntimeError("Failed to parse HTML")

    rows = extract_rows(soup, args.base_url)
    df = pd.DataFrame(rows, columns=["CoverUrl", "SongTitle", "SongURL", "Time", "Keys"])
    df.to_csv(args.output, index=False, quoting=csv.QUOTE_MINIMAL)
    logger.info(f"Wrote {len(df)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
