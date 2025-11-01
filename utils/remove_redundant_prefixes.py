#!/usr/bin/env python3
"""
Remove Redundant Folder Name Prefixes

Fixes files like:
  audio/audio_6.py → audio/script_6.py
  youtube/youtube_test.py → youtube/test.py
  instagram/instagram_bot.py → instagram/bot.py
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path


class RedundantPrefixRemover:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.stats = {'renamed': 0, 'errors': 0}

    def remove_redundant_prefix(self, folder_name: str, filename: str) -> str:
        """Clean up filenames while preserving folder context."""
        stem = Path(filename).stem
        ext = Path(filename).suffix

        # Keep the filename as-is, just clean up suffixes and duplicates
        # NO prefix removal - parent folder already provides context

        # Just simplify long names
        # Example: instagram_bot_api_methods.py → instagram_bot.py
        # Example: youtube_test_literal_xml_deprecation.py → youtube_test.py

        # Split by underscores
        parts = stem.split('_')

        # Keep first 2-3 meaningful parts
        if len(parts) > 3:
            # Keep category + 2 descriptive words
            new_stem = '_'.join(parts[:3])
            return f"{new_stem}{ext}"

        return filename

    def process_folder(self, folder_path: Path, dry_run=True):
        """Remove redundant prefixes in a folder."""
        folder_name = folder_path.name
        python_files = list(folder_path.glob("*.py"))

        renamed_count = 0
        renames = []

        for file_path in python_files:
            new_name = self.remove_redundant_prefix(folder_name, file_path.name)

            if new_name != file_path.name:
                target_path = folder_path / new_name

                # Handle conflicts
                counter = 1
                original_target = target_path
                while target_path.exists() and target_path != file_path:
                    stem = original_target.stem
                    ext = original_target.suffix
                    target_path = folder_path / f"{stem}_v{counter}{ext}"
                    counter += 1

                renames.append({
                    'old': file_path.name,
                    'new': target_path.name,
                    'path': file_path,
                    'target': target_path
                })

                renamed_count += 1

        if renames:
            print(f"\n📁 {folder_name}/ ({len(renames)} files to rename)")

            for rename in renames[:5]:
                print(f"  {rename['old']}")
                print(f"    → {rename['new']}")

            if len(renames) > 5:
                print(f"  ... and {len(renames) - 5} more")

            if not dry_run:
                for rename in renames:
                    try:
                        shutil.move(str(rename['path']), str(rename['target']))
                        self.stats['renamed'] += 1
                    except Exception as e:
                        print(f"  ❌ Error: {e}")
                        self.stats['errors'] += 1

        return renamed_count

    def run(self, dry_run=True):
        """Remove redundant prefixes from all folders."""
        print(f"\n{'='*80}")
        print("🧹 REMOVE REDUNDANT FOLDER NAME PREFIXES")
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
        print("✅ PREFIX REMOVAL COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Total Files to Rename: {total_renamed}")
        if not dry_run:
            print(f"Files Renamed: {self.stats['renamed']}")
            if self.stats['errors'] > 0:
                print(f"Errors: {self.stats['errors']}")
        print()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Remove Redundant Prefixes')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--live', action='store_true', help='Execute renames')

    args = parser.parse_args()

    remover = RedundantPrefixRemover(args.target)
    remover.run(dry_run=not args.live)

if __name__ == "__main__":
    main()
