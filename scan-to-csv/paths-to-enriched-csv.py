#!/usr/bin/env python3
"""
Convert a whitespace/quoted list of filesystem paths into an enriched CSV.

Intended for inputs like `pythons-md.txt`, which contains a shell-style list of
paths (may include quotes for paths with spaces).

This is inspired by `scan-to-csv/doc-source-enriched.py`, but operates on an
explicit path list instead of directory walking.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shlex
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


CATEGORIES_MAP: dict[str, str] = {
    # Programming languages
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "javascript",
    ".tsx": "typescript",
    ".sh": "shell",
    ".bash": "shell",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".rs": "rust",
    ".go": "go",
    # Markup & web
    ".md": "markdown",
    ".html": "html",
    ".xml": "xml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".css": "css",
    ".scss": "css",
    ".less": "css",
    # Data & config
    ".csv": "csv",
    ".tsv": "tsv",
    ".sql": "sql",
    ".conf": "config",
    ".config": "config",
    ".ini": "config",
    ".toml": "config",
    ".env": "config",
    # Documents
    ".pdf": "pdf",
    ".doc": "document",
    ".docx": "document",
    ".txt": "text",
    ".odt": "document",
    ".rtf": "document",
    # Media
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".gif": "image",
    ".svg": "image",
    ".mp3": "audio",
    ".wav": "audio",
    ".flac": "audio",
    ".mp4": "video",
    ".mkv": "video",
    ".avi": "video",
    ".mov": "video",
    # Archive
    ".zip": "archive",
    ".tar": "archive",
    ".gz": "archive",
    ".7z": "archive",
    ".rar": "archive",
}

MIME_TYPES: dict[str, str] = {
    "python": "text/x-python",
    "javascript": "text/javascript",
    "typescript": "text/typescript",
    "markdown": "text/markdown",
    "html": "text/html",
    "json": "application/json",
    "xml": "text/xml",
    "csv": "text/csv",
    "pdf": "application/pdf",
    "image": "image/*",
    "audio": "audio/*",
    "video": "video/*",
    "text": "text/plain",
    "archive": "application/octet-stream",
    "config": "text/plain",
}

SENSITIVE_BASENAMES = {
    ".env",
    "oauth_creds.json",
    "google_accounts.json",
    "settings.json",
}

SENSITIVE_PATH_PARTS = {
    ".git",
    ".history",
    "projects",
    "debug",
    "todos",
    "tmp",
    "session-reports",
}


def format_file_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    for unit in units[:-1]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def get_creation_date(path: Path) -> str:
    try:
        return datetime.fromtimestamp(path.stat().st_ctime).strftime("%m-%d-%y")
    except Exception:
        return "Unknown"


def get_last_modified(path: Path) -> str:
    try:
        return datetime.fromtimestamp(path.stat().st_mtime).strftime("%m-%d-%y %H:%M")
    except Exception:
        return "Unknown"


def detect_category(path: Path) -> str:
    ext = path.suffix.lower()
    return CATEGORIES_MAP.get(ext, "other")


def is_sensitive_path(path: Path) -> bool:
    if path.name in SENSITIVE_BASENAMES:
        return True
    parts = set(path.parts)
    if parts.intersection(SENSITIVE_PATH_PARTS):
        return True
    return False


def calculate_content_hash(path: Path, *, max_bytes: int) -> str:
    if max_bytes <= 0:
        return ""
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return ""
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()[:16]
    except Exception:
        return ""


def count_lines(path: Path, *, max_bytes: int) -> int:
    if max_bytes <= 0:
        return 0
    try:
        size = path.stat().st_size
        if size > max_bytes:
            return 0
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def read_path_list(input_path: Path) -> list[str]:
    raw = input_path.read_text("utf-8", errors="replace")
    if not raw.strip():
        return []
    return shlex.split(raw)


def build_rows(
    items: list[str],
    *,
    repo_root: Path,
    hash_max_bytes: int,
    lines_max_bytes: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for raw_item in items:
        full_path = Path(raw_item).expanduser()
        filename = full_path.name or str(full_path)
        exists = full_path.exists()
        is_dir = full_path.is_dir() if exists else False
        is_file = full_path.is_file() if exists else False

        if full_path.is_absolute():
            full_path_str = str(full_path)
        else:
            full_path_str = str((repo_root / full_path).resolve())
            full_path = Path(full_path_str)
            exists = full_path.exists()
            is_dir = full_path.is_dir() if exists else False
            is_file = full_path.is_file() if exists else False

        try:
            original_path = str(full_path.relative_to(repo_root))
        except Exception:
            original_path = full_path_str

        ext = full_path.suffix.lower() if is_file else ""
        category = detect_category(full_path) if is_file else ("directory" if is_dir else "missing")
        mime_type = MIME_TYPES.get(category, "application/octet-stream")

        size_bytes = 0
        file_size = ""
        creation_date = "Unknown"
        last_modified = "Unknown"
        content_hash = ""
        lines_of_code = 0

        if exists:
            try:
                st = full_path.stat()
                size_bytes = int(st.st_size) if is_file else 0
                file_size = format_file_size(size_bytes) if is_file else ""
                creation_date = get_creation_date(full_path)
                last_modified = get_last_modified(full_path)
            except Exception:
                pass

        if exists and is_file and not is_sensitive_path(full_path):
            content_hash = calculate_content_hash(full_path, max_bytes=hash_max_bytes)
            if category in {"python", "javascript", "typescript", "markdown", "text", "html", "css", "yaml", "xml", "json"}:
                lines_of_code = count_lines(full_path, max_bytes=lines_max_bytes)

        rows.append(
            {
                "filename": filename,
                "original_path": original_path,
                "full_path": full_path_str,
                "exists": exists,
                "is_dir": is_dir,
                "is_file": is_file,
                "file_extension": ext,
                "category": category,
                "mime_type": mime_type,
                "file_size": file_size,
                "file_size_bytes": size_bytes,
                "creation_date": creation_date,
                "last_modified": last_modified,
                "content_hash": content_hash,
                "lines_of_code": lines_of_code,
                "sensitive_skipped": bool(exists and is_file and is_sensitive_path(full_path)),
            }
        )
    return rows


def write_csv(output_path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "filename",
        "original_path",
        "full_path",
        "exists",
        "is_dir",
        "is_file",
        "file_extension",
        "category",
        "mime_type",
        "file_size",
        "file_size_bytes",
        "creation_date",
        "last_modified",
        "content_hash",
        "lines_of_code",
        "sensitive_skipped",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a path-list file to an enriched CSV (shell-quoted parsing)."
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_path",
        default="pythons-md.txt",
        help="Path-list input file (default: pythons-md.txt)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_path",
        default="pythons-md.csv",
        help="Output CSV path (default: pythons-md.csv)",
    )
    parser.add_argument(
        "--repo-root",
        dest="repo_root",
        default=str(Path.cwd()),
        help="Repo root for `original_path` relativization (default: cwd)",
    )
    parser.add_argument(
        "--hash-max-bytes",
        type=int,
        default=20 * 1024 * 1024,
        help="Max bytes to hash per file (default: 20971520). 0 disables hashing.",
    )
    parser.add_argument(
        "--lines-max-bytes",
        type=int,
        default=2 * 1024 * 1024,
        help="Max bytes to line-count per file (default: 2097152). 0 disables line counting.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    input_path = Path(args.input_path).expanduser()
    output_path = Path(args.output_path).expanduser()

    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(2)

    items = read_path_list(input_path)
    if not items:
        print(f"No paths found in input: {input_path}", file=sys.stderr)
        sys.exit(3)

    rows = build_rows(
        items,
        repo_root=repo_root,
        hash_max_bytes=int(args.hash_max_bytes),
        lines_max_bytes=int(args.lines_max_bytes),
    )
    write_csv(output_path, rows)
    print(f"Wrote CSV: {output_path} (rows={len(rows)})")


if __name__ == "__main__":
    main()

