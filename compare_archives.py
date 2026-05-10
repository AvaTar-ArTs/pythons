#!/usr/bin/env python3
"""
Summary of compare_archives.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

from pathlib import Path
import tarfile
import zipfile
from datetime import datetime
import csv

archive1 = Path.home() / "Music/nocTurneMeLoDieS_BEFORE_CLEANUP_20251226_102542.tar.gz"
archive2 = Path.home() / "Music/nocTurneMeLoDieS/zip/NocTurnE-meLoDieS-20251225T050332Z-3-002.zip"
target_dir = Path.home() / "Music/nocturnemelodies"

report_file = Path.home() / "archive_comparison_report.txt"

with open(report_file, 'w') as report:
    report.write("=" * 70 + "\n")
    report.write("ARCHIVE COMPARISON REPORT\n")
    report.write("=" * 70 + "\n\n")
    report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Check what exists
    report.write("📁 FILE CHECK\n")
    report.write("-" * 70 + "\n")
    
    archive1_exists = archive1.exists()
    archive2_exists = archive2.exists()
    target_exists = target_dir.exists()
    
    if archive1_exists:
        size1 = archive1.stat().st_size / (1024**3)
        report.write(f"✅ Archive 1: {archive1.name}\n")
        report.write(f"   Size: {size1:.2f} GB\n")
        report.write(f"   Path: {archive1}\n\n")
    else:
        report.write(f"❌ Archive 1 not found: {archive1}\n\n")
    
    if archive2_exists:
        size2 = archive2.stat().st_size / (1024**3)
        report.write(f"✅ Archive 2: {archive2.name}\n")
        report.write(f"   Size: {size2:.2f} GB\n")
        report.write(f"   Path: {archive2}\n\n")
    else:
        report.write(f"❌ Archive 2 not found: {archive2}\n\n")
    
    if target_exists:
        total_size = sum(f.stat().st_size for f in target_dir.rglob('*') if f.is_file()) / (1024**3)
        file_count = sum(1 for f in target_dir.rglob('*') if f.is_file())
        report.write(f"✅ Target directory: {target_dir}\n")
        report.write(f"   Size: {total_size:.2f} GB\n")
        report.write(f"   Files: {file_count}\n\n")
    else:
        report.write(f"❌ Target directory not found: {target_dir}\n\n")
    
    # Extract archive contents
    report.write("=" * 70 + "\n")
    report.write("EXTRACTING CONTENTS\n")
    report.write("-" * 70 + "\n")
    
    archive1_files = {}
    if archive1_exists:
        report.write(f"\n📦 Archive 1 contents...\n")
        try:
            with tarfile.open(archive1, 'r:gz') as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        archive1_files[member.name] = member.size
            report.write(f"   Found {len(archive1_files)} files\n")
        except Exception as e:
            report.write(f"   ⚠️  Error: {e}\n")
    
    archive2_files = {}
    if archive2_exists:
        report.write(f"\n📦 Archive 2 contents...\n")
        try:
            with zipfile.ZipFile(archive2, 'r') as zipf:
                for info in zipf.infolist():
                    if not info.is_dir():
                        archive2_files[info.filename] = info.file_size
            report.write(f"   Found {len(archive2_files)} files\n")
        except Exception as e:
            report.write(f"   ⚠️  Error: {e}\n")
    
    target_files = {}
    if target_exists:
        report.write(f"\n📁 Target directory contents...\n")
        for file_path in target_dir.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(target_dir)
                target_files[str(rel_path)] = file_path.stat().st_size
        report.write(f"   Found {len(target_files)} files\n")
    
    # Compare
    report.write("\n" + "=" * 70 + "\n")
    report.write("COMPARISON RESULTS\n")
    report.write("=" * 70 + "\n")
    
    def normalize_paths(files_dict):
        return {k.replace('\\', '/'): v for k, v in files_dict.items()}
    
    if archive1_files and target_files:
        report.write(f"\n📊 Archive 1 vs Target Directory:\n")
        report.write("-" * 70 + "\n")
        
        a1_norm = normalize_paths(archive1_files)
        t_norm = normalize_paths(target_files)
        
        common = set(a1_norm.keys()) & set(t_norm.keys())
        only_a1 = set(a1_norm.keys()) - set(t_norm.keys())
        only_target = set(t_norm.keys()) - set(a1_norm.keys())
        
        report.write(f"   Archive 1 files: {len(a1_norm)}\n")
        report.write(f"   Target dir files: {len(t_norm)}\n")
        report.write(f"   Common files: {len(common)}\n")
        report.write(f"   Only in Archive 1: {len(only_a1)}\n")
        report.write(f"   Only in Target: {len(only_target)}\n")
        
        size_diffs = []
        for file in common:
            if a1_norm[file] != t_norm[file]:
                size_diffs.append((file, a1_norm[file], t_norm[file]))
        
        if size_diffs:
            report.write(f"   Files with size differences: {len(size_diffs)}\n")
            report.write(f"\n   First 10 size differences:\n")
            for file, a1_size, t_size in size_diffs[:10]:
                report.write(f"      {file}\n")
                report.write(f"         Archive 1: {a1_size:,} bytes\n")
                report.write(f"         Target: {t_size:,} bytes\n")
    
    if archive2_files and target_files:
        report.write(f"\n📊 Archive 2 vs Target Directory:\n")
        report.write("-" * 70 + "\n")
        
        a2_norm = normalize_paths(archive2_files)
        t_norm = normalize_paths(target_files)
        
        common = set(a2_norm.keys()) & set(t_norm.keys())
        only_a2 = set(a2_norm.keys()) - set(t_norm.keys())
        only_target = set(t_norm.keys()) - set(a2_norm.keys())
        
        report.write(f"   Archive 2 files: {len(a2_norm)}\n")
        report.write(f"   Target dir files: {len(t_norm)}\n")
        report.write(f"   Common files: {len(common)}\n")
        report.write(f"   Only in Archive 2: {len(only_a2)}\n")
        report.write(f"   Only in Target: {len(only_target)}\n")
        
        size_diffs = []
        for file in common:
            if a2_norm[file] != t_norm[file]:
                size_diffs.append((file, a2_norm[file], t_norm[file]))
        
        if size_diffs:
            report.write(f"   Files with size differences: {len(size_diffs)}\n")
    
    if archive1_files and archive2_files:
        report.write(f"\n📊 Archive 1 vs Archive 2:\n")
        report.write("-" * 70 + "\n")
        
        a1_norm = normalize_paths(archive1_files)
        a2_norm = normalize_paths(archive2_files)
        
        common = set(a1_norm.keys()) & set(a2_norm.keys())
        only_a1 = set(a1_norm.keys()) - set(a2_norm.keys())
        only_a2 = set(a2_norm.keys()) - set(a1_norm.keys())
        
        report.write(f"   Archive 1 files: {len(a1_norm)}\n")
        report.write(f"   Archive 2 files: {len(a2_norm)}\n")
        report.write(f"   Common files: {len(common)}\n")
        report.write(f"   Only in Archive 1: {len(only_a1)}\n")
        report.write(f"   Only in Archive 2: {len(only_a2)}\n")
        
        size_diffs = []
        for file in common:
            if a1_norm[file] != a2_norm[file]:
                size_diffs.append((file, a1_norm[file], a2_norm[file]))
        
        if size_diffs:
            report.write(f"   Files with size differences: {len(size_diffs)}\n")
    
    report.write("\n" + "=" * 70 + "\n")

print(f"✅ Comparison report saved to: {report_file}")
