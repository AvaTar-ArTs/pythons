#!/usr/bin/env python3
"""Quick CSV analyzer and dedup finder — works with docs-*.csv output."""
import csv
import sys
import hashlib
from pathlib import Path
from collections import Counter, defaultdict

def analyze_csv(csv_path):
    rows = []
    with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    print(f"📊 {len(rows):,} files scanned\n")

    # Extension breakdown
    ext = Counter()
    for r in rows:
        fn = r.get('Filename', '')
        ext['.' + fn.rsplit('.', 1)[-1].lower() if '.' in fn else '(none)'] += 1
    print("=== BY EXTENSION ===")
    for e, c in ext.most_common(12):
        print(f"  {e:>8s}  {c:>7,}")

    # Top dirs
    top = Counter()
    for r in rows:
        p = r.get('Original Path', '')
        parts = p.strip('/').split('/')
        top[parts[-2] if len(parts) > 1 else parts[-1]] += 1
    print("\n=== TOP 15 DIRECTORIES ===")
    for d, c in top.most_common(15):
        print(f"  {d:>35s}  {c:>7,}")

    # Duplicate filenames
    names = defaultdict(list)
    for r in rows:
        names[r['Filename']].append(r['Original Path'])
    dups = {n: ps for n, ps in names.items() if len(ps) > 1}
    print(f"\n=== {len(dups):,} DUPLICATE FILENAMES ===")
    for n, ps in sorted(dups.items(), key=lambda x: -len(x[1]))[:20]:
        print(f"  {n:>30s}  →  {len(ps):>4} locations")

    return rows, dups

def content_hash(path, n=512):
    try:
        data = Path(path).read_bytes()[:n]
        return hashlib.md5(data).hexdigest()
    except:
        return None

def find_exact_dups(rows):
    """Find files with same name AND same content hash."""
    by_name_hash = defaultdict(list)
    for r in rows:
        h = content_hash(Path(r['Original Path']) / r['Filename'])
        if h:
            by_name_hash[(r['Filename'], h)].append(r)

    exact = {k: v for k, v in by_name_hash.items() if len(v) > 1}
    print(f"\n=== {len(exact):,} EXACT CONTENT DUPLICATES (same name + hash) ===")
    for (name, h), entries in sorted(exact.items(), key=lambda x: -len(x[1]))[:15]:
        print(f"  {name:>30s}  [{h}]  {len(entries)} copies")
        for e in entries[:3]:
            print(f"    → {e['Original Path']}  ({e['File Size']})")
    return exact

if __name__ == '__main__':
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "docs-04-12-21:16.csv"
    rows, dups = analyze_csv(csv_file)
    find_exact_dups(rows)
    print(f"\n✅ Analysis complete")
