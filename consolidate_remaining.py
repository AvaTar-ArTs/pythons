#!/usr/bin/env python3
"""
Consolidate remaining data files, web files, and archives.

Moves:
- Data files → data/reports/ or data/
- Web files → web/pages/
- Archives → _archive/
- Shell scripts → scripts/ or keep as-is

Usage: python consolidate_remaining.py [--dry-run] [--apply]
"""

import shutil
from pathlib import Path

PROJECT = Path(__file__).parent
DATA_DIR = PROJECT / "data"
REPORTS_DIR = DATA_DIR / "reports"
WEB_DIR = PROJECT / "web"
PAGES_DIR = WEB_DIR / "pages"
ARCHIVE_DIR = PROJECT / "_archive"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Consolidate remaining files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved")
    parser.add_argument("--apply", action="store_true", help="Execute the consolidation")
    args = parser.parse_args()

    if not (args.dry_run or args.apply):
        print("Use --dry-run or --apply")
        return

    print("Remaining Files Consolidation")
    print("=" * 40)

    moved = 0

    # Create dirs
    if args.apply:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        PAGES_DIR.mkdir(parents=True, exist_ok=True)
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Process remaining files
    for f in PROJECT.iterdir():
        if not f.is_file() or f.name.startswith(".") or f.name.startswith("consolidate_"):
            continue

        # Data files
        if f.suffix in [".csv", ".json", ".txt"]:
            if any(word in f.stem.lower() for word in ["analysis", "comparison", "report", "summary", "log"]):
                dst = REPORTS_DIR / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → data/reports/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → data/reports/")
                    moved += 1
            else:
                # Other data files
                dst = DATA_DIR / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → data/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → data/")
                    moved += 1

        # Web files
        elif f.suffix in [".html", ".xml"]:
            dst = PAGES_DIR / f.name
            if args.dry_run:
                print(f"    [move] {f.name} → web/pages/")
            else:
                shutil.move(str(f), str(dst))
                print(f"    Moved {f.name} → web/pages/")
                moved += 1

        # Archives
        elif f.suffix in [".gz", ".tar", ".zip"]:
            dst = ARCHIVE_DIR / f.name
            if args.dry_run:
                print(f"    [move] {f.name} → _archive/")
            else:
                shutil.move(str(f), str(dst))
                print(f"    Moved {f.name} → _archive/")
                moved += 1

        # Shell scripts - keep at root for now
        elif f.suffix == ".sh":
            if args.dry_run:
                print(f"    [keep] {f.name} (shell script)")
            continue

        # Python scripts - keep consolidation scripts
        elif f.suffix == ".py":
            if args.dry_run:
                print(f"    [keep] {f.name} (remaining Python)")
            continue

        # Other files
        else:
            if args.dry_run:
                print(f"    [unknown] {f.name} - manual review needed")
            continue

    print("\nSummary:")
    print(f"  Files moved: {moved}")


if __name__ == "__main__":
    main()
