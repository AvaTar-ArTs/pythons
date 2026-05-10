#!/usr/bin/env python3
"""
Execute Improved Reorganization

Safely reorganizes files based on improved analysis
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


class ImprovedReorganizer:
    """Execute reorganization based on improved analysis"""

    def __init__(self, analysis_file: Path, target_dir: Path = None):
        self.analysis_file = Path(analysis_file)

        with open(self.analysis_file) as f:
            self.analysis = json.load(f)

        self.base_path = Path(self.analysis["directory"])
        self.target_dir = Path(target_dir) if target_dir else self.base_path

    def execute(self, dry_run: bool = True):
        """Execute improved reorganization"""
        mode = "DRY RUN" if dry_run else "EXECUTION"
        print(f"🎯 IMPROVED REORGANIZATION - {mode}")
        print("=" * 70)
        print(f"Source: {self.base_path}")
        print(f"Target: {self.target_dir}")
        print(f"Categories: {self.analysis['improved_categories']}")
        print()

        if not dry_run:
            # Create backup
            self._create_backup()

        # Reorganize by improved categories
        self._reorganize_by_categories(dry_run)

        print()
        print("=" * 70)
        if dry_run:
            print("✅ Dry run complete! Review the plan above.")
            print("   Run with --execute to apply changes.")
        else:
            print("✅ Reorganization complete!")
            print(f"   Backup saved in: {self.base_path / 'archive' / 'backups'}")
        print("=" * 70)

    def _create_backup(self):
        """Create backup before reorganization"""
        print("📦 Creating backup...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.base_path / "archive" / "backups" / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Save analysis file
        shutil.copy(self.analysis_file, backup_dir / "analysis.json")
        print(f"   ✅ Backup created: {backup_dir}")
        print()

    def _reorganize_by_categories(self, dry_run: bool):
        """Reorganize files by improved categories"""
        categories = self.analysis["categories"]

        print(f"📁 Organizing into {len(categories)} functional categories:")
        print()

        moved_count = 0
        skipped_count = 0

        for category_name, category_data in sorted(
            categories.items(), key=lambda x: x[1]["count"], reverse=True
        ):
            files = category_data["files"]
            description = category_data["description"]
            count = category_data["count"]

            print(f"  📂 {category_name}/")
            print(f"     Description: {description}")
            print(f"     Files: {count}")

            if not dry_run:
                # Create category directory
                category_path = self.target_dir / category_name
                category_path.mkdir(parents=True, exist_ok=True)

                # Move files
                for file_path in files:
                    src = Path(file_path)

                    # Skip if already in the right place
                    if src.parent == category_path:
                        skipped_count += 1
                        continue

                    if src.exists():
                        dest = category_path / src.name

                        # Handle naming conflicts
                        if dest.exists() and dest != src:
                            base = dest.stem
                            ext = dest.suffix
                            counter = 1
                            while dest.exists():
                                dest = category_path / f"{base}_{counter}{ext}"
                                counter += 1

                        try:
                            shutil.move(str(src), str(dest))
                            moved_count += 1
                        except Exception as e:
                            print(f"      ⚠️  Error moving {src.name}: {e}")
                    else:
                        print(f"      ⚠️  File not found: {src.name}")

            print()

        if not dry_run:
            print(f"✅ Moved {moved_count} files")
            print(f"⏭️  Skipped {skipped_count} files (already in place)")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Execute Improved Reorganization")
    parser.add_argument("analysis_file", nargs="?", help="Improved analysis JSON file")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute reorganization (default: dry-run)",
    )
    parser.add_argument(
        "--directory", help="Target directory (default: source directory)"
    )

    args = parser.parse_args()

    # Find most recent improved analysis file if not specified
    if not args.analysis_file:
        cwd = Path.cwd()
        analysis_files = list(cwd.glob("improved_analysis_*.json"))

        if not analysis_files:
            print(
                "❌ No improved analysis file found. Run adaptive_recategorizer.py first."
            )
            sys.exit(1)

        args.analysis_file = max(analysis_files, key=lambda p: p.stat().st_mtime)
        print(f"📄 Using: {args.analysis_file.name}")
        print()

    reorganizer = ImprovedReorganizer(args.analysis_file, target_dir=args.directory)

    reorganizer.execute(dry_run=not args.execute)


if __name__ == "__main__":
    main()
