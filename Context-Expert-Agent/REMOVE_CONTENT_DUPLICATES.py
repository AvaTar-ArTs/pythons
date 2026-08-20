#!/usr/bin/env python3
"""
🗑️ REMOVE CONTENT DUPLICATES
Remove files with identical/similar CODE (regardless of name)
"""

import csv
import shutil
import ast
from pathlib import Path
from datetime import datetime

class ContentDuplicateRemover:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)

    def load_identical_code(self):
        """Load files with identical code"""
        csv_files = sorted(self.pythons_dir.glob('IDENTICAL_CODE_*.csv'), reverse=True)

        if not csv_files:
            return []

        identical_groups = []

        with open(csv_files[0], 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                paths = [self.pythons_dir / p for p in row['File Paths'].split(' | ')]
                identical_groups.append(paths)

        return identical_groups

    def load_similar_structure(self):
        """Load files with similar structure"""
        csv_files = sorted(self.pythons_dir.glob('SIMILAR_STRUCTURE_*.csv'), reverse=True)

        if not csv_files:
            return []

        similar_groups = []

        with open(csv_files[0], 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if int(row['File Count']) >= 5:  # Only large groups
                    paths = [self.pythons_dir / p for p in row['File Paths'].split(' | ')]
                    similar_groups.append(paths)

        return similar_groups

    def choose_best_file(self, files):
        """Choose the best file to keep from a group"""
        scores = []

        for f in files:
            if not f.exists():
                continue

            score = 0

            # Size (bigger usually = more complete)
            size = f.stat().st_size
            score += size / 100

            # Prefer cleaner names (no DOCS_PYTHON_, no _from_, etc.)
            name = f.name
            if 'DOCS_PYTHON_' not in name and '_from_' not in name:
                score += 100

            # Prefer shorter paths (less nested)
            depth = len(f.relative_to(self.pythons_dir).parts)
            score += max(0, 50 - depth * 10)

            # Content quality
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()

                try:
                    tree = ast.parse(content)

                    # Has docstring
                    if ast.get_docstring(tree):
                        score += 30

                    # Count functions/classes
                    func_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
                    class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])

                    score += func_count * 2
                    score += class_count * 5
                except:
                    pass
            except:
                pass

            scores.append((f, score))

        if not scores:
            return None, []

        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[0][0], [f for f, _ in scores[1:]]

    def execute_removal(self):
        """Execute content duplicate removal"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'content-duplicates-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("🔍 Loading content duplicate analysis...\n")

        identical = self.load_identical_code()
        similar = self.load_similar_structure()

        print(f"Found {len(identical)} sets with identical code")
        print(f"Found {len(similar)} sets with similar structure\n")

        print("🗑️  Processing identical code groups...\n")

        removed_identical = 0

        for group in identical:
            keep, delete = self.choose_best_file(group)

            if keep and delete:
                print(f"KEEP: {keep.name}")
                for f in delete:
                    try:
                        # Archive
                        rel_path = f.relative_to(self.pythons_dir)
                        archive_path = archive_dir / rel_path
                        archive_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, archive_path)

                        # Delete
                        f.unlink()
                        removed_identical += 1
                        print(f"  DELETE: {f.name}")
                    except Exception as e:
                        print(f"  ERROR: {f.name} - {e}")
                print()

        print(f"✅ Removed {removed_identical} files with identical code\n")

        print("🔍 Processing similar structure groups (high similarity)...\n")

        removed_similar = 0

        for group in similar:
            keep, delete = self.choose_best_file(group)

            if keep and len(delete) >= 3:  # Only remove if 3+ similar files
                print(f"KEEP: {keep.name} (from {len(group)} similar files)")

                for f in delete:
                    try:
                        # Archive
                        rel_path = f.relative_to(self.pythons_dir)
                        archive_path = archive_dir / rel_path
                        archive_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, archive_path)

                        # Delete
                        f.unlink()
                        removed_similar += 1
                    except:
                        pass

                if removed_similar % 20 == 0 and removed_similar > 0:
                    print(f"   ... processed {removed_similar} files")

        print(f"\n✅ Removed {removed_similar} files with similar structure\n")

        print("=" * 70)
        print("📊 CONTENT DEDUPLICATION SUMMARY")
        print("=" * 70)
        print(f"Identical code removed:     {removed_identical}")
        print(f"Similar structure removed:  {removed_similar}")
        print(f"TOTAL REMOVED:              {removed_identical + removed_similar}")
        print(f"Archive location:           {archive_dir}")
        print("=" * 70)

        return removed_identical + removed_similar


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🗑️  REMOVE CONTENT DUPLICATES                                ║
║     Remove files with identical/similar CODE                     ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    print("This will remove files that have:")
    print("  • Identical code (same content, different name)")
    print("  • Very similar functions/classes (copy-paste variations)")
    print("  • Keeping only the BEST version of each")
    print()

    confirm = input("Type 'REMOVE' to execute: ")

    if confirm == 'REMOVE':
        remover = ContentDuplicateRemover()
        total = remover.execute_removal()
        print(f"\n🎉 Content deduplication complete! Removed {total} duplicate files!")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()

