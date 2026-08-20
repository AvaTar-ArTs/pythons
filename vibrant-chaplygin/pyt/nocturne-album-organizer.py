#!/usr/bin/env python3
"""
NocTurnE Album Organizer
Organizes MP3 files and their companion files into album folders
Handles: .mp3, _transcript.txt, _analysis.txt, .srt files
"""

from pathlib import Path
import shutil
import argparse
from typing import List, Tuple, Set
from collections import defaultdict


# Configuration
MUSIC_ROOT = Path.home() / "Music" / "nocTurneMeLoDieS"
COMPANION_SUFFIXES = ["_transcript.txt", "_analysis.txt", ".srt"]


def find_companion_files(mp3_path: Path) -> List[Path]:
    """
    Find all companion files for a given MP3.
    Checks both flat structure and subfolder structure:
    - Flat: folder/file_transcript.txt
    - Subfolder: folder/transcripts/file_transcript.txt
    Returns list of existing companion file paths.
    """
    stem = mp3_path.stem
    parent = mp3_path.parent
    companions = []
    
    for suffix in COMPANION_SUFFIXES:
        # Check flat structure (file in same folder)
        companion_flat = parent / f"{stem}{suffix}"
        if companion_flat.exists():
            companions.append(companion_flat)
            continue
        
        # Check subfolder structure
        if suffix == "_transcript.txt":
            companion_sub = parent / "transcripts" / f"{stem}{suffix}"
            if companion_sub.exists():
                companions.append(companion_sub)
        elif suffix == "_analysis.txt":
            companion_sub = parent / "analysis" / f"{stem}{suffix}"
            if companion_sub.exists():
                companions.append(companion_sub)
        elif suffix == ".srt":
            companion_sub = parent / "transcripts" / f"{stem}{suffix}"
            if companion_sub.exists():
                companions.append(companion_sub)
    
    return companions


def get_album_name_from_path(mp3_path: Path) -> str:
    """
    Extract album name from MP3 filename.
    Handles various naming patterns:
    - Love_is_rubbish_Lets_Get_Trashy_Remix329.mp3 -> Love_is_rubbish
    - imperfection313.mp3 -> imperfection (if in Love_In_Imperfection folder)
    - Spine_of_Stars.mp3 -> Singles (if in root, no obvious album)
    """
    filename = mp3_path.stem
    
    # If already in a subfolder, use that folder name
    if mp3_path.parent != MUSIC_ROOT:
        return mp3_path.parent.name
    
    # Pattern matching for common prefixes
    album_patterns = {
        "Love_is_rubbish": "Love_Is_Rubbish",
        "Love_is_Rubbish": "Love_Is_Rubbish",
        "imperfection": "Love_In_Imperfection",
        "Witches": "Witches_Road",
        "Witches_Road": "Witches_Road",
        "Live_fast": "Love_Is_Rubbish",
        "Trash_Revolution": "Love_Is_Rubbish",
        "rubbish": "Love_Is_Rubbish",
    }
    
    # Check for pattern matches
    for pattern, album in album_patterns.items():
        if filename.startswith(pattern):
            return album
    
    # Default: use first part before underscore or number
    parts = filename.split('_')
    if len(parts) > 1:
        # Remove trailing numbers/versions
        base = '_'.join(p for p in parts if not p.isdigit() and not p.startswith('Remix'))
        return base if base else "Singles"
    
    return "Singles"


def organize_album(mp3_path: Path, dry_run: bool = False) -> Tuple[int, int]:
    """
    Organize an MP3 and its companion files into an album folder.
    Returns (moved_count, skipped_count)
    """
    # Determine album folder
    album_name = get_album_name_from_path(mp3_path)
    album_folder = MUSIC_ROOT / album_name
    
    # Skip if already in correct location
    if mp3_path.parent == album_folder:
        return (0, 1)
    
    # Create album folder
    if not dry_run:
        album_folder.mkdir(exist_ok=True)
    
    moved = 0
    skipped = 0
    
    # Find all companion files
    companions = find_companion_files(mp3_path)
    all_files = [mp3_path] + companions
    
    print(f"\n?? Album: {album_name}")
    print(f"   MP3: {mp3_path.name}")
    
    # Move each file
    for file_path in all_files:
        dest_path = album_folder / file_path.name
        
        # Check if destination already exists
        if dest_path.exists():
            print(f"   ??  Skip (exists): {file_path.name}")
            skipped += 1
            continue
        
        # Move file
        if dry_run:
            print(f"   [DRY RUN] Would move: {file_path.name}")
            moved += 1
        else:
            try:
                shutil.move(str(file_path), str(dest_path))
                print(f"   ? Moved: {file_path.name}")
                moved += 1
            except Exception as e:
                print(f"   ? Error moving {file_path.name}: {e}")
                skipped += 1
    
    return (moved, skipped)


def scan_and_organize(music_root: Path = MUSIC_ROOT, dry_run: bool = False):
    """
    Scan music library and organize all MP3s into album folders.
    """
    print(f"\n{'='*80}")
    print(f"  ?? NocTurnE Album Organizer")
    print(f"{'='*80}")
    print(f"\n?? Scanning: {music_root}")
    
    if dry_run:
        print(f"??  DRY RUN MODE - No files will be moved\n")
    
    # Find all MP3s in root directory
    root_mp3s = list(music_root.glob("*.mp3"))
    
    if not root_mp3s:
        print("\n? No MP3s found in root directory. All organized!")
        return
    
    print(f"\n?? Found {len(root_mp3s)} MP3(s) in root directory\n")
    
    total_moved = 0
    total_skipped = 0
    
    # Organize each MP3
    for mp3_path in sorted(root_mp3s):
        moved, skipped = organize_album(mp3_path, dry_run)
        total_moved += moved
        total_skipped += skipped
    
    # Summary
    print(f"\n{'='*80}")
    print(f"  ? Organization Complete!")
    print(f"{'='*80}")
    print(f"\n?? Summary:")
    print(f"   Files moved: {total_moved}")
    print(f"   Files skipped: {total_skipped}")
    
    if dry_run:
        print(f"\n??  This was a dry run - no files were actually moved")
        print(f"   Run without --dry-run to apply changes")
    
    print(f"\n{'='*80}\n")


def verify_organization(music_root: Path = MUSIC_ROOT):
    """
    Verify that all MP3s have their companion files in the same folder.
    """
    print(f"\n{'='*80}")
    print(f"  ?? Verifying Album Organization")
    print(f"{'='*80}\n")
    
    issues = []
    
    # Check all MP3s in all folders
    for mp3_path in music_root.rglob("*.mp3"):
        if mp3_path.parent == music_root:
            continue  # Skip root files (not yet organized)
        
        companions = find_companion_files(mp3_path)
        stem = mp3_path.stem
        
        # Check for missing companions
        for suffix in COMPANION_SUFFIXES:
            companion_path = mp3_path.parent / f"{stem}{suffix}"
            if suffix in ["_transcript.txt", "_analysis.txt"]:  # These are expected
                if not companion_path.exists():
                    issues.append(f"Missing {suffix}: {mp3_path.relative_to(music_root)}")
    
    if issues:
        print(f"??  Found {len(issues)} missing companion files:\n")
        for issue in issues[:20]:  # Show first 20
            print(f"   {issue}")
        if len(issues) > 20:
            print(f"   ... and {len(issues) - 20} more")
    else:
        print("? All organized MP3s have their companion files!")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize nocTurneMeLoDieS MP3s and companion files into album folders"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify organization and check for missing companion files"
    )
    parser.add_argument(
        "--music-root",
        type=Path,
        default=MUSIC_ROOT,
        help=f"Music library root (default: {MUSIC_ROOT})"
    )
    
    args = parser.parse_args()
    
    if args.verify:
        verify_organization(args.music_root)
    else:
        scan_and_organize(args.music_root, args.dry_run)
