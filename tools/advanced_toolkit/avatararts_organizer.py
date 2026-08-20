#!/usr/bin/env python3
"""
AvatarArts Music Organizer
Specialized organizer for YOUR_SUNO_SONGS and avatararts content
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
from collections import defaultdict
import json
import re
import shutil
from datetime import datetime

from file_intelligence import FileAnalyzer, FileFingerprint
from config_manager import get_config


class AvatarArtsOrganizer:
    """Organize avatararts music from YOUR_SUNO_SONGS"""
    
    def __init__(self, base_music_dir: Optional[Path] = None):
        self.config = get_config()
        self.base_music_dir = base_music_dir or Path.home() / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED'
        self.your_songs_dir = self.base_music_dir / 'YOUR_SUNO_SONGS'
        self.analyzer = FileAnalyzer(Path.home() / '.file_intelligence.db')
        
        # Category mappings for avatararts
        self.categories = {
            'cinematic': ['epic', 'orchestral', 'dramatic', 'film', 'trailer'],
            'ambient': ['ambient', 'atmospheric', 'meditation', 'calm', 'peaceful'],
            'electronic': ['synth', 'edm', 'electronic', 'techno', 'house'],
            'folk': ['folk', 'acoustic', 'indie', 'singer-songwriter'],
            'experimental': ['experimental', 'avant-garde', 'abstract', 'glitch'],
            'classical': ['classical', 'piano', 'violin', 'chamber', 'symphony'],
            'rock': ['rock', 'guitar', 'metal', 'punk'],
            'jazz': ['jazz', 'blues', 'swing', 'bebop'],
            'world': ['world', 'ethnic', 'tribal', 'traditional']
        }
    
    def scan_your_songs(self) -> List[FileFingerprint]:
        """Scan YOUR_SUNO_SONGS directory"""
        if not self.your_songs_dir.exists():
            print(f"Directory not found: {self.your_songs_dir}")
            return []
        
        print(f"Scanning: {self.your_songs_dir}")
        print("=" * 80)
        
        audio_files = []
        for ext in ['.mp3', '.wav', '.m4a', '.flac']:
            audio_files.extend(self.your_songs_dir.glob(f'*{ext}'))
        
        print(f"Found {len(audio_files)} audio files")
        
        fingerprints = []
        for audio_file in audio_files:
            fp = self.analyzer.analyze_file(audio_file)
            if fp:
                fingerprints.append(fp)
        
        return fingerprints
    
    def categorize_by_metadata(self, fingerprints: List[FileFingerprint]) -> Dict[str, List[FileFingerprint]]:
        """Categorize files by artist and genre"""
        by_artist = defaultdict(list)
        by_category = defaultdict(list)
        uncategorized = []
        
        for fp in fingerprints:
            # Check if it's avatararts
            artist = None
            if fp.metadata:
                artist = fp.metadata.get('artist', '').lower()
            
            if not artist:
                # Try to extract from filename
                if 'avatararts' in fp.path.name.lower() or 'avatar' in fp.path.name.lower():
                    artist = 'avatararts'
            
            if artist:
                by_artist[artist].append(fp)
                
                # Categorize by genre/style
                category = self._determine_category(fp)
                by_category[category].append(fp)
            else:
                uncategorized.append(fp)
        
        return {
            'by_artist': dict(by_artist),
            'by_category': dict(by_category),
            'uncategorized': uncategorized
        }
    
    def _determine_category(self, fp: FileFingerprint) -> str:
        """Determine category from metadata and filename"""
        text_to_check = fp.path.stem.lower()
        
        if fp.metadata:
            if fp.metadata.get('genre'):
                text_to_check += ' ' + fp.metadata['genre'].lower()
            if fp.metadata.get('album'):
                text_to_check += ' ' + fp.metadata['album'].lower()
            if fp.metadata.get('title'):
                text_to_check += ' ' + fp.metadata['title'].lower()
        
        # Check against category keywords
        for category, keywords in self.categories.items():
            if any(keyword in text_to_check for keyword in keywords):
                return category
        
        return 'general'
    
    def organize_avatararts_collection(self, dry_run: bool = True):
        """Organize all avatararts music"""
        print("AvatarArts Music Organization")
        print("=" * 80)
        print()
        
        # Scan files
        fingerprints = self.scan_your_songs()
        
        if not fingerprints:
            print("No files to organize")
            return
        
        print(f"\nAnalyzed {len(fingerprints)} files")
        print()
        
        # Categorize
        categorized = self.categorize_by_metadata(fingerprints)
        
        # Create organization plan
        plan = self._create_organization_plan(categorized)
        
        # Show summary
        self._show_plan_summary(plan)
        
        # Execute if not dry run
        if not dry_run:
            self._execute_plan(plan)
        else:
            print("\n??  DRY RUN - No files will be moved")
            print("Run with --execute to actually move files")
    
    def _create_organization_plan(self, categorized: Dict) -> Dict:
        """Create detailed organization plan"""
        plan = {
            'moves': [],
            'stats': {
                'total': 0,
                'by_artist': {},
                'by_category': {}
            }
        }
        
        # Organize by artist
        for artist, files in categorized['by_artist'].items():
            artist_dir = self.base_music_dir / 'BY_ARTIST' / self._sanitize_name(artist)
            
            for fp in files:
                category = self._determine_category(fp)
                target_dir = artist_dir / category
                target_path = target_dir / fp.path.name
                
                plan['moves'].append({
                    'source': fp.path,
                    'target': target_path,
                    'artist': artist,
                    'category': category,
                    'size': fp.size
                })
                
                plan['stats']['total'] += 1
                plan['stats']['by_artist'][artist] = plan['stats']['by_artist'].get(artist, 0) + 1
                plan['stats']['by_category'][category] = plan['stats']['by_category'].get(category, 0) + 1
        
        return plan
    
    def _show_plan_summary(self, plan: Dict):
        """Show organization plan summary"""
        print("Organization Plan")
        print("-" * 80)
        print()
        
        print(f"Total files to organize: {plan['stats']['total']}")
        print()
        
        print("By Artist:")
        for artist, count in sorted(plan['stats']['by_artist'].items()):
            print(f"  {artist}: {count} files")
        
        print()
        print("By Category:")
        for category, count in sorted(plan['stats']['by_category'].items()):
            print(f"  {category}: {count} files")
        
        print()
        print("Proposed Structure:")
        print(f"  {self.base_music_dir}/")
        print("    ??? BY_ARTIST/")
        for artist in sorted(plan['stats']['by_artist'].keys()):
            print(f"        ??? {artist}/")
            # Show categories for this artist
            artist_categories = set(
                move['category'] for move in plan['moves'] 
                if move['artist'] == artist
            )
            for category in sorted(artist_categories):
                count = sum(1 for m in plan['moves'] 
                          if m['artist'] == artist and m['category'] == category)
                print(f"            ??? {category}/ ({count} files)")
    
    def _execute_plan(self, plan: Dict):
        """Execute the organization plan"""
        print("\nExecuting organization plan...")
        print("=" * 80)
        
        success = 0
        errors = 0
        
        for move in plan['moves']:
            source = move['source']
            target = move['target']
            
            try:
                # Create target directory
                target.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                if source.exists() and not target.exists():
                    shutil.move(str(source), str(target))
                    success += 1
                    
                    if success % 20 == 0:
                        print(f"  Moved {success} files...")
                elif target.exists():
                    print(f"  Skip (exists): {target.name}")
                    errors += 1
                else:
                    print(f"  Error (not found): {source.name}")
                    errors += 1
                    
            except Exception as e:
                print(f"  Error moving {source.name}: {e}")
                errors += 1
        
        print()
        print("=" * 80)
        print(f"Complete! Moved {success} files, {errors} errors/skipped")
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for directory"""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = re.sub(r'\s+', '_', name)
        return name.strip('_')
    
    def find_related_lyrics(self, audio_path: Path) -> List[Path]:
        """Find lyrics/text files related to audio file"""
        related = []
        
        # Search in ~/Documents for matching text files
        docs_dir = Path.home() / 'Documents'
        if docs_dir.exists():
            base_name = audio_path.stem.lower()
            
            for text_file in docs_dir.rglob('*.txt'):
                if base_name in text_file.stem.lower():
                    related.append(text_file)
        
        return related
    
    def create_collection_index(self, output_path: Optional[Path] = None):
        """Create an index of all avatararts music"""
        fingerprints = self.scan_your_songs()
        categorized = self.categorize_by_metadata(fingerprints)
        
        index = {
            'generated': datetime.now().isoformat(),
            'total_files': len(fingerprints),
            'by_artist': {},
            'by_category': {}
        }
        
        # Build artist index
        for artist, files in categorized['by_artist'].items():
            index['by_artist'][artist] = [
                {
                    'filename': fp.path.name,
                    'title': fp.metadata.get('title') if fp.metadata else None,
                    'size': fp.size,
                    'duration': fp.metadata.get('duration') if fp.metadata else None,
                    'category': self._determine_category(fp)
                }
                for fp in files
            ]
        
        # Build category index
        for category, files in categorized['by_category'].items():
            index['by_category'][category] = len(files)
        
        # Save index
        output = output_path or self.base_music_dir / 'avatararts_index.json'
        with open(output, 'w') as f:
            json.dump(index, f, indent=2)
        
        print(f"Index saved to: {output}")
        return index
    
    def close(self):
        """Clean up"""
        self.analyzer.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='AvatarArts Music Organizer')
    parser.add_argument('command', choices=['scan', 'organize', 'index'])
    parser.add_argument('--execute', action='store_true', help='Actually move files (not dry run)')
    
    args = parser.parse_args()
    
    organizer = AvatarArtsOrganizer()
    
    try:
        if args.command == 'scan':
            fingerprints = organizer.scan_your_songs()
            categorized = organizer.categorize_by_metadata(fingerprints)
            
            print(f"\nFound {len(fingerprints)} files")
            print(f"Artists: {len(categorized['by_artist'])}")
            print(f"Categories: {len(categorized['by_category'])}")
            
        elif args.command == 'organize':
            organizer.organize_avatararts_collection(dry_run=not args.execute)
            
        elif args.command == 'index':
            organizer.create_collection_index()
    
    finally:
        organizer.close()
