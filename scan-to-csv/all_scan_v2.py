#!/usr/bin/env python3
"""
all_scan_v2.py -- File scanner with SHA256 dedup, media metadata, and cleanup.
O(1) dedup, shared utils, fixed exclusion patterns.
Usage: python all_scan_v2.py /path --output out.csv --dedup
"""

from __future__ import annotations
import argparse
import csv
import hashlib
import os
import re
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from exclude_patterns import DIR_EXCLUDES, FILE_EXCLUDES
from scanner_utils import (
    filter_excluded_dirs, format_duration, format_file_size,
    get_creation_date, is_path_excluded, unique_path,
)

FILE_CATEGORIES: dict[str, str] = {
    ".pdf": "Document", ".doc": "Document", ".docx": "Document",
    ".xlsx": "Spreadsheet", ".csv": "Data", ".md": "Doc", ".txt": "Text",
    ".py": "Code", ".js": "Code", ".ts": "Code", ".jsx": "Code",
    ".tsx": "Code", ".sh": "Script", ".rb": "Code", ".go": "Code",
    ".html": "Web", ".css": "Web", ".json": "Data", ".yaml": "Data",
    ".yml": "Data", ".xml": "Data", ".toml": "Data", ".svg": "Image",
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".m4a": "Audio",
    ".mp4": "Video", ".mov": "Video", ".avi": "Video", ".mkv": "Video",
    ".jpg": "Image", ".jpeg": "Image", ".png": "Image", ".gif": "Image",
    ".webp": "Image", ".ttf": "Font", ".woff2": "Font",
    ".zip": "Archive", ".tar": "Archive", ".gz": "Archive",
}

CSV_COLUMNS = [
    "Filename", "Extension", "Category", "File Size", "Duration",
    "Creation Date", "Original Path", "SHA256", "Is Duplicate",
    "Duplicate Of", "Lines", "Chars", "Width", "Height",
    "DPI", "Mode", "Bitrate", "Sample Rate",
]
# ── Metadata extractors ───────────────────────────────────────────

def _sha256(path: str, chunk: int = 65536) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(chunk), b""):
                h.update(block)
        return h.hexdigest()
    except Exception:
        return ""


def _audio_meta(path: str) -> dict:
    try:
        from mutagen.mp3 import MP3
        a = MP3(path)
        return {"duration": a.info.length, "bitrate": a.info.bitrate,
                "sample_rate": a.info.sample_rate}
    except Exception:
        return {}


def _video_meta(path: str) -> dict:
    try:
        from mutagen.mp4 import MP4
        return {"duration": MP4(path).info.length}
    except Exception:
        return {}


def _image_meta(path: str) -> dict:
    try:
        from PIL import Image
        with Image.open(path) as img:
            dpi = img.info.get("dpi", (None, None))
            return {"width": img.size[0], "height": img.size[1],
                    "dpi": f"{dpi[0]}x{dpi[1]}" if dpi[0] else "",
                    "mode": img.mode}
    except Exception:
        return {}


def _code_meta(path: str) -> dict:
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        return {"lines": text.count("\n") + 1, "chars": len(text)}
    except Exception:
        return {}


# ── Single-file scan ──────────────────────────────────────────────

def scan_one(path: str, *, enable_dedup: bool = False,
             enable_media: bool = True) -> Optional[dict]:
    try:
        st = os.stat(path)
    except OSError:
        return None
    fname = os.path.basename(path)
    ext = os.path.splitext(fname)[1].lower()
    cat = FILE_CATEGORIES.get(ext, "Other")
    row = {"filename": fname, "ext": ext, "category": cat,
           "size_bytes": st.st_size, "size": format_file_size(st.st_size),
           "creation_date": get_creation_date(path), "path": path,
           "sha256": "", "lines": "", "chars": "", "duration": "",
           "width": "", "height": "", "dpi": "", "mode": "",
           "bitrate": "", "sample_rate": ""}
    if enable_media:
        if cat == "Audio":
            m = _audio_meta(path)
            row["duration"] = format_duration(m.get("duration"))
            row["bitrate"] = m.get("bitrate", "")
            row["sample_rate"] = m.get("sample_rate", "")
        elif cat == "Video":
            m = _video_meta(path)
            row["duration"] = format_duration(m.get("duration"))
        elif cat == "Image":
            m = _image_meta(path)
            row["width"] = m.get("width", "")
            row["height"] = m.get("height", "")
            row["dpi"] = m.get("dpi", "")
            row["mode"] = m.get("mode", "")
        elif cat in ("Code", "Script"):
            m = _code_meta(path)
            row["lines"] = m.get("lines", "")
            row["chars"] = m.get("chars", "")
    if enable_dedup:
        row["sha256"] = _sha256(path)
    return row


# ── Main scan + write ─────────────────────────────────────────────

def scan_and_write(directories, output_csv, *, enable_dedup=False,
                   enable_media=True, max_workers=4,
                   include_exts=None):
    """Scan directories, write CSV, return (total, written)."""
    file_paths = []
    for top in directories:
        if not os.path.isdir(top):
            print(f"Warning: not a directory: {top}", file=sys.stderr)
            continue
        for root, dirs, files in os.walk(top):
            filter_excluded_dirs(root, dirs, dir_patterns=DIR_EXCLUDES,
                                 full_patterns=FILE_EXCLUDES)
            for fname in files:
                fpath = os.path.join(root, fname)
                if is_path_excluded(fpath, file_patterns=FILE_EXCLUDES):
                    continue
                if include_exts and os.path.splitext(fname)[1].lower() not in include_exts:
                    continue
                file_paths.append(fpath)
    total = len(file_paths)
    print(f"Files to scan: {total:,}")

    rows = []
    hash_to_paths = defaultdict(list)
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        fut = {ex.submit(scan_one, p, enable_dedup=enable_dedup,
                enable_media=enable_media): p for p in file_paths}
        for i, f in enumerate(as_completed(fut), 1):
            p = fut[f]
            try:
                row = f.result()
            except Exception:
                row = None
            if row is None:
                continue
            rows.append(row)
            if enable_dedup and row["sha256"]:
                hash_to_paths[row["sha256"]].append(p)
            if i % 500 == 0:
                print(f"  {i}/{total} scanned", flush=True)
    print(f"  {len(rows):,} files scanned successfully")

    # O(1) dedup: path->index lookup once
    dup_count = 0
    if enable_dedup:
        path_to_idx = {r["path"]: idx for idx, r in enumerate(rows)}
        for h, paths in hash_to_paths.items():
            if len(paths) <= 1:
                continue
            for p in paths[1:]:
                idx = path_to_idx.get(p)
                if idx is not None:
                    rows[idx]["is_duplicate"] = True
                    rows[idx]["duplicate_of"] = paths[0]
                    dup_count += 1
        print(f"Duplicates found (SHA256): {dup_count:,}")

    csv_path = unique_path(output_csv)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({
                "Filename": r["filename"], "Extension": r["ext"],
                "Category": r["category"], "File Size": r["size"],
                "Duration": r.get("duration", ""),
                "Creation Date": r["creation_date"],
                "Original Path": r["path"], "SHA256": r.get("sha256", ""),
                "Is Duplicate": r.get("is_duplicate", False),
                "Duplicate Of": r.get("duplicate_of", ""),
                "Lines": r.get("lines", ""), "Chars": r.get("chars", ""),
                "Width": r.get("width", ""), "Height": r.get("height", ""),
                "DPI": r.get("dpi", ""), "Mode": r.get("mode", ""),
                "Bitrate": r.get("bitrate", ""),
                "Sample Rate": r.get("sample_rate", ""),
            })

    cats = Counter(r["category"] for r in rows)
    total_bytes = sum(r["size_bytes"] for r in rows)
    print(f"\nWrote {len(rows):,} rows -> {csv_path}")
    print(f"Total size: {format_file_size(total_bytes)}")
    print("By category:")
    for cat, cnt in cats.most_common(12):
        print(f"  {cat:>15s}: {cnt:>7,}")
    return total, len(rows)


# ── Backup cleanup ────────────────────────────────────────────────

def cleanup_backups(directories, *, dry_run=True):
    patterns = [r"\.bak$", r"\.backup_\d+$", r"~$"]
    count = 0
    for top in directories:
        for root, dirs, files in os.walk(top):
            filter_excluded_dirs(root, dirs, dir_patterns=DIR_EXCLUDES)
            for fname in files:
                if any(re.search(p, fname) for p in patterns):
                    fpath = os.path.join(root, fname)
                    if dry_run:
                        print(f"  WOULD REMOVE: {fpath}")
                    else:
                        try:
                            os.remove(fpath)
                        except OSError as e:
                            print(f"  ERROR {fpath}: {e}", file=sys.stderr)
                    count += 1
    verb = "Would remove" if dry_run else "Removed"
    print(f"{verb} {count} backup files")
    return count


# ── CLI ───────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="all_scan_v2 — File scanner with SHA256 dedup")
    p.add_argument("directories", nargs="+", help="Directories to scan")
    p.add_argument("-o", "--output", default="all_scan.csv", help="Output CSV path")
    p.add_argument("--dedup", action="store_true", help="Enable SHA256 dedup")
    p.add_argument("--no-media", action="store_true", help="Skip media metadata")
    p.add_argument("--workers", type=int, default=4, help="Thread pool size")
    p.add_argument("--types", nargs="*", help="Only include extensions (e.g. .md .py)")
    p.add_argument("--cleanup", action="store_true", help="Remove .bak / ~ backup files")
    p.add_argument("--dry-run", action="store_true", help="With --cleanup: show, don't delete")
    args = p.parse_args()

    if args.cleanup:
        cleanup_backups(args.directories, dry_run=args.dry_run)
        return

    include_exts = None
    if args.types:
        include_exts = {e.lower() if e.startswith(".") else f".{e.lower()}"
                        for e in args.types}

    scan_and_write(
        args.directories, args.output,
        enable_dedup=args.dedup,
        enable_media=not args.no_media,
        max_workers=args.workers,
        include_exts=include_exts,
    )


if __name__ == "__main__":
    main()
