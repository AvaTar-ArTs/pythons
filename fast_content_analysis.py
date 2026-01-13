#!/usr/bin/env python3
"""
Fast content and function analysis - optimized for large directories.
"""

import sys
import hashlib
import ast
from pathlib import Path
from collections import defaultdict
import re


def extract_python_functions(file_path):
    """Extract function signatures from Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    func_sig = f"{node.name}({', '.join(args)})"
                    functions.append(func_sig)
            return sorted(functions)
        except:
            return []
    except:
        return None


def quick_hash(file_path, max_size=1024*1024):
    """Quick hash of file (first 1MB + size)."""
    try:
        stat = file_path.stat()
        if stat.st_size == 0:
            return "empty"
        if stat.st_size > max_size:
            # For large files, use size + first chunk
            with open(file_path, 'rb') as f:
                chunk = f.read(8192)
            return hashlib.md5(f"{stat.st_size}_{chunk}".encode()).hexdigest()
        else:
            # Small file, hash entire content
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
    except:
        return None


print("=" * 80)
print("FAST CONTENT & FUNCTION ANALYSIS")
print("=" * 80)

if len(sys.argv) < 2:
    print("Usage: python fast_content_analysis.py <directory>")
    sys.exit(1)

root_path = Path(sys.argv[1])
if not root_path.exists():
    print(f"Error: Directory not found: {root_path}")
    sys.exit(1)

print(f"\n📂 Analyzing: {root_path}")

# Collect files
print(f"\n📋 Scanning files...")
all_files = []
python_files = []

for file_path in root_path.rglob('*'):
    if file_path.is_file():
        try:
            stat = file_path.stat()
            rel_path = str(file_path.relative_to(root_path))
            all_files.append({
                'path': file_path,
                'rel_path': rel_path,
                'size': stat.st_size,
                'ext': file_path.suffix.lower(),
                'name': file_path.name
            })
            if file_path.suffix.lower() == '.py':
                python_files.append(file_path)
        except:
            pass

print(f"   Found {len(all_files):,} files")
print(f"   Python files: {len(python_files):,}")

# Exact duplicates (quick hash)
print(f"\n🔍 Finding exact duplicates...")
hash_groups = defaultdict(list)
for file_info in all_files:
    if file_info['size'] < 50 * 1024 * 1024:  # < 50MB
        file_hash = quick_hash(file_info['path'])
        if file_hash:
            hash_groups[file_hash].append(file_info['rel_path'])

exact_dupes = {k: v for k, v in hash_groups.items() if len(v) > 1}
print(f"   Found {len(exact_dupes)} groups of exact duplicates")

# Python function analysis
print(f"\n🐍 Analyzing Python functions...")
python_funcs = {}
for py_file in python_files[:200]:  # Limit to 200 files
    rel_path = str(py_file.relative_to(root_path))
    funcs = extract_python_functions(py_file)
    if funcs:
        func_key = tuple(funcs)
        python_funcs[rel_path] = funcs

# Group Python files by function signatures
func_groups = defaultdict(list)
for path, funcs in python_funcs.items():
    if funcs:
        func_groups[tuple(funcs)].append(path)

python_dupes = {k: v for k, v in func_groups.items() if len(v) > 1}
print(f"   Found {len(python_dupes)} Python files with identical functions")

# Report
print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

print(f"\n🔍 EXACT DUPLICATES")
if exact_dupes:
    total_dupe_files = sum(len(v) for v in exact_dupes.values())
    print(f"   Groups: {len(exact_dupes)}")
    print(f"   Total duplicate files: {total_dupe_files}")
    print(f"\n   Top duplicate groups:")
    for hash_key, file_list in list(exact_dupes.items())[:10]:
        print(f"   {len(file_list)} copies:")
        for rel_path in file_list[:3]:
            print(f"     - {rel_path}")
        if len(file_list) > 3:
            print(f"     ... and {len(file_list) - 3} more")
else:
    print("   ✅ No exact duplicates found")

print(f"\n🐍 PYTHON FUNCTIONAL DUPLICATES")
if python_dupes:
    print(f"   Found {len(python_dupes)} groups of Python files with identical functions")
    print(f"\n   Files with same functions:")
    for func_sig, file_list in list(python_dupes.items())[:15]:
        print(f"   Functions: {', '.join(func_sig[:3])}{'...' if len(func_sig) > 3 else ''}")
        print(f"      Found in {len(file_list)} files:")
        for rel_path in file_list:
            print(f"        - {rel_path}")
        print()
else:
    print("   ✅ No Python files with identical functions found")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
