#!/usr/bin/env python3
"""
Comprehensive duplicate cleanup script.
1. Remove .history/ folder duplicates (keep only latest versions)
2. Consolidate Python scripts (keep one canonical version)
3. Remove duplicate PDFs/HTMLs (keep organized versions in subdirectories)
4. Clean up "copy" variants after verifying they're identical
"""

import sys
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import ast


def calculate_hash(file_path):
    """Calculate MD5 hash of file."""
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception:
        return None


def extract_python_functions(file_path):
    """Extract function signatures from Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        tree = ast.parse(content)
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                func_sig = f"{node.name}({', '.join(args)})"
                functions.append(func_sig)
        return tuple(sorted(functions))
    except:
        return None


def cleanup_history_duplicates(root_path, dry_run=True):
    """Remove .history/ folder duplicates, keeping only latest versions."""
    print("\n" + "=" * 80)
    print("1. CLEANING UP .history/ FOLDER DUPLICATES")
    print("=" * 80)
    
    history_path = root_path / ".history"
    if not history_path.exists():
        print("   No .history folder found")
        return []
    
    # Find all files in .history
    history_files = list(history_path.rglob('*'))
    history_files = [f for f in history_files if f.is_file()]
    
    print(f"   Found {len(history_files)} files in .history/")
    
    # Group by base name (without timestamp)
    file_groups = defaultdict(list)
    for file_path in history_files:
        name = file_path.name
        # Extract base name (remove timestamp pattern like _20251202233615)
        base_name = re.sub(r'_\d{14}', '', name)
        base_name = re.sub(r'_\d{8}', '', base_name)
        file_groups[base_name].append(file_path)
    
    # For each group, keep only the newest file
    to_remove = []
    kept = []
    
    for base_name, files in file_groups.items():
        if len(files) > 1:
            # Sort by modification time (newest first)
            files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
            kept.append(files_sorted[0])
            to_remove.extend(files_sorted[1:])
    
    print(f"   Found {len(to_remove)} duplicate history files to remove")
    print(f"   Keeping {len(kept)} latest versions")
    
    if not dry_run:
        removed_count = 0
        for file_path in to_remove:
            try:
                file_path.unlink()
                removed_count += 1
            except Exception as e:
                print(f"     ⚠️  Error removing {file_path}: {e}")
        print(f"   ✓ Removed {removed_count} files")
    else:
        print(f"   [DRY RUN] Would remove {len(to_remove)} files")
        for file_path in to_remove[:10]:
            print(f"     - {file_path.relative_to(root_path)}")
        if len(to_remove) > 10:
            print(f"     ... and {len(to_remove) - 10} more")
    
    return to_remove


def consolidate_python_scripts(root_path, dry_run=True):
    """Consolidate Python scripts, keeping canonical versions."""
    print("\n" + "=" * 80)
    print("2. CONSOLIDATING PYTHON SCRIPTS")
    print("=" * 80)
    
    # Find all Python files
    python_files = list(root_path.rglob('*.py'))
    python_files = [f for f in python_files if f.is_file()]
    
    print(f"   Found {len(python_files)} Python files")
    
    # Group by function signatures
    func_groups = defaultdict(list)
    for py_file in python_files:
        funcs = extract_python_functions(py_file)
        if funcs:
            func_groups[funcs].append(py_file)
    
    # Find groups with multiple files (functional duplicates)
    duplicates = {k: v for k, v in func_groups.items() if len(v) > 1}
    
    print(f"   Found {len(duplicates)} groups of functionally identical scripts")
    
    to_remove = []
    kept = []
    
    for func_sig, files in duplicates.items():
        # Prefer files NOT in .history, NOT in subdirectories with "copy" or "(1)"
        def score_file(f):
            score = 0
            rel_path = str(f.relative_to(root_path))
            if '.history' in rel_path:
                score -= 1000
            if 'copy' in f.name.lower() or '(1)' in f.name or '(2)' in f.name:
                score -= 100
            # Prefer files in tools/scripts or root
            if 'tools/scripts' in rel_path:
                score += 50
            if '/' not in rel_path or rel_path.count('/') == 1:
                score += 20
            # Prefer newer files
            score += f.stat().st_mtime / 1000000
            return score
        
        files_sorted = sorted(files, key=score_file, reverse=True)
        kept.append(files_sorted[0])
        to_remove.extend(files_sorted[1:])
    
    print(f"   Found {len(to_remove)} duplicate Python scripts to remove")
    print(f"   Keeping {len(kept)} canonical versions")
    
    if not dry_run:
        removed_count = 0
        for file_path in to_remove:
            try:
                file_path.unlink()
                removed_count += 1
            except Exception as e:
                print(f"     ⚠️  Error removing {file_path}: {e}")
        print(f"   ✓ Removed {removed_count} files")
    else:
        print(f"   [DRY RUN] Would remove {len(to_remove)} files")
        for file_path in to_remove[:10]:
            print(f"     - {file_path.relative_to(root_path)}")
        if len(to_remove) > 10:
            print(f"     ... and {len(to_remove) - 10} more")
    
    return to_remove


def remove_duplicate_pdfs_htmls(root_path, dry_run=True):
    """Remove duplicate PDFs/HTMLs, keeping organized versions in subdirectories."""
    print("\n" + "=" * 80)
    print("3. REMOVING DUPLICATE PDFs/HTMLs")
    print("=" * 80)
    
    # Find PDFs and HTMLs
    pdf_files = list(root_path.rglob('*.pdf'))
    html_files = list(root_path.rglob('*.html'))
    all_files = [f for f in pdf_files + html_files if f.is_file()]
    
    print(f"   Found {len(pdf_files)} PDFs and {len(html_files)} HTMLs")
    
    # Group by filename
    name_groups = defaultdict(list)
    for file_path in all_files:
        name_groups[file_path.name].append(file_path)
    
    # Find duplicates
    duplicates = {k: v for k, v in name_groups.items() if len(v) > 1}
    
    print(f"   Found {len(duplicates)} duplicate filenames")
    
    to_remove = []
    kept = []
    
    for name, files in duplicates.items():
        # Prefer files in organized subdirectories (pdf/, html/, etc.)
        def score_file(f):
            score = 0
            rel_path = str(f.relative_to(root_path))
            # Prefer files in pdf/ or html/ subdirectories
            if 'pdf/' in rel_path or 'html/' in rel_path:
                score += 100
            # Prefer files in other organized subdirectories
            if '/' in rel_path and not rel_path.startswith('.'):
                score += 50
            # Penalize root directory files
            if '/' not in rel_path:
                score -= 10
            # Prefer newer files
            score += f.stat().st_mtime / 1000000
            return score
        
        files_sorted = sorted(files, key=score_file, reverse=True)
        kept.append(files_sorted[0])
        to_remove.extend(files_sorted[1:])
    
    print(f"   Found {len(to_remove)} duplicate PDFs/HTMLs to remove")
    print(f"   Keeping {len(kept)} organized versions")
    
    if not dry_run:
        removed_count = 0
        for file_path in to_remove:
            try:
                file_path.unlink()
                removed_count += 1
            except Exception as e:
                print(f"     ⚠️  Error removing {file_path}: {e}")
        print(f"   ✓ Removed {removed_count} files")
    else:
        print(f"   [DRY RUN] Would remove {len(to_remove)} files")
        for file_path in to_remove[:10]:
            print(f"     - {file_path.relative_to(root_path)}")
        if len(to_remove) > 10:
            print(f"     ... and {len(to_remove) - 10} more")
    
    return to_remove


def cleanup_copy_variants(root_path, dry_run=True):
    """Clean up 'copy' variants after verifying they're identical."""
    print("\n" + "=" * 80)
    print("4. CLEANING UP 'COPY' VARIANTS")
    print("=" * 80)
    
    # Find files with "copy", "(1)", "(2)", etc. in name
    all_files = list(root_path.rglob('*'))
    copy_files = []
    
    for file_path in all_files:
        if file_path.is_file():
            name_lower = file_path.name.lower()
            if 'copy' in name_lower or re.search(r'\(\d+\)', name_lower):
                copy_files.append(file_path)
    
    print(f"   Found {len(copy_files)} files with 'copy' or number variants")
    
    # Find originals and their copies
    to_remove = []
    verified = []
    
    for copy_file in copy_files:
        # Try to find original
        name = copy_file.name
        # Remove copy indicators
        original_name = re.sub(r'\s*\(copy\)', '', name, flags=re.IGNORECASE)
        original_name = re.sub(r'\s*\(1\)', '', original_name)
        original_name = re.sub(r'\s*\(2\)', '', original_name)
        original_name = re.sub(r'\s*copy', '', original_name, flags=re.IGNORECASE)
        
        # Look for original in same directory
        original_path = copy_file.parent / original_name
        
        if original_path.exists() and original_path != copy_file:
            # Verify they're identical
            hash_copy = calculate_hash(copy_file)
            hash_original = calculate_hash(original_path)
            
            if hash_copy and hash_original and hash_copy == hash_original:
                to_remove.append(copy_file)
                verified.append((original_path, copy_file))
    
    print(f"   Verified {len(verified)} copy variants are identical to originals")
    print(f"   Found {len(to_remove)} copy variants to remove")
    
    if not dry_run:
        removed_count = 0
        for file_path in to_remove:
            try:
                file_path.unlink()
                removed_count += 1
            except Exception as e:
                print(f"     ⚠️  Error removing {file_path}: {e}")
        print(f"   ✓ Removed {removed_count} files")
    else:
        print(f"   [DRY RUN] Would remove {len(to_remove)} files")
        for file_path in to_remove[:10]:
            print(f"     - {file_path.relative_to(root_path)}")
        if len(to_remove) > 10:
            print(f"     ... and {len(to_remove) - 10} more")
    
    return to_remove


import re

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cleanup_duplicates.py <directory> [--execute]")
        print("\nExample:")
        print("  python cleanup_duplicates.py /path/to/dir          # Dry run")
        print("  python cleanup_duplicates.py /path/to/dir --execute # Actually remove")
        sys.exit(1)
    
    root_path = Path(sys.argv[1])
    dry_run = '--execute' not in sys.argv
    
    if not root_path.exists():
        print(f"Error: Directory not found: {root_path}")
        sys.exit(1)
    
    print("=" * 80)
    print("DUPLICATE CLEANUP")
    print("=" * 80)
    print(f"\nDirectory: {root_path}")
    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTE'}")
    
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No files will be deleted")
        print("   Use --execute flag to actually remove files")
    
    all_removed = []
    
    # 1. Clean up .history duplicates
    removed1 = cleanup_history_duplicates(root_path, dry_run)
    all_removed.extend(removed1)
    
    # 2. Consolidate Python scripts
    removed2 = consolidate_python_scripts(root_path, dry_run)
    all_removed.extend(removed2)
    
    # 3. Remove duplicate PDFs/HTMLs
    removed3 = remove_duplicate_pdfs_htmls(root_path, dry_run)
    all_removed.extend(removed3)
    
    # 4. Clean up copy variants
    removed4 = cleanup_copy_variants(root_path, dry_run)
    all_removed.extend(removed4)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\n  Total files to remove: {len(all_removed)}")
    print(f"  From .history/: {len(removed1)}")
    print(f"  Python scripts: {len(removed2)}")
    print(f"  PDFs/HTMLs: {len(removed3)}")
    print(f"  Copy variants: {len(removed4)}")
    
    if not dry_run:
        print(f"\n✅ Cleanup complete!")
    else:
        print(f"\n💡 Run with --execute to perform cleanup")
