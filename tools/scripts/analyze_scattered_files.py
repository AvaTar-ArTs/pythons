#!/usr/bin/env python3
"""
Scattered Files Deep Analyzer
Analyzes large text inventory files across the system
"""

import os
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class ScatteredFilesAnalyzer:
    def __init__(self):
        self.files_to_analyze = [
            Path.home() / 'seo-workspace.txt',
            Path.home() / 'vids-all.txt',
            Path.home() / 'zip-csv.txt',
            Path.home() / 'AVATARARTS/17k-and-going.txt',
            Path.home() / 'AVATARARTS/documents-deepive.txt',
        ]

        self.analysis = {
            'files': {},
            'total_entries': 0,
            'by_type': Counter(),
            'by_location': defaultdict(int),
            'extensions': Counter(),
            'large_files': [],
            'duplicates': defaultdict(list),
        }

    def analyze_file_list(self, filepath):
        """Analyze a text file containing file listings"""
        print(f"\n📄 Analyzing {filepath.name}...")

        if not filepath.exists():
            print(f"   ⚠️  File not found: {filepath}")
            return None

        file_size = filepath.stat().st_size
        print(f"   Size: {file_size / (1024**2):.2f} MB")

        entries = []
        patterns = {
            'absolute_path': re.compile(r'^(/[^\s]+)'),
            'relative_path': re.compile(r'^([^\s/][^\s]+)'),
            'ls_output': re.compile(r'^\S+\s+\S+\s+\S+\s+\S+\s+(.+)'),
        }

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Try to extract file path
                file_path = None

                # Check for absolute path
                match = patterns['absolute_path'].match(line)
                if match:
                    file_path = match.group(1)
                # Check for relative path
                elif patterns['relative_path'].match(line):
                    file_path = line.split()[0] if ' ' in line else line
                # Check for ls -l format
                else:
                    match = patterns['ls_output'].match(line)
                    if match:
                        file_path = match.group(1)

                if file_path:
                    entries.append({
                        'path': file_path,
                        'line_num': line_num,
                        'raw': line
                    })

        # Analyze entries
        result = {
            'filepath': str(filepath),
            'size_bytes': file_size,
            'size_mb': file_size / (1024**2),
            'total_entries': len(entries),
            'extensions': Counter(),
            'directories': Counter(),
            'sample_entries': entries[:50]
        }

        for entry in entries:
            path = entry['path']

            # Extract extension
            if '.' in path:
                ext = '.' + path.split('.')[-1].lower()
                result['extensions'][ext] += 1
                self.analysis['extensions'][ext] += 1

            # Extract directory
            if '/' in path:
                parts = path.split('/')
                if len(parts) > 1:
                    # Get top-level directory
                    top_dir = parts[0] if parts[0] else (parts[1] if len(parts) > 1 else 'unknown')
                    result['directories'][top_dir] += 1
                    self.analysis['by_location'][top_dir] += 1

        self.analysis['files'][filepath.name] = result
        self.analysis['total_entries'] += len(entries)

        print(f"   ✓ Found {len(entries):,} file entries")
        print(f"   ✓ {len(result['extensions'])} unique file types")
        print(f"   ✓ {len(result['directories'])} unique directories")

        return result

    def find_scattered_txt_files(self):
        """Find all .txt files in home directory"""
        print("\n🔍 Finding scattered .txt files in ~/...")

        txt_files = []
        ignore_dirs = {'.git', 'node_modules', '.venv', '__pycache__', 'Library'}

        for root, dirs, files in os.walk(Path.home()):
            # Remove ignored directories from search
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            # Limit depth
            depth = root.count(os.sep) - str(Path.home()).count(os.sep)
            if depth > 3:
                continue

            for file in files:
                if file.endswith('.txt') and not file.startswith('.'):
                    filepath = Path(root) / file
                    try:
                        size = filepath.stat().st_size
                        if size > 1024:  # Only files > 1KB
                            txt_files.append({
                                'path': str(filepath.relative_to(Path.home())),
                                'size': size,
                                'modified': filepath.stat().st_mtime
                            })
                    except:
                        pass

        # Sort by size
        txt_files.sort(key=lambda x: x['size'], reverse=True)

        self.analysis['scattered_txt_files'] = txt_files[:100]  # Top 100

        print(f"   ✓ Found {len(txt_files):,} .txt files > 1KB")
        print(f"   ✓ Top 100 by size catalogued")

        return txt_files

    def generate_markdown_report(self, output_path):
        """Generate comprehensive Markdown report"""
        md = f"""# Scattered Files Deep Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Files Analyzed:** {len(self.analysis['files'])}
**Total Entries Found:** {self.analysis['total_entries']:,}

---

## 📊 Overview

| Inventory File | Size (MB) | Entries | Extensions | Directories |
|----------------|----------:|--------:|-----------:|------------:|
"""

        for filename, data in sorted(
            self.analysis['files'].items(),
            key=lambda x: x[1]['size_mb'],
            reverse=True
        ):
            md += f"| `{filename}` | {data['size_mb']:.2f} | {data['total_entries']:,} | {len(data['extensions'])} | {len(data['directories'])} |\n"

        md += f"""

**Total files catalogued across all inventories:** {self.analysis['total_entries']:,}

---

## 📁 File Type Distribution

### Top 30 Extensions Across All Inventories

| Extension | Count | Percentage |
|-----------|------:|-----------:|
"""

        total = sum(self.analysis['extensions'].values())
        for ext, count in self.analysis['extensions'].most_common(30):
            pct = (count / total * 100) if total > 0 else 0
            md += f"| `{ext}` | {count:,} | {pct:.1f}% |\n"

        md += """

---

## 📂 Location Analysis

### Top Directories Referenced

| Directory | Files Referenced |
|-----------|----------------:|
"""

        for location, count in sorted(
            self.analysis['by_location'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:30]:
            md += f"| `{location}` | {count:,} |\n"

        md += "\n---\n\n## 📄 Individual File Analysis\n\n"

        for filename, data in sorted(self.analysis['files'].items()):
            md += f"### {filename}\n\n"
            md += f"**Size:** {data['size_mb']:.2f} MB\n"
            md += f"**Total Entries:** {data['total_entries']:,}\n\n"

            if data['extensions']:
                md += "**Top 10 File Types:**\n\n"
                for ext, count in data['extensions'].most_common(10):
                    md += f"- `{ext}`: {count:,} files\n"
                md += "\n"

            if data['directories']:
                md += "**Top 10 Directories:**\n\n"
                for dir_name, count in data['directories'].most_common(10):
                    md += f"- `{dir_name}`: {count:,} files\n"
                md += "\n"

            if data['sample_entries']:
                md += "**Sample Entries (first 10):**\n\n"
                md += "```\n"
                for entry in data['sample_entries'][:10]:
                    md += f"{entry['path']}\n"
                md += "```\n\n"

            md += "---\n\n"

        # Add scattered txt files
        if self.analysis.get('scattered_txt_files'):
            md += "## 📝 Scattered .txt Files Found\n\n"
            md += "**Top 50 .txt files by size:**\n\n"
            md += "| File | Size (MB) | Location |\n"
            md += "|------|----------:|---------|\n"

            for file_info in self.analysis['scattered_txt_files'][:50]:
                size_mb = file_info['size'] / (1024**2)
                md += f"| `{Path(file_info['path']).name}` | {size_mb:.2f} | `{file_info['path']}` |\n"

        md += f"""

---

## 🎯 Key Findings

### Inventory Summary
- **seo-workspace.txt**: SEO and workspace files catalog
- **vids-all.txt**: Video file inventory (1,366 entries)
- **zip-csv.txt**: ZIP and CSV file listing (485 entries)
- **17k-and-going.txt**: Massive file catalog (~17,000+ files)
- **documents-deepdive.txt**: Documents directory analysis

### Most Common File Types
"""

        for ext, count in self.analysis['extensions'].most_common(10):
            md += f"- **{ext}**: {count:,} files\n"

        md += f"""

### Storage Implications
- Total files catalogued: {self.analysis['total_entries']:,}
- Inventory files total size: {sum(d['size_mb'] for d in self.analysis['files'].values()):.2f} MB
- Additional .txt files found: {len(self.analysis.get('scattered_txt_files', [])):,}

### Recommendations
1. **Consolidate Inventories**: Merge overlapping catalogs into single source of truth
2. **Clean Up Duplicates**: Cross-reference file lists to identify duplicates
3. **Archive Old Inventories**: Move historical snapshots to archive/
4. **Automate Scanning**: Use analyze scripts instead of manual text file inventories

---

## 🔧 Actions Available

### Re-scan Current State
```bash
# Re-generate file inventories
find ~/AVATARARTS -type f > ~/AVATARARTS/current-inventory-$(date +%Y%m%d).txt
find ~/Documents -type f > ~/Documents/documents-inventory-$(date +%Y%m%d).txt
find ~/Music -type f > ~/Music/music-inventory-$(date +%Y%m%d).txt
```

### Compare Inventories
```bash
# Find files in old inventory but not in new
comm -23 <(sort old-inventory.txt) <(sort new-inventory.txt) > removed-files.txt

# Find files in new but not old
comm -13 <(sort old-inventory.txt) <(sort new-inventory.txt) > added-files.txt
```

### Clean Up
```bash
# Archive old inventory files
mkdir -p ~/AVATARARTS/archive/inventories
mv ~/seo-workspace.txt ~/AVATARARTS/archive/inventories/
mv ~/vids-all.txt ~/AVATARARTS/archive/inventories/
mv ~/zip-csv.txt ~/AVATARARTS/archive/inventories/
```

---

*Report generated by Scattered Files Analyzer*
*Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        with open(output_path, 'w') as f:
            f.write(md)

        print(f"\n✅ Report saved to: {output_path}")
        return output_path

    def run_full_analysis(self):
        """Run complete scattered files analysis"""
        print("=" * 60)
        print("SCATTERED FILES DEEP ANALYSIS")
        print("=" * 60)

        # Analyze each inventory file
        for filepath in self.files_to_analyze:
            self.analyze_file_list(filepath)

        # Find additional scattered files
        self.find_scattered_txt_files()

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)

        # Generate report
        output_path = Path.cwd() / "SCATTERED_FILES_ANALYSIS.md"
        self.generate_markdown_report(output_path)

        print(f"\n📊 Summary:")
        print(f"   Inventory files analyzed: {len(self.analysis['files'])}")
        print(f"   Total entries catalogued: {self.analysis['total_entries']:,}")
        print(f"   Unique file types: {len(self.analysis['extensions'])}")
        print(f"   Scattered .txt files found: {len(self.analysis.get('scattered_txt_files', []))}")
        print()

def main():
    analyzer = ScatteredFilesAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
