#!/usr/bin/env python3
"""
Organize Album Companion Files
Moves companion files (transcripts, analyses, .srt) to be with their MP3s
Handles both flat and subfolder structures
"""

from pathlib import Path
import shutil
import argparse
from typing import List, Tuple


def organize_folder(folder_path: Path, dry_run: bool = False) -> Tuple[int, int]:
    """
    Organize companion files in a single folder.
    Moves files from transcripts/ and analysis/ subfolders to be with MP3s.
    Returns (moved_count, skipped_count)
    """
    moved = 0
    skipped = 0
    
    print(f"\n?? {folder_path.name}")
    
    # Find all MP3s in this folder
    mp3s = list(folder_path.glob("*.mp3"))
    
    if not mp3s:
        print(f"   ??  No MP3s found, skipping")
        return (0, 0)
    
    # Check for subfolder structure
    transcripts_dir = folder_path / "transcripts"
    analysis_dir = folder_path / "analysis"
    
    # Process each MP3
    for mp3 in mp3s:
        stem = mp3.stem
        
        # Check transcripts subfolder
        if transcripts_dir.exists():
            for suffix in ["_transcript.txt", ".srt"]:
                src = transcripts_dir / f"{stem}{suffix}"
                if src.exists():
                    dest = folder_path / f"{stem}{suffix}"
                    if dest.exists():
                        print(f"   ??  Skip (exists): {stem}{suffix}")
                        skipped += 1
                    else:
                        if dry_run:
                            print(f"   [DRY] Would move: transcripts/{stem}{suffix}")
                            moved += 1
                        else:
                            try:
                                shutil.move(str(src), str(dest))
                                print(f"   ? Moved: transcripts/{stem}{suffix}")
                                moved += 1
                            except Exception as e:
                                print(f"   ? Error: {e}")
                                skipped += 1
        
        # Check analysis subfolder
        if analysis_dir.exists():
            src = analysis_dir / f"{stem}_analysis.txt"
            if src.exists():
                dest = folder_path / f"{stem}_analysis.txt"
                if dest.exists():
                    print(f"   ??  Skip (exists): {stem}_analysis.txt")
                    skipped += 1
                else:
                    if dry_run:
                        print(f"   [DRY] Would move: analysis/{stem}_analysis.txt")
                        moved += 1
                    else:
                        try:
                            shutil.move(str(src), str(dest))
                            print(f"   ? Moved: analysis/{stem}_analysis.txt")
                            moved += 1
                        except Exception as e:
                            print(f"   ? Error: {e}")
                            skipped += 1
    
    # Clean up empty subfolders
    if not dry_run:
        for subdir in [transcripts_dir, analysis_dir]:
            if subdir.exists() and not any(subdir.iterdir()):
                subdir.rmdir()
                print(f"   ???  Removed empty: {subdir.name}/")
    
    return (moved, skipped)


def main():
    parser = argparse.ArgumentParser(
        description="Organize companion files within album folders"
    )
    parser.add_argument(
        "folders",
        nargs="+",
        type=Path,
        help="Album folders to organize"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )
    
    args = parser.parse_args()
    
    print(f"\n{'='*80}")
    print(f"  ?? Album Companion Organizer")
    print(f"{'='*80}")
    
    if args.dry_run:
        print(f"\n??  DRY RUN MODE - No files will be moved\n")
    
    total_moved = 0
    total_skipped = 0
    processed_folders = 0
    
    for folder_path in args.folders:
        if not folder_path.exists():
            print(f"\n??  Folder not found: {folder_path}")
            continue
        
        if not folder_path.is_dir():
            print(f"\n??  Not a directory: {folder_path}")
            continue
        
        moved, skipped = organize_folder(folder_path, args.dry_run)
        total_moved += moved
        total_skipped += skipped
        processed_folders += 1
    
    # Summary
    print(f"\n{'='*80}")
    print(f"  ? Organization Complete!")
    print(f"{'='*80}")
    print(f"\n?? Summary:")
    print(f"   Folders processed: {processed_folders}")
    print(f"   Files moved: {total_moved}")
    print(f"   Files skipped: {total_skipped}")
    
    if args.dry_run:
        print(f"\n??  This was a dry run - no files were actually moved")
        print(f"   Run without --dry-run to apply changes")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    main()
