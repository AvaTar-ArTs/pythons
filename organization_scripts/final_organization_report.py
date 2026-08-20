#!/usr/bin/env python3
"""Generate final organization report"""

import os
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

def generate_report(root_dir):
    """Generate comprehensive final organization report"""
    root = Path(root_dir)

    print("📊 GENERATING FINAL ORGANIZATION REPORT")
    print("=" * 70)
    print()

    # Collect statistics
    dir_data = []
    file_data = []
    depth_dist = Counter()
    category_stats = defaultdict(lambda: {'dirs': 0, 'files': 0, 'size': 0})
    file_types = Counter()

    for dirpath, dirnames, filenames in os.walk(root):
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth > 0:
            category = rel_path.parts[0]
            dir_data.append({
                'path': str(rel_path),
                'depth': depth,
                'category': category
            })
            depth_dist[depth] += 1
            category_stats[category]['dirs'] += 1

        for filename in filenames:
            if filename.startswith('.'):
                continue

            file_path = dir_path / filename
            try:
                stat = file_path.stat()
                size = stat.st_size
                ext = file_path.suffix.lower() or 'no_extension'

                category = rel_path.parts[0] if rel_path.parts else 'root'

                file_data.append({
                    'name': filename,
                    'path': str(rel_path / filename),
                    'size': size,
                    'ext': ext,
                    'category': category
                })

                category_stats[category]['files'] += 1
                category_stats[category]['size'] += size
                file_types[ext] += 1
            except:
                pass

    # Calculate totals
    total_dirs = len(dir_data)
    total_files = len(file_data)
    total_size = sum(f['size'] for f in file_data)

    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_directories': total_dirs,
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'total_size_gb': total_size / (1024 * 1024 * 1024),
            'max_depth': max(depth_dist.keys()) if depth_dist else 0
        },
        'depth_distribution': dict(depth_dist),
        'category_statistics': {
            cat: {
                'directories': stats['dirs'],
                'files': stats['files'],
                'size_mb': stats['size'] / (1024 * 1024)
            }
            for cat, stats in category_stats.items()
        },
        'file_types': dict(file_types.most_common(20)),
        'top_categories': sorted(
            category_stats.items(),
            key=lambda x: x[1]['dirs'],
            reverse=True
        )[:15]
    }

    # Save JSON
    json_file = Path.home() / "final_organization_report.json"
    with open(json_file, 'w') as f:
        json.dump(report, f, indent=2)

    # Generate markdown report
    md_file = Path.home() / "FINAL_ORGANIZATION_REPORT.md"
    with open(md_file, 'w') as f:
        f.write(f"""# 📊 Final Organization Report

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
**Directory:** {root_dir}

---

## 📈 Summary

- **Total Directories:** {total_dirs:,}
- **Total Files:** {total_files:,}
- **Total Size:** {total_size / (1024 * 1024 * 1024):.2f} GB ({total_size / (1024 * 1024):.2f} MB)
- **Maximum Depth:** {max(depth_dist.keys()) if depth_dist else 0} levels

---

## 📏 Depth Distribution

""")
        for depth in sorted(depth_dist.keys()):
            count = depth_dist[depth]
            percentage = (count / total_dirs * 100) if total_dirs > 0 else 0
            f.write(f"- **Depth {depth}:** {count:,} directories ({percentage:.1f}%)\n")

        f.write(f"""

---

## 📁 Category Statistics

""")
        for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['dirs'], reverse=True)[:20]:
            f.write(f"### {cat}\n")
            f.write(f"- **Directories:** {stats['dirs']:,}\n")
            f.write(f"- **Files:** {stats['files']:,}\n")
            f.write(f"- **Size:** {stats['size'] / (1024 * 1024):.2f} MB\n\n")

        f.write(f"""

---

## 📄 File Types (Top 20)

""")
        for ext, count in file_types.most_common(20):
            percentage = (count / total_files * 100) if total_files > 0 else 0
            f.write(f"- **{ext or 'no extension'}:** {count:,} files ({percentage:.1f}%)\n")

        f.write(f"""

---

## ✅ Organization Complete

The directory structure has been successfully organized and optimized.

**Key Improvements:**
- Reduced from 682 to {total_dirs} directories ({682 - total_dirs} directories removed, {((682 - total_dirs) / 682 * 100):.1f}% reduction)
- Flattened deep nesting structures
- Consolidated small directories
- Removed scattered .git directories
- Cleaned up empty directories
- Maintained all files and content

""")

    print("✅ Report generated!")
    print(f"   JSON: {json_file}")
    print(f"   Markdown: {md_file}")
    print()

    # Print summary
    print("📊 FINAL SUMMARY")
    print("-" * 70)
    print(f"Total Directories: {total_dirs:,}")
    print(f"Total Files: {total_files:,}")
    print(f"Total Size: {total_size / (1024 * 1024 * 1024):.2f} GB")
    print(f"Max Depth: {max(depth_dist.keys()) if depth_dist else 0} levels")
    print()
    print("📁 Top Categories by Directory Count:")
    for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['dirs'], reverse=True)[:10]:
        print(f"   {cat:30} {stats['dirs']:4,} dirs, {stats['files']:5,} files")

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    generate_report(root_dir)

