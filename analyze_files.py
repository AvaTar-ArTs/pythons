#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def get_purpose_from_file(filepath):
    """Extract one-line purpose from docstring or filename"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)
            
            # Look for module docstring
            lines = content.split('\n')
            for i, line in enumerate(lines[:50]):
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    # Found docstring
                    if i + 1 < len(lines):
                        doc_line = lines[i+1].strip()
                        if doc_line and not doc_line.startswith('"""') and not doc_line.startswith("'''"):
                            return doc_line[:100]
    except:
        pass
    return ""

def categorize_file(filepath, filename):
    """Categorize file based on name and content"""
    name_lower = filename.lower()
    
    # Cover/image handling
    if any(x in name_lower for x in ['cover', 'download_cover', 'image', 'artwork', 'album_art']):
        return 'cover'
    
    # Transcript/analysis
    if any(x in name_lower for x in ['transcript', 'transcribe', 'analysis', 'analyzer', 'analyze']):
        return 'transcript'
    
    # MP3 organization
    if any(x in name_lower for x in ['mp3', 'rename', 'organize', 'consolidate', 'move_music', 'organize_album', 'deduplicat', 'scan_']):
        return 'mp3'
    
    # Suno integration
    if any(x in name_lower for x in ['suno', 'suno_', 'uuid', 'download_suno', 'extract']):
        return 'suno'
    
    # Web/HTML
    if any(x in name_lower for x in ['html', 'gallery', 'web', 'site', 'mobile']):
        return 'web'
    
    # Distribution
    if any(x in name_lower for x in ['distro', 'spotify', 'soundcloud', 'distrokid', 'distribution', 'curator']):
        return 'distribution'
    
    # AI/ML/Knowledge
    if any(x in name_lower for x in ['nocturnememory', 'ai_', 'ai-', 'knowledge', 'autotag', 'embeddings', 'index']):
        return 'ai'
    
    return 'other'

base_path = "/Users/steven/Music/nocturneMelodies"
files = []

for root, dirs, filenames in os.walk(base_path):
    dirs[:] = [d for d in dirs if d not in ('venv', '.venv', 'venv313')]
    
    for fname in filenames:
        if fname.endswith('.py'):
            full_path = os.path.join(root, fname)
            files.append(full_path)

# Group by category
categories = {
    'cover': [],
    'transcript': [],
    'mp3': [],
    'suno': [],
    'web': [],
    'distribution': [],
    'ai': [],
    'other': []
}

for filepath in sorted(files):
    filename = os.path.basename(filepath)
    cat = categorize_file(filepath, filename)
    purpose = get_purpose_from_file(filepath)
    
    categories[cat].append({
        'path': filepath,
        'name': filename,
        'purpose': purpose
    })

# Print results
for cat_name in ['cover', 'transcript', 'mp3', 'suno', 'web', 'distribution', 'ai', 'other']:
    cat_files = categories[cat_name]
    print(f"\n=== {cat_name.upper()} ({len(cat_files)} files) ===")
    for item in cat_files:
        print(f"{item['path']}")
        if item['purpose']:
            print(f"  -> {item['purpose']}")

print(f"\n\nTotal: {len(files)} files")
