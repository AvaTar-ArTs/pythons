"""
Summary of categorize_abilities.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import csv
import os
import re
from collections import defaultdict

def categorize_dna(dna_string):
    dna = dna_string.lower()
    
    if any(x in dna for x in ['openai', 'anthropic', 'langchain', 'llm', 'gpt', 'axolotl', 'agent']):
        return "AI_LLM_Tools"
    if any(x in dna for x in ['instabot', 'instapy', 'instagram', 'facebook', 'twitter', 'social']):
        return "Social_Media_Automation"
    if any(x in dna for x in ['ffmpeg', 'pil', 'pydub', 'audio', 'video', 'image', 'upscale', 'cv2', 'moviepy']):
        return "Media_Processing"
    if any(x in dna for x in ['pandas', 'numpy', 'csv', 'json', 'data', 'analyze', 'matplotlib', 'plotly']):
        return "Data_Analysis"
    if any(x in dna for x in ['alembic', 'sqlalchemy', 'sqlite', 'db', 'postgres', 'supabase']):
        return "Database_Infrastructure"
    if any(x in dna for x in ['googleapiclient', 'pytube', 'youtube', 'yt_dlp']):
        return "YouTube_Tools"
    if any(x in dna for x in ['markdown', 'sphinx', 'docs', 'docstring', 'mkdocs']):
        return "Documentation_Tools"
    
    return "General_Utilities"

input_file = 'structural_dedupe_report.csv'
categories = defaultdict(list)

print("📂 Categorizing unique abilities...")

with open(input_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        dna = row['Abilities_Summary']
        cat = categorize_dna(dna)
        
        # Parse DNA for cleaner output
        # Format: f:func1,func2|c:Class1|i:import1,import2
        parts = row['Abilities_Summary'].split('|')
        funcs = parts[0].replace('f:', '') if len(parts) > 0 else ""
        classes = parts[1].replace('c:', '') if len(parts) > 1 else ""
        imports = parts[2].replace('i:', '') if len(parts) > 2 else ""
        
        # Get a friendly name from the first path
        paths = row['Paths'].split('; ')
        primary_path = paths[0]
        filename = os.path.basename(primary_path)
        
        categories[cat].append({
            'Tool_Name': filename,
            'Occurrences': row['Occurrences'],
            'Functions': funcs,
            'Classes': classes,
            'Imports': imports,
            'Primary_Path': primary_path,
            'All_Paths': row['Paths']
        })

# Create individual CSVs for each category
for cat, items in categories.items():
    output_path = f"Ability_Preview_{cat}.csv"
    with open(output_path, 'w', newline='') as f:
        fieldnames = ['Tool_Name', 'Occurrences', 'Functions', 'Classes', 'Imports', 'Primary_Path', 'All_Paths']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)
    print(f"   Created: {output_path} ({len(items)} unique tools)")

print("\n✨ Done! You now have a CSV 'Preview' for each major ability cluster.")
