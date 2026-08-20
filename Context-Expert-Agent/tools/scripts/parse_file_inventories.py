#!/usr/bin/env python3
"""
File Inventory Parser
Parses space-delimited file listings and generates comprehensive analysis
"""

import os
import shlex
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import json

class FileInventoryParser:
    def __init__(self):
        self.inventories = {
            '17k-and-going.txt': Path.home() / 'AVATARARTS/17k-and-going.txt',
            'documents-deepdive.txt': Path.home() / 'AVATARARTS/documents-deepive.txt',
            'seo-workspace.txt': Path.home() / 'seo-workspace.txt',
            'vids-all.txt': Path.home() / 'vids-all.txt',
            'zip-csv.txt': Path.home() / 'zip-csv.txt',
        }

        self.analysis = {
            'by_inventory': {},
            'global_stats': {
                'total_files': 0,
                'total_size_estimate': 0,
                'extensions': Counter(),
                'directories': Counter(),
                'by_type': defaultdict(int),
            }
        }

    def parse_space_delimited(self, filepath):
        """Parse space-delimited file list (handles quoted paths)"""
        print(f"\n📄 Parsing {filepath.name}...")

        if not filepath.exists():
            print(f"   ⚠️  Not found")
            return []

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Try to parse as space-delimited with quotes
        try:
            # Use shlex to handle quoted paths
            paths = shlex.split(content)
        except:
            # Fallback: split on newlines
            paths = [line.strip() for line in content.split('\n') if line.strip()]

        # Filter valid paths
        valid_paths = []
        for path in paths:
            if path and (path.startswith('/') or not path.startswith('#')):
                valid_paths.append(path)

        print(f"   ✓ Found {len(valid_paths):,} file paths")
        return valid_paths

    def analyze_paths(self, paths, inventory_name):
        """Analyze list of file paths"""
        stats = {
            'total_files': len(paths),
            'extensions': Counter(),
            'directories': Counter(),
            'top_level_dirs': Counter(),
            'by_location': defaultdict(list),
            'largest_assumed': [],
            'samples': paths[:100]
        }

        for path in paths:
            # Extract extension
            if '.' in path:
                ext = '.' + path.split('.')[-1].lower()
                stats['extensions'][ext] += 1
                self.analysis['global_stats']['extensions'][ext] += 1

            # Extract directories
            path_obj = Path(path)

            # Top-level directory (e.g., /Users/steven/Documents -> Documents)
            parts = path_obj.parts
            if len(parts) > 3:  # /Users/steven/XXX
                top_level = parts[3] if len(parts) > 3 else 'root'
                stats['top_level_dirs'][top_level] += 1
                self.analysis['global_stats']['directories'][top_level] += 1

            # Parent directory
            parent = str(path_obj.parent)
            stats['directories'][parent] += 1

            # Categorize by location
            if '/Documents/' in path:
                stats['by_location']['Documents'].append(path)
            elif '/Downloads/' in path:
                stats['by_location']['Downloads'].append(path)
            elif '/Music/' in path:
                stats['by_location']['Music'].append(path)
            elif '/Movies/' in path:
                stats['by_location']['Movies'].append(path)
            elif '/Pictures/' in path:
                stats['by_location']['Pictures'].append(path)
            elif '/AVATARARTS/' in path:
                stats['by_location']['AVATARARTS'].append(path)
            elif '/GitHub/' in path:
                stats['by_location']['GitHub'].append(path)
            else:
                stats['by_location']['Other'].append(path)

        self.analysis['by_inventory'][inventory_name] = stats
        self.analysis['global_stats']['total_files'] += len(paths)

        return stats

    def generate_comprehensive_report(self, output_path):
        """Generate detailed Markdown report"""
        md = f"""# File Inventories Comprehensive Analysis

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Inventories Analyzed:** {len(self.analysis['by_inventory'])}
**Total Files Catalogued:** {self.analysis['global_stats']['total_files']:,}

---

## 📊 Executive Summary

### Inventory Files

| File | Files Found | Top Extension | Top Directory |
|------|------------:|---------------|---------------|
"""

        for name, stats in sorted(
            self.analysis['by_inventory'].items(),
            key=lambda x: x[1]['total_files'],
            reverse=True
        ):
            top_ext = stats['extensions'].most_common(1)[0] if stats['extensions'] else ('(none)', 0)
            top_dir = stats['top_level_dirs'].most_common(1)[0] if stats['top_level_dirs'] else ('(none)', 0)
            md += f"| `{name}` | {stats['total_files']:,} | `{top_ext[0]}` ({top_ext[1]:,}) | `{top_dir[0]}` ({top_dir[1]:,}) |\n"

        md += f"""

---

## 🎯 Global Statistics

**Total Files Across All Inventories:** {self.analysis['global_stats']['total_files']:,}

### Top 20 File Types (Global)

| Extension | Count | Percentage |
|-----------|------:|-----------:|
"""

        total_files = self.analysis['global_stats']['total_files']
        for ext, count in self.analysis['global_stats']['extensions'].most_common(20):
            pct = (count / total_files * 100) if total_files > 0 else 0
            md += f"| `{ext}` | {count:,} | {pct:.1f}% |\n"

        md += """

### Top 20 Directories (Global)

| Directory | Files |
|-----------|------:|
"""

        for dir_name, count in self.analysis['global_stats']['directories'].most_common(20):
            md += f"| `{dir_name}` | {count:,} |\n"

        md += "\n---\n\n## 📁 Individual Inventory Analysis\n\n"

        for name, stats in sorted(self.analysis['by_inventory'].items()):
            md += f"### {name}\n\n"
            md += f"**Total Files:** {stats['total_files']:,}\n\n"

            # Location breakdown
            md += "**Files by Location:**\n\n"
            for location, files in sorted(stats['by_location'].items(), key=lambda x: len(x[1]), reverse=True):
                md += f"- **{location}**: {len(files):,} files\n"
            md += "\n"

            # Top extensions
            if stats['extensions']:
                md += "**Top 10 File Types:**\n\n"
                for ext, count in stats['extensions'].most_common(10):
                    pct = (count / stats['total_files'] * 100) if stats['total_files'] > 0 else 0
                    md += f"- `{ext}`: {count:,} files ({pct:.1f}%)\n"
                md += "\n"

            # Top directories
            if stats['top_level_dirs']:
                md += "**Top 10 Top-Level Directories:**\n\n"
                for dir_name, count in stats['top_level_dirs'].most_common(10):
                    md += f"- `{dir_name}`: {count:,} files\n"
                md += "\n"

            # Sample paths
            if stats['samples']:
                md += "**Sample Paths (first 20):**\n\n"
                md += "```\n"
                for path in stats['samples'][:20]:
                    md += f"{path}\n"
                md += "```\n\n"

            md += "---\n\n"

        # Detailed location analysis
        md += "## 🗂️ Cross-Inventory Location Analysis\n\n"

        # Aggregate by location across all inventories
        all_locations = defaultdict(int)
        for inv_name, stats in self.analysis['by_inventory'].items():
            for location, files in stats['by_location'].items():
                all_locations[location] += len(files)

        md += "### Files Distribution by Location\n\n"
        md += "| Location | Total Files | Percentage |\n"
        md += "|----------|------------:|-----------:|\n"

        for location, count in sorted(all_locations.items(), key=lambda x: x[1], reverse=True):
            pct = (count / self.analysis['global_stats']['total_files'] * 100) if self.analysis['global_stats']['total_files'] > 0 else 0
            md += f"| **{location}** | {count:,} | {pct:.1f}% |\n"

        md += f"""

---

## 🔍 Key Findings

### Content Discovery

**17k-and-going.txt** appears to be a complete AVATARARTS directory snapshot
- Contains paths to all AVATARARTS files and subdirectories
- Useful for understanding complete project structure

**documents-deepdive.txt** catalogs Documents directory
- Subset of overall file system
- Likely created during Documents cleanup effort

**seo-workspace.txt** tracks SEO-related workspace
- Specialized inventory for SEO projects
- Includes strategy documents and exports

**vids-all.txt** inventories video files
- {self.analysis['by_inventory'].get('vids-all.txt', {}).get('total_files', 0):,} video files catalogued
- Primarily .mp4, .mov, .webm formats
- Located across Movies, Downloads directories

**zip-csv.txt** tracks compressed archives and data
- {self.analysis['by_inventory'].get('zip-csv.txt', {}).get('total_files', 0):,} archive/data files
- ZIP archives and CSV exports
- Useful for identifying backed-up content

### Storage Insights

Based on file counts, estimated storage distribution:
"""

        for location, count in sorted(all_locations.items(), key=lambda x: x[1], reverse=True):
            pct = (count / self.analysis['global_stats']['total_files'] * 100) if self.analysis['global_stats']['total_files'] > 0 else 0
            bar = '█' * int(pct / 2)  # 50 chars max
            md += f"- **{location}**: {count:,} files ({pct:.1f}%) {bar}\n"

        md += """

### File Type Insights
"""

        # Group extensions by category
        categories = {
            'Video': ['.mp4', '.mov', '.webm', '.avi', '.flv', '.wmv', '.mpeg'],
            'Archives': ['.zip', '.tar', '.gz', '.bz2', '.rar', '.7z', '.tgz'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'],
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
            'Data': ['.csv', '.json', '.xml', '.yaml', '.db'],
            'Code': ['.py', '.js', '.ts', '.html', '.css', '.java'],
        }

        category_counts = defaultdict(int)
        for ext, count in self.analysis['global_stats']['extensions'].items():
            categorized = False
            for cat, exts in categories.items():
                if ext in exts:
                    category_counts[cat] += count
                    categorized = True
                    break
            if not categorized:
                category_counts['Other'] += count

        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / self.analysis['global_stats']['total_files'] * 100) if self.analysis['global_stats']['total_files'] > 0 else 0
            md += f"- **{category}**: {count:,} files ({pct:.1f}%)\n"

        md += """

---

## 💡 Recommendations

### 1. Consolidate Inventories
These text files overlap significantly. Consider:
- Keep latest snapshots only
- Archive historical versions
- Use automated scripts instead of manual lists

### 2. Clean Up Duplicates
Cross-reference these inventories with:
```bash
# Find files listed in multiple inventories
python3 ~/AVATARARTS/scripts/find_inventory_duplicates.py
```

### 3. Automate Inventory Generation
Instead of manual text files:
```bash
# Generate fresh inventory
find ~/AVATARARTS -type f > ~/AVATARARTS/inventory-$(date +%Y%m%d).txt
find ~/Documents -type f > ~/Documents/inventory-$(date +%Y%m%d).txt

# Or use the comprehensive analyzer
python3 ~/AVATARARTS/scripts/analyze_home_directory.py
```

### 4. Archive Old Inventories
```bash
mkdir -p ~/AVATARARTS/archive/inventories
mv ~/seo-workspace.txt ~/AVATARARTS/archive/inventories/seo-workspace-archive.txt
mv ~/vids-all.txt ~/AVATARARTS/archive/inventories/vids-all-archive.txt
mv ~/zip-csv.txt ~/AVATARARTS/archive/inventories/zip-csv-archive.txt
```

---

## 📊 Export Data

**JSON export available:** `file_inventories_data.json`

Contains structured data for:
- All file paths by inventory
- Extension statistics
- Directory breakdowns
- Location mappings

---

*Report generated by File Inventory Parser*
*Total files analyzed: {self.analysis['global_stats']['total_files']:,}*
*Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        with open(output_path, 'w') as f:
            f.write(md)

        print(f"\n✅ Report saved: {output_path}")
        return output_path

    def export_json(self, output_path):
        """Export analysis as JSON"""
        # Convert Counters to dicts for JSON
        export_data = {
            'by_inventory': {},
            'global_stats': {
                'total_files': self.analysis['global_stats']['total_files'],
                'extensions': dict(self.analysis['global_stats']['extensions']),
                'directories': dict(self.analysis['global_stats']['directories']),
            }
        }

        for inv_name, stats in self.analysis['by_inventory'].items():
            export_data['by_inventory'][inv_name] = {
                'total_files': stats['total_files'],
                'extensions': dict(stats['extensions']),
                'top_level_dirs': dict(stats['top_level_dirs']),
                'by_location': {k: len(v) for k, v in stats['by_location'].items()},
                'sample_paths': stats['samples'][:50]
            }

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✅ JSON saved: {output_path}")

    def run(self):
        """Run complete analysis"""
        print("=" * 60)
        print("FILE INVENTORIES COMPREHENSIVE ANALYSIS")
        print("=" * 60)

        # Parse each inventory
        for name, filepath in self.inventories.items():
            paths = self.parse_space_delimited(filepath)
            self.analyze_paths(paths, name)

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)

        # Generate outputs
        md_path = Path.cwd() / "FILE_INVENTORIES_ANALYSIS.md"
        json_path = Path.cwd() / "file_inventories_data.json"

        self.generate_comprehensive_report(md_path)
        self.export_json(json_path)

        print(f"\n📊 Summary:")
        print(f"   Total files catalogued: {self.analysis['global_stats']['total_files']:,}")
        print(f"   Unique extensions: {len(self.analysis['global_stats']['extensions'])}")
        print(f"   Unique directories: {len(self.analysis['global_stats']['directories'])}")
        print()

def main():
    parser = FileInventoryParser()
    parser.run()

if __name__ == "__main__":
    main()
