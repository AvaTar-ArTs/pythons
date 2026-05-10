#!/usr/bin/env python3
"""Remove scattered .git directories to reduce directory count"""

import os
import shutil
from pathlib import Path


def remove_git_dirs(root_dir, dry_run=True):
    """Remove all .git directories except the root one"""
    root = Path(root_dir)

    print("🗑️  REMOVING SCATTERED .GIT DIRECTORIES")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    git_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        if ".git" in dirnames:
            git_path = Path(dirpath) / ".git"
            if git_path.exists() and git_path.is_dir():
                rel_path = git_path.relative_to(root)
                git_dirs.append(git_path)

        # Don't walk into .git directories
        dirnames[:] = [d for d in dirnames if d != ".git"]

    print(f"Found {len(git_dirs)} .git directories")
    print()

    removed = 0
    total_size = 0

    for git_dir in git_dirs:
        try:
            # Calculate size
            size = sum(f.stat().st_size for f in git_dir.rglob("*") if f.is_file())
            total_size += size

            if not dry_run:
                shutil.rmtree(git_dir)

            removed += 1
            if removed <= 20:
                rel = git_dir.relative_to(root)
                size_mb = size / (1024 * 1024)
                print(
                    f"   {'Would remove' if dry_run else 'Removed'}: {rel} ({size_mb:.2f} MB)"
                )
        except Exception as e:
            if removed <= 5:
                print(f"   ⚠️  Error: {e}")

    print()
    print(f"   {'Would remove' if dry_run else 'Removed'}: {removed} .git directories")
    print(f"   Space freed: {total_size / (1024 * 1024):.2f} MB")
    print()

    if not dry_run:
        # Count directories after
        final_count = len([d for d in root.rglob("*") if d.is_dir()])
        print(f"📊 Final directory count: {final_count:,}")

    print("✅ Complete!")


if __name__ == "__main__":
    import sys

    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv
    remove_git_dirs(root_dir, dry_run)
