"""
Utilities File Operations Merge 6

This module provides functionality for utilities file operations merge 6.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Merge Experiments into Root
Move all experiments content to root, merge duplicates intelligently
"""

import shutil
import hashlib
from pathlib import Path
from collections import defaultdict


class ExperimentsMerger:
    """Merge experiments directory into root"""

    def __init__(self, base_dir: Path):
        """__init__ function."""

        self.base_dir = base_dir
        self.experiments_dir = base_dir / "experiments"
        self.actions = []

    def get_file_hash(self, file_path: Path):
        """Get MD5 hash of file for duplicate detection"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except (OSError, IOError, FileNotFoundError):
            return None

    def are_files_identical(self, file1: Path, file2: Path):
        """Check if two files are identical"""
        if not file1.exists() or not file2.exists():
            return False

        # Quick size check first
        if file1.stat().st_size != file2.stat().st_size:
            return False

        # Hash comparison for exact match
        return self.get_file_hash(file1) == self.get_file_hash(file2)

    def merge_text_files(self, source: Path, target: Path):
        """Merge two text files (README, requirements)"""

        try:
            source_content = source.read_text()
            target_content = target.read_text() if target.exists() else ""

            # For requirements.txt - merge unique lines
            if source.name == "requirements.txt":
                source_lines = set(line.strip() for line in source_content.split("\n") if line.strip())
                target_lines = set(line.strip() for line in target_content.split("\n") if line.strip())
                merged_lines = sorted(source_lines | target_lines)
                target.write_text("\n".join(merged_lines) + "\n")
                return True

            # For README.md - append with separator
            elif source.name == "README.md":
                if target.exists() and target_content.strip():
                    merged = target_content.rstrip() + "\n\n---\n\n# From experiments/\n\n" + source_content
                    target.write_text(merged)
                else:
                    shutil.copy2(source, target)
                return True

        except (OSError, IOError, FileNotFoundError):
            return False

        return False

    def build_merge_plan(self):
        """Build comprehensive merge plan"""

        # Directories to move
        dirs_to_move = [
            "analysis_artifacts",
            "archived_items",
            "old_versions",
            "reorganization_tools",
            "setup_tools",
            "test_data",
            "testing",
            "utilities",
        ]

        for dir_name in dirs_to_move:
            source = self.experiments_dir / dir_name
            if not source.exists():
                continue

            target = self.base_dir / dir_name

            if target.exists():
                # Target exists - need to merge
                self.actions.append({"type": "merge_dir", "source": source, "target": target, "name": dir_name})
            else:
                # Target doesn't exist - simple move
                self.actions.append({"type": "move_dir", "source": source, "target": target, "name": dir_name})

        # Text files to merge
        for filename in ["README.md", "requirements.txt"]:
            source = self.experiments_dir / filename
            if source.exists():
                target = self.base_dir / filename
                self.actions.append({"type": "merge_file", "source": source, "target": target, "name": filename})

    def merge_directory(self, source: Path, target: Path):
        """Recursively merge source directory into target"""

        moved = 0
        skipped = 0
        merged = 0

        for item in source.rglob("*"):
            if not item.is_file():
                continue

            rel_path = item.relative_to(source)
            target_file = target / rel_path

            # Create parent directory
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # Check if target exists
            if target_file.exists():
                # Check if identical
                if self.are_files_identical(item, target_file):
                    skipped += 1
                else:
                    # Different file - rename source
                    from datetime import datetime

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{target_file.stem}_from_experiments_{timestamp}{target_file.suffix}"
                    target_file = target_file.parent / new_name
                    shutil.move(str(item), str(target_file))
                    merged += 1
            else:
                # Target doesn't exist - move
                shutil.move(str(item), str(target_file))
                moved += 1

        return moved, skipped, merged

    def execute(self, dry_run=True):
        """Execute merge"""

        logger.info("=" * 70)
        logger.info(f"🔀 MERGE EXPERIMENTS TO ROOT {'(DRY RUN)' if dry_run else '(LIVE)'}")
        logger.info("=" * 70)
        print()

        self.build_merge_plan()

        if not self.actions:
            logger.info("✅ Nothing to merge!")
            return

        logger.info(f"📦 Found {len(self.actions)} items to process")
        print()

        total_moved = 0
        total_skipped = 0
        total_merged = 0

        for action in self.actions:
            logger.info(f"📂 {action['name']}")

            if action["type"] == "move_dir":
                if dry_run:
                    try:
                        file_count = len(list(action["source"].rglob("*")))
                        logger.info(f"   [DRY RUN] Would move entire directory ({file_count} items)")
                    except (OSError, IOError, FileNotFoundError):
                        logger.info(f"   [DRY RUN] Would move entire directory")
                else:
                    try:
                        shutil.move(str(action["source"]), str(action["target"]))
                        logger.info(f"   ✅ Moved to root")
                        total_moved += 1
                    except Exception as e:
                        logger.info(f"   ❌ ERROR: {str(e)[:50]}")

            elif action["type"] == "merge_dir":
                if dry_run:
                    try:
                        file_count = len(list(action["source"].rglob("*")))
                        logger.info(f"   [DRY RUN] Would merge with existing ({file_count} items)")
                    except (OSError, IOError, FileNotFoundError):
                        logger.info(f"   [DRY RUN] Would merge with existing")
                else:
                    try:
                        moved, skipped, merged = self.merge_directory(action["source"], action["target"])
                        logger.info(f"   ✅ Merged: {moved} moved, {skipped} duplicates skipped, {merged} renamed")
                        total_moved += moved
                        total_skipped += skipped
                        total_merged += merged
                    except Exception as e:
                        logger.info(f"   ❌ ERROR: {str(e)[:50]}")

            elif action["type"] == "merge_file":
                if dry_run:
                    logger.info(f"   [DRY RUN] Would merge with root/{action['name']}")
                else:
                    try:
                        if self.merge_text_files(action["source"], action["target"]):
                            logger.info(f"   ✅ Merged into root/{action['name']}")
                            total_merged += 1
                        else:
                            logger.info(f"   ⚠️  Kept separate (couldn't merge)")
                    except Exception as e:
                        logger.info(f"   ❌ ERROR: {str(e)[:50]}")

            print()

        logger.info("=" * 70)
        logger.info(f"{'Simulation' if dry_run else 'Merge'} complete!")
        if not dry_run:
            logger.info(f"   Moved: {total_moved}")
            logger.info(f"   Duplicates skipped: {total_skipped}")
            logger.info(f"   Merged/Renamed: {total_merged}")
        logger.info("=" * 70)

        if not dry_run:
            # Remove __pycache__
            pycache = self.experiments_dir / "__pycache__"
            if pycache.exists():
                shutil.rmtree(pycache)
                logger.info(f"\n🗑️  Removed experiments/__pycache__")

            # Remove experiments directory if empty
            try:
                remaining = list(self.experiments_dir.iterdir())
                if not remaining or (len(remaining) == 1 and remaining[0].name == ".DS_Store"):
                    if remaining:
                        remaining[0].unlink()  # Remove .DS_Store
                    self.experiments_dir.rmdir()
                    logger.info(f"🗑️  Removed empty experiments/ directory")
                    print()
                    logger.info("✨ Experiments fully merged into root!")
                else:
                    logger.info(f"\n⚠️  experiments/ still has {len(remaining)} items:")
                    for item in remaining[:5]:
                        logger.info(f"     • {item.name}")
            except Exception as e:
                logger.info(f"\n⚠️  Could not remove experiments/: {e}")

        if dry_run:
            logger.info("\n💡 To execute, run:")
            logger.info("   python3 merge_experiments_to_root.py --execute")


def main():
    """main function."""

    import sys

    base_dir = Path(Path("/Users/steven/Documents/python"))
    dry_run = "--execute" not in sys.argv

    merger = ExperimentsMerger(base_dir)
    merger.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
