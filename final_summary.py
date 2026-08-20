#!/usr/bin/env python3
import os
from collections import defaultdict

base_path = "/Users/steven/Music/nocturneMelodies"

categories = defaultdict(list)

def categorize(name_lower):
    if any(x in name_lower for x in ['cover', 'download_cover', 'image', 'artwork']):
        return 'cover'
    if any(x in name_lower for x in ['transcript', 'transcribe', 'analysis', 'analyzer']):
        return 'transcript'
    if any(x in name_lower for x in ['mp3', 'rename', 'organize', 'consolidate', 'move_music', 'deduplicat', 'scan_']):
        return 'mp3'
    if any(x in name_lower for x in ['suno', 'uuid', 'extract']):
        return 'suno'
    if any(x in name_lower for x in ['html', 'gallery', 'web', 'site', 'mobile']):
        return 'web'
    if any(x in name_lower for x in ['distro', 'spotify', 'soundcloud', 'distrokid', 'distribution', 'curator']):
        return 'distribution'
    if any(x in name_lower for x in ['nocturnememory', 'ai_', 'knowledge', 'autotag', 'embeddings', 'index']):
        return 'ai'
    return 'other'

for root, dirs, filenames in os.walk(base_path):
    dirs[:] = [d for d in dirs if d not in ('venv', '.venv', 'venv313')]
    
    for fname in filenames:
        if fname.endswith('.py'):
            full_path = os.path.join(root, fname)
            name_lower = fname.lower()
            cat = categorize(name_lower)
            
            rel_path = full_path.replace(base_path, '').lstrip('/')
            categories[cat].append(rel_path)

# Print summary
print("=" * 80)
print("PYTHON FILE CATEGORIZATION SUMMARY")
print("=" * 80)
print()

totals = {}
for cat in ['cover', 'transcript', 'mp3', 'suno', 'web', 'distribution', 'ai', 'other']:
    count = len(categories[cat])
    totals[cat] = count
    print(f"{cat.upper():20} {count:3} files")

print()
print(f"{'TOTAL':20} {sum(totals.values()):3} files")
print()

# Print OTHER files list
print("=" * 80)
print("OTHER/UNRELATED FILES")
print("=" * 80)
for fname in sorted(categories['other']):
    print(fname)

print(f"\nTotal 'other': {len(categories['other'])}")
