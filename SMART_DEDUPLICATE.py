#!/usr/bin/env python3
"""
🗑️ SMART DEDUPLICATION
Remove duplicate files keeping only the best version
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
import ast

class SmartDeduplicator:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.to_delete = []
        self.to_keep = []

    def load_duplicates(self):
        """Load duplicate analysis"""
        # Find latest reports
        exact_files = sorted(self.pythons_dir.glob('EXACT_DUPLICATES_*.csv'), reverse=True)
        similar_files = sorted(self.pythons_dir.glob('SIMILAR_NAMES_*.csv'), reverse=True)

        if not exact_files or not similar_files:
            print("❌ No duplicate reports found!")
            return False

        self.exact_file = exact_files[0]
        self.similar_file = similar_files[0]

        print(f"📄 Loading: {self.exact_file.name}")
        print(f"📄 Loading: {self.similar_file.name}\n")

        return True

    def analyze_similar_group(self, files):
        """Determine which file to keep in a similar group"""
        if len(files) <= 1:
            return files[0] if files else None, []

        # Score each file
        scores = []

        for f in files:
            if not f.exists():
                continue

            score = 0

            # Size (bigger is usually better - more complete)
            try:
                size = f.stat().st_size
                score += size / 100
            except:
                size = 0

            # Prefer files without version numbers
            name = f.name.lower()
            if not any(x in name for x in ['_1', '_2', '_3', '(1)', '(2)', ' copy', '-v1', '-v2']):
                score += 50

            # Prefer shorter names (cleaner)
            score += max(0, 50 - len(f.name))

            # Prefer files in organized locations
            path_str = str(f)
            if any(x in path_str for x in ['batch', 'misc', 'other', 'general', 'temp']):
                score -= 20

            # Analyze content quality
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                # Count functions/classes
                try:
                    tree = ast.parse(content)
                    func_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
                    class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])

                    score += func_count * 5
                    score += class_count * 10

                    # Has docstring
                    if ast.get_docstring(tree):
                        score += 20

                    # Has main
                    if any(n.name == 'main' for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
                        score += 10
                except:
                    pass
            except:
                pass

            scores.append((f, score))

        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Keep best, delete rest
        keep = scores[0][0]
        delete = [f for f, _ in scores[1:]]

        return keep, delete

    def process_exact_duplicates(self):
        """Process exact duplicates - keep one, delete rest"""
        print("🔍 Processing exact duplicates...\n")

        with open(self.exact_file, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                paths_str = row['File Paths']
                file_paths = [self.pythons_dir / p for p in paths_str.split(' | ')]

                # Keep first, delete rest
                keep, delete = self.analyze_similar_group(file_paths)

                if keep:
                    self.to_keep.append(keep)
                    self.to_delete.extend(delete)

        print(f"✅ Processed exact duplicates\n")

    def process_similar_names(self):
        """Process similar named files"""
        print("🔍 Processing similar name groups...\n")

        with open(self.similar_file, 'r') as f:
            reader = csv.DictReader(f)

            processed = 0
            for row in reader:
                if int(row['Variant Count']) < 2:
                    continue

                paths_str = row['File Paths']
                file_paths = [self.pythons_dir / p for p in paths_str.split(' | ')]

                # Only process if files actually exist
                existing_files = [f for f in file_paths if f.exists()]

                if len(existing_files) >= 2:
                    keep, delete = self.analyze_similar_group(existing_files)

                    if keep and keep not in self.to_keep:
                        self.to_keep.append(keep)
                        self.to_delete.extend([d for d in delete if d not in self.to_delete])
                        processed += 1

                if processed % 100 == 0:
                    print(f"   ... processed {processed} groups")

        print(f"✅ Processed {processed} similar name groups\n")

    def execute_deduplication(self, dry_run=True):
        """Execute the deduplication"""
        if dry_run:
            print("🔍 DRY RUN - No files will be deleted\n")
        else:
            print("⚠️  EXECUTING DEDUPLICATION\n")

            # Create archive
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_dir = self.pythons_dir / '_archive' / f'deduplication-{timestamp}'
            archive_dir.mkdir(parents=True, exist_ok=True)
            print(f"📦 Archive: {archive_dir}\n")

        stats = {'deleted': 0, 'kept': 0, 'errors': []}

        print(f"📊 Plan: Keep {len(self.to_keep)} files, delete {len(self.to_delete)} duplicates\n")

        # Delete duplicates
        for f in self.to_delete:
            if not f.exists():
                continue

            try:
                if not dry_run:
                    # Archive before delete
                    rel_path = f.relative_to(self.pythons_dir)
                    archive_path = archive_dir / rel_path
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, archive_path)

                    # Delete
                    f.unlink()

                stats['deleted'] += 1

                if stats['deleted'] % 100 == 0:
                    print(f"   ... processed {stats['deleted']} files")

            except Exception as e:
                stats['errors'].append(f"{f.name}: {e}")

        print(f"\n{'Would delete' if dry_run else 'Deleted'}: {stats['deleted']} duplicate files")

        if stats['errors']:
            print(f"⚠️  Errors: {len(stats['errors'])}")
            for err in stats['errors'][:10]:
                print(f"   {err}")

        return stats


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🗑️  SMART DEDUPLICATION                                      ║
║     Remove 3,938 duplicate files intelligently                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    dedup = SmartDeduplicator()

    if not dedup.load_duplicates():
        return

    # Process duplicates
    dedup.process_exact_duplicates()
    dedup.process_similar_names()

    # Show summary
    print("=" * 70)
    print("📊 DEDUPLICATION PLAN")
    print("=" * 70)
    print(f"Files to keep:    {len(dedup.to_keep)}")
    print(f"Files to delete:  {len(dedup.to_delete)}")

    total_size = sum(f.stat().st_size for f in dedup.to_delete if f.exists())
    print(f"Space to recover: {total_size / (1024*1024):.2f} MB")
    print("=" * 70)

    # Execute
    import sys
    if '--execute' in sys.argv:
        print()
        confirm = input("Type 'DEDUPLICATE' to remove duplicates: ")
        if confirm == 'DEDUPLICATE':
            dedup.execute_deduplication(dry_run=False)
            print("\n✅ Deduplication complete!")
        else:
            print("❌ Cancelled")
    else:
        dedup.execute_deduplication(dry_run=True)
        print("\n🎯 To execute: python3 SMART_DEDUPLICATE.py --execute")


if __name__ == "__main__":
    main()

