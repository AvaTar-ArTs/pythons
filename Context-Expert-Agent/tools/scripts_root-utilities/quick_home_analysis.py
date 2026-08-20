#!/usr/bin/env python3
"""Quick Home Directory Analysis"""
import subprocess
from pathlib import Path
from datetime import datetime

def quick_count(path, pattern):
    """Quick file count"""
    try:
        result = subprocess.run(
            ['find', path, '-name', pattern, '-type', 'f'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=30
        )
        if result.stdout.strip():
            return len(result.stdout.strip().split('\n'))
    except:
        pass
    return 0

def get_size(path):
    """Get directory size"""
    try:
        result = subprocess.run(
            ['du', '-sh', path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.split()[0]
    except:
        pass
    return "?"

home = Path.home()

# Key directories
dirs = {
    'AVATARARTS': home / 'AVATARARTS',
    'GitHub': home / 'GitHub',
    'pythons': home / 'pythons',
    'pythons-sort': home / 'pythons-sort',
    'Documents': home / 'Documents',
    'Downloads': home / 'Downloads',
    'Pictures': home / 'Pictures',
    'Music': home / 'Music',
    'Movies': home / 'Movies',
    'Library': home / 'Library',
    '.env.d': home / '.env.d',
    'claude-Convos': home / 'claude-Convos'
}

print("="* 90)
print("QUICK HOME DIRECTORY ANALYSIS")
print("="* 90)
print(f"Home: {home}")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print(f"{'Directory':<20} {'Size':>10} {'Python':>8} {'CSV':>8} {'JSON':>8} {'DB':>8} {'Images':>8}")
print("-" * 90)

total_py = 0
total_csv = 0
total_json = 0
total_db = 0
total_img = 0

for name, path in dirs.items():
    if not path.exists():
        continue

    print(f"{name:<20}", end='')

    size = get_size(str(path))
    print(f" {size:>10}", end='')

    py = quick_count(str(path), '*.py')
    total_py += py
    print(f" {py:>8,}", end='')

    csv = quick_count(str(path), '*.csv')
    total_csv += csv
    print(f" {csv:>8,}", end='')

    json = quick_count(str(path), '*.json')
    total_json += json
    print(f" {json:>8,}", end='')

    db = quick_count(str(path), '*.db') + quick_count(str(path), '*.sqlite')
    total_db += db
    print(f" {db:>8,}", end='')

    img = quick_count(str(path), '*.jpg') + quick_count(str(path), '*.png')
    total_img += img
    print(f" {img:>8,}")

print("-" * 90)
print(f"{'TOTAL':<20} {'':<10} {total_py:>8,} {total_csv:>8,} {total_json:>8,} {total_db:>8,} {total_img:>8,}")
print("=" * 90)

# Key findings
print("\nKEY FINDINGS:")
print(f"  Total Python files: {total_py:,}")
print(f"  Total CSV files: {total_csv:,}")
print(f"  Total JSON files: {total_json:,}")
print(f"  Total Databases: {total_db:,}")
print(f"  Total Images: {total_img:,}")

# Special checks
print("\nSPECIAL LOCATIONS:")

# .file_intelligence.db
file_intel_db = home / '.file_intelligence.db'
if file_intel_db.exists():
    size = file_intel_db.stat().st_size / 1024 / 1024
    print(f"  ✓ .file_intelligence.db exists ({size:.1f} MB)")

# .env.d structure
env_files = list((home / '.env.d').glob('*.env')) if (home / '.env.d').exists() else []
print(f"  ✓ .env.d has {len(env_files)} environment files")

# Music automation
music_py = quick_count(str(home / 'Music'), '*.py')
music_mp3 = quick_count(str(home / 'Music'), '*.mp3')
print(f"  ✓ Music has {music_py} Python scripts and {music_mp3} MP3 files")

print("\n" + "=" * 90)
print(f"Analysis complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 90)
