#!/usr/bin/env python3
"""
Merge conflicting numbered directories into existing directories
01_TOOLS → TOOLS, 02_DOCUMENTATION → DOCUMENTATION, 05_DATA → DATA
"""

import os
import shutil
from pathlib import Path
import hashlib

def get_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return None

def merge_directories(source_dir, target_dir, dry_run=True):
    """Merge source directory into target directory"""
    source = Path(source_dir)
    target = Path(target_dir)

    if not source.exists():
        print(f"⚠️  Source does not exist: {source}")
        return {'copied': 0, 'skipped': 0, 'versioned': 0, 'errors': 0}

    if not target.exists():
        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created target: {target}")

    stats = {'copied': 0, 'skipped': 0, 'versioned': 0, 'errors': 0}

    # Walk through source
    for root, dirs, files in os.walk(source):
        src_path = Path(root)
        rel_path = src_path.relative_to(source)
        dst_dir = target / rel_path

        # Skip .git and __pycache__
        if '.git' in rel_path.parts or '__pycache__' in rel_path.parts:
            continue

        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__')]

        if not dry_run:
            dst_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            if file.startswith('.'):
                continue

            src_file = src_path / file
            dst_file = dst_dir / file

            try:
                if dst_file.exists():
                    # Check if identical
                    src_hash = get_file_hash(src_file)
                    dst_hash = get_file_hash(dst_file)

                    if src_hash and dst_hash and src_hash == dst_hash:
                        stats['skipped'] += 1
                        continue
                    else:
                        # Version the file
                        base = file.rsplit('.', 1)
                        if len(base) == 2:
                            name, ext = base
                            versioned = f"{name}_from_{source.name}.{ext}"
                        else:
                            versioned = f"{file}_from_{source.name}"
                        dst_file = dst_dir / versioned
                        stats['versioned'] += 1
                        if stats['versioned'] <= 3:
                            print(f"  📝 Versioned: {rel_path / file} → {versioned}")
                else:
                    stats['copied'] += 1
                    if stats['copied'] <= 5:
                        print(f"  ✅ Copy: {rel_path / file}")

                if not dry_run:
                    shutil.copy2(src_file, dst_file)
            except Exception as e:
                stats['errors'] += 1
                if stats['errors'] <= 3:
                    print(f"  ❌ Error: {file}: {e}")

    return stats

def merge_conflicts(root_dir, dry_run=True):
    """Merge conflicting directories"""
    root = Path(root_dir)

    conflicts = [
        ('01_TOOLS', 'TOOLS'),
        ('02_DOCUMENTATION', 'DOCUMENTATION'),
        ('05_DATA', 'DATA'),
    ]

    print(f"\n🔄 Merging conflicting directories")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 70)

    total_stats = {'copied': 0, 'skipped': 0, 'versioned': 0, 'errors': 0}

    for source_name, target_name in conflicts:
        source = root / source_name
        target = root / target_name

        if not source.exists():
            print(f"\n⚠️  {source_name} does not exist, skipping")
            continue

        print(f"\n📁 {source_name} → {target_name}")
        stats = merge_directories(source, target, dry_run=dry_run)

        for key in total_stats:
            total_stats[key] += stats[key]

        print(f"   Copied: {stats['copied']}, Skipped: {stats['skipped']}, "
              f"Versioned: {stats['versioned']}, Errors: {stats['errors']}")

    print("\n" + "=" * 70)
    print("📊 TOTAL SUMMARY:")
    print(f"   Files copied:     {total_stats['copied']}")
    print(f"   Files skipped:    {total_stats['skipped']}")
    print(f"   Files versioned:  {total_stats['versioned']}")
    print(f"   Errors:           {total_stats['errors']}")
    print("=" * 70)

    return total_stats

if __name__ == "__main__":
    import sys

    target_dir = "/Users/steven/pythons"
    dry_run = "--execute" not in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print("   Pass --execute to perform actual merge\n")
    else:
        print("⚠️  LIVE MODE - Files will be copied!")
        print("   Executing merge...\n")

    stats = merge_conflicts(target_dir, dry_run=dry_run)

    if dry_run:
        print("\n💡 Run with --execute to perform the actual merge")
    else:
        print("\n✅ Merge complete!")
        print("\n💡 After verification, you can remove the numbered directories:")
        print("   rm -rf ~/pythons/01_TOOLS")
        print("   rm -rf ~/pythons/02_DOCUMENTATION")
        print("   rm -rf ~/pythons/05_DATA")

