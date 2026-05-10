#!/usr/bin/env python3
"""
Consolidate documentation files.

Moves:
- Archive docs (COMPLETE_*, FINAL_*, etc.) → docs/archive/
- Current docs (README, WORKFLOW, etc.) → docs/current/
- Specialized docs stay at root or docs/

Usage: python consolidate_docs.py [--dry-run] [--apply]
"""

import shutil
from pathlib import Path

PROJECT = Path(__file__).parent
DOCS_DIR = PROJECT / "docs"
CURRENT_DIR = DOCS_DIR / "current"
ARCHIVE_DIR = DOCS_DIR / "archive"

# Files to keep at root
KEEP_AT_ROOT = {
    "README.md",
    "WORKFLOW.md",
    "DATA_SCHEMA.md",
    "LYRICS_CSV_MD_REVIEW.md",
    "CODE_AWARE_REVIEW.md",
    "V4_V5_PLATFORM_REVIEW.md",
    "PARENT_CHILD_FOLDER_AWARENESS.md",
    "CONSOLIDATION_REPORT.md",
    "FOLDER_REORGANIZATION_PROPOSAL.md",
    "FINAL_CLEANUP_ANALYSIS.md",
}


def is_archive_doc(filename: str) -> bool:
    """Check if doc should go to archive."""
    archive_patterns = [
        "COMPLETE_",
        "FINAL_",
        "COMPREHENSIVE_",
        "FULL_",
        "PROJECT_",
        "NOCTURNEMELODIES_",
        "HTML_",
        "ARCHIVE_",
        "IMPLEMENTATION_",
        "CURRENT_STATE_",
        "ENHANCED_",
        "MUSIC_",
        "ALBUM_",
        "CONTENT_",
        "DUPLICATE_",
        "SUno_",
        "SYNC_",
    ]
    return any(filename.upper().startswith(pattern) for pattern in archive_patterns)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Consolidate documentation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved")
    parser.add_argument("--apply", action="store_true", help="Execute the consolidation")
    args = parser.parse_args()

    if not (args.dry_run or args.apply):
        print("Use --dry-run or --apply")
        return

    print("Documentation Consolidation")
    print("=" * 40)

    moved = 0

    # Create dirs
    if args.apply:
        CURRENT_DIR.mkdir(parents=True, exist_ok=True)
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Process MD files
    for f in PROJECT.glob("*.md"):
        if f.name in KEEP_AT_ROOT:
            if args.dry_run:
                print(f"    [keep] {f.name} (at root)")
            continue

        if is_archive_doc(f.name):
            dst = ARCHIVE_DIR / f.name
            if args.dry_run:
                print(f"    [move] {f.name} → docs/archive/")
            else:
                shutil.move(str(f), str(dst))
                print(f"    Moved {f.name} → docs/archive/")
                moved += 1
        else:
            dst = CURRENT_DIR / f.name
            if args.dry_run:
                print(f"    [move] {f.name} → docs/current/")
            else:
                shutil.move(str(f), str(dst))
                print(f"    Moved {f.name} → docs/current/")
                moved += 1

    print("\nSummary:")
    print(f"  Docs moved: {moved}")
    print(f"  Kept at root: {len(KEEP_AT_ROOT)} files")


if __name__ == "__main__":
    main()
