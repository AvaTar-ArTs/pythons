#!/usr/bin/env python3
"""Execute the rename plan"""
import csv
import shutil
from pathlib import Path


def execute_renames():
    """Execute all renames from RENAME_PLAN.csv"""
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS")
    plan_csv = base_dir / "RENAME_PLAN.csv"

    if not plan_csv.exists():
        print("? No RENAME_PLAN.csv found!")
        print("   Run: python3 rename_and_standardize.py first")
        return

    # Load plan
    with open(plan_csv) as f:
        reader = csv.DictReader(f)
        renames = list(reader)

    print(f"\n?? Loaded {len(renames)} renames\n")
    print("??  WARNING: This will rename files!")
    print("   Press Ctrl+C to cancel, or Enter to continue...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n? Cancelled")
        return

    success = 0
    failed = []
    skipped = 0

    for i, rename in enumerate(renames, 1):
        old_path = Path(rename["old_path"])
        new_path = Path(rename["new_path"])

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
            print(
                f"\n?? Progress: {i}/{len(renames)} (? {success} | ??  {skipped} | ? {len(failed)})\n",
            )

    print("\n" + "=" * 80)
    print("  ? RENAME COMPLETE!")
    print("=" * 80 + "\n")
    print(f"? Successfully renamed: {success}")
    print(f"??  Skipped: {skipped}")
    print(f"? Failed: {len(failed)}")

    if failed:
        print("\nFailed files:")
        for name in failed[:10]:
            print(f"  ? {name}")


if __name__ == "__main__":
    execute_renames()
