#!/usr/bin/env python3
"""
AVATARARTS Duplicate File Cleanup Script
Safely removes duplicate files, keeping the most recent/largest version
"""

import os
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import argparse

class DuplicateCleaner:
    def __init__(self, root_dir="/Users/steven/AVATARARTS", dry_run=True):
        self.root = Path(root_dir)
        self.dry_run = dry_run
        self.duplicates = defaultdict(list)
        self.deleted_files = []
        self.saved_space = 0

    def calculate_hash(self, filepath):
        """Calculate MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def find_duplicates(self):
        """Find all duplicate files by content hash"""
        print(f"🔍 Scanning for duplicates in {self.root}...")

        for root, dirs, files in os.walk(self.root):
            # Skip virtual environments and node_modules
            if '.venv' in root or 'node_modules' in root or '__pycache__' in root:
                continue

            root_path = Path(root)

            for file in files:
                if file.startswith('.'):
                    continue

                filepath = root_path / file

                try:
                    file_size = filepath.stat().st_size

                    # Only hash files smaller than 5MB to avoid memory issues
                    if file_size < 5 * 1024 * 1024:
                        file_hash = self.calculate_hash(filepath)
                        if file_hash:
                            self.duplicates[file_hash].append({
                                'path': filepath,
                                'size': file_size,
                                'mtime': filepath.stat().st_mtime,
                                'name': file
                            })
                except Exception as e:
                    print(f"⚠️  Error processing {filepath}: {e}")

        # Filter to only keep groups with 2+ files
        self.duplicates = {
            k: v for k, v in self.duplicates.items() if len(v) > 1
        }

        print(f"✅ Found {len(self.duplicates)} groups of duplicate files\n")

    def clean_duplicates(self):
        """Remove duplicate files, keeping the best version"""
        if not self.duplicates:
            print("No duplicates found!")
            return

        print(f"{'DRY RUN - ' if self.dry_run else ''}Cleaning duplicates...\n")

        for hash_val, files in sorted(
            self.duplicates.items(),
            key=lambda x: x[1][0]['size'] * len(x[1]),
            reverse=True
        ):
            # Sort by modification time (newest first), then by size (largest first)
            files.sort(key=lambda x: (x['mtime'], x['size']), reverse=True)

            # Keep the first file (newest/largest), delete the rest
            keep_file = files[0]
            delete_files = files[1:]

            print(f"📁 {keep_file['name']} ({keep_file['size'] / 1024:.1f} KB)")
            print(f"   ✅ KEEP: {keep_file['path'].relative_to(self.root)}")

            for file_to_delete in delete_files:
                rel_path = file_to_delete['path'].relative_to(self.root)
                print(f"   🗑️  DELETE: {rel_path}")

                if not self.dry_run:
                    try:
                        file_to_delete['path'].unlink()
                        self.deleted_files.append(str(rel_path))
                        self.saved_space += file_to_delete['size']
                    except Exception as e:
                        print(f"   ⚠️  ERROR: Could not delete {rel_path}: {e}")

            print()

    def generate_report(self):
        """Generate cleanup summary report"""
        report_path = self.root / "CLEANUP_SUMMARY.md"

        with open(report_path, 'w') as f:
            f.write("# AVATARARTS Duplicate Cleanup Summary\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN (no files deleted)' if self.dry_run else 'LIVE (files deleted)'}\n\n")
            f.write("---\n\n")

            f.write("## 📊 Summary\n\n")
            f.write(f"- **Duplicate groups found:** {len(self.duplicates)}\n")
            f.write(f"- **Files deleted:** {len(self.deleted_files)}\n")
            f.write(f"- **Space saved:** {self.saved_space / (1024**2):.2f} MB\n\n")

            if self.deleted_files:
                f.write("## 🗑️ Deleted Files\n\n")
                for file in sorted(self.deleted_files):
                    f.write(f"- `{file}`\n")

        print(f"✅ Report saved: {report_path}")

    def run(self):
        """Run the cleanup process"""
        print("=" * 60)
        print("AVATARARTS DUPLICATE CLEANUP")
        print("=" * 60)
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print()

        self.find_duplicates()
        self.clean_duplicates()

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Duplicate groups: {len(self.duplicates)}")
        print(f"Files deleted: {len(self.deleted_files)}")
        print(f"Space saved: {self.saved_space / (1024**2):.2f} MB")
        print()

        if self.dry_run:
            print("⚠️  This was a DRY RUN - no files were deleted")
            print("Run with --execute to actually delete files")
        else:
            self.generate_report()

def main():
    parser = argparse.ArgumentParser(
        description="Clean up duplicate files in AVATARARTS directory"
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Actually delete files (default is dry-run)'
    )
    parser.add_argument(
        '--dir',
        default='/Users/steven/AVATARARTS',
        help='Directory to clean (default: /Users/steven/AVATARARTS)'
    )

    args = parser.parse_args()

    cleaner = DuplicateCleaner(
        root_dir=args.dir,
        dry_run=not args.execute
    )
    cleaner.run()

if __name__ == "__main__":
    main()
