#!/usr/bin/env python3
"""
Complete Content Classifier
Classifies ALL your content by type: MUSIC vs VIDEO vs PODCAST vs AUDIOBOOK
All are YOUR originals, just different content types
"""

from pathlib import Path
from typing import Dict, List
import json
import subprocess
from collections import defaultdict
from config_manager import get_config


class ContentClassifier:
    """Classify your content by type and purpose"""
    
    def __init__(self):
        self.config = get_config()
        
        # Your content patterns
        self.content_types = {
            'MUSIC': {
                'duration': (30, 360),  # 30s - 6min
                'keywords': [
                    'beautiful mess', 'heroes', 'junkyard', 'moonlight',
                    'alley', 'trash', 'dance', 'love', 'echo', 'whisper',
                    'dream', 'night', 'shadow', 'willow'
                ],
                'artists': ['avatararts', 'avatar arts', 'suno', 'music'],
                'purpose': 'Streaming/Albums'
            },
            
            'GAMING_VIDEO': {
                'duration': (30, 600),
                'keywords': [
                    '[eso]', 'moonhunters', 'avatar mod', 'game',
                    'gameplay', 'walkthrough', 'blind run'
                ],
                'purpose': 'YouTube Gaming Channel'
            },
            
            'POLITICAL_PODCAST': {
                'duration': (30, 3600),
                'keywords': [
                    'project2025', 'project 2025', 'america', 'conservative',
                    'bureaucracy', 'administration', 'constitution',
                    'trump', 'political', 'democracy', 'federal'
                ],
                'purpose': 'Podcast/Commentary Channel'
            },
            
            'TUTORIAL_VIDEO': {
                'duration': (60, 3600),
                'keywords': [
                    'tutorial', 'canva', 'photoshop', 'design',
                    'how to', 'wrap', 'generative fill'
                ],
                'purpose': 'Tutorial/Education Channel'
            },
            
            'STORY_NARRATION': {
                'duration': (60, 1200),
                'keywords': [
                    'elion', 'divine quest', 'shadow syndicate',
                    'tale', 'lament', 'story', 'narration'
                ],
                'purpose': 'Story/Narration Content'
            },
            
            'SPIRITUAL_CONTENT': {
                'duration': (10, 600),
                'keywords': [
                    'metaphor', 'empowerment', 'mystical', 'divine',
                    'universal', 'law of attraction', 'self-discovery',
                    'true measure', 'secret thoughts'
                ],
                'purpose': 'Spiritual/Self-Help Content'
            },
            
            'SHORT_CLIP': {
                'duration': (0, 30),
                'keywords': [],
                'purpose': 'Social Media Clips/Reels'
            },
        }
    
    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze file and classify"""
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json',
                   '-show_format', str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode != 0:
                return None
            
            data = json.loads(result.stdout)
            format_info = data.get('format', {})
            tags = format_info.get('tags', {})
            
            duration = float(format_info.get('duration', 0))
            title = tags.get('title') or tags.get('TITLE') or ''
            artist = tags.get('artist') or tags.get('ARTIST') or ''
            
            # Build search text
            search_text = f"{file_path.name.lower()} {title.lower()} {artist.lower()}"
            
            # Classify
            content_type = self._classify(duration, search_text)
            
            return {
                'file': file_path.name,
                'path': str(file_path),
                'duration': duration,
                'content_type': content_type,
                'purpose': self.content_types.get(content_type, {}).get('purpose', 'Review'),
                'title': title,
                'artist': artist,
                'size_mb': round(file_path.stat().st_size / (1024 * 1024), 2),
            }
            
        except Exception as e:
            return None
    
    def _classify(self, duration: float, search_text: str) -> str:
        """Classify based on duration and keywords"""
        
        # Check each content type
        scores = {}
        
        for content_type, config in self.content_types.items():
            score = 0
            
            # Duration match
            min_dur, max_dur = config['duration']
            if min_dur <= duration <= max_dur:
                score += 10
            
            # Keyword match
            for keyword in config.get('keywords', []):
                if keyword in search_text:
                    score += 5
            
            if score > 0:
                scores[content_type] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        # Default based on duration
        if duration < 30:
            return 'SHORT_CLIP'
        elif duration <= 360:
            return 'MUSIC'
        else:
            return 'POLITICAL_PODCAST'
    
    def classify_collection(self, directory: Path) -> Dict:
        """Classify entire collection"""
        
        print("\n" + "=" * 80)
        print("  COMPLETE CONTENT CLASSIFICATION")
        print("  All YOUR content - organized by type & purpose")
        print("=" * 80 + "\n")
        
        # Get all audio files
        audio_files = []
        for ext in ['.mp3', '.wav', '.m4a', '.flac']:
            audio_files.extend(list(directory.rglob(f'*{ext}')))
        
        print(f"Analyzing {len(audio_files)} files...\n")
        
        classified = defaultdict(list)
        
        for i, audio_file in enumerate(audio_files, 1):
            if i % 50 == 0:
                print(f"  Processed {i}/{len(audio_files)}...")
            
            info = self.analyze_file(audio_file)
            if info:
                classified[info['content_type']].append(info)
        
        print(f"\n? Analyzed {len(audio_files)} files\n")
        
        return classified
    
    def show_results(self, classified: Dict):
        """Show classification results"""
        
        print("=" * 80)
        print("  YOUR CONTENT BY TYPE & PURPOSE")
        print("=" * 80 + "\n")
        
        # Sort by count
        for content_type in sorted(classified.keys(), key=lambda x: len(classified[x]), reverse=True):
            files = classified[content_type]
            total_duration = sum(f['duration'] for f in files)
            purpose = files[0]['purpose'] if files else ''
            
            print(f"\n{content_type}: {len(files)} files ({total_duration/60:.1f} minutes)")
            print(f"Purpose: {purpose}")
            print("-" * 80)
            
            # Show samples
            for info in files[:5]:
                print(f"  ? {info['file']}")
                if info['duration']:
                    print(f"    Duration: {info['duration']:.1f}s")
            
            if len(files) > 5:
                print(f"  ... and {len(files) - 5} more")
        
        # Summary
        print("\n" + "=" * 80)
        print("  ORGANIZATION RECOMMENDATIONS")
        print("=" * 80 + "\n")
        
        print("Organize YOUR content by purpose:\n")
        
        for content_type, files in classified.items():
            purpose = self.content_types.get(content_type, {}).get('purpose', 'Review')
            print(f"  {content_type:20s} ? {purpose}")
        
        print("\nAll are YOUR originals, just different content types!")
    
    def create_organization_plan(self, classified: Dict) -> Dict:
        """Create organization plan by content type"""
        
        base_dir = Path.home() / 'Music' / 'nocTurneMeLoDieS' / 'ORGANIZED_BY_TYPE'
        
        plan = {
            'MUSIC': base_dir / 'MUSIC' / 'Suno_Songs',
            'GAMING_VIDEO': base_dir / 'VIDEO' / 'Gaming',
            'POLITICAL_PODCAST': base_dir / 'PODCAST' / 'Political',
            'TUTORIAL_VIDEO': base_dir / 'VIDEO' / 'Tutorials',
            'STORY_NARRATION': base_dir / 'NARRATION' / 'Stories',
            'SPIRITUAL_CONTENT': base_dir / 'SPIRITUAL' / 'Metaphors',
            'SHORT_CLIP': base_dir / 'CLIPS' / 'Short_Form',
        }
        
        print("\n" + "=" * 80)
        print("  PROPOSED ORGANIZATION")
        print("=" * 80 + "\n")
        
        print("~/Music/nocTurneMeLoDieS/ORGANIZED_BY_TYPE/")
        for content_type, target_dir in plan.items():
            if content_type in classified:
                count = len(classified[content_type])
                print(f"  ??? {target_dir.relative_to(base_dir)}")
                print(f"  ?   ({count} files)")
        
        return plan


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Content Type Classifier')
    parser.add_argument('directory', nargs='?', 
                       default=str(Path.home() / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED/YOUR_SUNO_SONGS'))
    
    args = parser.parse_args()
    
    classifier = ContentClassifier()
    classified = classifier.classify_collection(Path(args.directory))
    classifier.show_results(classified)
    plan = classifier.create_organization_plan(classified)
    
    print("\nTo organize by type, run:")
    print("  python content_classifier.py organize")
