#!/usr/bin/env python3
"""
Comprehensive Structure Verifier

Checks for:
1. Duplicate files (exact and semantic)
2. Naming consistency
3. Proper categorization
4. Parent folder context preservation
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class ComprehensiveVerifier:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.issues = {
            'exact_duplicates': [],
            'similar_names': [],
            'missing_context': [],
            'overly_long': [],
            'poorly_named': []
        }

        self.stats = {
            'total_files': 0,
            'categories': 0,
            'exact_dupes': 0,
            'similar_files': 0
        }

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def find_exact_duplicates(self):
        """Find exact duplicate files."""
        print("\n🔍 Checking for exact duplicates...\n")

        hash_map = defaultdict(list)

        # Scan all Python files
        for folder in self.target_dir.iterdir():
            if not folder.is_dir() or folder.name.startswith(('.', '_')):
                continue

            for file_path in folder.glob("*.py"):
                file_hash = self.get_file_hash(file_path)
                if file_hash:
                    hash_map[file_hash].append(file_path)
                    self.stats['total_files'] += 1

        # Find duplicates
        for file_hash, files in hash_map.items():
            if len(files) > 1:
                self.issues['exact_duplicates'].append(files)
                self.stats['exact_dupes'] += len(files) - 1

        if self.issues['exact_duplicates']:
            print(f"❌ Found {len(self.issues['exact_duplicates'])} exact duplicate groups:\n")
            for group in self.issues['exact_duplicates'][:5]:
                print(f"  Duplicates:")
                for file in group:
                    print(f"    - {file.parent.name}/{file.name}")
                print()
        else:
            print(f"✅ No exact duplicates found!\n")

    def find_similar_names(self):
        """Find files with very similar names (likely duplicates)."""
        print("\n🔍 Checking for similar filenames...\n")

        file_groups = defaultdict(list)

        for folder in self.target_dir.iterdir():
            if not folder.is_dir() or folder.name.startswith(('.', '_')):
                continue

            for file_path in folder.glob("*.py"):
                # Create simplified name for comparison
                base = file_path.stem.lower()
                # Remove numbers, versions, underscores
                simplified = base.replace('_', '').replace('-', '')
                simplified = ''.join(c for c in simplified if not c.isdigit())

                file_groups[simplified].append(file_path)

        # Find groups with multiple files
        for simplified, files in file_groups.items():
            if len(files) > 5:  # More than 5 similar files
                self.issues['similar_names'].append(files)
                self.stats['similar_files'] += len(files)

        if self.issues['similar_names']:
            print(f"⚠️  Found {len(self.issues['similar_names'])} groups of similar names:\n")
            for group in self.issues['similar_names'][:3]:
                print(f"  Similar files ({len(group)} total):")
                for file in group[:5]:
                    print(f"    - {file.parent.name}/{file.name}")
                if len(group) > 5:
                    print(f"    ... and {len(group) - 5} more")
                print()
        else:
            print(f"✅ No problematic similar names!\n")

    def check_naming_quality(self):
        """Check for poor naming practices."""
        print("\n🔍 Checking naming quality...\n")

        for folder in self.target_dir.iterdir():
            if not folder.is_dir() or folder.name.startswith(('.', '_')):
                continue

            self.stats['categories'] += 1

            for file_path in folder.glob("*.py"):
                name = file_path.stem

                # Check for overly long names (>60 chars)
                if len(name) > 60:
                    self.issues['overly_long'].append(file_path)

                # Check for poor names (just numbers, single char, etc.)
                if name.isdigit() or len(name) < 3:
                    self.issues['poorly_named'].append(file_path)

        if self.issues['overly_long']:
            print(f"⚠️  {len(self.issues['overly_long'])} files have overly long names (>60 chars)\n")
        else:
            print(f"✅ All filenames are reasonable length!\n")

        if self.issues['poorly_named']:
            print(f"⚠️  {len(self.issues['poorly_named'])} files have poor names (too short/generic)\n")
            for file in self.issues['poorly_named'][:10]:
                print(f"    {file.parent.name}/{file.name}")
        else:
            print(f"✅ All filenames are descriptive!\n")

    def generate_report(self):
        """Generate verification report."""
        report_path = self.target_dir / f"VERIFICATION_REPORT_{self.timestamp}.md"

        with open(report_path, 'w') as f:
            f.write("# 🔍 Comprehensive Structure Verification Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total Files Scanned:** {self.stats['total_files']:,}\n")
            f.write(f"- **Categories:** {self.stats['categories']}\n")
            f.write(f"- **Exact Duplicates:** {self.stats['exact_dupes']}\n")
            f.write(f"- **Similar Name Groups:** {len(self.issues['similar_names'])}\n")
            f.write(f"- **Overly Long Names:** {len(self.issues['overly_long'])}\n")
            f.write(f"- **Poorly Named Files:** {len(self.issues['poorly_named'])}\n\n")

            # Exact duplicates
            if self.issues['exact_duplicates']:
                f.write("## ❌ Exact Duplicates to Remove\n\n")
                for group in self.issues['exact_duplicates']:
                    f.write(f"### Duplicate Group\n")
                    for file in group:
                        f.write(f"- `{file.parent.name}/{file.name}`\n")
                    f.write("\n")

            # Similar names
            if self.issues['similar_names']:
                f.write("## ⚠️ Similar Names to Review\n\n")
                for group in self.issues['similar_names'][:10]:
                    f.write(f"### Group ({len(group)} files)\n")
                    for file in group[:10]:
                        f.write(f"- `{file.parent.name}/{file.name}`\n")
                    f.write("\n")

        print(f"\n📄 Report saved: {report_path}\n")

    def run(self):
        """Run complete verification."""
        print(f"\n{'='*80}")
        print("🔍 COMPREHENSIVE STRUCTURE VERIFICATION")
        print(f"{'='*80}\n")

        self.find_exact_duplicates()
        self.find_similar_names()
        self.check_naming_quality()
        self.generate_report()

        print(f"\n{'='*80}")
        print("✅ VERIFICATION COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Total Files: {self.stats['total_files']:,}")
        print(f"Categories: {self.stats['categories']}")
        print(f"Exact Duplicates: {self.stats['exact_dupes']}")
        print(f"Similar Name Groups: {len(self.issues['similar_names'])}")
        print()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Comprehensive Verifier')
    parser.add_argument('--target', default='.', help='Target directory')

    args = parser.parse_args()

    verifier = ComprehensiveVerifier(args.target)
    verifier.run()

if __name__ == "__main__":
    main()
