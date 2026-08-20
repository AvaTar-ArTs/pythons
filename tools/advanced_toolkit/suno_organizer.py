#!/usr/bin/env python3
"""
Suno Music Organizer (avatararts = Suno artist)
Comprehensive organizer for YOUR_SUNO_SONGS with intelligent categorization
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict
import json
import re
import shutil
from datetime import datetime

from file_intelligence import FileAnalyzer, FileFingerprint
from config_manager import get_config


class SunoOrganizer:
    """Organize Suno-generated music (avatararts content)"""
    
    def __init__(self, base_music_dir: Optional[Path] = None):
        self.config = get_config()
        self.base_music_dir = base_music_dir or Path.home() / 'Music/nocTurneMeLoDieS/FINAL_ORGANIZED'
        self.your_songs_dir = self.base_music_dir / 'YOUR_SUNO_SONGS'
        self.analyzer = FileAnalyzer(Path.home() / '.file_intelligence.db')
        
        # Suno/AvatarArts identifiers
        self.suno_identifiers = [
            'suno', 'avatararts', 'avatar arts', 'ai-art', 'avatar_arts'
        ]
        
        # Genre/style detection patterns
        self.genre_patterns = {
            'cinematic': {
                'keywords': ['epic', 'orchestral', 'dramatic', 'film', 'trailer', 'cinematic', 'heroic', 'grand'],
                'indicators': ['symphony', 'orchestra', 'score', 'soundtrack']
            },
            'ambient': {
                'keywords': ['ambient', 'atmospheric', 'meditation', 'calm', 'peaceful', 'chill', 'relax'],
                'indicators': ['drone', 'soundscape', 'space', 'ethereal']
            },
            'electronic': {
                'keywords': ['synth', 'edm', 'electronic', 'techno', 'house', 'trance', 'electro'],
                'indicators': ['beat', 'bass', 'drop', 'bpm']
            },
            'folk': {
                'keywords': ['folk', 'acoustic', 'indie', 'singer-songwriter', 'storytelling'],
                'indicators': ['guitar', 'banjo', 'mandolin', 'ballad']
            },
            'rock': {
                'keywords': ['rock', 'metal', 'punk', 'grunge', 'alternative'],
                'indicators': ['guitar', 'riff', 'distortion', 'heavy']
            },
            'experimental': {
                'keywords': ['experimental', 'avant-garde', 'abstract', 'glitch', 'noise'],
                'indicators': ['experimental', 'weird', 'strange', 'unique']
            },
            'classical': {
                'keywords': ['classical', 'piano', 'violin', 'chamber', 'symphony', 'baroque', 'romantic'],
                'indicators': ['concerto', 'sonata', 'prelude', 'waltz']
            },
            'hip_hop': {
                'keywords': ['hip-hop', 'rap', 'trap', 'beats', 'boom bap'],
                'indicators': ['rap', 'mc', 'flow', 'bars']
            },
            'jazz': {
                'keywords': ['jazz', 'blues', 'swing', 'bebop', 'smooth jazz'],
                'indicators': ['saxophone', 'trumpet', 'improvisation', 'scat']
            },
            'world': {
                'keywords': ['world', 'ethnic', 'tribal', 'traditional', 'cultural'],
                'indicators': ['drums', 'chant', 'ritual', 'native']
            },
            'pop': {
                'keywords': ['pop', 'catchy', 'radio', 'mainstream', 'commercial'],
                'indicators': ['chorus', 'hook', 'verse']
            }
        }
        
        # Mood/theme detection
        self.moods = {
            'dark': ['dark', 'shadow', 'night', 'noir', 'gothic', 'grim', 'sinister'],
            'uplifting': ['uplifting', 'happy', 'joy', 'bright', 'positive', 'cheerful'],
            'melancholic': ['sad', 'melancholy', 'melancholic', 'somber', 'lonely', 'blue'],
            'energetic': ['energy', 'power', 'intense', 'dynamic', 'aggressive', 'fierce'],
            'peaceful': ['peace', 'calm', 'serene', 'tranquil', 'gentle', 'soft'],
            'mysterious': ['mystery', 'mystic', 'enigma', 'cryptic', 'secret']
        }
        
        # Project/series detection
        self.series_patterns = [
            r'(.+?)[-_]v\d+',  # Version pattern: song-v2
            r'(.+?)[-_]part[-_]?\d+',  # Part pattern: song-part-1
            r'(.+?)[-_]\d{4}$',  # Date pattern: song-2024
            r'(.+?)[-_](remix|cover|acoustic|live)',  # Variation pattern
            r'(.+?)[-_](intro|outro|interlude)',  # Section pattern
        ]
    
    def scan_suno_library(self) -> List[FileFingerprint]:
        """Scan all Suno/AvatarArts music"""
        if not self.your_songs_dir.exists():
            print(f"? Directory not found: {self.your_songs_dir}")
            return []
        
        print(f"?? Scanning Suno Library: {self.your_songs_dir}")
        print("=" * 80)
        
        audio_files = []
        for ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
            audio_files.extend(self.your_songs_dir.glob(f'*{ext}'))
        
        print(f"Found {len(audio_files)} audio files")
        print()
        
        fingerprints = []
        for i, audio_file in enumerate(audio_files, 1):
            if i % 50 == 0:
                print(f"  Analyzing {i}/{len(audio_files)}...")
            
            fp = self.analyzer.analyze_file(audio_file)
            if fp:
                fingerprints.append(fp)
        
        print(f"\n? Analyzed {len(fingerprints)} files")
        return fingerprints
    
    def classify_track(self, fp: FileFingerprint) -> Dict:
        """Deep classification of a Suno track"""
        
        # First determine content type by duration (simple & effective!)
        duration = 0
        if fp.metadata and fp.metadata.get('duration'):
            duration = float(fp.metadata.get('duration'))
        
        # Classify by duration
        if duration < 30:
            content_type = 'SHORT_AUDIO'  # UI sounds, jingles
        elif 30 <= duration <= 360:  # 30s to 6 min
            content_type = 'SONG'
        elif 360 < duration <= 1200:  # 6-20 min
            content_type = 'STORY'  # Narrations, extended pieces
        else:  # > 20 min
            content_type = 'AUDIOBOOK'  # Long-form content
        
        classification = {
            'content_type': content_type,
            'duration': duration,
            'genres': [],
            'moods': [],
            'series': None,
            'version': None,
            'is_suno': self._is_suno_track(fp),
            'confidence': 0.0
        }
        
        # Gather all text to analyze
        text_corpus = self._build_text_corpus(fp)
        
        # Detect genres
        genre_scores = {}
        for genre, patterns in self.genre_patterns.items():
            score = 0
            for keyword in patterns['keywords']:
                if keyword in text_corpus:
                    score += 2
            for indicator in patterns['indicators']:
                if indicator in text_corpus:
                    score += 1
            
            if score > 0:
                genre_scores[genre] = score
        
        # Get top genres
        if genre_scores:
            sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
            classification['genres'] = [g for g, s in sorted_genres[:3]]
            classification['confidence'] = min(sorted_genres[0][1] / 10.0, 1.0)
        
        # Detect moods
        for mood, keywords in self.moods.items():
            if any(keyword in text_corpus for keyword in keywords):
                classification['moods'].append(mood)
        
        # Detect series/project
        series_info = self._detect_series(fp)
        if series_info:
            classification['series'] = series_info['name']
            classification['version'] = series_info['version']
        
        return classification
    
    def _is_suno_track(self, fp: FileFingerprint) -> bool:
        """Determine if track is from Suno/AvatarArts"""
        if fp.metadata:
            artist = (fp.metadata.get('artist') or '').lower()
            album = (fp.metadata.get('album') or '').lower()
            
            if any(identifier in artist for identifier in self.suno_identifiers):
                return True
            if any(identifier in album for identifier in self.suno_identifiers):
                return True
        
        filename = fp.path.name.lower()
        return any(identifier in filename for identifier in self.suno_identifiers)
    
    def _build_text_corpus(self, fp: FileFingerprint) -> str:
        """Build comprehensive text corpus for analysis"""
        corpus = fp.path.stem.lower()
        
        if fp.metadata:
            for key in ['title', 'artist', 'album', 'genre', 'comment']:
                value = fp.metadata.get(key)
                if value:
                    corpus += ' ' + str(value).lower()
        
        return corpus
    
    def _detect_series(self, fp: FileFingerprint) -> Optional[Dict]:
        """Detect if track is part of a series"""
        filename = fp.path.stem
        
        for pattern in self.series_patterns:
            match = re.match(pattern, filename, re.IGNORECASE)
            if match:
                base_name = match.group(1)
                
                # Extract version/part number
                version_match = re.search(r'[-_]?v?(\d+)$', filename)
                version = version_match.group(1) if version_match else None
                
                return {
                    'name': base_name,
                    'version': version,
                    'pattern': pattern
                }
        
        return None
    
    def organize_by_genre_and_mood(self, fingerprints: List[FileFingerprint]) -> Dict:
        """Organize tracks by genre and mood"""
        organized = {
            'by_genre': defaultdict(list),
            'by_mood': defaultdict(list),
            'by_series': defaultdict(list),
            'by_content_type': defaultdict(list),
            'unclassified': [],
            'statistics': defaultdict(int)
        }
        
        for fp in fingerprints:
            classification = self.classify_track(fp)
            
            # Organize by content type first!
            content_type = classification['content_type']
            organized['by_content_type'][content_type].append((fp, classification))
            organized['statistics'][f'type_{content_type}'] += 1
            
            # Only classify SONGS by genre/mood
            if content_type == 'SONG':
                # Organize by primary genre
                if classification['genres']:
                    primary_genre = classification['genres'][0]
                    organized['by_genre'][primary_genre].append((fp, classification))
                    organized['statistics'][f'genre_{primary_genre}'] += 1
                else:
                    organized['unclassified'].append((fp, classification))
                    organized['statistics']['unclassified'] += 1
            
            # Organize by mood
            for mood in classification['moods']:
                organized['by_mood'][mood].append((fp, classification))
                organized['statistics'][f'mood_{mood}'] += 1
            
            # Organize by series
            if classification['series']:
                organized['by_series'][classification['series']].append((fp, classification))
                organized['statistics']['series_count'] += 1
            
            # Track Suno vs non-Suno
            if classification['is_suno']:
                organized['statistics']['suno_tracks'] += 1
            else:
                organized['statistics']['other_tracks'] += 1
        
        return organized
    
    def create_organization_structure(self, organized: Dict) -> Dict:
        """Create file organization plan"""
        plan = {
            'moves': [],
            'structure': defaultdict(list),
            'stats': {
                'total_moves': 0,
                'by_category': defaultdict(int)
            }
        }
        
        # Organize by genre (primary organization)
        for genre, tracks in organized['by_genre'].items():
            genre_dir = self.base_music_dir / 'SUNO_BY_GENRE' / genre.upper()
            
            for fp, classification in tracks:
                # Add mood subdirectory if present
                if classification['moods']:
                    target_dir = genre_dir / classification['moods'][0]
                else:
                    target_dir = genre_dir
                
                target_path = target_dir / fp.path.name
                
                plan['moves'].append({
                    'source': fp.path,
                    'target': target_path,
                    'genre': genre,
                    'moods': classification['moods'],
                    'series': classification['series'],
                    'confidence': classification['confidence']
                })
                
                plan['structure'][str(target_dir)].append(fp.path.name)
                plan['stats']['total_moves'] += 1
                plan['stats']['by_category'][genre] += 1
        
        # Organize series separately
        if organized['by_series']:
            series_dir = self.base_music_dir / 'SUNO_BY_SERIES'
            
            for series_name, tracks in organized['by_series'].items():
                series_path = series_dir / self._sanitize_name(series_name)
                
                for fp, classification in tracks:
                    target_path = series_path / fp.path.name
                    
                    # Don't duplicate if already planned
                    if not any(m['source'] == fp.path for m in plan['moves']):
                        plan['moves'].append({
                            'source': fp.path,
                            'target': target_path,
                            'genre': 'series',
                            'series': series_name,
                            'confidence': 1.0
                        })
                        
                        plan['structure'][str(series_path)].append(fp.path.name)
                        plan['stats']['total_moves'] += 1
        
        return plan
    
    def execute_organization(self, plan: Dict, dry_run: bool = True):
        """Execute the organization plan"""
        print()
        print("=" * 80)
        if dry_run:
            print("?? DRY RUN - Showing what would be done")
        else:
            print("?? EXECUTING ORGANIZATION")
        print("=" * 80)
        print()
        
        print(f"Total files to organize: {plan['stats']['total_moves']}")
        print()
        
        print("Organization by category:")
        for category, count in sorted(plan['stats']['by_category'].items()):
            print(f"  {category.upper()}: {count} files")
        
        print()
        print("Directory structure to create:")
        for directory in sorted(plan['structure'].keys())[:20]:
            file_count = len(plan['structure'][directory])
            print(f"  ?? {Path(directory).relative_to(self.base_music_dir)}")
            print(f"      ({file_count} files)")
        
        if len(plan['structure']) > 20:
            print(f"  ... and {len(plan['structure']) - 20} more directories")
        
        if dry_run:
            print()
            print("??  Run with --execute to actually move files")
            return
        
        # Execute moves
        print()
        print("Moving files...")
        success = 0
        errors = 0
        
        for move in plan['moves']:
            source = move['source']
            target = move['target']
            
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                
                if source.exists() and not target.exists():
                    shutil.move(str(source), str(target))
                    success += 1
                    
                    if success % 25 == 0:
                        print(f"  ? Moved {success}/{len(plan['moves'])} files...")
                elif target.exists():
                    errors += 1
                else:
                    errors += 1
                    
            except Exception as e:
                print(f"  ? Error: {source.name} - {e}")
                errors += 1
        
        print()
        print("=" * 80)
        print(f"? Complete! Moved {success} files, {errors} errors")
    
    def generate_catalog(self, output_path: Optional[Path] = None) -> Dict:
        """Generate comprehensive catalog of Suno music"""
        print("?? Generating Suno Music Catalog...")
        print()
        
        fingerprints = self.scan_suno_library()
        organized = self.organize_by_genre_and_mood(fingerprints)
        
        catalog = {
            'generated': datetime.now().isoformat(),
            'total_tracks': len(fingerprints),
            'statistics': dict(organized['statistics']),
            'by_genre': {},
            'by_mood': {},
            'by_series': {},
            'recommendations': []
        }
        
        # Build genre catalog
        for genre, tracks in organized['by_genre'].items():
            catalog['by_genre'][genre] = [
                {
                    'filename': fp.path.name,
                    'title': fp.metadata.get('title') if fp.metadata else None,
                    'duration': fp.metadata.get('duration') if fp.metadata else None,
                    'moods': classification['moods'],
                    'confidence': classification['confidence']
                }
                for fp, classification in tracks
            ]
        
        # Build mood catalog
        for mood, tracks in organized['by_mood'].items():
            catalog['by_mood'][mood] = len(tracks)
        
        # Build series catalog
        for series, tracks in organized['by_series'].items():
            catalog['by_series'][series] = [
                fp.path.name for fp, _ in tracks
            ]
        
        # Generate recommendations
        catalog['recommendations'] = self._generate_recommendations(organized)
        
        # Save catalog
        output = output_path or self.base_music_dir / 'suno_catalog.json'
        with open(output, 'w') as f:
            json.dump(catalog, f, indent=2)
        
        print(f"? Catalog saved to: {output}")
        
        # Print summary
        print()
        print("Catalog Summary:")
        print(f"  Total tracks: {catalog['total_tracks']}")
        print(f"  Genres: {len(catalog['by_genre'])}")
        print(f"  Moods: {len(catalog['by_mood'])}")
        print(f"  Series: {len(catalog['by_series'])}")
        
        return catalog
    
    def _generate_recommendations(self, organized: Dict) -> List[Dict]:
        """Generate listening recommendations"""
        recommendations = []
        
        # Top genre
        if organized['by_genre']:
            top_genre = max(organized['by_genre'].items(), key=lambda x: len(x[1]))
            recommendations.append({
                'type': 'top_genre',
                'genre': top_genre[0],
                'count': len(top_genre[1]),
                'message': f"You have {len(top_genre[1])} {top_genre[0]} tracks - your top genre!"
            })
        
        # Series to complete
        for series, tracks in organized['by_series'].items():
            if 2 <= len(tracks) <= 5:
                recommendations.append({
                    'type': 'series',
                    'name': series,
                    'tracks': len(tracks),
                    'message': f"Series '{series}' has {len(tracks)} tracks - consider creating more!"
                })
        
        return recommendations
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for directory"""
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = re.sub(r'\s+', '_', name)
        return name.strip('_')
    
    def close(self):
        """Clean up"""
        self.analyzer.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Suno Music Organizer (AvatarArts)',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('command', choices=['scan', 'organize', 'catalog'])
    parser.add_argument('--execute', action='store_true', 
                       help='Execute organization (not dry run)')
    parser.add_argument('--output', '-o', 
                       help='Output path for catalog')
    
    args = parser.parse_args()
    
    organizer = SunoOrganizer()
    
    try:
        if args.command == 'scan':
            fingerprints = organizer.scan_suno_library()
            organized = organizer.organize_by_genre_and_mood(fingerprints)
            
            print()
            print("Scan Results:")
            print(f"  Total tracks: {len(fingerprints)}")
            print(f"  Suno tracks: {organized['statistics']['suno_tracks']}")
            print(f"  Other tracks: {organized['statistics']['other_tracks']}")
            print()
            print("By Genre:")
            for genre, tracks in sorted(organized['by_genre'].items()):
                print(f"  {genre.upper()}: {len(tracks)} tracks")
            
        elif args.command == 'organize':
            fingerprints = organizer.scan_suno_library()
            organized = organizer.organize_by_genre_and_mood(fingerprints)
            plan = organizer.create_organization_structure(organized)
            organizer.execute_organization(plan, dry_run=not args.execute)
            
        elif args.command == 'catalog':
            output = Path(args.output) if args.output else None
            organizer.generate_catalog(output)
    
    finally:
        organizer.close()


if __name__ == '__main__':
    main()
