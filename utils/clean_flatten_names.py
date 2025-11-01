#!/usr/bin/env python3
"""
Clean and Fix Flattened Filenames

Removes duplicate suffixes and ensures proper parent-folder context.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import re

class CleanFlattenNames:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.stats = {'renamed': 0, 'errors': 0}

    def clean_filename(self, filename: str) -> str:
        """Clean up filename by removing duplicate suffixes and fixing naming."""
        name = filename

        # Remove duplicate counter suffixes like -1-1, -2-1, etc.
        name = re.sub(r'-\d+-\d+\.py$', '.py', name)
        name = re.sub(r'-\d+\.py$', '.py', name)

        # Remove version-like suffixes
        name = re.sub(r'_v\d+\.py$', '.py', name)

        # Remove (1) style duplicates
        name = re.sub(r'\(1\)', '', name)
        name = re.sub(r'\(\d+\)', '', name)

        # Clean up parent folder prefixes
        # If starts with -versions-, remove it
        if name.startswith('-versions-'):
            name = name[10:]  # Remove '-versions-'

        # Fix double dashes
        name = re.sub(r'--+', '-', name)

        # Fix leading/trailing dashes
        name = name.strip('-')

        # Ensure ends with .py
        if not name.endswith('.py'):
            name = name + '.py'

        return name

    def process_folder(self, folder_path: Path, dry_run=True):
        """Clean all filenames in a folder."""
        print(f"\n📁 {folder_path.name}/")

        python_files = list(folder_path.glob("*.py"))
        renamed_count = 0

        for file_path in python_files:
            clean_name = self.clean_filename(file_path.name)

            if clean_name != file_path.name:
                target_path = folder_path / clean_name

                # Handle conflicts
                counter = 1
                original_target = target_path
                while target_path.exists() and target_path != file_path:
                    stem = original_target.stem
                    ext = original_target.suffix
                    target_path = folder_path / f"{stem}-v{counter}{ext}"
                    counter += 1

                if renamed_count < 3:
                    print(f"  {file_path.name}")
                    print(f"    → {target_path.name}")

                if not dry_run:
                    try:
                        shutil.move(str(file_path), str(target_path))
                        self.stats['renamed'] += 1
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
                        self.stats['errors'] += 1

                renamed_count += 1

        if renamed_count > 3:
            print(f"  ... and {renamed_count - 3} more files renamed")

        return renamed_count

    def run(self, dry_run=True):
        """Clean all filenames in all category folders."""
        print(f"\n{'='*80}")
        print("🧹 CLEAN FLATTENED FILENAMES")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")

        # Get all category folders
        folders = [f for f in self.target_dir.iterdir()
                  if f.is_dir() and not f.name.startswith('_')
                  and not f.name.startswith('.')]

        total_renamed = 0
        for folder in sorted(folders):
            renamed = self.process_folder(folder, dry_run)
            total_renamed += renamed

        print(f"\n{'='*80}")
        print("✅ CLEANING COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Total Files Renamed: {total_renamed if dry_run else self.stats['renamed']}")
        if not dry_run and self.stats['errors'] > 0:
            print(f"Errors: {self.stats['errors']}")
        print()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Clean Flattened Filenames')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--live', action='store_true', help='Execute renames')

    args = parser.parse_args()

    cleaner = CleanFlattenNames(args.target)
    cleaner.run(dry_run=not args.live)

if __name__ == "__main__":
    main()
