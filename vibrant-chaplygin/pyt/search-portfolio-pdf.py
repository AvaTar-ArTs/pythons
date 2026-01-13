#!/usr/bin/env python3
"""
Search PDF Files for Portfolio Content
Find PDF resumes, portfolios, and skill documents
"""

from pathlib import Path
import csv
from datetime import datetime

def main():
    print("?? Searching PDF Files")
    print("=" * 80)
    
    locations = [
        (Path.home() / 'Documents', 'Documents'),
        (Path('/Volumes/2T-Xx'), '2T-Xx'),
        (Path('/Volumes/DeVonDaTa'), 'DeVonDaTa'),
    ]
    
    # For PDFs, check filename first (faster)
    keywords = [
        'resume', 'cv', 'portfolio', 'skills', 'experience',
        'python', 'developer', 'engineer', 'automation',
        'chaplinski', 'steven', 'quantumforge', 'avatararts'
    ]
    
    results = []
    
    for base_path, location_name in locations:
        if not base_path.exists():
            continue
        
        print(f"\n?? {location_name}")
        pdf_files = list(base_path.rglob('*.pdf'))
        print(f"  Found {len(pdf_files)} PDF files")
        
        for i, fp in enumerate(pdf_files, 1):
            if i % 100 == 0:
                print(f"    {i}/{len(pdf_files)}")
            
            # Check filename for keywords
            filename_lower = fp.name.lower()
            found = [kw for kw in keywords if kw in filename_lower]
            
            if len(found) >= 1:  # Any keyword match for PDFs
                results.append({
                    'location': location_name,
                    'path': str(fp),
                    'name': fp.name,
                    'size_kb': fp.stat().st_size / 1024,
                    'keywords': ', '.join(found),
                    'keyword_count': len(found)
                })
    
    # Save
    csv_path = Path.home() / 'Documents' / 'pythons' / '_analysis' / 'PORTFOLIO_PDF_FOUND.csv'
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['location', 'path', 'name', 'size_kb', 'keyword_count', 'keywords'])
        writer.writeheader()
        for r in sorted(results, key=lambda x: -x['keyword_count']):
            writer.writerow(r)
    
    print(f"\n? Found {len(results)} relevant PDF files")
    print(f"?? Saved: {csv_path}")
    
    # Top results
    print(f"\n?? Top 20:")
    for i, r in enumerate(sorted(results, key=lambda x: -x['keyword_count'])[:20], 1):
        print(f"  {i}. {r['name'][:70]} ({r['keyword_count']} keywords)")

if __name__ == "__main__":
    main()
