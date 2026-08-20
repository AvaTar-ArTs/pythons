#!/usr/bin/env python3
"""
Execute Comprehensive Deduplication & Rename
Actually performs the cleanup with safety checks
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys


def execute_cleanup(dry_run=True):
    root = Path(str(Path.home()) + "/documents/python")
    plan_file = root / "DEDUP_RENAME_PLAN.json"

    if not plan_file.exists():
        print("? Run comprehensive_dedup_rename.py first!")
        return

    with open(plan_file) as f:
        plan = json.load(f)

    mode = "?? DRY RUN" if dry_run else "?? EXECUTING"
    print(f"\n{mode} - COMPREHENSIVE CLEANUP")
    print("=" * 70)

    # Create backup archive first
    if not dry_run:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = root / f"PRE_CLEANUP_BACKUP_{timestamp}.tar.gz"

        print(f"?? Creating backup: {backup_file.name}")
        import tarfile

        with tarfile.open(backup_file, "w:gz") as tar:
            for item in plan["keep_rename"]:
                filepath = Path(item["old_path"])
                if filepath.exists():
                    tar.add(filepath, arcname=filepath.relative_to(root))
            for item in plan["delete_duplicate"]:
                filepath = Path(item["file"])
                if filepath.exists():
                    tar.add(filepath, arcname=filepath.relative_to(root))
        print(f"? Backup saved: {backup_file.name}\n")

    stats = {"renamed": 0, "deleted": 0, "errors": 0}

    # Step 1: Delete duplicates
    print("???  DELETING DUPLICATES:")
    print("-" * 70)

    for item in plan["delete_duplicate"]:
        filepath = Path(item["file"])
        dup_of = Path(item["duplicate_of"]).name

        if not filepath.exists():
            print(f"??  Already gone: {filepath.name}")
            continue

        if dry_run:
            print(f"Would delete: {filepath.name} (duplicate of {dup_of})")
        else:
            try:
                filepath.unlink()
                print(f"? Deleted: {filepath.name} (dup of {dup_of})")
                stats["deleted"] += 1
            except Exception as e:
                print(f"? Error deleting {filepath.name}: {e}")
                stats["errors"] += 1

    # Step 2: Rename files
    print(f"\n??  RENAMING TO DESCRIPTIVE NAMES:")
    print("-" * 70)

    by_category = defaultdict(list)
    for item in plan["keep_rename"]:
        by_category[item["category"]].append(item)

    for category in sorted(by_category.keys()):
        items = by_category[category]
        print(f"\n?? {category}/ ({len(items)} files)")

        for item in items:
            old_path = Path(item["old_path"])
            if not old_path.exists():
                continue

            new_path = old_path.parent / item["new_name"]

            if old_path == new_path:
                continue  # Already has the right name

            if new_path.exists() and new_path != old_path:
                print(f"??  Skip {old_path.name}: {item['new_name']} already exists")
                continue

            if dry_run:
                print(f"  {item['old_name']:40} ? {item['new_name']}")
            else:
                try:
                    old_path.rename(new_path)
                    print(f"  ? {item['old_name']:40} ? {item['new_name']}")
                    stats["renamed"] += 1
                except Exception as e:
                    print(f"  ? Error: {item['old_name']}: {e}")
                    stats["errors"] += 1

    # Summary
    print("\n" + "=" * 70)
    print("?? SUMMARY")
    print("=" * 70)

    if dry_run:
        print(f"Would rename: {len(plan['keep_rename'])} files")
        print(f"Would delete: {len(plan['delete_duplicate'])} duplicates")
        print("\n?? This was a DRY RUN - no changes made")
        print("\nTo execute:")
        print("  python3 execute_dedup_rename.py --execute")
    else:
        print(f"? Renamed: {stats['renamed']} files")
        print(f"? Deleted: {stats['deleted']} duplicates")
        print(f"? Errors: {stats['errors']}")
        print(f"\n?? Backup saved before changes")
        print("\n?? Cleanup complete!")

        # Save cleanup report
        report = {
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
            "backup_file": f"PRE_CLEANUP_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz",
        }

        with open(root / "CLEANUP_REPORT.json", "w") as f:
            json.dump(report, f, indent=2)


def main():
    dry_run = "--execute" not in sys.argv

    if not dry_run:
        print("??  WARNING: This will rename/delete files!")
        print("A backup will be created first.\n")
        response = input("Continue? (yes/no): ")
        if response.lower() != "yes":
            print("? Cancelled")
            return

    execute_cleanup(dry_run=dry_run)


if __name__ == "__main__":
    main()
