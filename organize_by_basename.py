#!/usr/bin/env python3
"""
Organize music by base name - group all versions/variations together
Example:
  Echoes_of_Moonlight315.mp3 → Echoes_of_Moonlight/echoes_of_moonlight315.mp3
  Echoes_of_Moonlight_Remastered320.mp3 → Echoes_of_Moonlight/echoes_of_moonlight_remastered320.mp3
"""
import os
import re
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

class BaseNameOrganizer:
    def __init__(self, root_dir, dry_run=True):
        self.root_dir = Path(root_dir).resolve()
        self.dry_run = dry_run
        self.stats = {'moved': 0, 'skipped': 0, 'errors': 0}

    def extract_base_name(self, filename):
        """
        Extract base name from filename by removing:
        - Duration codes (111, 222, 1234, etc at end)
        - Version tags (Remix, Remastered, Edit, v1, v2, etc)
        - Special suffixes
        """
        # Remove extension
        name = filename.replace('.mp3', '').replace('.MP3', '')

        # Remove duration codes at the end (3-4 digits)
        name = re.sub(r'\d{3,4}$', '', name)

        # Remove version indicators (case insensitive)
        # Remove trailing version numbers/tags
        name = re.sub(r'[_\s-]*(Remix|Remastered|Edit|og|OG|v\d+|_\d+|\(\d+\)|pt\d+).*$', '', name, flags=re.IGNORECASE)

        # Remove leading/trailing underscores and spaces
        name = name.strip('_- ')

        # Clean up multiple underscores
        name = re.sub(r'_+', '_', name)

        return name

    def group_files_by_basename(self):
        """Group MP3 files by their base name"""
        groups = defaultdict(list)

        # Find all MP3 files in root (not in subdirectories)
        for file in self.root_dir.glob('*.mp3'):
            if file.is_file():
                base_name = self.extract_base_name(file.name)
                if base_name:
                    groups[base_name].append(file)

        # Also check .MP3
        for file in self.root_dir.glob('*.MP3'):
            if file.is_file():
                base_name = self.extract_base_name(file.name)
                if base_name:
                    groups[base_name].append(file)

        return groups

    def organize(self):
        """Main organization function"""
        print("=" * 80)
        print("ORGANIZING BY BASE NAME")
        print("=" * 80)
        print(f"Root: {self.root_dir}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}\n")

        groups = self.group_files_by_basename()

        print(f"Found {len(groups)} unique base names")
        print(f"Total files: {sum(len(files) for files in groups.values())}\n")

        # Sort by number of files (descending)
        sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)

        for base_name, files in sorted_groups:
            # Skip if only one file and it's already in a folder
            if len(files) == 1:
                self.stats['skipped'] += 1
                continue

            # Create folder name
            folder_name = base_name
            target_dir = self.root_dir / folder_name

            print(f"\n📁 {folder_name}/ ({len(files)} files)")

            for file in files:
                # New filename: lowercase
                new_filename = file.name.lower()
                target_path = target_dir / new_filename

                # Check if already in place
                if file.resolve() == target_path.resolve():
                    continue

                if self.dry_run:
                    print(f"  [DRY RUN] {file.name} → {folder_name}/{new_filename}")
                else:
                    try:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file), str(target_path))
                        print(f"  ✓ Moved: {file.name}")
                        self.stats['moved'] += 1
                    except Exception as e:
                        print(f"  ✗ Error: {file.name} - {e}")
                        self.stats['errors'] += 1

        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Groups created: {len([g for g in groups.values() if len(g) > 1])}")
        print(f"Files moved: {self.stats['moved']}")
        print(f"Single files (skipped): {self.stats['skipped']}")
        print(f"Errors: {self.stats['errors']}")
        print("=" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="Organize music by base name - group versions together",
        epilog="Example: Echoes_of_Moonlight315.mp3 → Echoes_of_Moonlight/echoes_of_moonlight315.mp3"
    )
    parser.add_argument("--live", action="store_true", help="Execute changes (default is dry-run)")
    parser.add_argument("--dir", type=str, default="/Users/steven/Music/nocTurneMeLoDieS",
                       help="Root directory to process")

    args = parser.parse_args()

    organizer = BaseNameOrganizer(args.dir, dry_run=not args.live)
    organizer.organize()

if __name__ == "__main__":
    main()
