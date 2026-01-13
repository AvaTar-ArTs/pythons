#!/usr/bin/env python3
"""
Folder-by-Folder Cleanup Analyzer
Process one directory at a time for 2T-Xx volume
"""

import hashlib
import json
import csv
from pathlib import Path
from datetime import datetime

class FolderCleanup:
    """Analyze one folder at a time"""
    
    def __init__(self):
        self.master_dir = Path.home() / 'Documents' / 'pythons'
        self.analysis_dir = self.master_dir / '_analysis'
        self.analysis_dir.mkdir(exist_ok=True)
        self.master_index = self.load_master_index()
    
    def load_master_index(self):
        """Load master index"""
        index_file = self.analysis_dir / 'master_index.json'
        if index_file.exists():
            with open(index_file) as f:
                return json.load(f)
        return {}
    
    def quick_hash(self, filepath):
        """Fast hash"""
        try:
            stat = filepath.stat()
            with open(filepath, 'rb') as f:
                chunk = f.read(1024)
            return hashlib.md5(f"{filepath.name}{stat.st_size}{chunk}".encode()).hexdigest()
        except:
            return None
    
    def list_folders(self, base_path):
        """List top-level folders"""
        if not base_path.exists():
            return []
        
        folders = [d for d in base_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        return sorted(folders)
    
    def count_py_files(self, folder_path):
        """Count Python files in folder"""
        try:
            return len(list(folder_path.rglob('*.py')))
        except:
            return 0
    
    def analyze_folder(self, folder_path):
        """Analyze single folder"""
        folder_name = folder_path.name
        safe_name = folder_name.replace(' ', '_').replace('/', '_')
        
        print(f"\n?? Analyzing: {folder_name}")
        print("=" * 80)
        
        py_files = list(folder_path.rglob('*.py'))
        total = len(py_files)
        
        print(f"  Python files: {total}")
        
        if total == 0:
            print("  ??  No Python files, skipping")
            return
        
        duplicates = []
        unique = []
        
        for i, fp in enumerate(py_files, 1):
            if i % 100 == 0:
                print(f"    Progress: {i}/{total}")
            
            h = self.quick_hash(fp)
            if not h:
                continue
            
            info = {
                'path': str(fp),
                'name': fp.name,
                'size': fp.stat().st_size,
                'relative': str(fp.relative_to(folder_path))
            }
            
            if h in self.master_index:
                duplicates.append({
                    **info,
                    'master_path': self.master_index[h]['path']
                })
            else:
                unique.append(info)
        
        # Save results
        csv_path = self.analysis_dir / f'folder_{safe_name}_duplicates.csv'
        
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['External_Path', 'Relative_Path', 'Master_Path', 'Size_KB', 'Filename'])
            
            for d in duplicates:
                writer.writerow([
                    d['path'],
                    d['relative'],
                    f"~/Documents/pythons/{d['master_path']}",
                    f"{d['size']/1024:.1f}",
                    d['name']
                ])
        
        dup_size = sum(d['size'] for d in duplicates) / (1024**2)
        
        print(f"\n  ? Results:")
        print(f"    ? Duplicates: {len(duplicates)} ({dup_size:.1f} MB)")
        print(f"    ? Unique: {len(unique)}")
        print(f"    ? CSV: {csv_path.name}")
        
        return {
            'folder': folder_name,
            'total': total,
            'duplicates': len(duplicates),
            'unique': len(unique),
            'size_mb': dup_size,
            'csv': csv_path.name
        }

def main():
    import sys
    
    analyzer = FolderCleanup()
    
    if len(sys.argv) < 2:
        # Show menu
        print("?? Folder-by-Folder Cleanup")
        print("=" * 80)
        print("\nAvailable options:")
        print("\n1. List folders in /Volumes/2T-Xx")
        print("2. Analyze specific folder")
        print("3. Analyze ai-sites subfolders")
        print("\nUsage:")
        print("  python folder-by-folder-cleanup.py list")
        print("  python folder-by-folder-cleanup.py analyze <folder_path>")
        print("  python folder-by-folder-cleanup.py ai-sites")
        return
    
    command = sys.argv[1]
    
    if command == 'list':
        # List folders with Python file counts
        print("\n?? Folders in /Volumes/2T-Xx:")
        print("=" * 80)
        
        base = Path('/Volumes/2T-Xx')
        folders = analyzer.list_folders(base)
        
        folder_stats = []
        for folder in folders[:30]:
            count = analyzer.count_py_files(folder)
            if count > 0:
                folder_stats.append((folder.name, count))
        
        for name, count in sorted(folder_stats, key=lambda x: -x[1]):
            print(f"  {count:6,} .py files  ?  {name}")
        
        print(f"\nTo analyze a folder:")
        print(f"  python folder-by-folder-cleanup.py analyze <folder_name>")
    
    elif command == 'analyze':
        if len(sys.argv) < 3:
            print("Error: Specify folder name")
            return
        
        folder_name = sys.argv[2]
        folder_path = Path(f'/Volumes/2T-Xx/{folder_name}')
        
        if not folder_path.exists():
            print(f"Error: Folder not found: {folder_path}")
            return
        
        result = analyzer.analyze_folder(folder_path)
    
    elif command == 'ai-sites':
        # Analyze all ai-sites subfolders
        print("\n?? Analyzing ai-sites subfolders")
        print("=" * 80)
        
        base = Path('/Volumes/2T-Xx/ai-sites')
        folders = analyzer.list_folders(base)
        
        all_results = []
        
        for folder in folders[:10]:  # Process 10 folders at a time
            result = analyzer.analyze_folder(folder)
            if result:
                all_results.append(result)
        
        # Summary
        print("\n" + "=" * 80)
        print("?? AI-Sites Summary")
        print("=" * 80)
        
        total_dupes = sum(r['duplicates'] for r in all_results)
        total_size = sum(r['size_mb'] for r in all_results)
        
        print(f"\nProcessed {len(all_results)} folders:")
        for r in all_results:
            print(f"  ? {r['folder']}: {r['duplicates']} dupes ({r['size_mb']:.1f} MB)")
        
        print(f"\n?? Total:")
        print(f"  ? Duplicates: {total_dupes}")
        print(f"  ? Space to reclaim: {total_size:.1f} MB")

if __name__ == "__main__":
    main()
