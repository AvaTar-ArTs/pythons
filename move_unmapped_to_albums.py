#!/usr/bin/env python3
"""
Move renamed Unmapped_UUIDs content into ALBUMS, sorted by song.

- Midnight_Skin, Silent_Threads, etc. -> new ALBUMS/<Album>/
- Tears_Of_An_Englishman -> ALBUMS/Tears_Of_An_Englishman/ (exists)
- Jingle_My_Bells -> ALBUMS/Jingle_My_Bells/ (exists)
- Lets_Do_It + Lets_Do_It_2 -> ALBUMS/Lets_Do_It/
- Through_Our_Veins + Through_Our_Veins_2 -> ALBUMS/Through_Our_Veins/

Moves: MP3, transcript, analysis for each.
"""

import shutil
from pathlib import Path

UNMAPPED = Path(__file__).parent / "ALBUMS" / "Unmapped_UUIDs"
ALBUMS_DIR = Path(__file__).parent / "ALBUMS"

# base_name -> target album folder (canonical name)
MOVES = [
    ("Midnight_Skin", "Midnight_Skin"),
    ("Silent_Threads", "Silent_Threads"),
    ("When_It_All_Went_Wrong", "When_It_All_Went_Wrong"),
    ("Mooji_Satsang_Notice", "Mooji_Satsang_Notice"),
    ("Jingle_My_Bells", "Jingle_My_Bells"),
    ("Lets_Do_It", "Lets_Do_It"),
    ("Lets_Do_It_2", "Lets_Do_It"),
    ("Through_Our_Veins", "Through_Our_Veins"),
    ("Through_Our_Veins_2", "Through_Our_Veins"),
    ("Tears_Of_An_Englishman", "Tears_Of_An_Englishman"),
]


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    if not args.apply and not args.dry_run:
        p.error("Use --dry-run or --apply")

    mode = "[DRY RUN] " if args.dry_run else ""
    moved = 0

    for base_name, album_name in MOVES:
        target_dir = ALBUMS_DIR / album_name
        if args.apply:
            target_dir.mkdir(parents=True, exist_ok=True)

        # MP3
        src_mp3 = UNMAPPED / f"{base_name}.mp3"
        if src_mp3.exists():
            dst_mp3 = target_dir / src_mp3.name
            if dst_mp3.exists() and dst_mp3 != src_mp3:
                stem, ext = dst_mp3.stem, dst_mp3.suffix
                i = 1
                while dst_mp3.exists():
                    dst_mp3 = target_dir / f"{stem}_{i}{ext}"
                    i += 1
            if args.dry_run:
                print(f"{mode}{src_mp3.relative_to(UNMAPPED.parent)} -> {dst_mp3.relative_to(ALBUMS_DIR.parent)}")
            else:
                shutil.move(str(src_mp3), str(dst_mp3))
                print(f"  {src_mp3.name} -> {album_name}/")
            moved += 1

        # Transcript
        src_txt = UNMAPPED / "transcripts" / f"{base_name}_transcript.txt"
        if src_txt.exists():
            dst_txt = target_dir / src_txt.name
            if dst_txt.exists() and str(src_txt.resolve()) != str(dst_txt.resolve()):
                stem, ext = dst_txt.stem.replace("_transcript", ""), ".txt"
                i = 1
                while dst_txt.exists():
                    dst_txt = target_dir / f"{stem}_{i}_transcript.txt"
                    i += 1
            if args.dry_run:
                print(f"{mode}transcripts/{src_txt.name} -> {album_name}/")
            else:
                shutil.move(str(src_txt), str(dst_txt))
            moved += 1

        # Analysis
        src_an = UNMAPPED / "analysis" / f"{base_name}_analysis.txt"
        if src_an.exists():
            dst_an = target_dir / src_an.name
            if dst_an.exists() and str(src_an.resolve()) != str(dst_an.resolve()):
                stem = dst_an.stem.replace("_analysis", "")
                i = 1
                while dst_an.exists():
                    dst_an = target_dir / f"{stem}_{i}_analysis.txt"
                    i += 1
            if args.dry_run:
                print(f"{mode}analysis/{src_an.name} -> {album_name}/")
            else:
                shutil.move(str(src_an), str(dst_an))
            moved += 1

    print(f"\n{mode}Total: {moved} file(s) moved.")

    if args.apply:
        # Remove empty transcripts/ and analysis/ dirs if empty
        for sub in ("transcripts", "analysis"):
            d = UNMAPPED / sub
            if d.exists() and not any(d.iterdir()):
                d.rmdir()
                print(f"  Removed empty {d.relative_to(UNMAPPED.parent)}/")


if __name__ == "__main__":
    main()
