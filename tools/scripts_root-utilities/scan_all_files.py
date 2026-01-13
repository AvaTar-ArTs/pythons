#!/usr/bin/env python3
"""
📊 COMPREHENSIVE FILE SCANNER - ALL SCATTERED FILES
Scans /Users/steven for HTML, CSS, JS, JSON, XML, MD, and more
Saves CSV inventory to ~/workspace
"""

import os
import csv
from pathlib import Path
from datetime import datetime

print("🔍 SCANNING /Users/steven FOR ALL FILES...")
print("="*70)

# Target file extensions
extensions = {
    '.html', '.htm', '.css', '.js', '.jsx', '.ts', '.tsx',
    '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
    '.md', '.markdown', '.txt', '.csv', '.tsv', '.svg',
    '.pdf', '.docx', '.xlsx', '.log'
}

all_files = []
scan_root = Path('/Users/steven')

# Directories to skip
skip_dirs = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    'Library/Caches', 'Library/Logs', '.Trash'
}

print(f"Starting scan from: {scan_root}\n")

for root, dirs, files in os.walk(scan_root):
    # Filter out skip directories
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    
    for filename in files:
        filepath = Path(root) / filename
        ext = filepath.suffix.lower()
        
        if ext in extensions:
            try:
                stats = filepath.stat()
                
                # Category
                cat = {
                    '.html,.htm': 'HTML',
                    '.css': 'CSS',
                    '.js,.jsx,.ts,.tsx': 'JavaScript',
                    '.json,.yaml,.yml,.toml': 'Config',
                    '.xml': 'XML',
                    '.md,.markdown': 'Documentation',
                    '.txt': 'Text',
                    '.csv,.tsv': 'Data',
                    '.svg': 'SVG',
                    '.pdf': 'PDF'
                }.get(ext, 'Other')
                
                for key, value in {
                    '.html,.htm': 'HTML',
                    '.css': 'CSS',
                    '.js,.jsx,.ts,.tsx': 'JavaScript',
                    '.json,.yaml,.yml,.toml': 'Config'
                }.items():
                    if ext in key:
                        cat = value
                        break
                
                all_files.append({
                    'filename': filename,
                    'extension': ext,
                    'category': cat,
                    'filepath': str(filepath),
                    'size_kb': round(stats.st_size / 1024, 2),
                    'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M')
                })
                
                if len(all_files) % 1000 == 0:
                    print(f"   Found {len(all_files):,} files...")
                    
            except:
                continue

print(f"\n✅ Scan complete! Found {len(all_files):,} files\n")

# Write CSV
output_path = Path('/Users/steven/workspace/SCATTERED_FILES_INVENTORY.csv')
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'filename', 'extension', 'category', 'filepath', 'size_kb', 'modified'
    ])
    writer.writeheader()
    writer.writerows(all_files)

print(f"💾 CSV saved to: {output_path}")
print(f"📊 Total files: {len(all_files):,}\n")

# Summary
cats = {}
for f in all_files:
    cat = f['category']
    cats[cat] = cats.get(cat, 0) + 1

print("📈 BREAKDOWN:")
for cat, count in sorted(cats.items(), key=lambda x: x[1], reverse=True):
    print(f"   • {cat}: {count:,}")
