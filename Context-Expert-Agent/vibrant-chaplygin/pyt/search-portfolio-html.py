#!/usr/bin/env python3
"""
Search HTML Files for Portfolio Content
Find HTML files referencing Python, API, automation skills
"""

from pathlib import Path
import csv
from datetime import datetime

def search_html_content(filepath, keywords):
    """Search HTML file for keywords"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
        
        found = [kw for kw in keywords if kw in content]
        return found
    except:
        return []

def main():
    print("?? Searching HTML Files for Portfolio/Skills Content")
    print("=" * 80)
    
    # Search locations
    locations = [
        (Path.home() / 'Documents', 'Documents'),
        (Path('/Volumes/2T-Xx'), '2T-Xx'),
        (Path('/Volumes/DeVonDaTa'), 'DeVonDaTa'),
    ]
    
    # Skills to look for
    keywords = [
        'python', 'api', 'automation', 'developer', 'portfolio',
        'openai', 'gpt', 'claude', 'ai', 'machine learning',
        'instagram', 'youtube', 'social media', 'leonardo',
        'resume', 'cv', 'skills', 'experience', 'projects'
    ]
    
    results = []
    
    for base_path, location_name in locations:
        if not base_path.exists():
            print(f"  ??  {location_name} not accessible")
            continue
        
        print(f"\n?? Searching: {location_name}")
        
        html_files = list(base_path.rglob('*.html'))
        print(f"  Found {len(html_files)} HTML files")
        
        for i, filepath in enumerate(html_files, 1):
            if i % 50 == 0:
                print(f"    Progress: {i}/{len(html_files)}")
            
            found_keywords = search_html_content(filepath, keywords)
            
            if len(found_keywords) >= 3:  # At least 3 skill keywords
                results.append({
                    'location': location_name,
                    'path': str(filepath),
                    'name': filepath.name,
                    'size_kb': filepath.stat().st_size / 1024,
                    'keywords': ', '.join(found_keywords),
                    'keyword_count': len(found_keywords)
                })
    
    # Save to CSV
    output_dir = Path.home() / 'Documents' / 'pythons' / '_analysis'
    output_dir.mkdir(exist_ok=True)
    
    csv_path = output_dir / 'PORTFOLIO_HTML_FOUND.csv'
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['location', 'path', 'name', 'size_kb', 'keyword_count', 'keywords'])
        writer.writeheader()
        
        for r in sorted(results, key=lambda x: -x['keyword_count']):
            writer.writerow(r)
    
    print(f"\n" + "=" * 80)
    print("? HTML SEARCH COMPLETE")
    print("=" * 80)
    print(f"\n?? Results:")
    print(f"  ? Total relevant HTML files: {len(results)}")
    print(f"  ? Saved to: {csv_path}")
    
    # Show top 10
    print(f"\n?? Top 10 Most Relevant:")
    for i, r in enumerate(sorted(results, key=lambda x: -x['keyword_count'])[:10], 1):
        print(f"  {i}. {r['name']} ({r['keyword_count']} keywords)")
        print(f"     {r['path'][:80]}")

if __name__ == "__main__":
    main()
