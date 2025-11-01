#!/usr/bin/env python3
"""
Script Version Consolidator
Consolidates versioned scripts based on analysis
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


def consolidate_versions(dry_run=True):
    """Consolidate versioned scripts"""

    root = Path("/Users/steven/documents/python")
    report_file = root / "VERSION_ANALYSIS_REPORT.json"

    if not report_file.exists():
        print("? Please run analyze_versions.py first!")
        return

    # Load consolidation plan
    with open(report_file) as f:
        plan = json.load(f)

    # Create archive directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = root / f"_version_archive_{timestamp}"

    if not dry_run:
        archive_dir.mkdir(exist_ok=True)
        print(f"?? Created archive: {archive_dir.name}")

    print(f"\n{'?? DRY RUN MODE' if dry_run else '?? EXECUTING CONSOLIDATION'}")
    print("=" * 70)

    stats = {
        "families_processed": 0,
        "files_archived": 0,
        "files_renamed": 0,
        "bytes_freed": 0,
    }

    for item in plan:
        base_name = item["base_name"]
        category = item["category"]
        keep_path = Path(item["keep_path"])
        archives = item["archive"]

        if not archives:
            continue  # No versions to archive

        stats["families_processed"] += 1

        print(f"\n?? {category}/{base_name}")
        print(f"  ? Keeping: {item['keep']}")

        # Archive old versions
        for arch in archives:
            old_path = Path(arch["path"])

            if not old_path.exists():
                print(f"  ??  File not found: {arch['name']}")
                continue

            # Create category subdirectory in archive
            category_archive = archive_dir / category

            if not dry_run:
                category_archive.mkdir(exist_ok=True, parents=True)
                # Move file to archive
                dest = category_archive / arch["name"]
                shutil.move(str(old_path), str(dest))
                action = "Moved"
            else:
                action = "Would move"

            print(
                f"  ?? {action}: {arch['name']} ? _version_archive_{timestamp}/{category}/"
            )
            stats["files_archived"] += 1
            stats["bytes_freed"] += arch["size"]

        # Rename the keeper to canonical name (remove version suffix)
        canonical_name = f"{base_name}.py"
        canonical_path = keep_path.parent / canonical_name

        if keep_path.name != canonical_name and not canonical_path.exists():
            if not dry_run:
                shutil.copy2(str(keep_path), str(canonical_path))
                action = "Created"
            else:
                action = "Would create"

            print(f"  ?? {action}: {canonical_name} (canonical version)")
            stats["files_renamed"] += 1

    # Summary
    print("\n" + "=" * 70)
    print("?? CONSOLIDATION SUMMARY")
    print("=" * 70)
    print(f"Script families processed: {stats['families_processed']}")
    print(f"Files archived: {stats['files_archived']}")
    print(f"Canonical versions created: {stats['files_renamed']}")
    print(f"Disk space to be freed: {stats['bytes_freed'] / 1024 / 1024:.2f} MB")

    if dry_run:
        print("\n" + "=" * 70)
        print("?? This was a DRY RUN - no files were modified")
        print("\nTo actually consolidate:")
        print("  python3 consolidate_versions.py --execute")
    else:
        print(f"\n? Files archived to: {archive_dir.name}")
        print("\n??  IMPORTANT: Test your scripts before deleting the archive!")
        print("To restore if needed:")
        print(f"  cp -r {archive_dir}/*/* ./")

    return stats


def main():
    import sys

    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("?? Running in DRY RUN mode (no changes will be made)")
        print("   Add --execute flag to actually consolidate files")
        print()
    else:
        print("??  WARNING: This will move files!")
        response = input("Continue? (yes/no): ")
        if response.lower() != "yes":
            print("? Cancelled")
            return

    consolidate_versions(dry_run=dry_run)


if __name__ == "__main__":
    main()
