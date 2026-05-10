#!/usr/bin/env python3
"""
Sellable Products Extractor — reads docs CSV, identifies unique sellable items,
outputs a product catalog CSV ready for marketplace-uploader.

Usage: python extract_sellable.py /path/to/docs.csv
"""

import csv
import sys
from collections import defaultdict, Counter
from pathlib import Path

def load_csv(path):
    rows = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows

def categorize(filename, filepath):
    text = f"{filename} {filepath}".lower()
    categories = []

    if any(w in text for w in ['openai', 'llm', 'chatgpt', 'claude', 'gemini', 'gpt', 'ai_tool', 'ai_agent', 'rag', 'embed']):
        categories.append('AI/ML Tools')
    if any(w in text for w in ['instagram', 'youtube', 'twitter', 'social', 'bot', 'scraper', 'automation', 'workflow']):
        categories.append('Social Media Automation')
    if any(w in text for w in ['ffmpeg', 'audio', 'video', 'image', 'media', 'thumbnail', 'resize', 'convert', 'music', 'suno']):
        categories.append('Media Processing')
    if any(w in text for w in ['dedup', 'organize', 'rename', 'cleanup', 'file_', 'dir_', 'scanner', 'inventory']):
        categories.append('File Management')
    if any(w in text for w in ['analytics', 'dashboard', 'report', 'chart', 'data_', 'pandas', 'stat']):
        categories.append('Data & Analytics')
    if any(w in text for w in ['seo', 'keyword', 'marketing', 'rank', 'sitemap', 'backlink', 'a eo']):
        categories.append('SEO & Marketing')
    if any(w in text for w in ['mcp', 'hook', 'server_config', 'router', 'api_']):
        categories.append('MCP & Platform Tools')
    if any(w in text for w in ['analyzer', 'code_analy', 'complexity', 'quality', 'lint']):
        categories.append('Code Quality')

    return categories if categories else ['Utilities']

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_sellable.py <docs.csv>")
        sys.exit(1)

    rows = load_csv(sys.argv[1])
    print(f"📊 Loaded {len(rows):,} files from CSV\n")

    # Group by filename (deduplicate across locations)
    by_name = defaultdict(list)
    for row in rows:
        fn = row.get('Filename', '').strip()
        fp = row.get('Original Path', '').strip()
        if fn and fp and not any(skip in fp for skip in ['.git', 'node_modules', '__pycache__', 'site-packages', 'google-cloud-sdk']):
            by_name[fn].append(row)

    # Only keep files that appear in 1-5 locations (not massive duplicates)
    unique_files = {fn: entries for fn, entries in by_name.items() if 1 <= len(entries) <= 5}
    print(f"🔍 {len(unique_files):,} unique files (1-5 copies max)\n")

    # Categorize
    products = []
    for fn, entries in unique_files.items():
        best = entries[0]  # first occurrence
        cats = categorize(fn, best.get('Original Path', ''))
        products.append({
            'filename': fn,
            'size': best.get('File Size', ''),
            'path': best.get('Original Path', ''),
            'categories': '|'.join(cats),
            'copies': len(entries),
        })

    # Sort by category, then filename
    products.sort(key=lambda x: (x['categories'], x['filename']))

    # Count by category
    cat_counts = Counter()
    for p in products:
        for c in p['categories'].split('|'):
            cat_counts[c] += 1

    print("📁 By Category (unique files):")
    for cat, cnt in cat_counts.most_common():
        print(f"  {cat:>25s}  {cnt:>6,} files")

    # Output catalog
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/Users/steven/marketplace-uploader/data/sellable_catalog.csv"
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'size', 'path', 'categories', 'copies'])
        writer.writeheader()
        writer.writerows(products)

    print(f"\n📋 Catalog saved to: {out_path}")
    print(f"   {len(products):,} potentially sellable items identified")

    # Top 20 standalone product candidates (large, unique, useful names)
    print(f"\n🏆 TOP 20 PRODUCT CANDIDATES:")
    candidates = [p for p in products
                  if p['copies'] <= 3
                  and any(kw in p['filename'].lower() for kw in [
                      'analyzer', 'automation', 'builder', 'generator', 'optimizer',
                      'organizer', 'toolkit', 'pipeline', 'engine', 'framework',
                      'manager', 'orchestrat', 'suite', 'hub', 'forge'
                  ])]
    for p in candidates[:20]:
        print(f"  {p['filename']:<45s}  {p['size']:>10s}  [{p['categories']}]")

if __name__ == '__main__':
    main()
