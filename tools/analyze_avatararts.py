#!/usr/bin/env python3
"""
AVATARARTS Directory Deep Dive Analysis
Comprehensive inventory, categorization, and cleanup recommendations
"""

import os
import hashlib
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import csv

class AvatarArtsAnalyzer:
    def __init__(self, root_dir="/Users/steven/AVATARARTS"):
        self.root = Path(root_dir)
        self.stats = {
            'total_files': 0,
            'total_dirs': 0,
            'total_size': 0,
            'by_extension': Counter(),
            'by_directory': defaultdict(lambda: {'count': 0, 'size': 0}),
            'duplicates': defaultdict(list),
            'python_scripts': [],
            'csv_files': [],
            'markdown_docs': [],
            'json_configs': [],
            'large_files': [],
        }

    def calculate_hash(self, filepath):
        """Calculate MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def analyze(self):
        """Main analysis function"""
        print(f"🔍 Analyzing {self.root}...")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Walk directory tree
        for root, dirs, files in os.walk(self.root):
            self.stats['total_dirs'] += len(dirs)
            root_path = Path(root)

            for file in files:
                filepath = root_path / file

                try:
                    # Skip hidden files and system files
                    if file.startswith('.'):
                        continue

                    file_size = filepath.stat().st_size
                    self.stats['total_files'] += 1
                    self.stats['total_size'] += file_size

                    # Extension analysis
                    ext = filepath.suffix.lower()
                    self.stats['by_extension'][ext] += 1

                    # Directory analysis
                    rel_dir = str(root_path.relative_to(self.root))
                    self.stats['by_directory'][rel_dir]['count'] += 1
                    self.stats['by_directory'][rel_dir]['size'] += file_size

                    # Categorize specific file types
                    if ext == '.py':
                        self.stats['python_scripts'].append({
                            'path': str(filepath.relative_to(self.root)),
                            'size': file_size,
                            'name': file
                        })
                    elif ext == '.csv':
                        self.stats['csv_files'].append({
                            'path': str(filepath.relative_to(self.root)),
                            'size': file_size,
                            'name': file
                        })
                    elif ext == '.md':
                        self.stats['markdown_docs'].append({
                            'path': str(filepath.relative_to(self.root)),
                            'size': file_size,
                            'name': file
                        })
                    elif ext == '.json':
                        self.stats['json_configs'].append({
                            'path': str(filepath.relative_to(self.root)),
                            'size': file_size,
                            'name': file
                        })

                    # Track large files (>10MB)
                    if file_size > 10 * 1024 * 1024:
                        self.stats['large_files'].append({
                            'path': str(filepath.relative_to(self.root)),
                            'size': file_size,
                            'size_mb': file_size / (1024 * 1024)
                        })

                    # Detect duplicates by content hash (only for files <5MB)
                    if file_size < 5 * 1024 * 1024:
                        file_hash = self.calculate_hash(filepath)
                        if file_hash:
                            self.stats['duplicates'][file_hash].append({
                                'path': str(filepath.relative_to(self.root)),
                                'size': file_size,
                                'name': file
                            })

                except Exception as e:
                    print(f"⚠️  Error processing {filepath}: {e}")

        # Filter duplicates (keep only groups with 2+ files)
        self.stats['duplicates'] = {
            k: v for k, v in self.stats['duplicates'].items() if len(v) > 1
        }

        print(f"✅ Analysis complete!")
        print(f"   Files analyzed: {self.stats['total_files']:,}")
        print(f"   Directories: {self.stats['total_dirs']:,}")
        print(f"   Total size: {self.stats['total_size'] / (1024**3):.2f} GB\n")

    def generate_report(self):
        """Generate comprehensive markdown report"""
        report_path = self.root / "AVATARARTS_DEEP_DIVE_REPORT.md"

        with open(report_path, 'w') as f:
            # Header
            f.write("# AVATARARTS Deep Dive Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Files:** {self.stats['total_files']:,}\n")
            f.write(f"- **Total Directories:** {self.stats['total_dirs']:,}\n")
            f.write(f"- **Total Size:** {self.stats['total_size'] / (1024**3):.2f} GB\n")
            f.write(f"- **Python Scripts:** {len(self.stats['python_scripts']):,}\n")
            f.write(f"- **CSV Files:** {len(self.stats['csv_files']):,}\n")
            f.write(f"- **Markdown Docs:** {len(self.stats['markdown_docs']):,}\n")
            f.write(f"- **JSON Files:** {len(self.stats['json_configs']):,}\n")
            f.write(f"- **Duplicate File Groups:** {len(self.stats['duplicates']):,}\n\n")

            # File Types Breakdown
            f.write("## 📁 File Types Distribution\n\n")
            f.write("| Extension | Count | Percentage |\n")
            f.write("|-----------|------:|----------:|\n")
            for ext, count in self.stats['by_extension'].most_common(30):
                pct = (count / self.stats['total_files']) * 100
                ext_display = ext if ext else "(no extension)"
                f.write(f"| `{ext_display}` | {count:,} | {pct:.1f}% |\n")
            f.write("\n")

            # Largest Directories
            f.write("## 📂 Largest Directories (by file count)\n\n")
            sorted_dirs = sorted(
                self.stats['by_directory'].items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )[:30]

            f.write("| Directory | Files | Size (MB) |\n")
            f.write("|-----------|------:|----------:|\n")
            for dir_name, stats in sorted_dirs:
                size_mb = stats['size'] / (1024 * 1024)
                dir_display = dir_name if dir_name != '.' else '(root)'
                f.write(f"| `{dir_display}` | {stats['count']:,} | {size_mb:.1f} |\n")
            f.write("\n")

            # Duplicate Files
            if self.stats['duplicates']:
                f.write("## 🔄 Duplicate Files (Exact Content Matches)\n\n")
                f.write(f"Found **{len(self.stats['duplicates'])}** groups of duplicate files.\n\n")

                # Calculate potential savings
                total_duplicate_size = 0
                for hash_val, files in self.stats['duplicates'].items():
                    # Keep one, delete others
                    duplicate_size = files[0]['size'] * (len(files) - 1)
                    total_duplicate_size += duplicate_size

                f.write(f"**Potential space savings:** {total_duplicate_size / (1024**2):.1f} MB\n\n")

                # Show top 20 duplicate groups
                sorted_dupes = sorted(
                    self.stats['duplicates'].items(),
                    key=lambda x: x[1][0]['size'] * len(x[1]),
                    reverse=True
                )[:20]

                for i, (hash_val, files) in enumerate(sorted_dupes, 1):
                    f.write(f"### Duplicate Group {i}\n\n")
                    f.write(f"- **File:** `{files[0]['name']}`\n")
                    f.write(f"- **Size:** {files[0]['size'] / 1024:.1f} KB\n")
                    f.write(f"- **Copies:** {len(files)}\n")
                    f.write(f"- **Locations:**\n")
                    for file in files:
                        f.write(f"  - `{file['path']}`\n")
                    f.write("\n")
            else:
                f.write("## 🔄 Duplicate Files\n\n")
                f.write("✅ No exact duplicate files found.\n\n")

            # Large Files
            if self.stats['large_files']:
                f.write("## 💾 Large Files (>10 MB)\n\n")
                sorted_large = sorted(
                    self.stats['large_files'],
                    key=lambda x: x['size'],
                    reverse=True
                )[:50]

                f.write("| File | Size (MB) |\n")
                f.write("|------|----------:|\n")
                for file in sorted_large:
                    f.write(f"| `{file['path']}` | {file['size_mb']:.1f} |\n")
                f.write("\n")

            # Python Scripts Analysis
            f.write("## 🐍 Python Scripts Analysis\n\n")
            f.write(f"Total Python files: **{len(self.stats['python_scripts'])}**\n\n")

            # Find duplicate script names
            script_names = defaultdict(list)
            for script in self.stats['python_scripts']:
                script_names[script['name']].append(script['path'])

            duplicate_scripts = {k: v for k, v in script_names.items() if len(v) > 1}

            if duplicate_scripts:
                f.write(f"### 🔄 Duplicate Script Names: {len(duplicate_scripts)}\n\n")
                for name, paths in sorted(duplicate_scripts.items(), key=lambda x: len(x[1]), reverse=True)[:30]:
                    f.write(f"**`{name}`** ({len(paths)} copies):\n")
                    for path in paths:
                        f.write(f"- `{path}`\n")
                    f.write("\n")

            # CSV Files Analysis
            f.write("## 📊 CSV Files Analysis\n\n")
            f.write(f"Total CSV files: **{len(self.stats['csv_files'])}**\n\n")

            # Group by directory
            csv_by_dir = defaultdict(list)
            for csv in self.stats['csv_files']:
                dir_name = str(Path(csv['path']).parent)
                csv_by_dir[dir_name].append(csv['name'])

            f.write("### CSV Files by Directory (top 20):\n\n")
            sorted_csv_dirs = sorted(csv_by_dir.items(), key=lambda x: len(x[1]), reverse=True)[:20]
            for dir_name, files in sorted_csv_dirs:
                f.write(f"**`{dir_name}`** ({len(files)} files)\n")
                f.write("\n")

            # Markdown Docs Analysis
            f.write("## 📝 Markdown Documentation\n\n")
            f.write(f"Total markdown files: **{len(self.stats['markdown_docs'])}**\n\n")

            # Find readme files
            readme_files = [
                doc for doc in self.stats['markdown_docs']
                if 'readme' in doc['name'].lower() or 'index' in doc['name'].lower()
            ]

            if readme_files:
                f.write(f"### README/Index files ({len(readme_files)}):\n\n")
                for doc in sorted(readme_files, key=lambda x: x['path'])[:50]:
                    f.write(f"- `{doc['path']}`\n")
                f.write("\n")

        print(f"✅ Report generated: {report_path}")
        return report_path

    def generate_action_plan(self):
        """Generate actionable cleanup recommendations"""
        plan_path = self.root / "AVATARARTS_ACTION_PLAN.md"

        with open(plan_path, 'w') as f:
            f.write("# AVATARARTS Cleanup Action Plan\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            f.write("## 🎯 Priorities\n\n")

            # Priority 1: Duplicates
            if self.stats['duplicates']:
                duplicate_size = sum(
                    files[0]['size'] * (len(files) - 1)
                    for files in self.stats['duplicates'].values()
                )
                f.write(f"### Priority 1: Remove Duplicate Files\n")
                f.write(f"- **Impact:** Free up {duplicate_size / (1024**2):.1f} MB\n")
                f.write(f"- **Effort:** Low (automated)\n")
                f.write(f"- **Groups:** {len(self.stats['duplicates'])}\n\n")

            # Priority 2: Consolidate Python scripts
            script_names = defaultdict(list)
            for script in self.stats['python_scripts']:
                script_names[script['name']].append(script)
            duplicate_scripts = {k: v for k, v in script_names.items() if len(v) > 1}

            if duplicate_scripts:
                f.write(f"### Priority 2: Consolidate Duplicate Python Scripts\n")
                f.write(f"- **Impact:** Reduce confusion, improve maintainability\n")
                f.write(f"- **Effort:** Medium (requires review)\n")
                f.write(f"- **Duplicate names:** {len(duplicate_scripts)}\n\n")

            # Priority 3: Organize by project
            f.write(f"### Priority 3: Project Structure Organization\n")
            f.write(f"- **Impact:** Improved navigation and clarity\n")
            f.write(f"- **Effort:** High (manual organization)\n")
            f.write(f"- **Recommendation:** Separate music-empire, marketplace, SEO projects\n\n")

            # Detailed Actions
            f.write("## 📋 Detailed Actions\n\n")

            # Action 1: Cleanup script
            f.write("### Action 1: Run Duplicate Cleanup\n\n")
            f.write("```bash\n")
            f.write("# Review duplicates first\n")
            f.write("python3 analyze_avatararts.py --show-duplicates\n\n")
            f.write("# Then run cleanup (with dry-run)\n")
            f.write("python3 cleanup_avatararts_duplicates.py --dry-run\n\n")
            f.write("# Execute cleanup\n")
            f.write("python3 cleanup_avatararts_duplicates.py\n")
            f.write("```\n\n")

            # Action 2: Consolidate scripts
            f.write("### Action 2: Consolidate Python Scripts\n\n")
            f.write("Review these duplicate script names and consolidate:\n\n")
            for name, scripts in sorted(duplicate_scripts.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
                f.write(f"**`{name}`** - {len(scripts)} copies\n")
            f.write("\n")

            # Action 3: Archive old projects
            f.write("### Action 3: Archive Completed/Inactive Projects\n\n")
            f.write("Consider moving these to `archive/`:\n")
            f.write("- Projects marked 'complete' but not actively developed\n")
            f.write("- Old SEO content from previous campaigns\n")
            f.write("- Deprecated automation scripts\n\n")

        print(f"✅ Action plan generated: {plan_path}")
        return plan_path

    def export_inventory_csv(self):
        """Export file inventory to CSV"""
        csv_path = self.root / "AVATARARTS_INVENTORY.csv"

        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Path', 'Name', 'Size (bytes)', 'Size (MB)', 'Extension'])

            # Python scripts
            for item in sorted(self.stats['python_scripts'], key=lambda x: x['path']):
                writer.writerow([
                    'Python',
                    item['path'],
                    item['name'],
                    item['size'],
                    f"{item['size'] / (1024*1024):.2f}",
                    '.py'
                ])

            # CSV files
            for item in sorted(self.stats['csv_files'], key=lambda x: x['path']):
                writer.writerow([
                    'CSV',
                    item['path'],
                    item['name'],
                    item['size'],
                    f"{item['size'] / (1024*1024):.2f}",
                    '.csv'
                ])

            # Markdown
            for item in sorted(self.stats['markdown_docs'], key=lambda x: x['path']):
                writer.writerow([
                    'Markdown',
                    item['path'],
                    item['name'],
                    item['size'],
                    f"{item['size'] / (1024*1024):.2f}",
                    '.md'
                ])

            # JSON
            for item in sorted(self.stats['json_configs'], key=lambda x: x['path']):
                writer.writerow([
                    'JSON',
                    item['path'],
                    item['name'],
                    item['size'],
                    f"{item['size'] / (1024*1024):.2f}",
                    '.json'
                ])

        print(f"✅ Inventory exported: {csv_path}")
        return csv_path

def main():
    print("=" * 60)
    print("AVATARARTS DEEP DIVE ANALYSIS")
    print("=" * 60)
    print()

    analyzer = AvatarArtsAnalyzer()

    # Run analysis
    analyzer.analyze()

    # Generate reports
    print("\n📝 Generating reports...")
    report_path = analyzer.generate_report()
    plan_path = analyzer.generate_action_plan()
    csv_path = analyzer.export_inventory_csv()

    print("\n" + "=" * 60)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Main Report: {report_path}")
    print(f"📋 Action Plan: {plan_path}")
    print(f"📁 CSV Inventory: {csv_path}")
    print()

if __name__ == "__main__":
    main()
