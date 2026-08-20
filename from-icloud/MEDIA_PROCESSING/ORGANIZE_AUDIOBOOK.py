#!/usr/bin/env python3
"""
Organize "As A Man Thinketh" audiobook chapters into logical sections
"""

from pathlib import Path
import shutil

BASE = Path("/Users/steven/Documents/Audiobooks/As_A_Man_Thinketh")

print("=" * 80)
print("?? ORGANIZING AUDIOBOOK CHAPTERS")
print("=" * 80)
print()

# List all files
files = sorted([f for f in BASE.iterdir() if f.is_file()])

print(f"Found {len(files)} files")
print()

# Group by section
sections = {
    '1_Foreword': [],
    '2_Thought_and_Character': [],
    '3_Effect_of_Thought': [],
    '4_Thought_and_Purpose': [],
    '5_Thought_Factor_Achievement': [],
    '6_Visions_and_Ideals': [],
    '7_Serenity': [],
    '8_Other': []
}

for f in files:
    name = f.name.lower()
    
    if 'foreword' in name:
        sections['1_Foreword'].append(f)
    elif 'thought-and-character' in name or 'thought_and_character' in name:
        sections['2_Thought_and_Character'].append(f)
    elif 'effect' in name:
        sections['3_Effect_of_Thought'].append(f)
    elif 'purpose' in name:
        sections['4_Thought_and_Purpose'].append(f)
    elif 'achievement' in name or 'factor' in name:
        sections['5_Thought_Factor_Achievement'].append(f)
    elif 'vision' in name or 'ideal' in name:
        sections['6_Visions_and_Ideals'].append(f)
    elif 'serenity' in name or 'calmness' in name:
        sections['7_Serenity'].append(f)
    else:
        sections['8_Other'].append(f)

# Show groupings
for section, files_list in sections.items():
    if files_list:
        print(f"{section}: {len(files_list)} files")

print()

# Create section folders
DRY_RUN = False

if DRY_RUN:
    print("DRY RUN - showing what would happen:")
    print()

organized = 0
for section, files_list in sections.items():
    if not files_list:
        continue
    
    section_dir = BASE / section
    
    if not DRY_RUN:
        section_dir.mkdir(exist_ok=True)
    else:
        print(f"Would create: {section_dir.name}/")
    
    for f in sorted(files_list):
        dest = section_dir / f.name
        if not DRY_RUN:
            shutil.move(str(f), str(dest))
            organized += 1
        else:
            print(f"  ? {f.name}")

if DRY_RUN:
    print()
    print("Set DRY_RUN = False to execute")
else:
    print()
    print(f"? Organized {organized} files into {len([s for s in sections.values() if s])} sections")

print()
