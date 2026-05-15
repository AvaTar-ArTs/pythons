"""Shared utilities for scan-to-csv scanners.

Consolidates functions that were duplicated across doc-source.py,
doc-source-evolved.py, doc-source-enriched.py, all_for_csv.py, and
ecosystem_scan_compare.py.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Optional


# ── File-size formatting ──────────────────────────────────────────

def format_file_size(size_bytes: int | float) -> str:
    """Human-readable file size using base-2 units (B, KiB, MiB, GiB, TiB)."""
    size = float(size_bytes)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PiB"


def human_kb(kb: int) -> str:
    """Pretty-print a du -sk value (kilobytes) as K / M / G."""
    if kb < 1024:
        return f"{kb}K"
    mb = kb / 1024
    if mb < 1024:
        return f"{mb:.1f}M"
    return f"{mb / 1024:.1f}G"


# ── Timestamps ────────────────────────────────────────────────────

def get_creation_date(filepath: str) -> str:
    """Return file creation date as MM-DD-YY, or 'Unknown' on error."""
    try:
        return datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%m-%d-%y")
    except Exception:
        return "Unknown"


def get_last_modified(filepath: str) -> str:
    """Return last-modified timestamp as MM-DD-YY HH:MM, or 'Unknown'."""
    try:
        return datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%m-%d-%y %H:%M")
    except Exception:
        return "Unknown"


# ── Duration formatting ───────────────────────────────────────────

def format_duration(seconds: Optional[float]) -> str:
    """Format seconds as H:MM:SS or M:SS. Returns empty string for None."""
    if seconds is None:
        return ""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


# ── Path / filename helpers ───────────────────────────────────────

def sanitize_filename(name: str) -> str:
    """Replace characters invalid in filenames with hyphens."""
    return re.sub(r"[^a-zA-Z0-9_.-]", "-", name)


def unique_path(base_path: str) -> str:
    """If *base_path* exists, append _1, _2, … to find an unused name."""
    if not os.path.exists(base_path):
        return base_path
    base, ext = os.path.splitext(base_path)
    counter = 1
    while counter < 1000:  # safety cap
        candidate = f"{base}_{counter}{ext}"
        if not os.path.exists(candidate):
            return candidate
        counter += 1
    raise FileExistsError(f"Could not find unique path for {base_path}")


# ── Exclusion helpers (used with exclude_patterns.py) ─────────────

def is_path_excluded(
    file_path: str,
    dir_patterns: list[str] | None = None,
    file_patterns: list[str] | None = None,
    full_patterns: list[str] | None = None,
) -> bool:
    """Return True if *file_path* matches any exclusion pattern.

    Checks directory patterns against the parent path and file
    patterns against the full path.  If *full_patterns* is supplied
    it is also checked against the full path (backward compat).
    """
    patterns: list[str] = list(full_patterns or [])
    if dir_patterns:
        patterns.extend(dir_patterns)
    if file_patterns:
        patterns.extend(file_patterns)
    return any(re.search(p, file_path) for p in patterns)


def filter_excluded_dirs(
    root: str, dirnames: list[str],
    dir_patterns: list[str] | None = None,
    full_patterns: list[str] | None = None,
) -> None:
    """Mutate *dirnames* in-place, removing directories that match exclusion patterns.

    Designed for use inside ``os.walk``::

        for root, dirs, files in os.walk(path):
            filter_excluded_dirs(root, dirs, ...)
    """
    patterns = (dir_patterns or []) + (full_patterns or [])
    if not patterns:
        return
    # Keep dirs that do NOT match any pattern
    dirnames[:] = [
        d for d in dirnames
        if not any(re.search(p, os.path.join(root, d)) for p in patterns)
    ]
