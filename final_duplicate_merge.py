#!/usr/bin/env python3
"""
Final Duplicate Merge - Eliminate remaining redundancies
Merge underscore/hyphen variants and similar categories
"""

import shutil
from pathlib import Path


class FinalMerge:
    """Final pass to eliminate all remaining duplicates"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

        # Final merges - keep the ultra-specific (action-based) versions
        self.final_merges = {
            # Keep data-analyzer (more specific action)
            'data-analyzer': ['data-analysis', 'data_analysis', 'data_management'],

            # Keep data-extractor (more specific action)
            'data-extractor': ['data-extraction'],

            # Keep image-resizer (more specific action than processing)
            'image-resizer': ['image-processing'],

            # Keep video-editor (more specific action than processing)
            'video-editor': ['video-processing'],

            # Merge social media automation
            'bot-automation': ['social-media-automation'],

            # Merge YouTube variants
            'youtube-automation': [],  # Keep as is

            # Merge utility variants
            'utilities': ['utility', 'utils'],

            # Merge CSV processor
            'csv-processor': ['api-csv-processor'],

            # Merge monitor tool
            'monitor-tool': [],  # Keep as is

            # Merge scheduler
            'scheduler': [],  # Keep as is

            # Keep transcribe-analysis (most specific)
            'transcribe-analysis': [],

            # Keep upscaler (most specific)
            'upscaler': [],

            # Keep gallery-generator (most specific)
            'gallery-generator': [],

            # Keep thumbnail-generator (most specific)
            'thumbnail-generator': [],

            # Keep watermark-tool (most specific)
            'watermark-tool': [],

            # Keep text-to-speech (most specific)
            'text-to-speech': [],

            # Keep json-processor
            'json-processor': [],

            # Keep pdf-converter
            'pdf-converter': [],

            # Merge general utility directories
            'general-scripts': [],

            # Consolidate automation
            'automation': [],

            # Keep batch-processor
            'batch-processor': [],

            # Keep backup-tool
            'backup-tool': [],

            # Merge Ai-cLi into ai-chatbot
            'ai-chatbot': ['Ai-cLi'],
        }

    def execute_final_merge(self, dry_run=True):
        """Execute final merge to eliminate all duplicates"""

        print("🎯 Final Duplicate Merge - Eliminating Last Redundancies")
        print("=" * 70)
        print()

        merged_count = 0

        for target_dir, source_dirs in self.final_merges.items():
            if not source_dirs:
                continue

            target_path = self.base_dir / target_dir
            existing_sources = [d for d in source_dirs if (self.base_dir / d).exists()]

            if not existing_sources:
                continue

            print(f"📁 {target_dir}/ ← {len(existing_sources)} directories")

            if not dry_run and not target_path.exists():
                target_path.mkdir(parents=True)

            for source_dir in existing_sources:
                source_path = self.base_dir / source_dir

                if dry_run:
                    try:
                        item_count = len(list(source_path.rglob('*')))
                        print(f"   [DRY RUN] Would merge: {source_dir} ({item_count} items)")
                    except:
                        print(f"   [DRY RUN] Would merge: {source_dir}")
                else:
                    try:
                        # Move all contents
                        for item in source_path.iterdir():
                            dest = target_path / item.name
                            if not dest.exists():
                                shutil.move(str(item), str(dest))
                            else:
                                # Handle conflict
                                if item.is_file():
                                    new_name = f"{item.stem}_from_{source_dir}{item.suffix}"
                                else:
                                    new_name = f"{item.name}_from_{source_dir}"
                                shutil.move(str(item), str(target_path / new_name))

                        # Remove empty source
                        source_path.rmdir()
                        print(f"   ✅ Merged and removed: {source_dir}")
                    except Exception as e:
                        print(f"   ⚠️  Error with {source_dir}: {e}")

                merged_count += 1

            print()

        print("=" * 70)
        print(f"✅ Final merge {'simulation' if dry_run else 'execution'} complete!")
        print(f"   Directories {'would be' if dry_run else ''} merged: {merged_count}")
        print("=" * 70)

        if dry_run:
            print("\n💡 To execute, run:")
            print("   python3 final_duplicate_merge.py --execute")

def main():
    import sys

    base_dir = Path("/Users/steven/Documents/python")
    dry_run = '--execute' not in sys.argv

    merger = FinalMerge(base_dir)
    merger.execute_final_merge(dry_run=dry_run)

if __name__ == '__main__':
    main()
