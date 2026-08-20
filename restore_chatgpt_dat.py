#!/usr/bin/env python3
"""
restore_chatgpt_dat.py

Detect the real type of ChatGPT-export .dat files and create properly
named copies such as:

    file_....dat -> file_....jpg
    file_....dat -> file_....png
    file_....dat -> file_....webp
    file_....dat -> file_....wav
    file_....dat -> file_....mp4
    file_....dat -> file_....zip
    file_....dat -> file_....json
    ...

Original files are NEVER modified.

Usage:
    python3 restore_chatgpt_dat.py "/path/to/export"

Optional:
    python3 restore_chatgpt_dat.py "/path/to/export" --output ~/Desktop/restored
    python3 restore_chatgpt_dat.py "/path/to/export" --images-only
    python3 restore_chatgpt_dat.py "/path/to/export" --dry-run
"""

from __future__ import annotations

import argparse
import csv
import json
import mimetypes
import shutil
import subprocess
from collections import Counter
from pathlib import Path


MAGIC_SIGNATURES = [
    (b"\x89PNG\r\n\x1a\n", ".png", "image/png"),
    (b"\xff\xd8\xff", ".jpg", "image/jpeg"),
    (b"GIF87a", ".gif", "image/gif"),
    (b"GIF89a", ".gif", "image/gif"),
    (b"RIFF", None, None),
    (b"PK\x03\x04", ".zip", "application/zip"),
    (b"%PDF", ".pdf", "application/pdf"),
    (b"\x1f\x8b", ".gz", "application/gzip"),
    (b"ID3", ".mp3", "audio/mpeg"),
    (b"OggS", ".ogg", "audio/ogg"),
    (b"fLaC", ".flac", "audio/flac"),
]


MIME_TO_EXT = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
    "image/heic": ".heic",
    "image/heif": ".heif",
    "image/tiff": ".tiff",
    "image/bmp": ".bmp",
    "image/svg+xml": ".svg",

    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/mpeg": ".mp3",
    "audio/mp4": ".m4a",
    "audio/aac": ".aac",
    "audio/flac": ".flac",
    "audio/ogg": ".ogg",

    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "video/webm": ".webm",
    "video/x-matroska": ".mkv",

    "application/pdf": ".pdf",
    "application/zip": ".zip",
    "application/json": ".json",
    "text/plain": ".txt",
    "text/html": ".html",
}


IMAGE_EXTS = {
    ".jpg", ".jpeg", ".png", ".webp", ".gif",
    ".bmp", ".tif", ".tiff", ".heic", ".heif", ".svg"
}


def read_head(path: Path, size: int = 4096) -> bytes:
    try:
        with path.open("rb") as f:
            return f.read(size)
    except OSError:
        return b""


def detect_magic(path: Path):
    head = read_head(path)

    if not head:
        return None, None, "empty"

    # WebP = RIFF....WEBP
    if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
        return ".webp", "image/webp", "magic"

    # WAV = RIFF....WAVE
    if head.startswith(b"RIFF") and head[8:12] == b"WAVE":
        return ".wav", "audio/wav", "magic"

    # MP4 / MOV family
    if len(head) >= 12 and head[4:8] == b"ftyp":
        brand = head[8:12]

        mov_brands = {
            b"qt  ",
        }

        if brand in mov_brands:
            return ".mov", "video/quicktime", "magic"

        return ".mp4", "video/mp4", "magic"

    for signature, ext, mime in MAGIC_SIGNATURES:
        if head.startswith(signature) and ext:
            return ext, mime, "magic"

    # JSON
    stripped = head.lstrip()

    if stripped.startswith((b"{", b"[")):
        try:
            with path.open("r", encoding="utf-8") as f:
                json.load(f)
            return ".json", "application/json", "json"
        except Exception:
            pass

    # SVG / HTML / text-ish
    try:
        text = head.decode("utf-8")

        lower = text.lower().lstrip()

        if "<svg" in lower[:1000]:
            return ".svg", "image/svg+xml", "text"

        if (
            lower.startswith("<!doctype html")
            or lower.startswith("<html")
        ):
            return ".html", "text/html", "text"

    except UnicodeDecodeError:
        pass

    return None, None, None


def detect_with_file(path: Path):
    """
    macOS/Linux fallback using the `file` command.
    """
    try:
        result = subprocess.run(
            ["file", "--brief", "--mime-type", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

        mime = result.stdout.strip()

        if not mime:
            return None, None

        ext = MIME_TO_EXT.get(mime)

        if not ext:
            guessed = mimetypes.guess_extension(mime)

            if guessed:
                ext = guessed

        return ext, mime

    except FileNotFoundError:
        return None, None


def detect(path: Path):
    ext, mime, method = detect_magic(path)

    if ext:
        return ext, mime, method

    ext, mime = detect_with_file(path)

    if ext:
        return ext, mime, "file"

    return ".unknown", mime or "application/octet-stream", "unknown"


def unique_destination(dest: Path) -> Path:
    if not dest.exists():
        return dest

    n = 2

    while True:
        candidate = dest.with_name(
            f"{dest.stem}_{n}{dest.suffix}"
        )

        if not candidate.exists():
            return candidate

        n += 1


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "source",
        type=Path,
        help="Root ChatGPT export directory",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory",
    )

    parser.add_argument(
        "--images-only",
        action="store_true",
        help="Only restore detected image files",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Detect/report without copying",
    )

    parser.add_argument(
        "--move",
        action="store_true",
        help="Move instead of copy. NOT recommended initially.",
    )

    args = parser.parse_args()

    source = args.source.expanduser().resolve()

    if not source.is_dir():
        raise SystemExit(f"Not a directory: {source}")

    output = (
        args.output.expanduser().resolve()
        if args.output
        else source / "_RESTORED_ASSETS"
    )

    if not args.dry_run:
        output.mkdir(parents=True, exist_ok=True)

    dat_files = sorted(source.rglob("*.dat"))

    print()
    print("ChatGPT DAT Asset Restorer")
    print("=" * 72)
    print(f"Source : {source}")
    print(f"Output : {output}")
    print(f"DATs   : {len(dat_files):,}")
    print()

    counts = Counter()
    manifest_rows = []

    for i, src in enumerate(dat_files, start=1):

        if output in src.parents:
            continue

        ext, mime, method = detect(src)

        counts[ext] += 1

        if args.images_only and ext not in IMAGE_EXTS:
            continue

        relative_parent = src.parent.relative_to(source)

        dest_dir = output / relative_parent

        dest = dest_dir / f"{src.stem}{ext}"

        if not args.dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = unique_destination(dest)

            if args.move:
                shutil.move(str(src), str(dest))
            else:
                shutil.copy2(src, dest)

        status = (
            "WOULD RESTORE"
            if args.dry_run
            else "RESTORED"
        )

        print(
            f"[{i:5}/{len(dat_files):5}] "
            f"{status:<13} "
            f"{src.name} -> {src.stem}{ext}"
        )

        manifest_rows.append({
            "source": str(src),
            "detected_extension": ext,
            "mime_type": mime,
            "detection_method": method,
            "destination": str(dest),
            "size_bytes": src.stat().st_size,
        })

    print()
    print("=" * 72)
    print("DETECTED TYPES")

    for ext, count in counts.most_common():
        print(f"{ext:12} {count:8,}")

    print("=" * 72)

    if not args.dry_run:
        manifest = output / "_restore_manifest.csv"

        with manifest.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "source",
                    "detected_extension",
                    "mime_type",
                    "detection_method",
                    "destination",
                    "size_bytes",
                ],
            )

            writer.writeheader()
            writer.writerows(manifest_rows)

        print()
        print(f"Manifest: {manifest}")
        print(f"Restored: {len(manifest_rows):,} files")

    print()


if __name__ == "__main__":
    main()
