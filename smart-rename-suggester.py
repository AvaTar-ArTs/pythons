#!/usr/bin/env python3
"""
Smart Rename Suggester
Analyzes the CSV and provides intelligent rename suggestions
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class SmartRenameSuggester:
    """Intelligent rename suggestions based on actual functionality"""
    
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)
        self.scripts = []
        self.load_csv()
        
    def load_csv(self):
        """Load CSV data"""
        with open(self.csv_path, 'r') as f:
            reader = csv.DictReader(f)
            self.scripts = list(reader)
        print(f"✅ Loaded {len(self.scripts)} scripts")
    
    def suggest_rename(self, script):
        """Suggest better name based on description and functionality"""
        current = script['current_name']
        desc = script['description'].lower()
        apis = script['apis_used'].lower()
        category = script['category']
        
        # Skip if already renamed or has good name
        if current in ['etsy-listing-generator.py', 'personal-ai-assistant.py', 
                       'seo-content-organizer.py', 'file-diff-viewer.py']:
            return current, "KEEP", "Already renamed"
        
        # Extract key action and subject from description
        
        # Social Media patterns
        if 'instagram' in current:
            if 'follow' in desc and 'unfollow' in desc:
                return 'instagram-auto-follow-unfollow.py', 'RENAME', 'Auto-follows and unfollows users'
            elif 'bot' in desc or 'automat' in desc:
                if 'like' in desc:
                    return 'instagram-auto-liker.py', 'RENAME', 'Automatically likes posts'
                elif 'comment' in desc:
                    return 'instagram-auto-commenter.py', 'RENAME', 'Automatically comments'
                elif 'upload' in desc or 'post' in desc:
                    return 'instagram-auto-poster.py', 'RENAME', 'Automatically posts content'
                else:
                    return 'instagram-bot.py', 'RENAME', 'General Instagram bot'
            elif 'scrap' in desc or 'download' in desc:
                return 'instagram-content-scraper.py', 'RENAME', 'Scrapes Instagram content'
            elif 'whisper' in current:
                return 'instagram-whisper-captions.py', 'RENAME', 'Generates captions with Whisper'
        
        # YouTube patterns
        if 'youtube' in current:
            if 'upload' in desc:
                return 'youtube-auto-uploader.py', 'RENAME', 'Uploads videos to YouTube'
            elif 'short' in current or 'short' in desc:
                return 'youtube-shorts-uploader.py', 'RENAME', 'Uploads YouTube Shorts'
            elif 'download' in desc:
                return 'youtube-video-downloader.py', 'RENAME', 'Downloads YouTube videos'
            elif 'comment' in desc:
                return 'youtube-auto-commenter.py', 'RENAME', 'Auto-comments on videos'
        
        # Reddit patterns  
        if 'reddit' in current:
            if 'post' in desc or 'submit' in desc:
                return 'reddit-auto-poster.py', 'RENAME', 'Posts to Reddit'
            elif 'scrap' in desc:
                return 'reddit-content-scraper.py', 'RENAME', 'Scrapes Reddit content'
        
        # Image analysis patterns
        if category == 'Image Analysis':
            if 'gpt' in apis or 'vision' in desc:
                if 'csv' in desc or 'enrich' in desc:
                    return 'gpt-vision-csv-enricher.py', 'RENAME', 'Enriches CSV with GPT Vision'
                elif 'batch' in desc:
                    return 'gpt-vision-batch-analyzer.py', 'RENAME', 'Batch analyzes images'
                else:
                    return 'gpt-vision-image-analyzer.py', 'RENAME', 'Analyzes images with GPT Vision'
            elif 'duplicate' in desc:
                return 'find-duplicate-images.py', 'RENAME', 'Finds duplicate images'
            elif 'upscale' in desc or 'enhance' in desc:
                return 'upscale-images.py', 'RENAME', 'Upscales/enhances images'
            elif 'compress' in desc or 'optimize' in desc:
                return 'optimize-images.py', 'RENAME', 'Compresses/optimizes images'
            elif 'metadata' in desc or 'exif' in desc:
                return 'extract-image-metadata.py', 'RENAME', 'Extracts image metadata'
        
        # Audio patterns
        if category == 'Audio Generation':
            if 'tts' in desc or 'text-to-speech' in desc or 'speech' in desc:
                if 'openai' in apis:
                    return 'openai-tts-generator.py', 'RENAME', 'OpenAI text-to-speech'
                elif 'elevenlabs' in apis:
                    return 'elevenlabs-tts-generator.py', 'RENAME', 'ElevenLabs TTS'
                elif 'aws' in current or 'polly' in current:
                    return current, 'KEEP', 'Already clear'
                else:
                    return 'text-to-speech-generator.py', 'RENAME', 'Generic TTS'
            elif 'audiobook' in desc:
                return 'audiobook-producer.py', 'RENAME', 'Creates audiobooks'
            elif 'normalize' in desc:
                return 'normalize-audio.py', 'RENAME', 'Normalizes audio levels'
            elif 'convert' in desc:
                if 'aiff' in current and 'mp3' in current:
                    return current, 'KEEP', 'Already clear'
                return 'audio-converter.py', 'RENAME', 'Converts audio formats'
        
        # Code analysis patterns
        if category == 'Code Analysis':
            if 'complexity' in desc:
                return 'python-complexity-analyzer.py', 'RENAME', 'Analyzes code complexity'
            elif 'quality' in desc or 'lint' in desc:
                return 'code-quality-analyzer.py', 'RENAME', 'Checks code quality'
            elif 'review' in desc:
                return 'python-code-review-system.py', 'RENAME', 'Reviews Python code'
            elif 'ast' in desc or 'deep' in desc:
                return 'deep-code-analyzer.py', 'RENAME', 'Deep AST analysis'
        
        # File organization patterns
        if category == 'File Organization':
            if 'duplicate' in desc:
                return 'find-duplicate-files.py', 'RENAME', 'Finds duplicates'
            elif 'clean' in desc and 'filename' in desc:
                return 'clean-filenames.py', 'RENAME', 'Cleans up filenames'
            elif 'flatten' in desc:
                return 'flatten-directories.py', 'RENAME', 'Flattens directory structure'
            elif 'organiz' in desc:
                return 'organize-files-by-type.py', 'RENAME', 'Organizes by type'
            elif 'sort' in desc:
                return 'sort-files-intelligent.py', 'RENAME', 'Intelligently sorts files'
        
        # Default: needs review
        return current, 'REVIEW', 'Needs manual review'
    
    def analyze_and_suggest(self):
        """Analyze all scripts and provide suggestions"""
        suggestions = defaultdict(list)
        
        for script in self.scripts:
            suggested_name, action, reason = self.suggest_rename(script)
            
            script['suggested_name'] = suggested_name
            script['action'] = action
            script['rename_reason'] = reason
            
            suggestions[script['category']].append(script)
        
        return suggestions
    
    def print_suggestions_by_category(self, suggestions, limit_per_cat=20):
        """Print suggestions organized by category"""
        
        # Sort categories by file count
        sorted_cats = sorted(suggestions.items(), key=lambda x: len(x[1]), reverse=True)
        
        for category, scripts in sorted_cats:
            print(f"\n{'='*80}")
            print(f"📂 {category.upper()} ({len(scripts)} files)")
            print('='*80)
            
            # Show top scripts in this category
            for i, script in enumerate(sorted(scripts, key=lambda x: x['current_name'])[:limit_per_cat], 1):
                current = script['current_name']
                suggested = script['suggested_name']
                action = script['action']
                desc = script['description'][:100]
                
                if action == 'RENAME' and current != suggested:
                    print(f"\n{i}. {current}")
                    print(f"   → {suggested}")
                    print(f"   What it does: {desc}")
                    print(f"   Reason: {script['rename_reason']}")
                elif action == 'DELETE':
                    print(f"\n{i}. ❌ DELETE: {current}")
                    print(f"   Reason: {script['rename_reason']}")
                elif action == 'KEEP':
                    print(f"\n{i}. ✅ KEEP: {current}")
            
            if len(scripts) > limit_per_cat:
                print(f"\n   ... and {len(scripts) - limit_per_cat} more files")
    
    def save_suggestions_csv(self):
        """Save suggestions to new CSV"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = self.csv_path.parent / f'_rename_suggestions_{timestamp}.csv'
        
        fieldnames = [
            'current_name',
            'suggested_name', 
            'action',
            'category',
            'description',
            'rename_reason',
            'apis_used',
            'lines',
            'size_kb',
            'reason'
        ]
        
        # Sort by category, then current name
        sorted_scripts = sorted(self.scripts, key=lambda x: (x['category'], x['current_name']))
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_scripts)
        
        return output_path


def main():
    csv_path = Path.home() / 'pythons' / '_all_scripts_analysis_20251106_132427.csv'
    
    suggester = SmartRenameSuggester(csv_path)
    suggestions = suggester.analyze_and_suggest()
    
    print("\n🤖 SMART RENAME SUGGESTIONS")
    print("="*80)
    print("\nAnalyzing all 767 scripts and providing intelligent suggestions...")
    
    suggester.print_suggestions_by_category(suggestions, limit_per_cat=10)
    
    # Save updated CSV
    output_csv = suggester.save_suggestions_csv()
    
    print(f"\n{'='*80}")
    print(f"💾 Suggestions saved to:")
    print(f"   {output_csv}")
    print(f"\n💡 Review the CSV and update 'suggested_name' where needed")


if __name__ == '__main__':
    main()
