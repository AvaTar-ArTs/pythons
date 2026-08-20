#!/usr/bin/env python3
"""
Massive Text Inventory Analyzer
Parses large text files containing file paths and categorizes them intelligently
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
import json
from datetime import datetime

class MassiveTextAnalyzer:
    """Analyze massive text files containing file inventories"""

    def __init__(self, avatararts_dir="/Users/steven/AVATARARTS"):
        self.base_dir = Path(avatararts_dir)
        self.text_files = {
            '20k-steven.txt': {'size': '7.5MB', 'expected_lines': 20000},
            '17k-and-going.txt': {'size': '1.7MB', 'expected_lines': 17000},
            'documents-deepive.txt': {'size': '240KB', 'expected_lines': 5000},
            'html-yell.txt': {'size': '74KB', 'expected_lines': 2000},
            'claude-rsources.txt': {'size': '77KB', 'expected_lines': 2000},
            'seo-aeo-zips.txt': {'size': '598KB', 'expected_lines': 10000},
        }

        self.stats = {}

    def parse_file_inventory(self, file_path: Path):
        """Parse a text file containing file paths (space-separated with quotes)"""
        print(f"\n📂 Analyzing: {file_path.name}")

        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path}")
            return None

        stats = {
            'total_lines': 0,
            'file_paths': 0,
            'by_extension': Counter(),
            'by_directory': Counter(),
            'by_type': {
                'documents': 0,    # .md, .txt, .html, .pdf
                'code': 0,         # .py, .js, .ts, .sh
                'media': 0,        # .mp4, .mp3, .png, .jpg
                'data': 0,         # .json, .csv, .xml
                'archives': 0,     # .zip, .tar, .gz
                'other': 0
            },
            'paths': [],
            'largest_directories': Counter(),
        }

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            stats['total_lines'] = content.count('\n') + 1

            # Split by space but respect quotes
            import shlex
            try:
                paths = shlex.split(content)
            except ValueError:
                # Fallback: simple split if shlex fails
                paths = content.split()

            for path in paths:
                path = path.strip()

                if not path or '/' not in path:
                    continue

                stats['file_paths'] += 1
                stats['paths'].append(path)

                # Extract extension
                path_obj = Path(path)
                ext = path_obj.suffix.lower() if path_obj.suffix else 'no_ext'
                stats['by_extension'][ext] += 1

                # Categorize by type
                if ext in ['.md', '.txt', '.html', '.pdf', '.rst', '.qmd']:
                    stats['by_type']['documents'] += 1
                elif ext in ['.py', '.js', '.ts', '.sh', '.go', '.rs']:
                    stats['by_type']['code'] += 1
                elif ext in ['.mp4', '.mp3', '.wav', '.m4a', '.png', '.jpg', '.jpeg', '.gif']:
                    stats['by_type']['media'] += 1
                elif ext in ['.json', '.csv', '.xml', '.yaml', '.yml']:
                    stats['by_type']['data'] += 1
                elif ext in ['.zip', '.tar', '.gz', '.bz2']:
                    stats['by_type']['archives'] += 1
                else:
                    stats['by_type']['other'] += 1

                # Extract top-level directory
                try:
                    # Get the first meaningful directory after /Users/steven
                    if '/Users/steven/' in path:
                        parts = path.split('/Users/steven/')[1].split('/')
                        if parts:
                            top_dir = parts[0]
                            stats['largest_directories'][top_dir] += 1
                    elif path.startswith('/'):
                        parts = [p for p in path.split('/') if p]
                        if parts:
                            stats['largest_directories'][parts[0]] += 1
                except Exception as e:
                    pass

        print(f"  ✓ Analyzed {stats['total_lines']:,} lines")
        print(f"  ✓ Found {stats['file_paths']:,} file paths")

        return stats

    def analyze_all(self):
        """Analyze all text inventory files"""
        print("🔍 Analyzing All Text Inventories\n")
        print("=" * 70)

        for filename, info in self.text_files.items():
            file_path = self.base_dir / filename
            stats = self.parse_file_inventory(file_path)

            if stats:
                self.stats[filename] = stats

                # Show quick summary
                print(f"\n  Top 5 Extensions:")
                for ext, count in stats['by_extension'].most_common(5):
                    print(f"    {ext}: {count:,}")

                print(f"\n  File Types:")
                for type_name, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
                    if count > 0:
                        pct = (count / stats['file_paths'] * 100) if stats['file_paths'] > 0 else 0
                        print(f"    {type_name}: {count:,} ({pct:.1f}%)")

                print(f"\n  Top 5 Directories:")
                for dir_name, count in stats['largest_directories'].most_common(5):
                    print(f"    {dir_name}: {count:,} files")

                print("\n" + "=" * 70)

        return self.stats

    def generate_summary_report(self):
        """Generate comprehensive summary"""
        print("\n\n📊 COMPREHENSIVE SUMMARY REPORT\n")
        print("=" * 70)

        total_files = sum(s.get('file_paths', 0) for s in self.stats.values())
        total_lines = sum(s.get('total_lines', 0) for s in self.stats.values())

        print(f"\n**TOTALS ACROSS ALL INVENTORY FILES:**")
        print(f"  Total Lines: {total_lines:,}")
        print(f"  Total File Paths: {total_files:,}")

        # Aggregate extension counts
        all_extensions = Counter()
        for stats in self.stats.values():
            all_extensions.update(stats['by_extension'])

        print(f"\n**TOP 20 FILE EXTENSIONS (Across All Inventories):**")
        for ext, count in all_extensions.most_common(20):
            pct = (count / total_files * 100) if total_files > 0 else 0
            print(f"  {ext:15s}: {count:6,} ({pct:5.1f}%)")

        # Aggregate file types
        all_types = Counter()
        for stats in self.stats.values():
            for type_name, count in stats['by_type'].items():
                all_types[type_name] += count

        print(f"\n**FILE TYPES DISTRIBUTION:**")
        for type_name, count in sorted(all_types.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_files * 100) if total_files > 0 else 0
            print(f"  {type_name:15s}: {count:6,} ({pct:5.1f}%)")

        # Aggregate directories
        all_dirs = Counter()
        for stats in self.stats.values():
            all_dirs.update(stats['largest_directories'])

        print(f"\n**TOP 15 DIRECTORIES (By File Count):**")
        for dir_name, count in all_dirs.most_common(15):
            pct = (count / total_files * 100) if total_files > 0 else 0
            print(f"  {dir_name:30s}: {count:6,} ({pct:5.1f}%)")

        print("\n" + "=" * 70)

        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'extensions': dict(all_extensions.most_common(50)),
            'types': dict(all_types),
            'directories': dict(all_dirs.most_common(30))
        }

    def save_consolidated_analysis(self, output_dir=None):
        """Save detailed analysis to JSON"""
        if output_dir is None:
            output_dir = self.base_dir

        output_file = Path(output_dir) / f'text_inventories_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        with open(output_file, 'w') as f:
            json.dump(self.stats, f, indent=2, default=str)

        print(f"\n✅ Detailed analysis saved to: {output_file}")
        return output_file

    def extract_md_html_files(self):
        """Extract all .md and .html files for further processing"""
        md_html_files = []

        for filename, stats in self.stats.items():
            for path in stats.get('paths', []):
                path_obj = Path(path)
                ext = path_obj.suffix.lower()

                if ext in ['.md', '.html', '.htm']:
                    md_html_files.append({
                        'path': path,
                        'extension': ext,
                        'source_file': filename,
                        'name': path_obj.name
                    })

        print(f"\n📄 Found {len(md_html_files):,} MD/HTML files across all inventories")

        # Save to separate CSV for processing
        csv_file = self.base_dir / 'md_html_files_consolidated.csv'
        import csv

        with open(csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['path', 'extension', 'source_file', 'name'])
            writer.writeheader()
            writer.writerows(md_html_files)

        print(f"✅ MD/HTML files list saved to: {csv_file}")

        return md_html_files


def main():
    """Main entry point"""
    analyzer = MassiveTextAnalyzer()

    # Analyze all text inventory files
    stats = analyzer.analyze_all()

    # Generate comprehensive summary
    summary = analyzer.generate_summary_report()

    # Save detailed analysis
    analyzer.save_consolidated_analysis()

    # Extract MD/HTML files specifically
    md_html_files = analyzer.extract_md_html_files()

    print("\n\n🎯 NEXT STEPS:")
    print("=" * 70)
    print("\n1. Review the generated JSON file for detailed breakdowns")
    print("2. Check md_html_files_consolidated.csv for all MD/HTML files")
    print("3. Use content-awareness intelligence to categorize the 50K+ files")
    print("4. Integrate findings into AVATARARTS_INVENTORY.csv")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
