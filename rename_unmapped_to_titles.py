#!/usr/bin/env python3
"""
Rename Unmapped_UUIDs MP3s, transcripts, and analysis files to human-readable titles
based on transcription/analysis results.
"""

from pathlib import Path

UNMAPPED = Path(__file__).parent / "ALBUMS" / "Unmapped_UUIDs"

# Current stem (no ext) -> new base name (no ext)
RENAME_MAP = {
    "6206280c_F8cf_419c_87b2_4b6cdf824602": "Midnight_Skin",
    "F17765a2_E849_4eb6_83d5_Dd7812e93de4": "Silent_Threads",
    "Untitled": "When_It_All_Went_Wrong",
    "Untitled_1": "Mooji_Satsang_Notice",
    "Untitled_21e0596f_1": "Jingle_My_Bells",
    "Untitled_4d043422_1": "Through_Our_Veins",
    "Untitled_533a72ad_1": "Lets_Do_It",
    "Untitled_8115bcda_1": "Through_Our_Veins_2",
    "Untitled_D815024c_1": "Lets_Do_It_2",
    "Untitled_Ee349f21_1": "Tears_Of_An_Englishman",
}


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="Print renames only")
    p.add_argument("--apply", action="store_true", help="Apply renames")
    args = p.parse_args()
    if not args.dry_run and not args.apply:
        p.error("Use --dry-run or --apply")

    transcripts = UNMAPPED / "transcripts"
    analysis = UNMAPPED / "analysis"

    moves = []

    for old_stem, new_stem in RENAME_MAP.items():
        # Transcript
        src = transcripts / f"{old_stem}_transcript.txt"
        dst = transcripts / f"{new_stem}_transcript.txt"
        if src.exists():
            moves.append((src, dst))

        # Analysis
        src = analysis / f"{old_stem}_analysis.txt"
        dst = analysis / f"{new_stem}_analysis.txt"
        if src.exists():
            moves.append((src, dst))

        # MP3 (can be in root or nested)
        for mp3 in UNMAPPED.rglob(f"{old_stem}.mp3"):
            dst = mp3.parent / f"{new_stem}.mp3"
            moves.append((mp3, dst))

    for src, dst in moves:
        if src == dst:
            continue
        if dst.exists() and not args.dry_run:
            print(f"SKIP (dest exists): {src.name} -> {dst.name}")
            continue
        if args.dry_run:
            print(f"  {src.relative_to(UNMAPPED)} -> {dst.relative_to(UNMAPPED)}")
        else:
            src.rename(dst)
            print(f"  {src.name} -> {dst.name}")

    if args.dry_run:
        print(f"\n{len(moves)} rename(s) would be applied. Run with --apply to execute.")
    else:
        print(f"\nRenamed {len(moves)} file(s).")


if __name__ == "__main__":
    main()
