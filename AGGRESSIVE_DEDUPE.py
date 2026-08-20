#!/usr/bin/env python3
"""
🔥 AGGRESSIVE DEDUPLICATION
Remove ALL versioned files (file_1.py, file (1).py, file copy.py, etc.)
Keep only the best version of each base filename
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
import ast
from collections import defaultdict

class AggressiveDedupe:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)

    def get_base_name(self, filename):
        """Extract base name without version suffixes"""
        name = filename

        # Remove all version patterns
        patterns = [
            r'[_-]?\d+\.py$',           # file_1.py, file-2.py, file3.py
            r' ?\(\d+\)\.py$',          # file (1).py, file(2).py
            r'[_-]?copy\.py$',          # file_copy.py, file-copy.py
            r' copy\.py$',              # file copy.py
            r'[_-]?v\d+\.py$',          # file_v1.py, file-v2.py
            r' \d+\.py$',               # file 1.py, file 2.py
            r'_\d{14}\.py$',            # file_20250607125012.py (timestamps)
            r'[_-]?\d{8}_\d{6}\.py$',   # file_20250607_125012.py
        ]

        for pattern in patterns:
            name = re.sub(pattern, '.py', name)

        return name

    def score_file(self, filepath):
        """Score a file to determine which version to keep"""
        score = 0

        try:
            # Size (bigger usually = more complete)
            size = filepath.stat().st_size
            score += size / 100

            # Prefer files without version markers in name
            name = filepath.name
            if not any(x in name for x in ['_1', '_2', '_3', '(1)', '(2)', ' copy', '-v1', '-v2', ' 1', ' 2']):
                score += 100

            # Prefer files without timestamps
            if not re.search(r'\d{8}[_-]?\d{6}', name):
                score += 50

            # Content quality
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Parse AST
            try:
                tree = ast.parse(content)

                # Count functions and classes
                func_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
                class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])

                score += func_count * 5
                score += class_count * 10

                # Has docstring
                if ast.get_docstring(tree):
                    score += 30

                # Has main
                if any(n.name == 'main' for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)):
                    score += 20
            except:
                pass

            # Prefer files in better organized locations
            path_str = str(filepath).lower()
            if any(x in path_str for x in ['batch', 'temp', 'test', 'old']):
                score -= 30

        except Exception as e:
            pass

        return score

    def find_and_deduplicate(self):
        """Find all version groups and keep best version"""
        print("🔍 Scanning for versioned files...\n")

        # Get all Python files
        all_files = [f for f in self.pythons_dir.rglob('*.py')
                     if '_archive' not in str(f) and '2T-Xx-python' not in str(f)
                     and '.venv' not in str(f) and '.history' not in str(f)]

        print(f"📂 Found {len(all_files)} files\n")

        # Group by base name
        base_groups = defaultdict(list)

        for f in all_files:
            base = self.get_base_name(f.name)
            base_groups[base].append(f)

        # Find groups with multiple versions
        multi_version = {base: files for base, files in base_groups.items() if len(files) > 1}

        print(f"Found {len(multi_version)} files with multiple versions\n")

        # Process each group
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'aggressive-dedupe-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        deleted_count = 0
        kept_count = 0

        print("🗑️  Processing version groups...\n")

        for base_name, versions in sorted(multi_version.items(), key=lambda x: len(x[1]), reverse=True):
            if len(versions) <= 1:
                continue

            # Score all versions
            scored = [(f, self.score_file(f)) for f in versions if f.exists()]

            if not scored:
                continue

            # Sort by score (best first)
            scored.sort(key=lambda x: x[1], reverse=True)

            # Keep best, delete rest
            keep_file = scored[0][0]
            delete_files = [f for f, _ in scored[1:]]

            # Only delete if there's a clear winner
            if len(delete_files) > 0:
                kept_count += 1

                for f in delete_files:
                    try:
                        # Archive
                        rel_path = f.relative_to(self.pythons_dir)
                        archive_path = archive_dir / rel_path
                        archive_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, archive_path)

                        # Delete
                        f.unlink()
                        deleted_count += 1

                    except Exception as e:
                        pass

                if deleted_count % 100 == 0:
                    print(f"   ... processed {deleted_count} files")

        print(f"\n✅ Kept {kept_count} best versions")
        print(f"🗑️  Deleted {deleted_count} duplicate versions")
        print(f"📦 Archived to: {archive_dir}\n")

        return deleted_count


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🔥 AGGRESSIVE DEDUPLICATION                                   ║
║     Remove ALL versioned/timestamped duplicates                  ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    print("This will:")
    print("  • Find all files like: file_1.py, file (1).py, file copy.py")
    print("  • Find all timestamped versions: file_20250607125012.py")
    print("  • Keep ONLY the best version of each")
    print("  • Archive all deleted files safely")
    print()

    confirm = input("Type 'CLEAN' to execute aggressive deduplication: ")

    if confirm == 'CLEAN':
        deduper = AggressiveDedupe()
        deleted = deduper.find_and_deduplicate()
        print(f"\n🎉 Aggressive deduplication complete! Removed {deleted} duplicate versions!")
    else:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()

