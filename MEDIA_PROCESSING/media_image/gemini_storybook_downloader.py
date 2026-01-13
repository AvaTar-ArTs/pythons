# TODO: Resolve circular dependencies by restructuring imports
# TODO: Reduce nesting depth by using early returns and guard clauses

# String constants
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
ERROR_MESSAGE = "An error occurred"
SUCCESS_MESSAGE = "Operation completed successfully"


# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3
DEFAULT_PORT = 8080


import asyncio
import aiohttp

async def async_request(url: str, session: aiohttp.ClientSession) -> str:
    """Async HTTP request."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logger.error(f"Async request failed: {e}")
        return None

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_request(url, session) for url in urls]
        return await asyncio.gather(*tasks)


from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper

def retry_decorator(max_retries = 3):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator


from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    """Abstract base class for processors."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


class SingletonMeta(type):
    """Thread-safe singleton metaclass."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    import html
from __future__ import annotations
from dataclasses import dataclass, asdict
from functools import lru_cache
from pathlib import Path
from playwright.async_api import async_playwright
from typing import List, Dict, Optional, Tuple
import argparse, asyncio, csv, hashlib, json, os, re, sys, time, urllib.parse
import json
import logging

class Config:
    """Configuration class for global variables."""
    DPI_300 = 300
    DPI_72 = 72
    KB_SIZE = 1024
    MB_SIZE = 1024 * 1024
    GB_SIZE = 1024 * 1024 * 1024
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_BATCH_SIZE = 100
    MAX_FILE_SIZE = 9 * 1024 * 1024  # 9MB
    DEFAULT_QUALITY = 85
    DEFAULT_WIDTH = 1920
    DEFAULT_HEIGHT = 1080
    cache = {}
    key = str(args) + str(kwargs)
    cache[key] = func(*args, **kwargs)
    logger = logging.getLogger(__name__)
    SAFE_CHARS = re.compile(r"[^A-Za-z0-9._ -]+")
    text = text.strip()
    text = text.replace("/", "-").replace(":", "-")
    text = SAFE_CHARS.sub("", text)
    text = re.sub(r"\\s+", " ", text).strip()
    parsed = urllib.parse.urlparse(url)
    tail = parsed.path.rstrip("/").split("/")[-1]
    resp = await page.request.get(url)
    assets = set()
    imgs = await page.locator("img").evaluate_all(
    sources = await page.locator("source").evaluate_all(
    medias = await page.locator("video, audio").evaluate_all(
    styles = await page.evaluate(
    m = re.findall(r"url\\\((?:\"|\')?([^\"\')]+)(?:\"|\')?\\\)", bg)
    meta_imgs = await page.locator(
    expanded = set()
    parts = [p.strip().split(" ")[0] for p in u.split(", ")]
    expanded = {u for u in expanded if u and not u.startswith("data:")}
    text = await page.evaluate(
    title = await page.title()
    data = {}
    ldjson = await page.locator('script[type
    parsed = []
    boot = await page.evaluate(
    browser = await p.chromium.launch(headless
    context = await browser.new_context()
    page = await context.new_page()
    resp = await page.goto(url, wait_until
    title = await extract_page_title(page)
    folder_name = slugify(title, default
    dest = ensure_dir(out_root / folder_name)
    assets_dir = ensure_dir(dest / "assets")
    html_content = await page.content()
    text = await extract_page_text(page)
    metadata = {
    candidates = await gather_src_candidates(page)
    seen_hashes = set()
    idx = 1
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    absu = u
    absu = page.url if u.startswith("#") else urllib.parse.urljoin(page.url, u)
    lower = absu.lower()
    kind = "asset"
    kind = "image"
    kind = "video"
    kind = "audio"
    data = await fetch_binary(page, absu)
    h = sha256_bytes(data)
    fname = f"{kind}_{idx:03d}{ext_for(absu, kind)}"
    rec = DownloadRecord(
    index = idx, 
    kind = kind, 
    url = absu, 
    filename = str(Path("assets") / fname), 
    sha256_16 = h, 
    bytes = len(data), 
    BATCH = 6
    batch = candidates[i : i + BATCH]
    tasks = [classify_and_fetch(u) for u in batch]
    w = csv.writer(f)
    ap = argparse.ArgumentParser(description
    args = ap.parse_args()
    u = line.strip()
    urls = [u.strip() for u in urls if u.strip()]
    out_root = ensure_dir(Path(args.out))
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    p.mkdir(parents = True, exist_ok
    @lru_cache(maxsize = 128)
    @lru_cache(maxsize = 128)
    return slugify(tail or parsed.netloc, default = "gemini_item")
    "els = > els.map(e
    "els = > els.flatMap(e
    "els = > els.flatMap(e
    () = > Array.from(document.querySelectorAll('*'))
    .map(el = > getComputedStyle(el).backgroundImage)
    .filter(bg = > bg && bg.startsWith('url('))
    'meta[property = "og:image"], meta[name
    ).evaluate_all("els = > els.map(e
    () = > {
    const sel = document.querySelector('main, article, [role
    """Grab any JSON blobs embedded in <script type = 'application/ld+json'> and window.__INITIAL_STATE__-style."""
    "els = > els.map(e
    data["ld_json"] = parsed
    () = > {
    const out = {};
    try { out[k] = window[k]; } catch (e) {}
    data["boot"] = boot
    (dest / "page.html").write_text(html_content, encoding = "utf-8")
    (dest / "text.md").write_text(text, encoding = "utf-8")
    json.dumps(metadata, indent = 2, ensure_ascii
    records: List[DownloadRecord] = []
    @lru_cache(maxsize = 128)
    idx + = 1
    ap.add_argument("urls", nargs = "*", help
    ap.add_argument("--file", "-f", dest = "file", help
    ap.add_argument("--out", "-o", default = "downloads", help
    urls: List[str] = []


# Constants



def sanitize_html(html_content): -> Any
    """Sanitize HTML content to prevent XSS."""
    return html.escape(html_content)


def safe_sql_query(query, params): -> Any
    """Execute SQL query safely with parameterized queries."""
    # Use parameterized queries to prevent SQL injection
    return execute_query(query, params)


def validate_input(data, validators): -> Any
    """Validate input data."""
    for field, validator in validators.items():
        if field in data:
            if not validator(data[field]):
                raise ValueError(f"Invalid {field}: {data[field]}")
    return True


def memoize(func): -> Any
    """Memoization decorator."""

    def wrapper(*args, **kwargs): -> Any
        if key not in cache:
        return cache[key]

    return wrapper


class Config:
    # TODO: Replace global variable with proper structure

#!/usr/bin/env python3
"""
Gemini Storybook Downloader (macOS-friendly)
--------------------------------------------

Downloads assets (images, videos, audio) and text/metadata from public
Gemini "storybook" share links, e.g.:
  https://gemini.google.com/gem/storybook/<id>
  https://g.co/gemini/share/<id>

It renders pages with Playwright (Chromium) so JS-driven content is captured.

Usage:
  # one-off
  python gemini_storybook_downloader.py <url1> <url2> ...

  # or from a file (one URL per line)
  python gemini_storybook_downloader.py --file urls.txt

Output:
  ./downloads/<sanitized-title-or-id>/
      page.html
      metadata.json
      text.md
      assets/
        img_001.jpg ...
        video_001.mp4 ...
        audio_001.mp3 ...
      manifest.csv

Install:
  pip install -r requirements.txt
  playwright install chromium

Notes:
- Only public share links are supported. If a link requires login, this script
  will still attempt to render but may save a "Sign in" page instead.
- This script avoids duplicate downloads via a content-hash manifest.
"""


# ---------- Utilities ----------



def slugify(text: str, default: str = "gemini_storybook") -> str:
    if not text:
        return default
    return text or default


def ensure_dir(p: Path) -> Path:
    return p


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def sanitize_url_to_id(url: str) -> str:
    try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        return "gemini_item"


# ---------- Core scrape helpers ----------


async def fetch_binary(page, url: str) -> Optional[bytes]:
    try:
        if resp.ok:
            return await resp.body()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        logger.info(f"[warn] fetch_binary failed for {url}: {e}")
    return None


async def gather_src_candidates(page):
    """Collect candidate asset URLs from DOM: <img>, <source>, <video>, <audio>, CSS backgrounds, and meta."""

    # images
    )
    for u in imgs:
        if u:
            assets.add(u)

    # <source> inside <picture>, <video>, <audio>
    )
    for u in sources:
        if u:
            assets.add(u)

    # video/audio elements
    )
    for u in medias:
        if u:
            assets.add(u)

    # CSS background images
        """
    """
    )
    for bg in styles:
        # url("..."), url('...') or url(...)
        for u in m:
            if u:
                assets.add(u)

    # OpenGraph/Twitter meta images
    for u in meta_imgs:
        if u:
            assets.add(u)

    # Parse srcset lists into concrete URLs
    for u in assets:
        if ", " in u and " " in u:
            # srcset like "url1 320w, url2 640w"
            for p in parts:
                if p:
                    expanded.add(p)
        else:
            expanded.add(u)

    # filter out data: URIs; we can't easily persist those as files
    return list(expanded)


async def extract_page_text(page) -> str:
    # Try to get main text; fallback to visible body text
    try:
        # Some Gemini pages may have article or main
            """
                return sel ? sel.innerText : document.body.innerText;
            }
        """
        )
        return text.strip()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        return ""


async def extract_page_title(page) -> str:
    try:
        return title.strip()
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        return ""


async def extract_embedded_json(page) -> Dict:
    try:
        )
        for blob in ldjson:
            try:
                parsed.append(json.loads(blob))
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                pass
        if parsed:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        pass

    try:
        # try a few common bootstraps
            """
                for (const k of Object.keys(window)) {
                    if (k.startsWith('__') && typeof window[k] === 'object') {
                    }
                }
                return out;
            }
        """
        )
        if boot:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
        pass

    return data


# ---------- Downloader ----------


@dataclass
class DownloadRecord:
    index: int
    kind: str
    url: str
    filename: str
    sha256_16: str
    bytes: int


async def download_storybook(url: str, out_root: Path) -> Path:
    async with async_playwright() as p:

        logger.info(f"[info] Navigating: {url}")

        # Derive folder name from title (or URL id)

        # Save full HTML after render

        # Save text

        # Save embedded metadata JSON, plus basic page meta
            "source_url": url, 
            "saved_at_epoch": time.time(), 
            "title": title, 
            "extracted_json": await extract_embedded_json(page), 
        }
        (dest / "metadata.json").write_text(
        )

        # Collect assets and download


        def ext_for(url: str, kind_hint: str) -> str:
            for ext in [
                ".png", 
                ".jpg", 
                ".jpeg", 
                ".webp", 
                ".gif", 
                ".svg", 
                ".mp4", 
                ".webm", 
                ".mov", 
                ".m4v", 
                ".mp3", 
                ".wav", 
                ".m4a", 
                ".ogg", 
                ".aac", 
            ]:
                if path.endswith(ext):
                    return ext
            # fallback by kind
            if kind_hint == "image":
                return ".jpg"
            if kind_hint == "video":
                return ".mp4"
            if kind_hint == "audio":
                return ".mp3"
            return ".bin"

        async def classify_and_fetch(u: str) -> Optional[DownloadRecord]:
            # Make absolute
            try:
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
                pass
            # Guess kind by extension / mime
            if any(lower.endswith(x) for x in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"]):
            elif any(lower.endswith(x) for x in [".mp4", ".webm", ".mov", ".m4v"]):
            elif any(lower.endswith(x) for x in [".mp3", ".wav", ".m4a", ".ogg", ".aac"]):

            if not data:
                return None
            if h in seen_hashes:
                return None
            seen_hashes.add(h)

            nonlocal idx
            (assets_dir / fname).write_bytes(data)
            )
            return rec

        # Parallel-ish downloads in small batches
        for i in range(0, len(candidates), BATCH):
            for r in await asyncio.gather(*tasks):
                if r:
                    records.append(r)

        # Write manifest
        with open(dest / "manifest.csv", "w", newline="", encoding="utf-8") as f:
            w.writerow(["index", "kind", "url", "filename", "sha256_16", "bytes"])
            for r in records:
                w.writerow([r.index, r.kind, r.url, r.filename, r.sha256_16, r.bytes])

        await context.close()
        await browser.close()

        logger.info(f"[done] Saved to: {dest}")
        return dest


async def main():

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                for line in fh:
                    if u and not u.startswith("#"):
                        urls.append(u)
        except FileNotFoundError:
            logger.info(f"[error] File not found: {args.file}")
            sys.exit(1)

    urls.extend(u for u in args.urls if u.strip())
    if not urls:
        logger.info("[error] Provide at least one URL or --file urls.txt")
        sys.exit(2)

    for url in urls:
        try:
            await download_storybook(url, out_root)
    except (ValueError, TypeError, RuntimeError) as e:
        logger.error(f"Specific error occurred: {e}")
        raise
            logger.info(f"[error] Failed to download {url}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
