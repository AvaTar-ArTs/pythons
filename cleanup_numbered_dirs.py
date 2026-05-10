#!/usr/bin/env python3
"""
Clean up numbered directory prefixes (00_, 01_, etc.) in AVATARARTS

Systematically rename directories to remove numbering prefixes for cleaner organization.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

class DirectoryCleaner:
    def __init__(self, root_path: str = "/Users/steven/AVATARARTS"):
        self.root_path = Path(root_path)
        self.renames = []

    def find_numbered_directories(self) -> List[Tuple[Path, str]]:
        """Find all directories with numbered prefixes (00_, 01_, etc.)."""
        numbered_dirs = []

        # Skip .git directories
        for dir_path in self.root_path.rglob('*'):
            if dir_path.is_dir() and not any(part.startswith('.') for part in dir_path.parts):
                dir_name = dir_path.name

                # Match patterns like "00_ACTIVE", "01_Strategic_Framework", "1_CORE_PLATFORM", etc.
                match = re.match(r'^(\d+)[_\s-]*(.+)$', dir_name)
                if match:
                    number = match.group(1)
                    new_name = match.group(2)

                    # Skip if the new name would be empty or just underscores
                    if new_name and new_name not in ['_', '-', '']:
                        numbered_dirs.append((dir_path, new_name))

        return numbered_dirs

    def analyze_renames(self) -> List[Tuple[Path, str, str]]:
        """Analyze what renames would occur and check for conflicts."""
        numbered_dirs = self.find_numbered_directories()
        renames = []

        for dir_path, new_name in numbered_dirs:
            current_name = dir_path.name
            new_path = dir_path.parent / new_name

            # Check for conflicts
            conflict = "❌ CONFLICT" if new_path.exists() else "✅ OK"

            renames.append((dir_path, current_name, new_name, conflict))

        return renames

    def execute_renames(self, dry_run: bool = True) -> List[str]:
        """Execute the directory renames."""
        renames = self.analyze_renames()
        executed = []

        print("🧹 CLEANING NUMBERED DIRECTORY PREFIXES")
        print("=" * 50)

        # Filter out conflicts first
        safe_renames = [r for r in renames if "✅ OK" in r[3]]

        if not safe_renames:
            print("❌ No safe renames found (all would conflict)")
            return []

        print(f"📋 Found {len(safe_renames)} safe renames:")
        print()

        for dir_path, current_name, new_name, status in safe_renames:
            new_path = dir_path.parent / new_name

            if dry_run:
                print(f"🔍 Would rename: {dir_path} → {new_path}")
                executed.append(f"DRY_RUN: {current_name} → {new_name}")
            else:
                try:
                    dir_path.rename(new_path)
                    print(f"✅ Renamed: {current_name} → {new_name}")
                    executed.append(f"RENAMED: {current_name} → {new_name}")
                except Exception as e:
                    print(f"❌ Failed to rename {current_name}: {e}")

        # Report conflicts
        conflicts = [r for r in renames if "❌ CONFLICT" in r[3]]
        if conflicts:
            print(f"\n⚠️  {len(conflicts)} conflicts found (skipped):")
            for dir_path, current_name, new_name, status in conflicts[:5]:  # Show first 5
                print(f"   • {current_name} → {new_name} (target exists)")

        return executed

def main():
    import sys

    cleaner = DirectoryCleaner()

    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        print("⚠️  EXECUTING LIVE RENAMES - This will modify directory names!")
        response = input("Continue? (yes/no): ")
        if response.lower() == 'yes':
            results = cleaner.execute_renames(dry_run=False)
            print(f"\n✅ Completed {len(results)} renames")
        else:
            print("❌ Operation cancelled")
    else:
        print("🔍 DRY RUN - Showing what would be renamed:")
        print()
        results = cleaner.execute_renames(dry_run=True)
        print(f"\n📊 Total safe renames available: {len(results)}")
        print("\n🚀 To execute the renames, run:")
        print("   python3 cleanup_numbered_dirs.py --execute")

if __name__ == "__main__":
    main()