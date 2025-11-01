"""
Media Processing Audio Gemini 1

This module provides functionality for media processing audio gemini 1.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

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

from __future__ import annotations
import argparse, asyncio, csv, hashlib, json, os, re, sys, time, urllib.parse
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from playwright.async_api import async_playwright

# ---------- Utilities ----------

SAFE_CHARS = re.compile(r"[^A-Za-z0-9._ -]+")


def slugify(text: str, default: str = "gemini_storybook") -> str:
    if not text:
        return default
    text = text.strip()
    text = text.replace("/", "-").replace(":", "-")
    text = SAFE_CHARS.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or default
def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def sanitize_url_to_id(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
        tail = parsed.path.rstrip("/").split("/")[-1]
        return slugify(tail or parsed.netloc, default="gemini_item")
    except (requests.RequestException, urllib.error.URLError, ConnectionError):
        return "gemini_item"


# ---------- Core scrape helpers ----------


async def fetch_binary(page, url: str) -> Optional[bytes]:
    try:
        resp = await page.request.get(url)
        if resp.ok:
            return await resp.body()
    except Exception as e:
        logger.info(f"[warn] fetch_binary failed for {url}: {e}")
    return None


async def gather_src_candidates(page):
    """Collect candidate asset URLs from DOM: <img>, <source>, <video>, <audio>, CSS backgrounds, and meta."""
    assets = set()

    # images
    imgs = await page.locator("img").evaluate_all(
        "els => els.map(e => e.currentSrc || e.src || e.getAttribute('src') || '')"
    )
    for u in imgs:
        if u:
            assets.add(u)

    # <source> inside <picture>, <video>, <audio>
    sources = await page.locator("source").evaluate_all(
        "els => els.flatMap(e => [e.srcset || '', e.src || '', e.getAttribute('srcset') || '', e.getAttribute('src') || ''])"
    )
    for u in sources:
        if u:
            assets.add(u)

    # video/audio elements
    medias = await page.locator("video, audio").evaluate_all(
        "els => els.flatMap(e => [e.src || '', e.getAttribute('src') || ''])"
    )
    for u in medias:
        if u:
            assets.add(u)

    # CSS background images
    styles = await page.evaluate(
        """
        () => Array.from(document.querySelectorAll('*'))
            .map(el => getComputedStyle(el).backgroundImage)
            .filter(bg => bg && bg.startsWith('url('))
    """
    )
    for bg in styles:
        # url("..."), url('...') or url(...)
        m = re.findall(r"url\\((?:\"|\')?([^\"\')]+)(?:\"|\')?\\)", bg)
        for u in m:
            if u:
                assets.add(u)

    # OpenGraph/Twitter meta images
    meta_imgs = await page.locator(
        'meta[property="og:image"], meta[name="twitter:image"]'
    ).evaluate_all("els => els.map(e => e.content || '')")
    for u in meta_imgs:
        if u:
            assets.add(u)

    # Parse srcset lists into concrete URLs
    expanded = set()
    for u in assets:
        if "," in u and " " in u:
            # srcset like "url1 320w, url2 640w"
            parts = [p.strip().split(" ")[0] for p in u.split(",")]
            for p in parts:
                if p:
                    expanded.add(p)
        else:
            expanded.add(u)

    # filter out data: URIs; we can't easily persist those as files
    expanded = {u for u in expanded if u and not u.startswith("data:")}
    return list(expanded)


async def extract_page_text(page) -> str:
    # Try to get main text; fallback to visible body text
    try:
        # Some Gemini pages may have article or main
        text = await page.evaluate(
            """
            () => {
                const sel = document.querySelector('main, article, [role="main"], body');
                return sel ? sel.innerText : document.body.innerText;
            }
        """
        )
        return text.strip()
    except Exception:
        return ""


async def extract_page_title(page) -> str:
    try:
        title = await page.title()
        return title.strip()
    except Exception:
        return ""


async def extract_embedded_json(page) -> Dict:
    """Grab any JSON blobs embedded in <script type='application/ld+json'> and window.__INITIAL_STATE__-style."""
    data = {}
    try:
        ldjson = await page.locator('script[type="application/ld+json"]').evaluate_all(
            "els => els.map(e => e.textContent)"
        )
        parsed = []
        for blob in ldjson:
            try:
                parsed.append(json.loads(blob))
            except (json.JSONDecodeError, ValueError):
                pass
        if parsed:
            data["ld_json"] = parsed
    except (json.JSONDecodeError, ValueError):
        pass

    try:
        # try a few common bootstraps
        boot = await page.evaluate(
            """
            () => {
                const out = {};
                for (const k of Object.keys(window)) {
                    if (k.startsWith('__') && typeof window[k] === 'object') {
                        try { out[k] = window[k]; } catch (e) {}
                    }
                }
                return out;
            }
        """
        )
        if boot:
            data["boot"] = boot
    except (IndexError, KeyError):
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
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        logger.info(f"[info] Navigating: {url}")
        resp = await page.goto(url, wait_until="networkidle", timeout=120_000)

        # Derive folder name from title (or URL id)
        title = await extract_page_title(page)
        folder_name = slugify(title, default=sanitize_url_to_id(url))
        dest = ensure_dir(out_root / folder_name)
        assets_dir = ensure_dir(dest / "assets")

        # Save full HTML after render
        html_content = await page.content()
        (dest / "page.html").write_text(html_content, encoding="utf-8")

        # Save text
        text = await extract_page_text(page)
        (dest / "text.md").write_text(text, encoding="utf-8")

        # Save embedded metadata JSON, plus basic page meta
        metadata = {
            "source_url": url,
            "saved_at_epoch": time.time(),
            "title": title,
            "extracted_json": await extract_embedded_json(page),
        }
        (dest / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        # Collect assets and download
        candidates = await gather_src_candidates(page)

        records: List[DownloadRecord] = []
        seen_hashes = set()
        idx = 1

        def ext_for(url: str, kind_hint: str) -> str:
            parsed = urllib.parse.urlparse(url)
            path = parsed.path.lower()
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
            absu = u
            try:
                absu = page.url if u.startswith("#") else urllib.parse.urljoin(page.url, u)
            except (requests.RequestException, urllib.error.URLError, ConnectionError):
                pass
            # Guess kind by extension / mime
            lower = absu.lower()
            kind = "asset"
            if any(lower.endswith(x) for x in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"]):
                kind = "image"
            elif any(lower.endswith(x) for x in [".mp4", ".webm", ".mov", ".m4v"]):
                kind = "video"
            elif any(lower.endswith(x) for x in [".mp3", ".wav", ".m4a", ".ogg", ".aac"]):
                kind = "audio"

            data = await fetch_binary(page, absu)
            if not data:
                return None
            h = sha256_bytes(data)
            if h in seen_hashes:
                return None
            seen_hashes.add(h)

            nonlocal idx
            fname = f"{kind}_{idx:03d}{ext_for(absu, kind)}"
            (assets_dir / fname).write_bytes(data)
            rec = DownloadRecord(
                index=idx,
                kind=kind,
                url=absu,
                filename=str(Path("assets") / fname),
                sha256_16=h,
                bytes=len(data),
            )
            idx += 1
            return rec

        # Parallel-ish downloads in small batches
        BATCH = 6
        for i in range(0, len(candidates), BATCH):
            batch = candidates[i : i + BATCH]
            tasks = [classify_and_fetch(u) for u in batch]
            for r in await asyncio.gather(*tasks):
                if r:
                    records.append(r)

        # Write manifest
        with open(dest / "manifest.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["index", "kind", "url", "filename", "sha256_16", "bytes"])
            for r in records:
                w.writerow([r.index, r.kind, r.url, r.filename, r.sha256_16, r.bytes])

        await context.close()
        await browser.close()

        logger.info(f"[done] Saved to: {dest}")
        return dest


async def main():
    ap = argparse.ArgumentParser(description="Download Gemini Storybook share pages and assets.")
    ap.add_argument("urls", nargs="*", help="One or more Gemini share URLs.")
    ap.add_argument("--file", "-f", dest="file", help="Path to a text file with one URL per line.")
    ap.add_argument("--out", "-o", default="downloads", help="Output folder (default: downloads)")
    args = ap.parse_args()

    urls: List[str] = []
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                for line in fh:
                    u = line.strip()
                    if u and not u.startswith("#"):
                        urls.append(u)
        except FileNotFoundError:
            logger.info(f"[error] File not found: {args.file}")
            sys.exit(1)

    urls.extend(u for u in args.urls if u.strip())
    urls = [u.strip() for u in urls if u.strip()]
    if not urls:
        logger.info("[error] Provide at least one URL or --file urls.txt")
        sys.exit(2)

    out_root = ensure_dir(Path(args.out))
    for url in urls:
        try:
            await download_storybook(url, out_root)
        except Exception as e:
            logger.info(f"[error] Failed to download {url}: {e}")


if __name__ == "__main__":
    asyncio.run(main())
