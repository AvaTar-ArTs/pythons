#!/usr/bin/env python3
"""
Search Markdown Files for Portfolio Content
"""

from pathlib import Path
import csv
from datetime import datetime

def search_md_content(filepath, keywords):
    """Search MD file for keywords"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
        found = [kw for kw in keywords if kw in content]
        return found
    except:
        return []

def main():
    print("?? Searching Markdown Files")
    print("=" * 80)
    
    locations = [
        (Path.home() / 'Documents', 'Documents'),
        (Path('/Volumes/2T-Xx'), '2T-Xx'),
        (Path('/Volumes/DeVonDaTa'), 'DeVonDaTa'),
    ]
    
    keywords = [
        'python', 'api', 'automation', 'developer', 'portfolio',
        'openai', 'gpt', 'claude', 'ai', 'machine learning',
        'instagram', 'youtube', 'social media', 'leonardo',
        'resume', 'cv', 'skills', 'experience', 'projects', 'suno'
    ]
    
    results = []
    
    for base_path, location_name in locations:
        if not base_path.exists():
            continue
        
        print(f"\n?? {location_name}")
        md_files = list(base_path.rglob('*.md'))
        print(f"  Found {len(md_files)} .md files")
        
        for i, fp in enumerate(md_files, 1):
            if i % 100 == 0:
                print(f"    {i}/{len(md_files)}")
            
            found = search_md_content(fp, keywords)
            
            if len(found) >= 3:
                results.append({
                    'location': location_name,
                    'path': str(fp),
                    'name': fp.name,
                    'size_kb': fp.stat().st_size / 1024,
                    'keywords': ', '.join(found),
                    'keyword_count': len(found)
                })
    
    # Save results
    csv_path = Path.home() / 'Documents' / 'pythons' / '_analysis' / 'PORTFOLIO_MARKDOWN_FOUND.csv'
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['location', 'path', 'name', 'size_kb', 'keyword_count', 'keywords'])
        writer.writeheader()
        for r in sorted(results, key=lambda x: -x['keyword_count']):
            writer.writerow(r)
    
    print(f"\n? Found {len(results)} relevant markdown files")
    print(f"?? Saved: {csv_path}")
    
    # Top 20
    print(f"\n?? Top 20:")
    for i, r in enumerate(sorted(results, key=lambda x: -x['keyword_count'])[:20], 1):
        print(f"  {i}. {r['name']} ({r['keyword_count']} keywords, {r['size_kb']:.0f}KB)")

if __name__ == "__main__":
    main()
