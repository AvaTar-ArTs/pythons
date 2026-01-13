#!/usr/bin/env python3
"""
Smart Cleanup Tool for External Volumes
Safely remove redundant Python files based on ~/Documents/pythons master copies
"""

import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import json

class ExternalVolumeCleanup:
    """Intelligently clean up external volumes"""
    
    def __init__(self):
        self.master_dir = Path.home() / 'Documents' / 'pythons'
        self.external_volumes = {
            '2T-Xx': Path('/Volumes/2T-Xx'),
            'DeVonDaTa': Path('/Volumes/DeVonDaTa'),
        }
        
        self.master_hashes = {}  # hash -> filepath
        self.external_files = defaultdict(list)
        self.duplicates_to_remove = []
        self.safe_to_remove = []
        self.keep_files = []
        
    def hash_file(self, filepath):
        """Get MD5 hash of file"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def scan_master_directory(self):
        """Scan ~/Documents/pythons and hash all files"""
        print("?? Scanning Master Directory (~/Documents/pythons)...")
        print("=" * 80)
        
        py_files = list(self.master_dir.rglob('*.py'))
        print(f"Found {len(py_files)} Python files in master directory")
        
        for i, filepath in enumerate(py_files, 1):
            if i % 100 == 0:
                print(f"  Progress: {i}/{len(py_files)}")
            
            file_hash = self.hash_file(filepath)
            if file_hash:
                self.master_hashes[file_hash] = filepath
        
        print(f"? Indexed {len(self.master_hashes)} unique files")
    
    def scan_external_volumes(self):
        """Scan external volumes for Python files"""
        print("\n?? Scanning External Volumes...")
        print("=" * 80)
        
        for vol_name, vol_path in self.external_volumes.items():
            if not vol_path.exists():
                print(f"??  {vol_name} not mounted")
                continue
            
            print(f"\n?? Scanning {vol_name}...")
            py_files = list(vol_path.rglob('*.py'))
            print(f"  Found {len(py_files)} Python files")
            
            for i, filepath in enumerate(py_files, 1):
                if i % 1000 == 0:
                    print(f"  Progress: {i}/{len(py_files)}")
                
                file_hash = self.hash_file(filepath)
                if file_hash:
                    self.external_files[vol_name].append({
                        'path': filepath,
                        'hash': file_hash,
                        'size': filepath.stat().st_size,
                        'is_duplicate': file_hash in self.master_hashes,
                        'master_path': self.master_hashes.get(file_hash)
                    })
    
    def analyze_duplicates(self):
        """Analyze which external files are duplicates"""
        print("\n?? Analyzing Duplicates...")
        print("=" * 80)
        
        total_duplicates = 0
        total_size = 0
        
        for vol_name, files in self.external_files.items():
            duplicates = [f for f in files if f['is_duplicate']]
            dup_size = sum(f['size'] for f in duplicates)
            
            print(f"\n{vol_name}:")
            print(f"  Total files: {len(files)}")
            print(f"  Duplicates: {len(duplicates)}")
            print(f"  Size to save: {dup_size / (1024**3):.2f} GB")
            
            total_duplicates += len(duplicates)
            total_size += dup_size
            
            self.duplicates_to_remove.extend(duplicates)
        
        print(f"\n?? Total Summary:")
        print(f"  Total duplicates: {total_duplicates}")
        print(f"  Total space to reclaim: {total_size / (1024**3):.2f} GB")
    
    def categorize_for_removal(self):
        """Categorize files into removal categories"""
        print("\n???  Categorizing Files...")
        print("=" * 80)
        
        categories = {
            'exact_duplicates': [],      # Exact copies of master files
            'node_modules': [],           # Node modules (safe to delete)
            'pycache': [],                # Python cache (safe to delete)
            'venv': [],                   # Virtual environments (safe to delete)
            'backup_dirs': [],            # Backup directories
            'test_files': [],             # Test files
        }
        
        for vol_name, files in self.external_files.items():
            for file_info in files:
                path_str = str(file_info['path'])
                
                # Exact duplicates
                if file_info['is_duplicate']:
                    categories['exact_duplicates'].append(file_info)
                
                # Node modules
                if 'node_modules' in path_str:
                    categories['node_modules'].append(file_info)
                
                # Python cache
                if '__pycache__' in path_str or path_str.endswith('.pyc'):
                    categories['pycache'].append(file_info)
                
                # Virtual environments
                if '/venv/' in path_str or '/.venv/' in path_str or '/env/' in path_str:
                    categories['venv'].append(file_info)
                
                # Backup directories
                if any(x in path_str.lower() for x in ['backup', '_bak', '.bak', 'old', 'archive']):
                    categories['backup_dirs'].append(file_info)
                
                # Test files
                if '/test/' in path_str or path_str.endswith('_test.py') or path_str.endswith('test_.py'):
                    categories['test_files'].append(file_info)
        
        print("\n?? Removal Categories:")
        for cat_name, items in categories.items():
            if items:
                size = sum(f['size'] for f in items)
                print(f"  ? {cat_name}: {len(items)} files ({size / (1024**2):.1f} MB)")
        
        return categories
    
    def generate_removal_plan(self, categories):
        """Generate detailed removal plan"""
        print("\n?? Generating Removal Plan...")
        
        plan_path = self.master_dir / 'CLEANUP_PLAN.md'
        
        content = f"""# ?? External Volume Cleanup Plan

> **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **Status**: REVIEW REQUIRED - DO NOT AUTO-EXECUTE

## ??  IMPORTANT WARNINGS

1. **Review this plan carefully before executing**
2. **Backup recommended before deletion**
3. **Some files may be valuable even if duplicates**
4. **Check project dependencies**

---

## ?? Summary

### Files to Remove by Category

"""
        
        total_files = 0
        total_size = 0
        
        for cat_name, items in categories.items():
            if items:
                cat_size = sum(f['size'] for f in items)
                total_files += len(items)
                total_size += cat_size
                
                content += f"\n### {cat_name.replace('_', ' ').title()}\n"
                content += f"- **Count**: {len(items)} files\n"
                content += f"- **Size**: {cat_size / (1024**2):.1f} MB\n"
                content += f"- **Safety**: "
                
                if cat_name in ['pycache', 'node_modules']:
                    content += "? SAFE (can be regenerated)\n"
                elif cat_name in ['venv']:
                    content += "? SAFE (virtual environments)\n"
                elif cat_name == 'exact_duplicates':
                    content += "??  VERIFY (duplicates of master files)\n"
                else:
                    content += "??  REVIEW CAREFULLY\n"
        
        content += f"""

---

## ?? Impact

- **Total files to remove**: {total_files:,}
- **Total space to reclaim**: {total_size / (1024**3):.2f} GB
- **Estimated time**: ~{total_files // 1000} minutes

---

## ?? Recommended Actions

### Phase 1: Safe Deletions (Auto-safe)
1. ? Delete `__pycache__` directories
2. ? Delete `node_modules` directories  
3. ? Delete virtual environments (`venv/`, `.venv/`, `env/`)

### Phase 2: Duplicate Removal (Verify)
1. ??  Review exact duplicates list
2. ??  Verify master copies are working
3. ??  Delete confirmed duplicates

### Phase 3: Backup/Archive Cleanup (Manual)
1. ?? Review backup directories
2. ?? Identify outdated backups
3. ?? Archive or delete as appropriate

---

## ?? Detailed File Lists

### Exact Duplicates (Top 50)

These files exist in ~/Documents/pythons and can be removed from external volumes:

"""
        
        # List top 50 exact duplicates
        exact_dupes = categories.get('exact_duplicates', [])
        for i, dup in enumerate(sorted(exact_dupes, key=lambda x: -x['size'])[:50], 1):
            content += f"\n{i}. **{dup['path'].name}**\n"
            content += f"   - External: `{dup['path']}`\n"
            content += f"   - Master: `{dup['master_path']}`\n"
            content += f"   - Size: {dup['size'] / 1024:.1f} KB\n"
        
        if len(exact_dupes) > 50:
            content += f"\n... and {len(exact_dupes) - 50} more duplicates\n"
        
        content += """

---

## ???  Execution Commands

### Preview Mode (Recommended First)
```bash
python cleanup-external-volumes.py --preview
```

### Safe Deletions Only
```bash
python cleanup-external-volumes.py --safe-only
```

### Full Cleanup (After Review)
```bash
python cleanup-external-volumes.py --execute
```

---

## ?? Backup Recommendation

Before executing any deletions:

```bash
# Create backup of file list
cp CLEANUP_PLAN.md CLEANUP_PLAN_BACKUP_$(date +%Y%m%d).md

# Optional: Create archive of files to be deleted
tar -czf external_volumes_backup_$(date +%Y%m%d).tar.gz [files...]
```

---

## ??  Manual Review Required

**DO NOT AUTO-EXECUTE** without reviewing:
1. Exact duplicates - verify master copies work
2. Backup directories - may contain valuable old versions
3. Test files - may have important test data
4. Archive directories - may have historical code

---

*Generated by cleanup-external-volumes.py*
"""
        
        with open(plan_path, 'w') as f:
            f.write(content)
        
        print(f"? Cleanup plan saved: {plan_path}")
        
        # Also save JSON for programmatic access
        json_path = self.master_dir / 'CLEANUP_PLAN.json'
        with open(json_path, 'w') as f:
            # Convert Path objects to strings for JSON
            json_data = {}
            for cat_name, items in categories.items():
                json_data[cat_name] = [
                    {
                        'path': str(item['path']),
                        'hash': item['hash'],
                        'size': item['size'],
                        'master_path': str(item.get('master_path', ''))
                    }
                    for item in items
                ]
            json.dump(json_data, f, indent=2)
        
        print(f"? JSON plan saved: {json_path}")
        
        return plan_path
    
    def execute_safe_cleanup(self, dry_run=True):
        """Execute safe cleanup operations"""
        print("\n?? Executing Safe Cleanup...")
        print("=" * 80)
        
        if dry_run:
            print("??  DRY RUN MODE - No files will be deleted")
        
        safe_categories = ['pycache', 'node_modules']
        
        for vol_name, vol_path in self.external_volumes.items():
            if not vol_path.exists():
                continue
            
            print(f"\n?? Cleaning {vol_name}...")
            
            # Find __pycache__ directories
            pycache_dirs = list(vol_path.rglob('__pycache__'))
            print(f"  Found {len(pycache_dirs)} __pycache__ directories")
            
            if not dry_run:
                for pycache in pycache_dirs[:10]:  # Limit for safety
                    try:
                        shutil.rmtree(pycache)
                        print(f"    ? Removed: {pycache}")
                    except Exception as e:
                        print(f"    ? Error: {pycache}: {e}")
            
            # Find node_modules directories
            node_modules = list(vol_path.rglob('node_modules'))
            print(f"  Found {len(node_modules)} node_modules directories")
            
            if not dry_run and len(node_modules) < 50:  # Safety check
                for nm in node_modules[:5]:  # Very conservative
                    try:
                        shutil.rmtree(nm)
                        print(f"    ? Removed: {nm}")
                    except Exception as e:
                        print(f"    ? Error: {nm}: {e}")
    
    def run(self, mode='analyze'):
        """Run cleanup analysis"""
        print("?? External Volume Cleanup Tool")
        print("=" * 80)
        print(f"Mode: {mode}")
        print()
        
        # Scan master directory
        self.scan_master_directory()
        
        # Scan external volumes
        self.scan_external_volumes()
        
        # Analyze duplicates
        self.analyze_duplicates()
        
        # Categorize files
        categories = self.categorize_for_removal()
        
        # Generate plan
        plan_path = self.generate_removal_plan(categories)
        
        print("\n" + "=" * 80)
        print("? Analysis Complete!")
        print("=" * 80)
        print(f"\n?? Review the cleanup plan: {plan_path}")
        print(f"\n??  IMPORTANT: Review carefully before executing any deletions!")
        
        if mode == 'safe-preview':
            self.execute_safe_cleanup(dry_run=True)

def main():
    import sys
    
    mode = sys.argv[1] if len(sys.argv) > 1 else 'analyze'
    
    cleanup = ExternalVolumeCleanup()
    cleanup.run(mode=mode)

if __name__ == "__main__":
    main()
