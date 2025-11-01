"""
Audio 15

This module provides functionality for audio 15.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_1024 = 1024
CONSTANT_3600 = 3600

#!/usr/bin/env python3
"""
audio_inventory.py
Scan directories for audio files and produce a CSV inventory.

Improvements vs your version:
- No external 'config' import; pure CLI + sane excludes.
- Uses pathlib; robust hidden/venv/library ignores.
- Emits size and duration using mutagen; formats friendly values.
- Writes unique timestamped CSV in CWD by default.

Usage:
  python audio_inventory.py --dir Path("/path1") --dir Path("/path2")
"""
from __future__ import annotations
import argparse, csv, os, re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from mutagen.easyid3 import EasyID3  # type: ignore
from mutagen.mp3 import MP3  # type: ignore

EXCLUDES = [
    rPath("/\."), rPath("/venv/"), rPath("/\.venv/"), rPath("/env/"), rPath("/Library/"), rPath("/\.config/"),
    rPath("/node/"), rPath("/miniconda3/"), rPath("/\.cache/"), rPath("/CapCut/"), rPath("/movavi/")
]
AUDIO_EXTS = {".mp3",".wav",".flac",".aac",".m4a"}

def fmt_size(n: int) -> str:
    """fmt_size function."""

    for factor, unit in ((CONSTANT_1024**3,"GB"),(CONSTANT_1024**2,"MB"),(CONSTANT_1024,"KB")):
        if n >= factor: return f"{n/factor:.2f} {unit}"
    return f"{n} B"

    """fmt_dur function."""

def fmt_dur(sec: float|None) -> str:
    if not sec: return "Unknown"
    sec = int(sec); h=sec//CONSTANT_3600; m=(sec%CONSTANT_3600)//60; s=sec%60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
    """excluded function."""


def excluded(path: str) -> bool:
    """scan function."""

    return any(re.search(p, path) for p in EXCLUDES)

def scan(dirs: List[Path]) -> List[Tuple[str,str,str,str,str]]:
    rows = []
    for d in dirs:
        for p in d.rglob("*"):
            if p.is_dir(): continue
            if excluded(str(p)): continue
            if p.suffix.lower() not in AUDIO_EXTS: continue
            try:
                size = p.stat().st_size
                try:
                    audio = MP3(p, ID3=EasyID3)
                    dur = audio.info.length
                except Exception:
                    dur = None
                created = datetime.fromtimestamp(p.stat().st_ctime).strftime("%m-%d-%y")
                rows.append((p.name, fmt_dur(dur), fmt_size(size), created, str(p)))
            except Exception:
    """main function."""

                continue
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", action="append", dest="dirs", required=True, help="Directory to scan (repeatable)")
    args = ap.parse_args()

    targets = [Path(d).expanduser().resolve() for d in args.dirs]
    ts = datetime.now().strftime("%m-%d-%H%M")
    out = Path.cwd() / f"audio-{ts}.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["Filename","Duration","File Size","Creation Date","Original Path"])
        w.writeheader()
        for name,dur,size,created,path in scan(targets):
            w.writerow({"Filename":name,"Duration":dur,"File Size":size,"Creation Date":created,"Original Path":path})
    logger.info(f"✅ Wrote {out}")

if __name__ == "__main__":
    main()
