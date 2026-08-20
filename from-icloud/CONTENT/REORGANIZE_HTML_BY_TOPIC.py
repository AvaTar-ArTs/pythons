#!/usr/bin/env python3
"""
Reorganize HTML by Topic
Moves files from 'organized/' into a new topic-based structure 'organized_topics/'.
"""

from pathlib import Path
import shutil
from collections import defaultdict
import csv
from datetime import datetime

# Config
SOURCE_DIR = Path("organized")
DEST_DIR = Path("organized_topics")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = Path(f"HTML_TOPIC_REORG_LOG_{TIMESTAMP}.csv")

# Topic Definitions (Same as Analysis)
TOPICS = {
    'Music & Audio': ['music', 'song', 'lyrics', 'audio', 'mp3', 'band', 'album', 'sound', 'spotify', 'playlist', 'track', 'guitar', 'piano', 'composer', 'suno'],
    'Movies & Video': ['movie', 'film', 'cinema', 'video', 'youtube', 'mp4', 'watch', 'stream', 'netflix', 'clip', 'vlog', 'shorts', 'reel', 'production', 'studio', 'anim'],
    'AI & Prompts': ['prompt', 'midjourney', 'dalle', 'stable diffusion', 'leonardo.ai', 'gpt', 'llm', 'openai', 'claude', 'artificial intelligence', 'generative', 'bot'],
    'Design & Art': ['design', 'art', 'illustration', 'logo', 'graphic', 'sketch', 'drawing', 'creative', 'canvas', 'svg', 'png', 'jpg', 'photoshop', 'gallery', 'image'],
    'Tech & Coding': ['python', 'code', 'script', 'programming', 'developer', 'github', 'api', 'terminal', 'bash', 'linux', 'macos', 'software', 'app', 'css', 'html', 'json'],
    'Business & SEO': ['marketing', 'seo', 'business', 'finance', 'money', 'crypto', 'sales', 'brand', 'strategy', 'analytics', 'linkedin', 'social media', 'shop', 'store'],
    'Personal & Health': ['health', 'recipe', 'food', 'diet', 'journal', 'diary', 'personal', 'fitness', 'workout', 'mindfulness'],
}

def get_topic(filename, content):
    best_topic = 'Uncategorized'
    max_matches = 0
    
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    for topic, keywords in TOPICS.items():
        matches = 0
        # Heavy weight on filename
        if any(k in filename_lower for k in keywords):
            matches += 3
        
        # Light weight on content
        matches += sum(1 for k in keywords if k in content_lower)
        
        if matches > max_matches and matches > 0:
            max_matches = matches
            best_topic = topic
            
    return best_topic

print("="*80)
print(f"🔄 REORGANIZING BY TOPIC")
print(f"Source: {SOURCE_DIR}")
print(f"Dest:   {DEST_DIR}")
print("="*80)

# 1. Scan Source
print("\n1. Scanning Source Files...")
source_files = list(SOURCE_DIR.rglob("*.html"))
print(f"   Found {len(source_files):,} files to re-organize.")

if not source_files:
    print("   No files found. Exiting.")
    exit()

# 2. Move Files
print("\n2. Categorizing & Moving...")
moved_count = 0
stats = defaultdict(int)

DEST_DIR.mkdir(exist_ok=True)

with open(LOG_FILE, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['original_path', 'new_path', 'topic'])
    
    for i, f in enumerate(source_files, 1):
        try:
            content = f.read_text(errors='ignore')[:2000]
            topic = get_topic(f.name, content)
            
            target_dir = DEST_DIR / topic
            target_dir.mkdir(exist_ok=True)
            
            new_path = target_dir / f.name
            
            # Handle Collisions
            counter = 1
            while new_path.exists():
                stem = f.stem
                suffix = f.suffix
                new_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            shutil.move(str(f), str(new_path))
            
            writer.writerow([str(f), str(new_path), topic])
            stats[topic] += 1
            moved_count += 1
            
        except Exception as e:
            print(f"   Error moving {f.name}: {e}")
        
        if i % 500 == 0:
            print(f"   Processed {i}/{len(source_files)}...")

# 3. Cleanup Empty Dirs in Source
print("\n3. Cleaning up empty source directories...")
for p in sorted(SOURCE_DIR.rglob('*'), key=lambda x: len(x.parts), reverse=True):
    if p.is_dir() and not any(p.iterdir()):
        try:
            p.rmdir()
        except:
            pass

# Remove source root if empty
if SOURCE_DIR.exists() and not any(SOURCE_DIR.iterdir()):
    SOURCE_DIR.rmdir()

print("\n" + "="*80)
print("✅ REORGANIZATION COMPLETE")
print("="*80)
for topic, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
    print(f"📁 {topic:20s}: {count:,} files")

print(f"\nTotal Moved: {moved_count:,}")
print(f"New Location: {DEST_DIR.resolve()}")
