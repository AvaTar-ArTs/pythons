#!/usr/bin/env python3
"""
🔍 FIND DUPLICATE CONTENT & SIMILAR FILENAMES
Find files that are duplicates or near-duplicates (renamed versions)
"""

import hashlib
import difflib
from pathlib import Path
from collections import defaultdict
import csv
from datetime import datetime

class DuplicateFinder:
    def __init__(self, pythons_dir="/Users/steven/pythons"):
        self.pythons_dir = Path(pythons_dir)
        self.files = []
        self.hash_map = defaultdict(list)
        self.similar_names = defaultdict(list)

    def get_file_hash(self, filepath):
        """Calculate MD5 hash"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def normalize_filename(self, filename):
        """Normalize filename for comparison"""
        # Remove common variations
        name = filename.lower()
        name = name.replace('.py', '')
        name = name.replace('_', '')
        name = name.replace('-', '')
        name = name.replace(' ', '')
        name = name.replace('(', '')
        name = name.replace(')', '')
        name = name.replace('copy', '')
        name = name.replace('1', '')
        name = name.replace('2', '')
        name = name.replace('3', '')
        name = name.replace('v1', '')
        name = name.replace('v2', '')
        name = name.replace('v3', '')
        return name

    def scan_all_files(self):
        """Scan all Python files"""
        print("🔍 Scanning all Python files for duplicates...\n")

        # Get all .py files (skip _archive)
        all_files = []
        for f in self.pythons_dir.rglob('*.py'):
            if '_archive' not in str(f) and '2T-Xx-python' not in str(f):
                all_files.append(f)

        print(f"📂 Found {len(all_files)} Python files (excluding archives)\n")

        for i, filepath in enumerate(all_files, 1):
            file_hash = self.get_file_hash(filepath)
            normalized = self.normalize_filename(filepath.name)

            self.files.append({
                'path': filepath,
                'name': filepath.name,
                'normalized': normalized,
                'hash': file_hash,
                'size': filepath.stat().st_size if filepath.exists() else 0
            })

            # Group by hash
            if file_hash:
                self.hash_map[file_hash].append(filepath)

            # Group by normalized name
            self.similar_names[normalized].append(filepath)

            if i % 1000 == 0:
                print(f"   ... scanned {i} files")

        print(f"\n✅ Scan complete!\n")
        return len(self.files)

    def find_exact_duplicates(self):
        """Find exact content duplicates"""
        exact_dupes = []

        for file_hash, paths in self.hash_map.items():
            if len(paths) > 1:
                exact_dupes.append({
                    'hash': file_hash,
                    'count': len(paths),
                    'files': paths,
                    'size': paths[0].stat().st_size if paths[0].exists() else 0
                })

        # Sort by count
        exact_dupes.sort(key=lambda x: x['count'], reverse=True)
        return exact_dupes

    def find_similar_filenames(self):
        """Find files with similar names (likely duplicates/versions)"""
        similar = []

        for normalized, paths in self.similar_names.items():
            if len(paths) > 1:
                # Get actual names
                names = [p.name for p in paths]

                similar.append({
                    'normalized': normalized,
                    'count': len(paths),
                    'files': paths,
                    'names': names
                })

        # Sort by count
        similar.sort(key=lambda x: x['count'], reverse=True)
        return similar

    def find_name_pattern_dupes(self):
        """Find common naming patterns indicating duplicates"""
        patterns = defaultdict(list)

        for file_info in self.files:
            name = file_info['name']

            # Remove common suffixes/versions
            base_patterns = [
                (r'_\d+\.py$', name.replace('_1.py', '').replace('_2.py', '').replace('_3.py', '')),
                (r' \(\d+\)\.py$', name.replace(' (1).py', '').replace(' (2).py', '').replace(' (3).py', '')),
                (r'-\d+\.py$', name.replace('-1.py', '').replace('-2.py', '').replace('-3.py', '')),
                (r'(_copy|_Copy| copy| Copy)\.py$', name.replace('_copy.py', '.py').replace(' copy.py', '.py')),
                (r'(-v\d+|_v\d+)\.py$', name.replace('-v1.py', '.py').replace('-v2.py', '.py')),
            ]

            for pattern_regex, base_name in base_patterns:
                import re
                if re.search(pattern_regex, name):
                    patterns[base_name].append(file_info['path'])
                    break
            else:
                # No pattern matched
                patterns[name].append(file_info['path'])

        # Find patterns with multiple files
        pattern_dupes = []
        for base_name, paths in patterns.items():
            if len(paths) > 1:
                pattern_dupes.append({
                    'base': base_name,
                    'count': len(paths),
                    'files': paths
                })

        pattern_dupes.sort(key=lambda x: x['count'], reverse=True)
        return pattern_dupes

    def save_report(self, exact_dupes, similar_names, pattern_dupes):
        """Save comprehensive report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 1. Exact duplicates CSV
        csv_file = self.pythons_dir / f'EXACT_DUPLICATES_{timestamp}.csv'
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Hash', 'File Count', 'Size (KB)', 'File Paths'])

            for dup in exact_dupes:
                paths_str = ' | '.join(str(p.relative_to(self.pythons_dir)) for p in dup['files'])
                writer.writerow([
                    dup['hash'],
                    dup['count'],
                    f"{dup['size'] / 1024:.2f}",
                    paths_str
                ])

        print(f"✅ Exact duplicates: {csv_file.name}")

        # 2. Similar names CSV
        csv_file2 = self.pythons_dir / f'SIMILAR_NAMES_{timestamp}.csv'
        with open(csv_file2, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Normalized Name', 'Variant Count', 'Actual Names', 'File Paths'])

            for sim in similar_names[:500]:  # Top 500
                names_str = ' | '.join(sim['names'])
                paths_str = ' | '.join(str(p.relative_to(self.pythons_dir)) for p in sim['files'])
                writer.writerow([
                    sim['normalized'],
                    sim['count'],
                    names_str,
                    paths_str
                ])

        print(f"✅ Similar names: {csv_file2.name}")

        # 3. Pattern duplicates CSV
        csv_file3 = self.pythons_dir / f'PATTERN_DUPLICATES_{timestamp}.csv'
        with open(csv_file3, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Base Name', 'Version Count', 'File Paths'])

            for pat in pattern_dupes[:500]:
                paths_str = ' | '.join(str(p.relative_to(self.pythons_dir)) for p in pat['files'])
                writer.writerow([
                    pat['base'],
                    pat['count'],
                    paths_str
                ])

        print(f"✅ Pattern duplicates: {csv_file3.name}")


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║     🔍 FIND DUPLICATE CONTENT & SIMILAR FILENAMES                ║
║     Identify renamed versions and true duplicates                ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    finder = DuplicateFinder()

    # Scan all files
    count = finder.scan_all_files()

    # Find duplicates
    print("🔍 Finding exact content duplicates...")
    exact_dupes = finder.find_exact_duplicates()
    print(f"   Found {len(exact_dupes)} sets of exact duplicates\n")

    print("🔍 Finding similar filenames...")
    similar_names = finder.find_similar_filenames()
    print(f"   Found {len(similar_names)} sets of similar names\n")

    print("🔍 Finding naming pattern duplicates...")
    pattern_dupes = finder.find_name_pattern_dupes()
    print(f"   Found {len(pattern_dupes)} naming pattern groups\n")

    # Print summary
    print("=" * 70)
    print("📊 DUPLICATION SUMMARY")
    print("=" * 70)
    print(f"Total files scanned:       {count}")
    print(f"Exact duplicates:          {len(exact_dupes)} sets")
    print(f"Similar name groups:       {len(similar_names)} sets")
    print(f"Pattern duplicates:        {len(pattern_dupes)} groups")

    total_dupe_files = sum(d['count'] - 1 for d in exact_dupes)
    total_similar_files = sum(s['count'] - 1 for s in similar_names)

    print(f"\nPotential files to remove: {total_dupe_files + total_similar_files}")
    print("=" * 70)

    # Show top examples
    print("\n🔥 TOP 20 EXACT DUPLICATE SETS:\n")
    for i, dup in enumerate(exact_dupes[:20], 1):
        print(f"{i:2}. {dup['count']} copies ({dup['size']/1024:.1f} KB each)")
        for path in dup['files'][:5]:
            print(f"    • {path.relative_to(finder.pythons_dir)}")
        if len(dup['files']) > 5:
            print(f"    ... and {len(dup['files']) - 5} more")
        print()

    print("🔤 TOP 20 SIMILAR NAME GROUPS:\n")
    for i, sim in enumerate(similar_names[:20], 1):
        print(f"{i:2}. {sim['count']} variations of '{sim['normalized']}'")
        for name in sim['names'][:5]:
            print(f"    • {name}")
        if len(sim['names']) > 5:
            print(f"    ... and {len(sim['names']) - 5} more")
        print()

    # Save reports
    print("💾 Saving reports...")
    finder.save_report(exact_dupes, similar_names, pattern_dupes)

    print("\n✅ Analysis complete! Review CSV files for full details.")


if __name__ == "__main__":
    main()

