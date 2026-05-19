#!/usr/bin/env python3
"""
Clean up remaining files after consolidation.

Moves:
- .pyc files → delete (compiled bytecode)
- Remaining .py files → analyze and categorize
- Documentation files → docs/current/ or docs/archive/
- Data files → data/ or data/reports/
- Archives → _archive/

Usage: python cleanup_remaining.py [--dry-run] [--apply]
"""

import shutil
from pathlib import Path

PROJECT = Path(__file__).parent
DOCS_DIR = PROJECT / "docs"
DATA_DIR = PROJECT / "data"
ARCHIVE_DIR = PROJECT / "_archive"


def categorize_remaining_files() -> dict[str, list[Path]]:
    """Categorize remaining root files."""
    categories = {
        "pyc_files": [],
        "py_scripts": [],
        "docs_current": [],  # README, WORKFLOW, etc.
        "docs_archive": [],  # COMPLEX, FINAL, etc.
        "data_files": [],  # json, csv, txt data
        "archives": [],  # tar.gz, etc.
        "web_files": [],  # html, xml, etc.
        "config_files": [],  # json, sh configs
        "unknown": [],
    }

    for f in PROJECT.iterdir():
        if not f.is_file() or f.name.startswith(".") or f.name in ["README.md"]:
            continue

        # .pyc files
        if f.suffix == ".pyc":
            categories["pyc_files"].append(f)
            continue

        # Python scripts (not consolidation scripts)
        if f.suffix == ".py" and not f.name.startswith("consolidate_"):
            categories["py_scripts"].append(f)
            continue

        # Documentation
        if f.suffix == ".md":
            # Current docs: shorter, practical names
            if any(word in f.name.lower() for word in ["readme", "workflow", "data", "quickstart"]):
                categories["docs_current"].append(f)
            else:
                categories["docs_archive"].append(f)
            continue

        # Data files
        if f.suffix in [".csv", ".json", ".txt"] and not f.name.endswith(".md"):
            # Check if it's data vs report
            if any(word in f.name.lower() for word in ["analysis", "comparison", "report", "summary", "log"]):
                categories["data_files"].append(f)
            else:
                categories["data_files"].append(f)
            continue

        # Archives
        if f.suffix in [".gz", ".tar", ".zip"]:
            categories["archives"].append(f)
            continue

        # Web files
        if f.suffix in [".html", ".xml"]:
            categories["web_files"].append(f)
            continue

        # Config files
        if f.suffix in [".sh", ".json"]:
            categories["config_files"].append(f)
            continue

        # Unknown
        categories["unknown"].append(f)

    return categories


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Clean up remaining files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved")
    parser.add_argument("--apply", action="store_true", help="Execute the cleanup")
    args = parser.parse_args()

    if not (args.dry_run or args.apply):
        print("Use --dry-run or --apply")
        return

    print("Remaining Files Cleanup Plan")
    print("=" * 50)

    categories = categorize_remaining_files()
    total_moved = 0

    for category, files in categories.items():
        if not files:
            continue

        print(f"\n{category.upper().replace('_', ' ')} ({len(files)} files):")

        if category == "pyc_files":
            # Delete .pyc files
            for f in files:
                if args.dry_run:
                    print(f"    [delete] {f.name}")
                else:
                    f.unlink()
                    print(f"    Deleted {f.name}")
                    total_moved += 1

        elif category == "docs_current":
            # Move to docs/current/
            current_dir = DOCS_DIR / "current"
            if args.apply:
                current_dir.mkdir(parents=True, exist_ok=True)

            for f in files:
                dst = current_dir / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → docs/current/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → docs/current/")
                    total_moved += 1

        elif category == "docs_archive":
            # Move to docs/archive/
            archive_docs_dir = DOCS_DIR / "archive"
            if args.apply:
                archive_docs_dir.mkdir(parents=True, exist_ok=True)

            for f in files:
                dst = archive_docs_dir / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → docs/archive/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → docs/archive/")
                    total_moved += 1

        elif category == "data_files":
            # Move to data/reports/ or data/
            reports_dir = DATA_DIR / "reports"
            if args.apply:
                reports_dir.mkdir(parents=True, exist_ok=True)

            for f in files:
                dst = reports_dir / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → data/reports/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → data/reports/")
                    total_moved += 1

        elif category == "archives":
            # Move to _archive/
            if args.apply:
                ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

            for f in files:
                dst = ARCHIVE_DIR / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → _archive/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → _archive/")
                    total_moved += 1

        elif category == "web_files":
            # Move to web/pages/
            pages_dir = PROJECT / "web" / "pages"
            if args.apply:
                pages_dir.mkdir(parents=True, exist_ok=True)

            for f in files:
                dst = pages_dir / f.name
                if args.dry_run:
                    print(f"    [move] {f.name} → web/pages/")
                else:
                    shutil.move(str(f), str(dst))
                    print(f"    Moved {f.name} → web/pages/")
                    total_moved += 1

        elif category == "py_scripts":
            # These need manual review - show them
            print("    Manual review needed:")
            for f in files:
                print(f"        {f.name} - analyze purpose")

        elif category == "config_files":
            # These need manual review
            print("    Manual review needed:")
            for f in files:
                print(f"        {f.name} - analyze purpose")

        elif category == "unknown":
            print("    Manual review needed:")
            for f in files:
                print(f"        {f.name} - unknown type")

    print("\nSummary:")
    print(f"  Files processed: {total_moved}")
    print("  Remaining categories need manual review: py_scripts, config_files, unknown")


if __name__ == "__main__":
    main()
