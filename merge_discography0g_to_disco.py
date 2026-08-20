#!/usr/bin/env python3
"""
Full merge: Discography0g → DISCO
Copies ALL files (MP3, txt, images) from Discography0g into matching DISCO album folders.

Matching: normalized folder name comparison between source albums and DISCO albums.
"""

import re
import shutil
from pathlib import Path

SRC = Path("/Users/steven/Music/nocturneMelodies/Discography0g")
DST = Path("/Users/steven/Music/nocturneMelodies/DISCO")

def normalize(s: str) -> str:
    """Strip emoji, quotes, punctuation, lowercase, collapse spaces."""
    s = re.sub(r'[\u2600-\u27BF\U0001F300-\U0001F9FF\U0001FA00-\U0001FA6F\uFE00-\uFE0F]', '', s)
    s = re.sub(r'["\'`()\[\]{}]', '', s)
    s = re.sub(r'[^a-z0-9\s]', ' ', s.lower())
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def build_index():
    """Map normalized name → DISCO folder path."""
    idx = {}
    for d in DST.iterdir():
        if d.is_dir() and d.name not in ('audio', 'covers'):
            idx[normalize(d.name)] = d
    return idx

def find_match(src_norm: str, idx: dict) -> Path | None:
    if src_norm in idx:
        return idx[src_norm]
    # Try partial match
    src_words = set(src_norm.split())
    for norm, path in idx.items():
        dst_words = set(norm.split())
        if len(src_words & dst_words) >= 2:
            return path
        if src_norm in norm or norm in src_norm:
            return path
    return None

def main():
    idx = build_index()
    print(f"DISCO index: {len(idx)} albums")
    print(f"Source: {SRC}")
    print()
    
    albums = sorted([d for d in SRC.iterdir() if d.is_dir()])
    print(f"Source albums: {len(albums)}\n")
    
    copied = 0
    skipped = 0
    unmatched_albums = []
    unmatched_files = 0
    
    for album_dir in albums:
        album_norm = normalize(album_dir.name)
        target = find_match(album_norm, idx)
        
        if not target:
            unmatched_albums.append(album_dir.name)
            # Copy unmatched files to a fallback folder
            fallback = DST / "Unmatched_From_Discography0g" / album_dir.name
            for f in album_dir.rglob('*'):
                if f.is_file():
                    fallback.mkdir(parents=True, exist_ok=True)
                    dest = fallback / f.name
                    if not dest.exists():
                        shutil.copy2(str(f), str(dest))
                        unmatched_files += 1
            continue
        
        for src_file in sorted(album_dir.rglob('*')):
            if not src_file.is_file():
                continue
            
            dest = target / src_file.name
            if not dest.exists():
                shutil.copy2(str(src_file), str(dest))
                copied += 1
                if copied <= 15:
                    print(f"  ✓ {album_dir.name}/{src_file.name} → {target.name}/")
            else:
                skipped += 1
    
    print(f"\n{'=' * 60}")
    print(f"FULL MERGE COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Files copied:       {copied}")
    print(f"  Files skipped:      {skipped} (already in DISCO)")
    print(f"  Unmatched albums:   {len(unmatched_albums)}")
    if unmatched_albums:
        for a in unmatched_albums[:10]:
            print(f"    → {a}")
        if len(unmatched_albums) > 10:
            print(f"    ... and {len(unmatched_albums) - 10} more")
        print(f"  Files in unmatched: {unmatched_files} (copied to Unmatched_From_Discography0g/)")

if __name__ == "__main__":
    main()
