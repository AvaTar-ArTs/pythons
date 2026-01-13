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
  python audio_inventory.py --dir "/path1" --dir "/path2"
"""
from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from mutagen.easyid3 import EasyID3  # type: ignore
from mutagen.mp3 import MP3  # type: ignore

EXCLUDES = [
    r"/\.", r"/venv/", r"/\.venv/", r"/env/", r"/Library/", r"/\.config/",
    r"/node/", r"/miniconda3/", r"/\.cache/", r"/CapCut/", r"/movavi/"
]
AUDIO_EXTS = {".mp3",".wav",".flac",".aac",".m4a"}

def fmt_size(n: int) -> str:
    for factor, unit in ((1024**3,"GB"),(1024**2,"MB"),(1024,"KB")):
        if n >= factor: return f"{n/factor:.2f} {unit}"
    return f"{n} B"

def fmt_dur(sec: float|None) -> str:
    if not sec: return "Unknown"
    sec = int(sec); h=sec//3600; m=(sec%3600)//60; s=sec%60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def excluded(path: str) -> bool:
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
    print(f"✅ Wrote {out}")

if __name__ == "__main__":
    main()
