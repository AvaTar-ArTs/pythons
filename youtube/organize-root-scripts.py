#!/usr/bin/env python3
"""
Organize Root Python Scripts by Content

Moves all remaining .py files from root into appropriate category folders.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import ast

class RootScriptOrganizer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Category keywords
        self.categories = {
            '01-core-tools': ['tool', 'utility', 'fixer', 'organizer', 'analyzer', 'deep', 'intelligent'],
            '02-youtube-automation': ['youtube', 'yt-', 'ytube', 'video', 'playlist'],
            '03-ai-creative-tools': ['openai', 'gpt', 'claude', 'gemini', 'groq', 'xai', 'mistral', 'llm', 'ai-'],
            '04-web-scraping': ['scrape', 'crawler', 'spider', 'seo', 'backlink'],
            '05-social-media': ['instagram', 'tiktok', 'reddit', 'twitter', 'facebook', 'telegram', 'bot'],
            '06-media-processing': ['image', 'audio', 'mp3', 'mp4', 'video', 'upscale', 'resize', 'convert'],
            '07-utilities': ['file', 'folder', 'directory', 'backup', 'migrate', 'move', 'copy', 'clean'],
            '08-analysis-tools': ['analyze', 'analyzer', 'analysis', 'metric', 'stat', 'monitor'],
            '09-documentation': ['doc', 'document', 'pydoc', 'sphinx', 'markdown'],
            '10-archived-projects': []  # Catch-all
        }
        
        self.stats = {'moved': 0, 'errors': 0}
    
    def categorize_script(self, file_path: Path) -> str:
        """Determine category for a Python script."""
        name = file_path.stem.lower()
        
        # Check filename keywords
        for category, keywords in self.categories.items():
            if category == '10-archived-projects':
                continue
            
            if any(keyword in name for keyword in keywords):
                return category
        
        # Try content analysis
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()[:5000]  # First 5000 chars
            
            content_lower = content.lower()
            
            # Check imports and content
            if any(x in content_lower for x in ['youtube', 'yt-dlp', 'pytube']):
                return '02-youtube-automation'
            
            if any(x in content_lower for x in ['openai', 'anthropic', 'gemini']):
                return '03-ai-creative-tools'
            
            if any(x in content_lower for x in ['instabot', 'instaclient', 'selenium']):
                return '05-social-media'
            
            if any(x in content_lower for x in ['pil', 'pillow', 'opencv', 'ffmpeg']):
                return '06-media-processing'
        except:
            pass
        
        # Default to utilities or archived
        if any(x in name for x in ['test', 'example', 'temp', 'old']):
            return '10-archived-projects'
        
        return '07-utilities'
    
    def organize(self, dry_run=True):
        """Organize all Python scripts in root."""
        print(f"\n{'='*80}")
        print("🔧 ORGANIZING ROOT PYTHON SCRIPTS")
        print(f"{'='*80}\n")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}\n")
        
        # Get all .py files in root
        root_scripts = [f for f in self.target_dir.glob("*.py")]
        
        print(f"Found {len(root_scripts)} Python scripts in root\n")
        
        categorized = {}
        for category in self.categories.keys():
            categorized[category] = []
        
        # Categorize each file
        for script in sorted(root_scripts):
            category = self.categorize_script(script)
            categorized[category].append(script)
        
        # Show summary
        print("📊 CATEGORIZATION:\n")
        for category, scripts in sorted(categorized.items()):
            if scripts:
                print(f"{category}: {len(scripts)} scripts")
                if len(scripts) <= 3:
                    for s in scripts:
                        print(f"  - {s.name}")
                else:
                    for s in scripts[:3]:
                        print(f"  - {s.name}")
                    print(f"  ... and {len(scripts) - 3} more")
                print()
        
        # Move files
        if not dry_run:
            print(f"\n🚀 Moving files...\n")
            
            for category, scripts in categorized.items():
                category_dir = self.target_dir / category
                category_dir.mkdir(exist_ok=True)
                
                for script in scripts:
                    target = category_dir / script.name
                    
                    # Handle duplicates
                    counter = 1
                    original_target = target
                    while target.exists():
                        stem = original_target.stem
                        suffix = original_target.suffix
                        target = category_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    try:
                        shutil.move(str(script), str(target))
                        self.stats['moved'] += 1
                    except Exception as e:
                        print(f"❌ Error moving {script.name}: {e}")
                        self.stats['errors'] += 1
        
        print(f"\n{'='*80}")
        print("✅ COMPLETE!")
        print(f"{'='*80}\n")
        print(f"Scripts Categorized: {len(root_scripts)}")
        if not dry_run:
            print(f"Scripts Moved: {self.stats['moved']}")
            if self.stats['errors'] > 0:
                print(f"Errors: {self.stats['errors']}")
        print()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Organize Root Scripts')
    parser.add_argument('--target', default='.', help='Target directory')
    parser.add_argument('--live', action='store_true', help='Execute moves')
    
    args = parser.parse_args()
    
    organizer = RootScriptOrganizer(args.target)
    organizer.organize(dry_run=not args.live)

if __name__ == "__main__":
    main()

