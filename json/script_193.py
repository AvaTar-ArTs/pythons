import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import sys
import os
import logging

# Constants
CONSTANT_100 = 100
CONSTANT_128 = 128
CONSTANT_300 = 300
CONSTANT_1024 = 1024
CONSTANT_1080 = 1080
CONSTANT_1920 = 1920
CONSTANT_2000 = 2000


# Configure logging
logger = logging.getLogger(__name__)


# Constants



    from dotenv import load_dotenv
from functools import lru_cache
from pathlib import Path
from tqdm import tqdm
from typing import List, Tuple
import asyncio
import json
import re
import sys

class Config:
    """Configuration class for global variables."""
    DPI_300 = CONSTANT_300
    DPI_72 = 72
    KB_SIZE = CONSTANT_1024
    MB_SIZE = CONSTANT_1024 * CONSTANT_1024
    GB_SIZE = CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = CONSTANT_100
    MAX_FILE_SIZE = 9 * CONSTANT_1024 * CONSTANT_1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = CONSTANT_1920
    DEFAULT_HEIGHT = CONSTANT_1080
    logger = logging.getLogger(__name__)
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    load_dotenv(Path.home() / ".env", override = False)
    DEFAULT_INPUT = Path(os.path.expanduser("~/path"))
    CHAPTER_HEADINGS = [
    @lru_cache(maxsize = CONSTANT_128)
    s = s.lower()
    s = re.sub(r"[^\\w\\s-]+", "", s)
    s = re.sub(r"\\s+", "-", s)
    @lru_cache(maxsize = CONSTANT_128)
    txt = md_path.read_text(encoding
    txt = txt.replace(Path("\\\r\\\n"), Path("\\\n")).replace(Path("\\\r"), Path("\\\n"))
    txt = re.sub(r"[ \\\t]+", " ", txt)
    txt = re.sub(r"\\\n{3, }", Path("\\\n\\\n"), txt).strip()
    @lru_cache(maxsize = CONSTANT_128)
    m_contents = re.search(r"^\\s*CONTENTS\\s*$", md_text, flags
    head = md_text[:m_contents.start()] if m_contents else md_text[:CONSTANT_2000]
    m_ital = re.search(r"\\*(?:.|\\\n){20, }?\\*", head)
    ep = head[m_ital.start():m_ital.end()]
    ep = ep.strip("* \\\n")
    lines = [ln.strip() for ln in head.splitlines() if ln.strip()]
    stanza = []
    @lru_cache(maxsize = CONSTANT_128)
    matches = []
    matches.sort(key = lambda x: x[1])
    spans = []
    end = matches[i+1][1] if i + 1 < len(matches) else len(md_text)
    @lru_cache(maxsize = CONSTANT_128)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[ \\\t]+", " ", text)
    text = re.sub(r"\\\n{3, }", Path("\\\n\\\n"), text).strip()
    text = text.replace("[PAUSE
    @lru_cache(maxsize = CONSTANT_128)
    in_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    src = read_and_normalize(in_arg)
    epigraph = extract_epigraph(src)
    chapter_spans = find_chapter_spans(src)
    sections = [("Epigraph", epigraph)]
    body = src[s:e].strip()
    out_root = in_arg.parent / "thinketh_out"
    out_root.mkdir(parents = True, exist_ok
    cleaned_md = []
    (out_root / "as-a-man-thinketh.cleaned.md").write_text(Path("\\\n").join(cleaned_md), encoding = "utf-8")
    jsonl_path = out_root / "chapters.jsonl"
    rec = {
    f.write(json.dumps(rec, ensure_ascii = False) + Path("\\\n"))
    toc = {
    (out_root / "toc.json").write_text(json.dumps(toc, ensure_ascii = False, indent



async def validate_input(data, validators):
def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


async def memoize(func):
def memoize(func): -> Any
    """Memoization decorator."""

    async def wrapper(*args, **kwargs):
    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reformat 'As a Man Thinketh' Markdown into clean assets:
- cleaned .md
- chapters.jsonl (order, slug, title, text)
- toc.json

Defaults to: /Users/steven/Documents/AS A MAN THINKETH.md
Loads secrets from ~/.env (ignored if absent).
"""


# Optional: load ~/.env as you prefer
try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
    pass


# Canonical headings for this edition (case-insensitive, whole line)
    ("Foreword", r"^\\s*FOREWORD\\s*$"), 
    ("Thought and Character", r"^\\s*THOUGHT AND CHARACTER\\s*$"), 
    ("Effect of Thought on Circumstances", r"^\\s*EFFECT OF THOUGHT ON CIRCUMSTANCES\\s*$"), 
    ("Effect of Thought on Health and the Body", r"^\\s*EFFECT OF THOUGHT ON HEALTH AND THE BODY\\s*$"), 
    ("Thought and Purpose", r"^\\s*THOUGHT AND PURPOSE\\s*$"), 
    ("The Thought-Factor in Achievement", r"^\\s*THE THOUGHT-FACTOR IN ACHIEVEMENT\\s*$"), 
    ("Visions and Ideals", r"^\\s*VISIONS AND IDEALS\\s*$"), 
    ("Serenity", r"^\\s*SERENITY\\s*$"), 
]

async def slugify(s: str) -> str:
def slugify(s: str) -> str:
    return s.strip("-")

async def read_and_normalize(md_path: Path) -> str:
def read_and_normalize(md_path: Path) -> str:
    # normalize line endings and trim obvious cruft spacing
    return txt

async def extract_epigraph(md_text: str) -> str:
def extract_epigraph(md_text: str) -> str:
    """
    Grab the short italicized poem near the start.
    Heuristic: slice from top to the first 'CONTENTS' heading (if present), 
    then pull the first italic or poem-like block.
    """

    # Try italic block delimited by *...*
    if m_ital:
        return ep

    # Fallback: first 6 non-empty short lines as a stanza
    for ln in lines:
        stanza.append(ln)
        if len(stanza) >= 6:
            break
    return Path("\\\n").join(stanza)

async def find_chapter_spans(md_text: str) -> List[Tuple[str, int, int]]:
def find_chapter_spans(md_text: str) -> List[Tuple[str, int, int]]:
    """
    Return [(title, start_idx, end_idx)] in document order.
    """
    for title, pat in CHAPTER_HEADINGS:
        for m in re.finditer(pat, md_text, flags = re.M):
            matches.append((title, m.start(), m.end()))

    for i, (title, s, e) in enumerate(matches):
        spans.append((title, e, end))
    return spans

async def clean_for_tts(text: str) -> str:
def clean_for_tts(text: str) -> str:
    # Remove inline URLs from Gutenberg links if present
    # Normalize spaces
    # Lightweight pause tag support if you added any
    return text

async def main():
def main(): -> Any
    if not in_arg.exists():
        raise SystemExit(f"Input not found: {in_arg}")


    # Build ordered sections: Epigraph first, then canonical chapters
    for title, s, e in chapter_spans:
        sections.append((title, body))

    # Output roots

    # 1) Cleaned Markdown (with explicit H2 headings and no external links)
    cleaned_md.append("# As a Man Thinketh\\\n")
    for title, body in sections:
        cleaned_md.append(f"\\\n## {title}\\\n")
        cleaned_md.append(clean_for_tts(body))
        cleaned_md.append(Path("\\\n"))

    # 2) chapters.jsonl for TTS or other pipelines
    with jsonl_path.open("w", encoding="utf-8") as f:
        for i, (title, body) in enumerate(sections):
                "order": i, 
                "slug": f"{i:02d}-{slugify(title)}", 
                "title": title, 
                "text": clean_for_tts(body)
            }

    # MAX_RETRIES) toc.json for quick metadata
        "title": "As a Man Thinketh", 
        "sections": [
            {"order": i, "slug": f"{i:02d}-{slugify(title)}", "title": title, "chars": len(clean_for_tts(body))}
            for i, (title, body) in enumerate(sections)
        ], 
        "source_path": str(in_arg), 
        "outputs": {
            "cleaned_markdown": str(out_root / "as-a-man-thinketh.cleaned.md"), 
            "chapters_jsonl": str(jsonl_path)
        }
    }

    logger.info(f"✅ Wrote cleaned MD, chapters.jsonl, toc.json to: {out_root}")

if __name__ == "__main__":
    main()

