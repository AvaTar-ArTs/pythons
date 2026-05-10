"""
Summary of generate_master_migration.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import csv
import os
import hashlib
from collections import defaultdict

def categorize_dna(dna_string):
    dna = dna_string.lower()
    if any(x in dna for x in ['openai', 'anthropic', 'langchain', 'llm', 'gpt', 'axolotl', 'agent']):
        return "AI-ML"
    if any(x in dna for x in ['instabot', 'instapy', 'instagram', 'facebook', 'twitter', 'social']):
        return "Social-Automation"
    if any(x in dna for x in ['ffmpeg', 'pil', 'pydub', 'audio', 'video', 'image', 'upscale', 'cv2', 'moviepy']):
        return "Media-Processing"
    if any(x in dna for x in ['pandas', 'numpy', 'csv', 'json', 'data', 'analyze', 'matplotlib', 'plotly']):
        return "Data-Analysis"
    if any(x in dna for x in ['alembic', 'sqlalchemy', 'sqlite', 'db', 'postgres', 'supabase']):
        return "Infrastructure"
    if any(x in dna for x in ['googleapiclient', 'pytube', 'youtube', 'yt_dlp']):
        return "YouTube-Tools"
    if any(x in dna for x in ['markdown', 'sphinx', 'docs', 'docstring', 'mkdocs']):
        return "Documentation"
    return "Utilities"

def get_project_context(path):
    parts = path.split('/')
    if 'AVATARARTS' in parts:
        idx = parts.index('AVATARARTS')
        if idx + 1 < len(parts): return parts[idx+1]
    if 'pythons' in parts:
        idx = parts.index('pythons')
        if idx + 1 < len(parts): return parts[idx+1]
    if 'GitHub' in parts:
        idx = parts.index('GitHub')
        if idx + 1 < len(parts): return parts[idx+1]
    return "General"

# 1. Load Structural DNA
dna_map = {} # path -> hash
dna_details = {} # hash -> dna_string
clusters = defaultdict(list) # hash -> list of paths

print("📊 Loading structural data...")
with open('structural_dedupe_report.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dna_hash = row['DNA_Hash']
        paths = row['Paths'].split('; ')
        dna_details[dna_hash] = row['Abilities_Summary']
        for p in paths:
            dna_map[p] = dna_hash
            clusters[dna_hash].append(p)

# 2. Process all scripts for Migration
master_plan = []
processed_hashes = set()

print("🚀 Generating Master Before --> After mapping...")
with open('real_python_scripts.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        curr_path = row['Path']
        filename = row['Filename']
        dna_hash = dna_map.get(curr_path)
        
        if not dna_hash: continue
        
        category = categorize_dna(dna_details[dna_hash])
        context = get_project_context(curr_path)
        
        # Decide if this is the "Primary" copy
        # We prefer copies in 'final_sorted_scripts' or '00_ACTIVE'
        is_primary = False
        if dna_hash not in processed_hashes:
            # Simple heuristic: the first one we find is master unless we find a better one in the cluster
            # But since we want a clean mapping, we'll pick the "best" path from the cluster
            best_path = curr_path
            cluster_paths = clusters[dna_hash]
            for cp in cluster_paths:
                if 'final_sorted_scripts' in cp or '00_ACTIVE' in cp:
                    best_path = cp
                    break
            
            if curr_path == best_path:
                status = "KEEP (Master)"
                new_path = f"~/Documents/CsV/{category}/{context}/Production/{filename}"
                processed_hashes.add(dna_hash)
            else:
                status = "ARCHIVE (Duplicate)"
                new_path = f"~/Documents/CsV/Archive/Duplicates/{dna_hash[:8]}/{filename}"
        else:
            status = "ARCHIVE (Duplicate)"
            new_path = f"~/Documents/CsV/Archive/Duplicates/{dna_hash[:8]}/{filename}"

        master_plan.append({
            'Filename': filename,
            'Status': status,
            'Category': category,
            'Before_Path': curr_path,
            'After_Path': new_path,
            'Ability_DNA': dna_hash[:12]
        })

# 3. Write Master Plan
output_file = 'MASTER_BEFORE_AFTER_MIGRATION.csv'
with open(output_file, 'w', newline='') as f:
    fieldnames = ['Filename', 'Status', 'Category', 'Before_Path', 'After_Path', 'Ability_DNA']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(master_plan)

print(f"✨ MASTER PLAN COMPLETE: {len(master_plan)} items mapped.")
print(f"File saved to: {output_file}")
