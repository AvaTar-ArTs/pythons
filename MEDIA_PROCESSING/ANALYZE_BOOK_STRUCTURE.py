#!/usr/bin/env python3
"""
Analyze the actual book text to determine TRUE chapter structure
"""

from pathlib import Path
import re

# Read the actual book text
BOOK_TEXT = Path("/Users/steven/Documents/markD/As-a-Man-Thinketh/as-a-man-thinketh.cleaned.md")

print("=" * 80)
print("?? ANALYZING ACTUAL BOOK STRUCTURE")
print("=" * 80)
print()

with open(BOOK_TEXT, 'r') as f:
    content = f.read()

print(f"Book length: {len(content)} characters")
print()

# Find chapter markers
chapters = []
lines = content.split('\n')

current_chapter = None
for i, line in enumerate(lines):
    # Look for chapter headings (usually ## or bold)
    if line.startswith('#') or line.isupper() and len(line) > 5 and len(line) < 100:
        chapters.append({
            'line': i,
            'title': line.strip('#').strip(),
            'preview': lines[i+1:i+3] if i+1 < len(lines) else []
        })

print(f"Found {len(chapters)} potential chapters:")
print()

for ch in chapters[:20]:  # Show first 20
    print(f"{ch['line']:5d} | {ch['title']}")

print()
print("=" * 80)

# Search for specific chapter names we see in audio files
chapter_names = [
    'foreword',
    'thought and character',
    'effect of thought on circumstances',
    'effect of thought on health',
    'thought and purpose',
    'thought factor in achievement',
    'visions and ideals',
    'serenity'
]

print("SEARCHING FOR KNOWN CHAPTERS:")
print()

for name in chapter_names:
    # Case-insensitive search
    pattern = re.compile(re.escape(name), re.IGNORECASE)
    matches = pattern.findall(content)
    
    if matches:
        # Find context
        for match in content.split('\n'):
            if pattern.search(match):
                print(f"? {name.upper()}")
                print(f"  ? {match.strip()}")
                break
    else:
        print(f"? {name} - NOT FOUND")

print()
