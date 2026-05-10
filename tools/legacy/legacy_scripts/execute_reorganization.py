#!/usr/bin/env python3
"""
Execute Intelligent Reorganization
Moves files into functional categories based on ML/NLP analysis
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


class ReorganizationExecutor:
    """Execute the intelligent reorganization plan"""

    def __init__(self, analysis_file: Path, base_path: Path):
        self.analysis_file = Path(analysis_file)
        self.base_path = Path(base_path).expanduser()
        self.analysis_data = None
        self.load_analysis()

    def load_analysis(self):
        """Load the analysis report"""
        print(f"📄 Loading analysis: {self.analysis_file.name}")
        with open(self.analysis_file, "r") as f:
            self.analysis_data = json.load(f)
        print(
            f"   ✅ Loaded {self.analysis_data['total_files_analyzed']} file analyses"
        )
        print(
            f"   ✅ Found {self.analysis_data['clusters_discovered']} functional categories"
        )
        print()

    def create_backup(self):
        """Create backup of current structure"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = (
            self.base_path / "archive" / "backups" / f"pre_reorganization_{timestamp}"
        )

        print(f"💾 Creating backup: {backup_dir.name}")
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Save current directory listing
        listing_file = backup_dir / "directory_structure.txt"
        with open(listing_file, "w") as f:
            f.write("Directory structure before reorganization\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("=" * 70 + "\n\n")

            for item in sorted(self.base_path.iterdir()):
                if item.is_dir() and not item.name.startswith("."):
                    f.write(f"{item.name}/\n")

        print(f"   ✅ Backup created: {backup_dir}")
        print()
        return backup_dir

    def show_summary(self):
        """Show reorganization summary"""
        print("📊 REORGANIZATION SUMMARY")
        print("=" * 70)

        structure = self.analysis_data["proposed_structure"]
        total_files = sum(len(files) for files in structure.values())

        print(f"\nTotal files to organize: {total_files}")
        print(f"Functional categories: {len(structure)}\n")

        # Show top categories
        sorted_cats = sorted(structure.items(), key=lambda x: len(x[1]), reverse=True)

        print("Top 15 categories by size:\n")
        for i, (category, files) in enumerate(sorted_cats[:15], 1):
            print(f"{i:2d}. {category:30s} {len(files):4d} files")

        print(f"\n... and {len(sorted_cats) - 15} more categories")
        print()

    def execute(self, dry_run: bool = True):
        """Execute the reorganization"""
        mode = "🔍 DRY RUN MODE" if dry_run else "✅ EXECUTING REORGANIZATION"
        print("=" * 70)
        print(mode)
        print("=" * 70)
        print()

        structure = self.analysis_data["proposed_structure"]

        if not dry_run:
            # Create backup first
            backup_dir = self.create_backup()

        moved_count = 0
        error_count = 0
        skipped_count = 0

        for category, files in sorted(structure.items()):
            # Create category directory
            category_dir = self.base_path / category

            if not dry_run:
                # Handle case where a file exists with the same name as our directory
                if category_dir.exists() and not category_dir.is_dir():
                    # Move the conflicting file to archive
                    conflict_dir = self.base_path / "archive" / "naming_conflicts"
                    conflict_dir.mkdir(parents=True, exist_ok=True)
                    conflict_dest = conflict_dir / category_dir.name
                    print(
                        f"   ⚠️  Moving conflicting file: {category} → archive/naming_conflicts/"
                    )
                    shutil.move(str(category_dir), str(conflict_dest))

                category_dir.mkdir(exist_ok=True)

            print(f"\n📁 {category}/ ({len(files)} files)")

            for filename in files:
                # Find the file
                matches = list(self.base_path.rglob(filename))

                if not matches:
                    print(f"   ⚠️  Not found: {filename}")
                    skipped_count += 1
                    continue

                # Use first match (should be unique)
                source = matches[0]

                # Skip if already in correct location
                if source.parent == category_dir:
                    skipped_count += 1
                    continue

                destination = category_dir / filename

                # Check for conflicts
                if destination.exists():
                    print(f"   ⚠️  Conflict: {filename} (already exists in {category}/)")
                    skipped_count += 1
                    continue

                # Move the file
                if dry_run:
                    print(f"   → {filename}")
                    moved_count += 1
                else:
                    try:
                        shutil.move(str(source), str(destination))
                        moved_count += 1
                        if moved_count % 100 == 0:
                            print(f"   ✅ Moved {moved_count} files so far...")
                    except Exception as e:
                        print(f"   ❌ Error moving {filename}: {e}")
                        error_count += 1

        # Summary
        print("\n" + "=" * 70)
        print("📊 REORGANIZATION RESULTS")
        print("=" * 70)
        print(f"\nFiles moved: {moved_count}")
        print(f"Files skipped: {skipped_count}")
        print(f"Errors: {error_count}")
        print()

        if dry_run:
            print("This was a DRY RUN - no files were actually moved.")
            print("\nTo execute the reorganization:")
            print("  python3 execute_reorganization.py --execute")
        else:
            print("✅ Reorganization complete!")
            print(f"\nBackup created at: {backup_dir}")
            print("\nNew structure:")
            print("  ~/Documents/python/")
            for category in sorted(structure.keys())[:10]:
                print(f"  ├── {category}/")
            print(f"  └── ... and {len(structure) - 10} more categories")

        print()

    def show_examples(self):
        """Show example files in each category"""
        print("\n📝 CATEGORY EXAMPLES")
        print("=" * 70)

        structure = self.analysis_data["proposed_structure"]
        categories_to_show = [
            "transcribe-analysis",
            "upscaler",
            "gallery-generator",
            "youtube-downloader",
            "instagram-bot",
            "image-converter",
            "video-converter",
            "seo-optimizer",
            "batch-processor",
            "text-to-speech",
        ]

        for category in categories_to_show:
            if category in structure:
                files = structure[category][:5]
                print(f"\n{category}/ ({len(structure[category])} files)")
                for f in files:
                    print(f"  • {f}")

        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Execute intelligent workspace reorganization"
    )
    parser.add_argument(
        "--analysis",
        default="intelligent_analysis_20251026_011216.json",
        help="Analysis report file (default: latest)",
    )
    parser.add_argument(
        "--directory",
        default="~/Documents/python",
        help="Base directory (default: ~/Documents/python)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the reorganization (default is dry-run)",
    )
    parser.add_argument(
        "--show-examples",
        action="store_true",
        help="Show example files in each category",
    )

    args = parser.parse_args()

    # Find latest analysis file if not specified
    base_path = Path(args.directory).expanduser()
    analysis_files = sorted(base_path.glob("intelligent_analysis_*.json"), reverse=True)

    if not analysis_files:
        print("❌ No analysis file found!")
        print("Run intelligent_reorganizer.py first to generate analysis.")
        sys.exit(1)

    analysis_file = base_path / args.analysis if args.analysis else analysis_files[0]

    if not analysis_file.exists():
        print(f"❌ Analysis file not found: {analysis_file}")
        sys.exit(1)

    # Create executor
    executor = ReorganizationExecutor(analysis_file, base_path)

    # Show summary
    executor.show_summary()

    # Show examples if requested
    if args.show_examples:
        executor.show_examples()
        return

    # Execute
    executor.execute(dry_run=not args.execute)


if __name__ == "__main__":
    main()
