#!/usr/bin/env python3
"""
Topic Analysis Script
Analyzes HTML files in 'organized/' to propose a better, topic-based structure.
"""

from pathlib import Path
from collections import defaultdict, Counter
import re

ORGANIZED_DIR = Path("organized")

# Expanded Topic Keywords
TOPICS = {
    'Music & Audio': ['music', 'song', 'lyrics', 'audio', 'mp3', 'band', 'album', 'sound', 'spotify', 'playlist', 'track', 'guitar', 'piano', 'composer'],
    'Movies & Video': ['movie', 'film', 'cinema', 'video', 'youtube', 'mp4', 'watch', 'stream', 'netflix', 'clip', 'vlog', 'shorts', 'reel', 'production', 'studio'],
    'AI & Prompts': ['prompt', 'midjourney', 'dalle', 'stable diffusion', 'leonardo.ai', 'gpt', 'llm', 'openai', 'claude', 'artificial intelligence', 'generative'],
    'Design & Art': ['design', 'art', 'illustration', 'logo', 'graphic', 'sketch', 'drawing', 'creative', 'canvas', 'svg', 'png', 'jpg', 'photoshop'],
    'Tech & Coding': ['python', 'code', 'script', 'programming', 'developer', 'github', 'api', 'terminal', 'bash', 'linux', 'macos', 'software', 'app'],
    'Business & SEO': ['marketing', 'seo', 'business', 'finance', 'money', 'crypto', 'sales', 'brand', 'strategy', 'analytics', 'linkedin', 'social media'],
    'Personal & Health': ['health', 'recipe', 'food', 'diet', 'journal', 'diary', 'personal', 'fitness', 'workout', 'mindfulness'],
}

print("="*80)
print(f"🧠 ANALYZING TOPICS IN: {ORGANIZED_DIR.resolve()}")
print("="*80)

topic_counts = Counter()
file_mappings = defaultdict(list)
uncategorized = []

# Get all files
all_files = list(ORGANIZED_DIR.rglob("*.html"))
print(f"\nScanning {len(all_files):,} files...")

for i, f in enumerate(all_files, 1):
    try:
        # Read content sample (first 2k chars usually enough for context)
        content = f.read_text(errors='ignore')[:2000].lower()
        filename = f.name.lower()
        
        # Determine Topic
        best_topic = None
        max_matches = 0
        
        for topic, keywords in TOPICS.items():
            matches = 0
            # Check filename (weighted higher)
            if any(k in filename for k in keywords):
                matches += 3
            
            # Check content
            matches += sum(1 for k in keywords if k in content)
            
            if matches > max_matches and matches > 0:
                max_matches = matches
                best_topic = topic
        
        if best_topic:
            topic_counts[best_topic] += 1
            file_mappings[best_topic].append(f)
        else:
            uncategorized.append(f)
            
    except Exception:
        pass
        
    if i % 500 == 0:
        print(f"   Analyzed {i} files...")

print("\n" + "="*80)
print("📊 PROPOSED TOPIC STRUCTURE")
print("="*80)

for topic, count in topic_counts.most_common():
    print(f"📁 {topic:20s}: {count:,} files")

print(f"📁 Uncategorized       : {len(uncategorized):,} files")

print("\nExamples from 'Music & Audio':")
for f in file_mappings['Music & Audio'][:5]:
    print(f"   - {f.name}")

print("\nExamples from 'Movies & Video':")
for f in file_mappings['Movies & Video'][:5]:
    print(f"   - {f.name}")
