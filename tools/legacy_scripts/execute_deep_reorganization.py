#!/usr/bin/env python3
"""
Execute Deep Reorganization
Move files to ultra-specific categories based on analysis
"""

import json
import shutil
from pathlib import Path


class DeepReorganizationExecutor:
    """Execute the deep reorganization plan"""

    def __init__(self, base_dir: Path, analysis_file: Path):
        self.base_dir = base_dir
        self.analysis_file = analysis_file
        with open(analysis_file) as f:
            self.analysis = json.load(f)

    def execute(self, dry_run=True):
        """Execute reorganization"""

        print("=" * 70)
        print(f"🚀 DEEP REORGANIZATION {'(DRY RUN)' if dry_run else '(LIVE)'}")
        print("=" * 70)
        print()
        print(f"Files to organize: {self.analysis['total_categorized']}")
        print(f"Categories: {self.analysis['categories_discovered']}")
        print()

        moved_count = 0
        skipped_count = 0
        error_count = 0

        for category_name, category_data in sorted(self.analysis['categories'].items()):
            category_path = self.base_dir / category_name

            # Don't show categories with no files to move
            files_to_move = []
            for file_rel_path in category_data['files']:
                source_path = self.base_dir / file_rel_path
                # Skip if already in target directory
                if source_path.parent == category_path:
                    continue
                files_to_move.append(file_rel_path)

            if not files_to_move:
                continue

            print(f"📁 {category_name}/ ← {len(files_to_move)} files")

            if not dry_run and not category_path.exists():
                category_path.mkdir(parents=True)

            for file_rel_path in files_to_move[:5]:  # Show first 5
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
                        new_name = f"{source_path.stem}_from_{source_dir}{source_path.suffix}"
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

            if len(files_to_move) > 5:
                remaining = len(files_to_move) - 5
                if dry_run:
                    print(f"   [DRY RUN] ... and {remaining} more files")
                else:
                    # Move remaining files silently
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
                        except:
                            error_count += 1

                    print(f"   ✅ Moved {remaining} more files")

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
            print(f"   python3 execute_deep_reorganization.py {self.analysis_file.name} --execute")

def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")

    # Find most recent analysis file
    analyses = list(base_dir.glob('deep_reorganization_plan_*.json'))
    if not analyses:
        print("❌ No analysis file found")
        print("   Run ultimate_deep_reorganization.py first")
        return

    analysis_file = max(analyses, key=lambda p: p.stat().st_mtime)
    print(f"📄 Using: {analysis_file.name}\n")

    dry_run = '--execute' not in sys.argv

    executor = DeepReorganizationExecutor(base_dir, analysis_file)
    executor.execute(dry_run=dry_run)

if __name__ == '__main__':
    main()
