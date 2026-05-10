#!/usr/bin/env python3
"""from pathlib import Path
import csv
import re
import shutil
?? COMPREHENSIVE RENAMER
Standardize both MP3 and transcript filenames for clean matching
"""


def clean_filename(name: str) -> str:
    """Create clean, standardized filename"""
    # Remove common suffixes and tags
    name = re.sub(r"_\d{3}$", "", name)  # Remove trailing numbers like _359
    name = re.sub(
        r"\s*-\s*\[?(Edit|Remix|Remastered|Cover)\]?",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"\s*\(\d+:\d+\)", "", name)  # Remove duration timestamps
    name = re.sub(r"\s*\(\d+\)", "", name)  # Remove (1), (2), etc
    name = re.sub(r"_\d+$", "", name)  # Remove trailing _1, _2, etc

    # Normalize separators
    name = name.replace("_", " ").replace("-", " ")

    # Remove special characters
    name = re.sub(r"[?????????????]", "", name)  # Remove emojis
    name = re.sub(r"\[.*?\]", "", name)  # Remove [brackets]
    name = re.sub(r"\(.*?\)", "", name)  # Remove (parentheses)

    # Normalize whitespace
    name = " ".join(name.split())

    # Title case
    name = name.title()

    return name.strip()


def propose_renames():
    """Propose standardized names for all MP3s and transcripts"""
    print("\n" + "=" * 80)
    print("  ?? COMPREHENSIVE FILE RENAMER")
    print("  Standardize MP3s AND Transcripts")
    print("=" * 80 + "\n")

    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    fuzzy_csv = base_dir / "TRANSCRIPT_MATCHING" / "FUZZY_MATCHES.csv"

    if not fuzzy_csv.exists():
        print("? Run match_transcripts.py first!")
        return

    # Load fuzzy matches
    with open(fuzzy_csv) as f:
        reader = csv.DictReader(f)
        fuzzy_matches = list(reader)

    print(f"?? Loaded {len(fuzzy_matches)} fuzzy-matched pairs\n")

    # Analyze all folders
    folders = [d for d in base_dir.iterdir() if d.is_dir() and d.name[0].isupper()]

    all_renames = []

    for folder in sorted(folders):
        mp3_files = list(folder.glob("*.mp3"))
        txt_files = list(folder.glob("*.txt"))

        if not mp3_files:
            continue

        print(f"?? {folder.name}")
        print(f"   MP3s: {len(mp3_files)} | TXTs: {len(txt_files)}")

        # Build rename proposals for this folder
        folder_renames = []

        # Get fuzzy matches for this folder
        folder_matches = [m for m in fuzzy_matches if m["folder"] == folder.name]

        for match in folder_matches:
            mp3_stem = match["mp3"]
            txt_stem = match["txt"]

            # Create clean standardized name
            clean_name = clean_filename(mp3_stem)

            # Avoid duplicates by adding folder-specific prefix if needed
            if folder.name != "Singles":
                # Use folder name as context
                folder_prefix = folder.name.replace("_", " ")
                if not clean_name.lower().startswith(folder_prefix.lower().split()[0]):
                    # Add folder context if not already present
                    pass  # Keep as is

            mp3_old = folder / f"{mp3_stem}.mp3"
            txt_old = folder / f"{txt_stem}.txt"

            # Create new standardized names
            mp3_new = folder / f"{clean_name}.mp3"
            txt_new = folder / f"{clean_name}.txt"

            # Only rename if different
            if mp3_old.exists() and mp3_old != mp3_new:
                folder_renames.append(
                    {
                        "type": "mp3",
                        "folder": folder.name,
                        "old_path": str(mp3_old),
                        "new_path": str(mp3_new),
                        "old_name": mp3_stem,
                        "new_name": clean_name,
                    },
                )

            if txt_old.exists() and txt_old != txt_new:
                folder_renames.append(
                    {
                        "type": "txt",
                        "folder": folder.name,
                        "old_path": str(txt_old),
                        "new_path": str(txt_new),
                        "old_name": txt_stem,
                        "new_name": clean_name,
                    },
                )

        if folder_renames:
            print(f"   ?? Proposing {len(folder_renames)} renames")
            # Show first 3 examples
            for rename in folder_renames[:3]:
                print(f"      {rename['type'].upper()}: {rename['old_name'][:50]}")
                print(f"           ? {rename['new_name'][:50]}")
            if len(folder_renames) > 3:
                print(f"      ... and {len(folder_renames) - 3} more")

            all_renames.extend(folder_renames)

        print()

    # Save rename plan
    if all_renames:
        plan_csv = base_dir / "RENAME_PLAN.csv"

        with open(plan_csv, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "type",
                    "folder",
                    "old_path",
                    "new_path",
                    "old_name",
                    "new_name",
                ],
            )
            writer.writeheader()
            writer.writerows(all_renames)

        print("=" * 80)
        print("  ?? RENAME SUMMARY")
        print("=" * 80 + "\n")

        mp3_renames = [r for r in all_renames if r["type"] == "mp3"]
        txt_renames = [r for r in all_renames if r["type"] == "txt"]

        print(f"Total renames proposed: {len(all_renames)}")
        print(f"  ? MP3 files: {len(mp3_renames)}")
        print(f"  ? TXT files: {len(txt_renames)}")
        print()

        print("?? Rename plan saved: RENAME_PLAN.csv")
        print()
        print("??  REVIEW THE PLAN BEFORE EXECUTING!")
        print("   Open RENAME_PLAN.csv to review all proposed renames")
        print()
        print("To execute renames, run:")
        print("   python3 execute_renames.py")
        print()
    else:
        print("? All files already have clean names!")


def create_executor():
    """Create the rename executor script"""
    executor_code = "\'"#!/usr/bin/env python3
"""Execute the rename plan"""

import csv
import shutil
from pathlib import Path

def execute_renames():
    """Execute all renames from RENAME_PLAN.csv"""
    
    base_dir = Path('/Users/steven/Music/nocTurneMeLoDieS')
    plan_csv = base_dir / 'RENAME_PLAN.csv'
    
    if not plan_csv.exists():
        print("? No RENAME_PLAN.csv found!")
        print("   Run: python3 rename_and_standardize.py first")
        return
    
    # Load plan
    with open(plan_csv, 'r') as f:
        reader = csv.DictReader(f)
        renames = list(reader)
    
    print(f"\\n?? Loaded {len(renames)} renames\\n")
    print("??  WARNING: This will rename files!")
    print("   Press Ctrl+C to cancel, or Enter to continue...")
    try:
        input()
    except KeyboardInterrupt:
        print("\\n\\n? Cancelled")
        return
    
    success = 0
    failed = []
    skipped = 0
    
    for i, rename in enumerate(renames, 1):
        old_path = Path(rename['old_path'])
        new_path = Path(rename['new_path'])
        
        if not old_path.exists():
            print(f"??  {i:3d}. Skipped (not found): {old_path.name}")
            skipped += 1
            continue
        
        if new_path.exists():
            print(f"??  {i:3d}. Skipped (target exists): {new_path.name}")
            skipped += 1
            continue
        
        try:
            shutil.move(str(old_path), str(new_path))
            print(f"? {i:3d}. {rename['type'].upper()}: {old_path.name[:50]}")
            print(f"         ? {new_path.name[:50]}")
            success += 1
        except Exception as e:
            print(f"? {i:3d}. Failed: {old_path.name} - {e}")
            failed.append(old_path.name)
        
        if i % 50 == 0:
            print(f"\\n?? Progress: {i}/{len(renames)} (? {success} | ??  {skipped} | ? {len(failed)})\\n")
    
    print("\\n" + "="*80)
    print("  ? RENAME COMPLETE!")
    print("="*80 + "\\n")
    print(f"? Successfully renamed: {success}")
    print(f"??  Skipped: {skipped}")
    print(f"? Failed: {len(failed)}")
    
    if failed:
        print(f"\\nFailed files:")
        for name in failed[:10]:
            print(f"  ? {name}")

if __name__ == '__main__':
    execute_renames()
"\'"

    executor_path = Path("/Users/steven/Music/nocTurneMeLoDieS/execute_renames.py")
    with open(executor_path, "w") as f:
        f.write(executor_code)
    executor_path.chmod(0o755)

    print("?? Created: execute_renames.py")


if __name__ == "__main__":
    propose_renames()
    create_executor()
