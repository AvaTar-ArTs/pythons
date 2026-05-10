#!/usr/bin/env python3
"""
Execute Enhanced Reorganization
Move files to enhanced, more specific categories
"""

import json
import shutil
from pathlib import Path


class EnhancedReorganizationExecutor:
    """Execute enhanced reorganization with new specific categories"""

    def __init__(self, base_dir: Path, analysis_file: Path):
        self.base_dir = base_dir
        self.analysis_file = analysis_file
        with open(analysis_file) as f:
            self.analysis = json.load(f)

    def execute(self, dry_run=True):
        """Execute enhanced reorganization"""

        print("=" * 70)
        print(f"🧠 ENHANCED REORGANIZATION {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()
        print(f"Files to organize: {self.analysis['total_categorized']}")
        print(f"Categories: {self.analysis['categories_discovered']}")
        print()

        moved_count = 0
        skipped_count = 0
        error_count = 0

        for category_name, category_data in sorted(
            self.analysis["categories"].items(),
            key=lambda x: len(x[1]["files"]),
            reverse=True,
        ):
            category_path = self.base_dir / category_name

            # Don't show categories with no files to move
            files_to_move = []
            for file_rel_path in category_data["files"]:
                source_path = self.base_dir / file_rel_path

                # Skip if doesn't exist
                if not source_path.exists():
                    continue

                # Skip if already in target directory
                if source_path.parent == category_path:
                    continue

                files_to_move.append(file_rel_path)

            if not files_to_move:
                continue

            print(f"📁 {category_name}/ ← {len(files_to_move)} files")

            if not dry_run and not category_path.exists():
                category_path.mkdir(parents=True)

            # Show first 5 files
            for file_rel_path in files_to_move[:5]:
                source_path = self.base_dir / file_rel_path
                dest_path = category_path / source_path.name

                if not source_path.exists():
                    skipped_count += 1
                    continue

                if dest_path.exists():
                    # Handle conflict
                    if dry_run:
                        print(f"   [DRY RUN] Conflict: {source_path.name}")
                    else:
                        # Add source directory to name
                        source_dir = source_path.parent.name
                        new_name = (
                            f"{source_path.stem}_from_{source_dir}{source_path.suffix}"
                        )
                        dest_path = category_path / new_name
                        try:
                            shutil.move(str(source_path), str(dest_path))
                            print(f"   ✅ Moved (renamed): {source_path.name}")
                        except Exception as e:
                            print(f"   ❌ Error: {source_path.name} - {e}")
                            error_count += 1
                            continue
                    moved_count += 1
                else:
                    if dry_run:
                        print(f"   [DRY RUN] Would move: {source_path.name}")
                    else:
                        try:
                            shutil.move(str(source_path), str(dest_path))
                            print(f"   ✅ Moved: {source_path.name}")
                        except Exception as e:
                            print(f"   ❌ Error: {source_path.name} - {e}")
                            error_count += 1
                            continue
                    moved_count += 1

            # Move remaining files silently
            if len(files_to_move) > 5:
                remaining = len(files_to_move) - 5
                if dry_run:
                    print(f"   [DRY RUN] ... and {remaining} more files")
                else:
                    moved_remaining = 0
                    for file_rel_path in files_to_move[5:]:
                        source_path = self.base_dir / file_rel_path
                        dest_path = category_path / source_path.name

                        if not source_path.exists():
                            skipped_count += 1
                            continue

                        if dest_path.exists():
                            source_dir = source_path.parent.name
                            new_name = f"{source_path.stem}_from_{source_dir}{source_path.suffix}"
                            dest_path = category_path / new_name

                        try:
                            shutil.move(str(source_path), str(dest_path))
                            moved_count += 1
                            moved_remaining += 1
                        except:
                            error_count += 1

                    print(f"   ✅ Moved {moved_remaining} more files")

            print()

        print("=" * 70)
        print(f"{'Simulation' if dry_run else 'Execution'} complete!")
        print(f"   Files {'would be' if dry_run else ''} moved: {moved_count}")
        print(f"   Skipped: {skipped_count}")
        if error_count > 0:
            print(f"   Errors: {error_count}")
        print("=" * 70)

        if dry_run:
            print("\n💡 To execute for real, run:")
            print("   python3 execute_enhanced_reorganization.py --execute")


def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    analysis_file = base_dir / "enhanced_reorganization_plan_20251026_034934.json"

    if not analysis_file.exists():
        print("❌ Analysis file not found")
        return

    dry_run = "--execute" not in sys.argv

    executor = EnhancedReorganizationExecutor(base_dir, analysis_file)
    executor.execute(dry_run=dry_run)


if __name__ == "__main__":
    main()
