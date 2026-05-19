#!/usr/bin/env python3
"""
Execute the changes from BEFORE_AFTER_REVIEW.csv
Moves, keeps, and deletes files/folders as specified.
"""

import sys
import csv
import shutil
from pathlib import Path
from collections import defaultdict


def execute_changes(csv_file, dry_run=True):
    """Execute changes from CSV file."""
    root_path = Path.home() / "pythons"
    csv_path = Path(csv_file)

    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_file}")
        return

    print("=" * 80)
    print("🚀 EXECUTING CHANGES FROM CSV")
    print("=" * 80)
    print()

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("   Run with --execute to apply changes")
        print()
    else:
        print("⚠️  EXECUTE MODE - Changes will be applied!")
        print()

    # Read CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"📊 Loaded {len(rows)} items from CSV")
    print()

    # Group by action
    by_action = defaultdict(list)
    for row in rows:
        by_action[row["action"]].append(row)

    stats = {"moved": 0, "deleted": 0, "kept": 0, "errors": 0, "skipped": 0}

    # Process deletions first (safest)
    print("=" * 80)
    print("🗑️  PROCESSING DELETIONS")
    print("=" * 80)
    print()

    for row in by_action.get("delete", []):
        file_path = root_path / row["before_path"]

        if not file_path.exists():
            print(f"⚠️  SKIP: {row['before_path']} (not found)")
            stats["skipped"] += 1
            continue

        if dry_run:
            print(f"   Would delete: {row['before_path']}")
            stats["deleted"] += 1
        else:
            try:
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                print(f"   ✅ Deleted: {row['before_path']}")
                stats["deleted"] += 1
            except Exception as e:
                print(f"   ❌ Error deleting {row['before_path']}: {e}")
                stats["errors"] += 1

    print()

    # Process moves
    print("=" * 80)
    print("📦 PROCESSING MOVES")
    print("=" * 80)
    print()

    # Sort by priority (P1 first)
    moves = sorted(by_action.get("move", []), key=lambda x: x["priority"])

    for row in moves:
        source_path = root_path / row["before_path"]
        dest_path = root_path / row["after_path"]

        if not source_path.exists():
            print(f"⚠️  SKIP: {row['before_path']} (not found)")
            stats["skipped"] += 1
            continue

        # Check if destination already exists
        if dest_path.exists():
            print(f"⚠️  SKIP: {row['after_path']} (already exists)")
            stats["skipped"] += 1
            continue

        if dry_run:
            print(f"   Would move: {row['before_path']}")
            print(f"            → {row['after_path']}")
            stats["moved"] += 1
        else:
            try:
                # Create destination directory if needed
                if row["type"] == "file":
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Move the file/folder
                shutil.move(str(source_path), str(dest_path))
                print(f"   ✅ Moved: {row['before_path']} → {row['after_path']}")
                stats["moved"] += 1
            except Exception as e:
                print(f"   ❌ Error moving {row['before_path']}: {e}")
                stats["errors"] += 1

    print()

    # Process keeps (just log them)
    print("=" * 80)
    print("✅ PROCESSING KEEPS")
    print("=" * 80)
    print()

    keeps = by_action.get("keep", [])
    stats["kept"] = len(keeps)

    if len(keeps) > 0:
        print(f"   {len(keeps)} items will remain unchanged")
        if len(keeps) <= 10:
            for row in keeps:
                print(f"      • {row['before_path']}")
        else:
            for row in keeps[:5]:
                print(f"      • {row['before_path']}")
            print(f"      ... and {len(keeps) - 5} more")

    print()

    # Summary
    print("=" * 80)
    print("📊 EXECUTION SUMMARY")
    print("=" * 80)
    print()
    print(f"   Moved:    {stats['moved']}")
    print(f"   Deleted:  {stats['deleted']}")
    print(f"   Kept:     {stats['kept']}")
    print(f"   Skipped:  {stats['skipped']}")
    print(f"   Errors:   {stats['errors']}")
    print()

    if dry_run:
        print("=" * 80)
        print("💡 This was a DRY RUN - no changes were made")
        print("   Run with --execute to apply these changes")
        print("=" * 80)
    else:
        print("=" * 80)
        print("✅ Changes applied!")
        print("   Review the results and test your code")
        print("=" * 80)


def main():
    """Main function."""
    csv_file = Path.home() / "pythons" / "BEFORE_AFTER_REVIEW.csv"
    dry_run = "--execute" not in sys.argv

    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_file}")
        print("   Run generate_before_after_csv.py first")
        return

    execute_changes(csv_file, dry_run=dry_run)


if __name__ == "__main__":
    main()
