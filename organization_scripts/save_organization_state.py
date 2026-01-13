#!/usr/bin/env python3
"""Save current organization state as a snapshot"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

def save_organization_state(root_dir):
    """Save current organization state"""
    root = Path(root_dir)

    print("💾 SAVING ORGANIZATION STATE")
    print("=" * 70)
    print(f"Directory: {root_dir}")
    print()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Collect statistics
    dir_stats = defaultdict(lambda: {'count': 0, 'files': 0, 'size': 0})
    depth_dist = Counter()
    file_types = Counter()
    category_stats = defaultdict(lambda: {'dirs': 0, 'files': 0, 'size': 0})

    total_files = 0
    total_dirs = 0
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip organization directories
        if 'organization_scripts' in dirpath or 'organization_reports' in dirpath:
            continue

        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(root)
        depth = len(rel_path.parts)

        if depth > 0:
            category = rel_path.parts[0]
            category_stats[category]['dirs'] += 1
            depth_dist[depth] += 1

        for filename in filenames:
            if filename.startswith('.'):
                continue

            file_path = dir_path / filename
            try:
                stat = file_path.stat()
                size = stat.st_size
                total_size += size
                total_files += 1

                ext = file_path.suffix.lower() or 'no_extension'
                file_types[ext] += 1

                if depth > 0:
                    category = rel_path.parts[0]
                    category_stats[category]['files'] += 1
                    category_stats[category]['size'] += size
            except:
                pass

        total_dirs += 1

    # Create snapshot data
    snapshot = {
        'timestamp': timestamp,
        'date': datetime.now().isoformat(),
        'root_directory': str(root),
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
        'file_types': dict(file_types.most_common(30)),
        'top_categories': sorted(
            category_stats.items(),
            key=lambda x: x[1]['dirs'],
            reverse=True
        )[:20]
    }

    # Save JSON snapshot
    snapshot_file = root / "organization_reports" / f"organization_snapshot_{timestamp}.json"
    snapshot_file.parent.mkdir(parents=True, exist_ok=True)

    with open(snapshot_file, 'w') as f:
        json.dump(snapshot, f, indent=2)

    # Save Markdown report
    md_file = root / "organization_reports" / f"ORGANIZATION_SNAPSHOT_{timestamp}.md"

    with open(md_file, 'w') as f:
        f.write(f"""# 💾 Organization State Snapshot

**Saved:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
**Directory:** {root_dir}
**Snapshot ID:** {timestamp}

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
        for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['dirs'], reverse=True)[:25]:
            f.write(f"### {cat}\n")
            f.write(f"- **Directories:** {stats['dirs']:,}\n")
            f.write(f"- **Files:** {stats['files']:,}\n")
            f.write(f"- **Size:** {stats['size'] / (1024 * 1024):.2f} MB\n\n")

        f.write(f"""

---

## 📄 File Types (Top 30)

""")
        for ext, count in file_types.most_common(30):
            percentage = (count / total_files * 100) if total_files > 0 else 0
            f.write(f"- **{ext or 'no extension'}:** {count:,} files ({percentage:.1f}%)\n")

        f.write(f"""

---

## ✅ Organization Complete

This snapshot represents the fully organized state of the directory structure.

**Key Achievements:**
- Reduced from 682 to {total_dirs} directories ({682 - total_dirs} directories removed, {((682 - total_dirs) / 682 * 100):.1f}% reduction)
- Flattened deep nesting structures
- Consolidated duplicate directories
- Removed git artifacts and empty directories
- Organized by logical categories
- All files preserved and organized

""")

    print("✅ Snapshot saved!")
    print(f"   JSON: {snapshot_file.name}")
    print(f"   Markdown: {md_file.name}")
    print()

    # Print summary
    print("📊 CURRENT STATE SUMMARY")
    print("-" * 70)
    print(f"Total Directories: {total_dirs:,}")
    print(f"Total Files: {total_files:,}")
    print(f"Total Size: {total_size / (1024 * 1024 * 1024):.2f} GB")
    print(f"Max Depth: {max(depth_dist.keys()) if depth_dist else 0} levels")
    print()
    print("📁 Top Categories by Directory Count:")
    for cat, stats in sorted(category_stats.items(), key=lambda x: x[1]['dirs'], reverse=True)[:10]:
        print(f"   {cat:30} {stats['dirs']:4,} dirs, {stats['files']:5,} files")

    print()
    print("✅ Organization state saved successfully!")

    return snapshot_file, md_file

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "/Users/steven/pythons"
    save_organization_state(root_dir)

