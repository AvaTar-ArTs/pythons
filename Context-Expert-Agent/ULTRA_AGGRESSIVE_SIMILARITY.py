#!/usr/bin/env python3
"""
🔥 ULTRA AGGRESSIVE SIMILARITY SCANNER
Find files that are 80%+ similar in content/structure
Lower threshold to catch more duplicates
"""

import ast
import difflib
from pathlib import Path
from collections import defaultdict
import shutil
from datetime import datetime

class UltraAggressiveScanner:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.files_data = []

    def get_code_fingerprint(self, filepath):
        """Get comprehensive code fingerprint"""
        fingerprint = {
            'path': filepath,
            'name': filepath.name,
            'size': 0,
            'lines': 0,
            'func_names': [],
            'class_names': [],
            'import_names': [],
            'code_structure': '',
            'content': ''
        }

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            fingerprint['size'] = len(content)
            fingerprint['lines'] = len(content.splitlines())
            fingerprint['content'] = content

            # Parse AST
            try:
                tree = ast.parse(content)

                # Extract structure
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        fingerprint['func_names'].append(node.name)
                    elif isinstance(node, ast.ClassDef):
                        fingerprint['class_names'].append(node.name)
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            fingerprint['import_names'].append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            fingerprint['import_names'].append(node.module)

                # Create structure signature
                fingerprint['code_structure'] = (
                    f"funcs:{','.join(sorted(fingerprint['func_names']))}"
                    f"|classes:{','.join(sorted(fingerprint['class_names']))}"
                    f"|imports:{','.join(sorted(set(fingerprint['import_names'])))}"
                )
            except:
                pass

        except:
            pass

        return fingerprint

    def scan_all(self):
        """Scan all files"""
        print("🔥 ULTRA AGGRESSIVE SCAN - Finding similar content...\n")

        files = [f for f in self.pythons_dir.rglob('*.py')
                 if '_archive' not in str(f) and '2T-Xx-python' not in str(f)
                 and '.venv' not in str(f) and '.history' not in str(f)]

        print(f"📂 Analyzing {len(files)} files...\n")

        for i, f in enumerate(files, 1):
            fp = self.get_code_fingerprint(f)
            self.files_data.append(fp)

            if i % 500 == 0:
                print(f"   ... analyzed {i} files")

        print(f"\n✅ Scan complete!\n")
        return len(self.files_data)

    def compare_content_similarity(self, content1, content2):
        """Calculate content similarity (0-100%)"""
        # Normalize: remove comments and extra whitespace
        def normalize(content):
            lines = []
            for line in content.splitlines():
                # Remove comments
                line = line.split('#')[0].strip()
                if line:
                    lines.append(line)
            return '\n'.join(lines)

        norm1 = normalize(content1)
        norm2 = normalize(content2)

        if not norm1 or not norm2:
            return 0

        ratio = difflib.SequenceMatcher(None, norm1, norm2).ratio()
        return ratio * 100

    def find_similar_content(self, threshold=80):
        """Find files with 80%+ similar content"""
        print(f"🔍 Finding files with {threshold}%+ similar content...\n")

        similar_groups = []
        checked = set()

        # Compare all pairs (this will take a while for large sets)
        for i, fp1 in enumerate(self.files_data):
            if i in checked:
                continue

            if not fp1['content'] or fp1['size'] < 100:  # Skip tiny files
                continue

            group = [fp1]

            # Find similar files
            for j, fp2 in enumerate(self.files_data[i+1:], start=i+1):
                if j in checked:
                    continue

                if not fp2['content']:
                    continue

                # Quick filter: size difference
                size_ratio = min(fp1['size'], fp2['size']) / max(fp1['size'], fp2['size'], 1)
                if size_ratio < 0.7:  # More than 30% size difference
                    continue

                # Quick filter: structure signature
                if fp1['code_structure'] and fp2['code_structure']:
                    if fp1['code_structure'] == fp2['code_structure']:
                        group.append(fp2)
                        checked.add(j)
                        continue

                # Deep comparison (expensive)
                if len(fp1['content']) > 1000 and len(fp2['content']) > 1000:
                    # Only compare if both are substantial
                    similarity = self.compare_content_similarity(fp1['content'], fp2['content'])

                    if similarity >= threshold:
                        group.append(fp2)
                        checked.add(j)

            if len(group) > 1:
                similar_groups.append(group)
                checked.add(i)

            if (i % 100 == 0):
                print(f"   ... compared {i}/{len(self.files_data)} files (found {len(similar_groups)} groups)")

        print(f"\n✅ Found {len(similar_groups)} groups of similar files\n")
        return similar_groups

    def print_summary(self, groups, threshold):
        """Print similarity summary"""
        print("=" * 70)
        print(f"📊 SIMILARITY SCAN ({threshold}%+ threshold)")
        print("=" * 70)
        print(f"Similar groups found:  {len(groups)}")

        total_dupes = sum(len(g) - 1 for g in groups)
        print(f"Potential files to remove: {total_dupes}")
        print("=" * 70)

        if groups:
            print("\n🔥 TOP 20 SIMILAR GROUPS:\n")

            sorted_groups = sorted(groups, key=lambda x: len(x), reverse=True)

            for i, group in enumerate(sorted_groups[:20], 1):
                print(f"{i:2}. {len(group)} similar files:")
                for fp in group[:5]:
                    print(f"    • {fp['name']} ({fp['lines']} lines)")
                if len(group) > 5:
                    print(f"    ... and {len(group) - 5} more")

                # Show what they have in common
                if group[0]['func_names']:
                    common_funcs = set(group[0]['func_names'])
                    for fp in group[1:]:
                        common_funcs &= set(fp['func_names'])
                    if common_funcs:
                        print(f"    Common functions: {', '.join(list(common_funcs)[:5])}")
                print()

    def remove_duplicates(self, groups):
        """Remove duplicate files, keeping best version"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        archive_dir = self.pythons_dir / '_archive' / f'ultra-aggressive-{timestamp}'
        archive_dir.mkdir(parents=True, exist_ok=True)

        print("🗑️  Removing similar files...\n")

        removed = 0

        for group in groups:
            # Score each file
            scores = []
            for fp in group:
                score = 0
                score += fp['size'] / 100  # Size
                score += len(fp['func_names']) * 5  # Functions
                score += len(fp['class_names']) * 10  # Classes

                # Prefer clean names
                if '_from_' not in fp['name'] and 'DOCS_PYTHON_' not in fp['name']:
                    score += 100

                scores.append((fp, score))

            # Sort by score
            scores.sort(key=lambda x: x[1], reverse=True)

            # Keep best, remove rest
            keep = scores[0][0]
            to_remove = [fp for fp, _ in scores[1:]]

            for fp in to_remove:
                try:
                    # Archive
                    rel_path = fp['path'].relative_to(self.pythons_dir)
                    archive_path = archive_dir / rel_path
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(fp['path'], archive_path)

                    # Delete
                    fp['path'].unlink()
                    removed += 1

                    if removed % 50 == 0:
                        print(f"   ... removed {removed} files")
                except:
                    pass

        print(f"\n✅ Removed {removed} similar files")
        print(f"📦 Archived to: {archive_dir}\n")

        return removed


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🔥 ULTRA AGGRESSIVE SIMILARITY SCANNER                        ║
║     Find files with 80%+ similar content (lower threshold!)      ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    scanner = UltraAggressiveScanner()

    # Scan all files
    count = scanner.scan_all()

    # Find similar content (80% threshold)
    groups = scanner.find_similar_content(threshold=80)

    # Print summary
    scanner.print_summary(groups, 80)

    if groups:
        confirm = input("\nType 'AGGRESSIVE' to remove similar files: ")

        if confirm == 'AGGRESSIVE':
            removed = scanner.remove_duplicates(groups)
            print(f"🎉 Ultra aggressive cleanup complete! Removed {removed} files!")
        else:
            print("\n❌ Cancelled")
    else:
        print("\n✅ No similar files found at 80% threshold!")


if __name__ == "__main__":
    main()

