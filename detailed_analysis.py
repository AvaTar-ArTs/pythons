#!/usr/bin/env python3
import os
import re
import ast
from pathlib import Path
from collections import defaultdict

def extract_functions_and_classes(filepath):
    """Extract function and class names from Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(3000)  # Read first 3KB for structure
        
        tree = ast.parse(content)
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return functions[:5], classes[:3]  # Limit output
    except:
        return [], []

def get_docstring(filepath):
    """Extract module docstring"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        in_docstring = False
        docstring = ""
        for i, line in enumerate(lines[:30]):
            if '"""' in line or "'''" in line:
                if not in_docstring:
                    in_docstring = True
                    docstring = line.split('"""')[1] if '"""' in line else line.split("'''")[1]
                else:
                    in_docstring = False
                    break
            elif in_docstring:
                docstring += " " + line.strip()
        
        return docstring.strip()[:80] if docstring else ""
    except:
        return ""

base_path = "/Users/steven/Music/nocturneMelodies"

# Create detailed reports per category
categories = {
    'cover': [],
    'transcript': [],
    'mp3': [],
    'suno': [],
    'web': [],
    'distribution': [],
    'ai': [],
}

def categorize(name_lower):
    if any(x in name_lower for x in ['cover', 'download_cover', 'image', 'artwork']):
        return 'cover'
    if any(x in name_lower for x in ['transcript', 'transcribe', 'analysis', 'analyzer']):
        return 'transcript'
    if any(x in name_lower for x in ['mp3', 'rename', 'organize', 'consolidate', 'move_music', 'deduplicat', 'scan_']):
        return 'mp3'
    if any(x in name_lower for x in ['suno', 'uuid', 'extract']):
        return 'suno'
    if any(x in name_lower for x in ['html', 'gallery', 'web', 'site', 'mobile']):
        return 'web'
    if any(x in name_lower for x in ['distro', 'spotify', 'soundcloud', 'distrokid']):
        return 'distribution'
    if any(x in name_lower for x in ['nocturnememory', 'ai_', 'knowledge', 'autotag', 'embeddings', 'index']):
        return 'ai'
    return None

for root, dirs, filenames in os.walk(base_path):
    dirs[:] = [d for d in dirs if d not in ('venv', '.venv', 'venv313')]
    
    for fname in filenames:
        if fname.endswith('.py'):
            full_path = os.path.join(root, fname)
            name_lower = fname.lower()
            cat = categorize(name_lower)
            
            if cat:
                funcs, classes = extract_functions_and_classes(full_path)
                purpose = get_docstring(full_path)
                
                categories[cat].append({
                    'path': full_path,
                    'name': fname,
                    'purpose': purpose,
                    'functions': funcs,
                    'classes': classes
                })

# Print detailed categorized output
for cat_name in ['cover', 'transcript', 'mp3', 'suno', 'web', 'distribution', 'ai']:
    items = categories[cat_name]
    print(f"\n{'='*80}")
    print(f"{cat_name.upper()} ({len(items)} files)")
    print('='*80)
    
    for item in items:
        path = item['path']
        rel_path = path.replace(base_path, '').lstrip('/')
        print(f"\n{rel_path}")
        if item['purpose']:
            print(f"  Purpose: {item['purpose']}")
        if item['classes']:
            print(f"  Classes: {', '.join(item['classes'])}")
        if item['functions']:
            print(f"  Functions: {', '.join(item['functions'][:3])}")

