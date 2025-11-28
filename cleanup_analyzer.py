#!/usr/bin/env python3
"""
CLEANUP ANALYZER - Identify files safe to remove from ~/
Finds duplicates, cache files, temporary files, and unused content
"""

import os
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Set
from collections import defaultdict

class CleanupAnalyzer:
    """Analyzes home directory for files safe to remove"""
    
    def __init__(self, home_dir: str = "~"):
        self.home_dir = Path(home_dir).expanduser()
        self.findings = {
            'duplicates': [],
            'cache_files': [],
            'temp_files': [],
            'old_files': [],
            'large_files': [],
            'empty_dirs': [],
            'backup_files': [],
            'log_files': [],
            'python_cache': [],
            'node_modules': [],
            'total_size_removable': 0,
        }
        self.safe_patterns = {
            'cache': ['.cache', '.Cache', 'Cache', '__pycache__', '.pyc', '.pyo'],
            'temp': ['.tmp', '.temp', '.swp', '.swo', '.DS_Store', '.localized'],
            'backup': ['.bak', '.backup', '~', '.old', '.orig'],
            'log': ['.log', '.logs'],
            'python': ['__pycache__', '.pyc', '.pyo', '.pytest_cache'],
            'node': ['node_modules', '.npm', '.yarn'],
        }
    
    def analyze(self, max_depth: int = 5) -> Dict[str, Any]:
        """Perform comprehensive cleanup analysis"""
        print("🔍 CLEANUP ANALYZER - Finding files safe to remove")
        print("="*70)
        print(f"📁 Analyzing: {self.home_dir}\n")
        
        # Skip system directories
        skip_dirs = {
            '.Trash', '.Trashes', 'Library', 'Applications', 
            'System', 'System Volume Information', '.Spotlight-V100'
        }
        
        print("1️⃣  Finding duplicate files...")
        self._find_duplicates(max_depth, skip_dirs)
        
        print("2️⃣  Finding cache files...")
        self._find_cache_files(max_depth, skip_dirs)
        
        print("3️⃣  Finding temporary files...")
        self._find_temp_files(max_depth, skip_dirs)
        
        print("4️⃣  Finding old/unused files...")
        self._find_old_files(max_depth, skip_dirs, days_old=90)
        
        print("5️⃣  Finding large files (>100MB)...")
        self._find_large_files(max_depth, skip_dirs, min_size_mb=100)
        
        print("6️⃣  Finding backup files...")
        self._find_backup_files(max_depth, skip_dirs)
        
        print("7️⃣  Finding log files...")
        self._find_log_files(max_depth, skip_dirs)
        
        print("8️⃣  Finding Python cache...")
        self._find_python_cache(max_depth, skip_dirs)
        
        print("9️⃣  Finding empty directories...")
        self._find_empty_dirs(max_depth, skip_dirs)
        
        # Calculate total size
        self._calculate_total_size()
        
        return self.findings
    
    def _find_duplicates(self, max_depth: int, skip_dirs: Set[str]):
        """Find duplicate files by hash"""
        file_hashes = defaultdict(list)
        files_processed = 0
        
        for root, dirs, files in os.walk(self.home_dir):
            # Skip system directories
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                try:
                    if not filepath.is_file():
                        continue
                    
                    # Skip very large files for hashing
                    size = filepath.stat().st_size
                    if size > 100 * 1024 * 1024:  # > 100MB
                        continue
                    
                    # Calculate hash (first 1MB only for speed)
                    with open(filepath, 'rb') as f:
                        chunk = f.read(1024 * 1024)  # 1MB
                        file_hash = hashlib.md5(chunk).hexdigest()
                    
                    file_hashes[file_hash].append({
                        'path': str(filepath.relative_to(self.home_dir)),
                        'size': size,
                        'modified': datetime.fromtimestamp(filepath.stat().st_mtime),
                    })
                    
                    files_processed += 1
                    if files_processed % 1000 == 0:
                        print(f"   Processed {files_processed} files...")
                
                except (OSError, PermissionError):
                    continue
        
        # Find duplicates (2+ files with same hash)
        for file_hash, files in file_hashes.items():
            if len(files) > 1:
                # Sort by modified date (keep newest)
                files.sort(key=lambda x: x['modified'], reverse=True)
                duplicates = files[1:]  # All except the first (newest)
                
                total_duplicate_size = sum(f['size'] for f in duplicates)
                
                self.findings['duplicates'].append({
                    'hash': file_hash,
                    'keep': files[0],
                    'remove': duplicates,
                    'total_size': total_duplicate_size,
                    'count': len(duplicates),
                })
        
        print(f"   ✅ Found {len(self.findings['duplicates'])} duplicate groups")
    
    def _find_cache_files(self, max_depth: int, skip_dirs: Set[str]):
        """Find cache files"""
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            # Check directory name
            dir_name = Path(root).name
            if any(pattern.lower() in dir_name.lower() for pattern in self.safe_patterns['cache']):
                for file in files:
                    filepath = Path(root) / file
                    try:
                        size = filepath.stat().st_size
                        self.findings['cache_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'type': 'cache_directory',
                        })
                    except:
                        pass
            
            # Check file extensions
            for file in files:
                filepath = Path(root) / file
                if any(filepath.name.endswith(ext) for ext in ['.cache', '.Cache']):
                    try:
                        size = filepath.stat().st_size
                        self.findings['cache_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'type': 'cache_file',
                        })
                    except:
                        pass
    
    def _find_temp_files(self, max_depth: int, skip_dirs: Set[str]):
        """Find temporary files"""
        temp_extensions = ['.tmp', '.temp', '.swp', '.swo', '.DS_Store', '.localized']
        
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                
                # Check extension
                if any(filepath.name.endswith(ext) for ext in temp_extensions):
                    try:
                        size = filepath.stat().st_size
                        modified = datetime.fromtimestamp(filepath.stat().st_mtime)
                        
                        self.findings['temp_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'modified': modified,
                            'age_days': (datetime.now() - modified).days,
                        })
                    except:
                        pass
    
    def _find_old_files(self, max_depth: int, skip_dirs: Set[str], days_old: int = 90):
        """Find old files that haven't been accessed in X days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                try:
                    stat = filepath.stat()
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    accessed = datetime.fromtimestamp(stat.st_atime)
                    
                    # Check if file is old and not recently accessed
                    if modified < cutoff_date and accessed < cutoff_date:
                        size = stat.st_size
                        
                        # Skip important file types
                        ext = filepath.suffix.lower()
                        if ext in ['.py', '.js', '.json', '.md', '.txt', '.pdf', '.doc', '.docx']:
                            continue
                        
                        self.findings['old_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'modified': modified,
                            'accessed': accessed,
                            'age_days': (datetime.now() - modified).days,
                        })
                except:
                    pass
    
    def _find_large_files(self, max_depth: int, skip_dirs: Set[str], min_size_mb: int = 100):
        """Find large files"""
        min_size = min_size_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                try:
                    size = filepath.stat().st_size
                    if size >= min_size:
                        # Check if it's a system file or important
                        if filepath.name.startswith('.'):
                            continue
                        
                        self.findings['large_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'size_mb': size / (1024 * 1024),
                            'modified': datetime.fromtimestamp(filepath.stat().st_mtime),
                        })
                except:
                    pass
        
        # Sort by size
        self.findings['large_files'].sort(key=lambda x: x['size'], reverse=True)
    
    def _find_backup_files(self, max_depth: int, skip_dirs: Set[str]):
        """Find backup files"""
        backup_patterns = ['.bak', '.backup', '~', '.old', '.orig']
        
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                
                if any(filepath.name.endswith(ext) or filepath.name.endswith('~') 
                       for ext in backup_patterns):
                    try:
                        size = filepath.stat().st_size
                        self.findings['backup_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'type': 'backup',
                        })
                    except:
                        pass
    
    def _find_log_files(self, max_depth: int, skip_dirs: Set[str]):
        """Find log files"""
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                
                if filepath.suffix == '.log' or 'log' in filepath.name.lower():
                    try:
                        size = filepath.stat().st_size
                        modified = datetime.fromtimestamp(filepath.stat().st_mtime)
                        
                        self.findings['log_files'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'modified': modified,
                            'age_days': (datetime.now() - modified).days,
                        })
                    except:
                        pass
    
    def _find_python_cache(self, max_depth: int, skip_dirs: Set[str]):
        """Find Python cache files and directories"""
        for root, dirs, files in os.walk(self.home_dir):
            # Check for __pycache__ directories
            if '__pycache__' in dirs:
                pycache_dir = Path(root) / '__pycache__'
                try:
                    total_size = sum(f.stat().st_size for f in pycache_dir.rglob('*') if f.is_file())
                    self.findings['python_cache'].append({
                        'path': str(pycache_dir.relative_to(self.home_dir)),
                        'size': total_size,
                        'type': 'pycache_dir',
                    })
                except:
                    pass
            
            dirs[:] = [d for d in dirs if d not in skip_dirs and d != '__pycache__']
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            # Check for .pyc files
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix in ['.pyc', '.pyo']:
                    try:
                        size = filepath.stat().st_size
                        self.findings['python_cache'].append({
                            'path': str(filepath.relative_to(self.home_dir)),
                            'size': size,
                            'type': 'pyc_file',
                        })
                    except:
                        pass
    
    def _find_empty_dirs(self, max_depth: int, skip_dirs: Set[str]):
        """Find empty directories"""
        for root, dirs, files in os.walk(self.home_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            depth = len(Path(root).relative_to(self.home_dir).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            dir_path = Path(root)
            try:
                # Check if directory is empty
                if not any(dir_path.iterdir()):
                    self.findings['empty_dirs'].append({
                        'path': str(dir_path.relative_to(self.home_dir)),
                    })
            except:
                pass
    
    def _calculate_total_size(self):
        """Calculate total size of removable files"""
        total = 0
        
        # Duplicates
        for dup in self.findings['duplicates']:
            total += dup['total_size']
        
        # Cache files
        total += sum(f['size'] for f in self.findings['cache_files'])
        
        # Temp files
        total += sum(f['size'] for f in self.findings['temp_files'])
        
        # Old files
        total += sum(f['size'] for f in self.findings['old_files'])
        
        # Backup files
        total += sum(f['size'] for f in self.findings['backup_files'])
        
        # Log files
        total += sum(f['size'] for f in self.findings['log_files'])
        
        # Python cache
        total += sum(f['size'] for f in self.findings['python_cache'])
        
        self.findings['total_size_removable'] = total


def format_size(size: int) -> str:
    """Format file size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def generate_report(findings: Dict, output_file: Path):
    """Generate cleanup report"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🧹 CLEANUP ANALYSIS REPORT\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 📊 Summary\n\n")
        f.write(f"- **Total Removable Size:** {format_size(findings['total_size_removable'])}\n")
        f.write(f"- **Duplicate Groups:** {len(findings['duplicates'])}\n")
        f.write(f"- **Cache Files:** {len(findings['cache_files'])}\n")
        f.write(f"- **Temp Files:** {len(findings['temp_files'])}\n")
        f.write(f"- **Old Files:** {len(findings['old_files'])}\n")
        f.write(f"- **Backup Files:** {len(findings['backup_files'])}\n")
        f.write(f"- **Log Files:** {len(findings['log_files'])}\n")
        f.write(f"- **Python Cache:** {len(findings['python_cache'])}\n")
        f.write(f"- **Empty Directories:** {len(findings['empty_dirs'])}\n\n")
        
        # Duplicates
        if findings['duplicates']:
            f.write("## 🔄 Duplicate Files\n\n")
            f.write("**SAFE TO REMOVE** - Keep the newest, remove older duplicates\n\n")
            total_dup_size = sum(d['total_size'] for d in findings['duplicates'])
            f.write(f"**Total Size:** {format_size(total_dup_size)}\n\n")
            
            for i, dup in enumerate(findings['duplicates'][:20], 1):  # Top 20
                f.write(f"### Duplicate Group {i}\n\n")
                f.write(f"**Keep:** `{dup['keep']['path']}` ({format_size(dup['keep']['size'])})\n\n")
                f.write("**Remove:**\n")
                for file in dup['remove']:
                    f.write(f"- `{file['path']}` ({format_size(file['size'])}, {file['modified'].strftime('%Y-%m-%d')})\n")
                f.write(f"\n**Savings:** {format_size(dup['total_size'])}\n\n")
        
        # Cache files
        if findings['cache_files']:
            f.write("## 💾 Cache Files\n\n")
            f.write("**SAFE TO REMOVE** - Cache can be regenerated\n\n")
            cache_size = sum(f['size'] for f in findings['cache_files'])
            f.write(f"**Total Size:** {format_size(cache_size)}\n\n")
            
            for file in findings['cache_files'][:30]:  # Top 30
                f.write(f"- `{file['path']}` ({format_size(file['size'])})\n")
            f.write("\n")
        
        # Temp files
        if findings['temp_files']:
            f.write("## 🗑️  Temporary Files\n\n")
            f.write("**SAFE TO REMOVE** - Temporary files\n\n")
            temp_size = sum(f['size'] for f in findings['temp_files'])
            f.write(f"**Total Size:** {format_size(temp_size)}\n\n")
            
            for file in findings['temp_files'][:50]:  # Top 50
                f.write(f"- `{file['path']}` ({format_size(file['size'])}, {file['age_days']} days old)\n")
            f.write("\n")
        
        # Python cache
        if findings['python_cache']:
            f.write("## 🐍 Python Cache\n\n")
            f.write("**SAFE TO REMOVE** - Python cache can be regenerated\n\n")
            pycache_size = sum(f['size'] for f in findings['python_cache'])
            f.write(f"**Total Size:** {format_size(pycache_size)}\n\n")
            
            for item in findings['python_cache'][:30]:
                f.write(f"- `{item['path']}` ({format_size(item['size'])})\n")
            f.write("\n")
        
        # Large files (for review)
        if findings['large_files']:
            f.write("## 📦 Large Files (>100MB)\n\n")
            f.write("**REVIEW BEFORE REMOVING** - Large files that might be candidates\n\n")
            
            for file in findings['large_files'][:20]:  # Top 20
                f.write(f"- `{file['path']}` ({format_size(file['size'])}, modified {file['modified'].strftime('%Y-%m-%d')})\n")
            f.write("\n")
        
        f.write("---\n\n")
        f.write("**⚠️  IMPORTANT:** Review all files before deleting. This report identifies candidates for removal but does not delete anything automatically.\n")


def main():
    """Main execution"""
    analyzer = CleanupAnalyzer("~")
    findings = analyzer.analyze(max_depth=5)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = Path.home() / f'CLEANUP_ANALYSIS_{timestamp}.json'
    report_file = Path.home() / f'CLEANUP_REPORT_{timestamp}.md'
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2, default=str)
    
    generate_report(findings, report_file)
    
    print(f"\n{'='*70}")
    print("✅ CLEANUP ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"📄 JSON Data: {json_file}")
    print(f"📝 Report: {report_file}")
    print(f"\n💾 Total Removable Size: {format_size(findings['total_size_removable'])}")
    print(f"   Duplicates: {len(findings['duplicates'])} groups")
    print(f"   Cache Files: {len(findings['cache_files'])}")
    print(f"   Temp Files: {len(findings['temp_files'])}")
    print(f"   Python Cache: {len(findings['python_cache'])}")
    print(f"   Empty Dirs: {len(findings['empty_dirs'])}")


if __name__ == '__main__':
    main()

