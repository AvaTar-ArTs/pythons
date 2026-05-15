#!/usr/bin/env python3
"""
COMPREHENSIVE HOME DIRECTORY CONTENT SCAN
==========================================
Scans entire ~/ for all content files:
- Python (.py)
- Shell scripts (.sh)
- Markdown (.md)
- HTML (.html, .htm)
- JSON (.json)
- YAML (.yml, .yaml)
- Text (.txt)
- Config (.toml, .ini, .cfg)
- JavaScript (.js)
- TypeScript (.ts)
- CSS (.css)
- SQL (.sql)
- And more...

Excludes system/dependency directories.
"""

import os
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ============================================================
# Configuration
# ============================================================

HOME = Path("/Users/steven")
OUTPUT_DIR = HOME / "python-marketplace-inventory"
CONTENT_CSV = OUTPUT_DIR / "COMPREHENSIVE_CONTENT_SCAN.csv"
CONTENT_SUMMARY = OUTPUT_DIR / "CONTENT_SCAN_SUMMARY.md"
DISCOVERED_CONTENT_CSV = OUTPUT_DIR / "DISCOVERED_CONTENT.csv"

# File extensions to scan
CONTENT_EXTENSIONS = {
    # Code
    '.py': 'Python',
    '.sh': 'Shell Script',
    '.bash': 'Bash Script',
    '.zsh': 'Zsh Script',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.jsx': 'React JavaScript',
    '.tsx': 'React TypeScript',
    
    # Web
    '.html': 'HTML',
    '.htm': 'HTML',
    '.css': 'CSS',
    '.scss': 'SCSS',
    '.sass': 'SASS',
    '.less': 'LESS',
    
    # Data/Config
    '.json': 'JSON',
    '.yaml': 'YAML',
    '.yml': 'YAML',
    '.toml': 'TOML',
    '.ini': 'INI Config',
    '.cfg': 'Config',
    '.conf': 'Config',
    '.env': 'Environment',
    
    # Documentation
    '.md': 'Markdown',
    '.txt': 'Text',
    '.rst': 'reStructuredText',
    '.org': 'Org Mode',
    
    # Database
    '.sql': 'SQL',
    '.db': 'Database',
    '.sqlite': 'SQLite',
    
    # Templates
    '.jinja': 'Jinja Template',
    '.jinja2': 'Jinja2 Template',
    '.tpl': 'Template',
    
    # Other
    '.xml': 'XML',
    '.csv': 'CSV Data',
    '.log': 'Log File',
    '.ipynb': 'Jupyter Notebook',
}

# Directories to EXCLUDE (system/dependency/cache)
EXCLUDE_DIRS = {
    # System
    'Library', 'Applications', 'Public', 'Movies', 'Music', 'Pictures',
    'Desktop', '.Trash',
    
    # Package managers
    'node_modules', '.nvm', '.npm', '.npm-global', '.cargo', '.rustup',
    '.rbenv', '.bun', '.bundle', '.gem', '.mamba', '.pixi', '.conda',
    '.oh-my-zsh', 'google-cloud-sdk',
    
    # Virtual environments
    '.venv', '.venv_dev', 'site-packages', 'dist-packages',
    
    # Cache/Build
    '.cache', 'build', 'dist', '.eggs', '__pycache__', '.pytest_cache',
    '.mypy_cache', '.tox', '.nox',
    
    # IDE/Editor
    '.vscode/extensions', '.cursor/extensions', '.local/share/uv',
    
    # Docker/Containers
    '.docker',
    
    # SSH/Security
    '.ssh', '.gnupg', '.secrets',
    
    # Logs/Backups
    'backups', 'logs', '.update_logs',
    
    # Browser data
    'chromium',
}

# ============================================================
# Scanning Functions
# ============================================================

def should_exclude_dir(dir_name: str, dir_path: Path) -> bool:
    """Check if directory should be excluded."""
    if dir_name in EXCLUDE_DIRS:
        return True
    
    path_str = str(dir_path)
    for pattern in EXCLUDE_DIRS:
        if pattern in path_str:
            return True
    
    return False


def scan_home_directory() -> list:
    """Scan entire home directory for content files."""
    content_files = []
    dirs_scanned = 0
    errors = 0
    
    print(f"🔍 Scanning {HOME}...")
    
    try:
        for root, dirs, files in os.walk(HOME, topdown=True):
            root_path = Path(root)
            
            # Filter excluded directories
            dirs[:] = [d for d in dirs if not should_exclude_dir(d, root_path / d)]
            
            dirs_scanned += 1
            
            if dirs_scanned % 100 == 0:
                print(f"   Scanned {dirs_scanned} directories, found {len(content_files):,} files...")
            
            for file in files:
                file_path = root_path / file
                ext = file_path.suffix.lower()
                
                if ext in CONTENT_EXTENSIONS:
                    try:
                        stat = file_path.stat()
                        content_files.append({
                            'file_name': file,
                            'full_path': str(file_path),
                            'extension': ext,
                            'file_type': CONTENT_EXTENSIONS[ext],
                            'file_size_kb': round(stat.st_size / 1024, 1),
                            'last_modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                            'parent_dir': root_path.relative_to(HOME).parts[0] if len(root_path.relative_to(HOME).parts) > 0 else 'root',
                        })
                    except Exception:
                        errors += 1
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ Scan complete!")
    print(f"   Directories scanned: {dirs_scanned:,}")
    print(f"   Errors: {errors}")
    print(f"   Content files found: {len(content_files):,}")
    
    return content_files


def analyze_content(content_files: list):
    """Analyze content files by type, directory, etc."""
    
    # By file type
    by_type = defaultdict(int)
    for f in content_files:
        by_type[f['file_type']] += 1
    
    # By directory
    by_dir = defaultdict(int)
    for f in content_files:
        by_dir[f['parent_dir']] += 1
    
    # By extension
    by_ext = defaultdict(int)
    for f in content_files:
        by_ext[f['extension']] += 1
    
    # Total size
    total_size = sum(f['file_size_kb'] for f in content_files)
    
    return {
        'by_type': dict(sorted(by_type.items(), key=lambda x: x[1], reverse=True)),
        'by_dir': dict(sorted(by_dir.items(), key=lambda x: x[1], reverse=True)),
        'by_ext': dict(sorted(by_ext.items(), key=lambda x: x[1], reverse=True)),
        'total_size_mb': round(total_size / 1024, 1),
        'total_files': len(content_files),
    }


def save_results(content_files: list, analysis: dict):
    """Save scan results."""
    
    # Save full CSV
    with open(CONTENT_CSV, 'w', newline='', encoding='utf-8') as f:
        if content_files:
            fieldnames = list(content_files[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(content_files)
    
    print(f"\n💾 Saved full results: {CONTENT_CSV}")
    
    # Save summary
    with open(CONTENT_SUMMARY, 'w', encoding='utf-8') as f:
        f.write("# 🔍 Comprehensive Content Scan Results\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| **Total Content Files** | {analysis['total_files']:,} |\n")
        f.write(f"| **Total Size** | {analysis['total_size_mb']:,} MB |\n")
        f.write(f"| **File Types** | {len(analysis['by_type'])} |\n")
        f.write(f"| **Directories** | {len(analysis['by_dir'])} |\n\n")
        
        f.write("## By File Type\n\n")
        f.write("| Type | Count |\n")
        f.write("|------|-------|\n")
        for ftype, count in analysis['by_type'].items():
            f.write(f"| {ftype} | {count:,} |\n")
        
        f.write("\n## By Extension\n\n")
        f.write("| Extension | Count |\n")
        f.write("|-----------|-------|\n")
        for ext, count in analysis['by_ext'].items():
            f.write(f"| {ext} | {count:,} |\n")
        
        f.write("\n## Top Directories\n\n")
        f.write("| Directory | Files |\n")
        f.write("|-----------|-------|\n")
        for dir_name, count in list(analysis['by_dir'].items())[:30]:
            f.write(f"| {dir_name} | {count:,} |\n")
    
    print(f"💾 Saved summary: {CONTENT_SUMMARY}")
    
    # Save discovered content (files not in previous scans)
    # This would require loading previous inventory - simplified version
    with open(DISCOVERED_CONTENT_CSV, 'w', newline='', encoding='utf-8') as f:
        if content_files:
            fieldnames = list(content_files[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(content_files)
    
    print(f"💾 Saved discovered content: {DISCOVERED_CONTENT_CSV}")


def main():
    """Run comprehensive content scan."""
    
    print("="*70)
    print("🔍 COMPREHENSIVE HOME DIRECTORY CONTENT SCAN")
    print("="*70)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Scan
    content_files = scan_home_directory()
    
    if not content_files:
        print("\n⚠️  No content files found!")
        return
    
    # Analyze
    print("\n📊 Analyzing content...")
    analysis = analyze_content(content_files)
    
    # Save
    print("\n💾 Saving results...")
    save_results(content_files, analysis)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 SCAN SUMMARY")
    print("="*70)
    
    print(f"\n📄 Total Content Files: {analysis['total_files']:,}")
    print(f"💾 Total Size: {analysis['total_size_mb']:,} MB")
    
    print("\n📂 Top File Types:")
    for ftype, count in list(analysis['by_type'].items())[:10]:
        print(f"   {ftype:30s} {count:,}")
    
    print("\n📁 Top Directories:")
    for dir_name, count in list(analysis['by_dir'].items())[:15]:
        print(f"   {dir_name:40s} {count:,}")
    
    print("\n" + "="*70)
    print("✅ SCAN COMPLETE!")
    print("="*70)
    print(f"\n📁 Results saved to: {OUTPUT_DIR}")
    print("="*70)


if __name__ == "__main__":
    main()
