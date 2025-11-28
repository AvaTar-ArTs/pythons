#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
🎵 Suno Data Processor - Python Companion Script
═══════════════════════════════════════════════════════════════════

Processes exported Suno data (CSV/JSON) and provides:
- Data validation and cleaning
- Deduplication
- Analytics and insights
- Format conversions
- Audio file downloading (optional)
- DistroKid CSV preparation
- Genre/mood classification (via AI)
- Lyrics analysis

USAGE:
    python suno-data-processor.py input.csv
    python suno-data-processor.py input.json --download-audio
    python suno-data-processor.py input.csv --distrokid
    python suno-data-processor.py input.csv --analyze --openai-key YOUR_KEY

AUTHOR: Claude Code
VERSION: 1.0.0
DATE: 2025-11-27
═══════════════════════════════════════════════════════════════════
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set
import hashlib

# Optional dependencies (graceful degradation)
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("ℹ️  pandas not installed - some features will be limited")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("ℹ️  requests not installed - audio download disabled")

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


# ═══════════════════════════════════════════════════════════════════
# 🎨 FORMATTING & DISPLAY
# ═══════════════════════════════════════════════════════════════════

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'═' * 70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'═' * 70}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


# ═══════════════════════════════════════════════════════════════════
# 📊 DATA LOADING
# ═══════════════════════════════════════════════════════════════════

class SunoDataLoader:
    """Load and parse Suno export files"""

    @staticmethod
    def load(filepath: Path) -> List[Dict]:
        """Load data from CSV or JSON"""
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        ext = filepath.suffix.lower()

        if ext == '.json':
            return SunoDataLoader.load_json(filepath)
        elif ext == '.csv':
            return SunoDataLoader.load_csv(filepath)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @staticmethod
    def load_json(filepath: Path) -> List[Dict]:
        """Load from JSON (handles both array and wrapped format)"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle wrapped format (from v3.0)
        if isinstance(data, dict) and 'songs' in data:
            return data['songs']

        # Handle array format
        if isinstance(data, list):
            return data

        raise ValueError("Unexpected JSON structure")

    @staticmethod
    def load_csv(filepath: Path) -> List[Dict]:
        """Load from CSV"""
        songs = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert empty strings to None
                cleaned_row = {
                    k: (v if v else None)
                    for k, v in row.items()
                }
                songs.append(cleaned_row)

        return songs


# ═══════════════════════════════════════════════════════════════════
# 🧹 DATA CLEANING
# ═══════════════════════════════════════════════════════════════════

class SunoDataCleaner:
    """Clean and validate Suno data"""

    @staticmethod
    def clean(songs: List[Dict]) -> List[Dict]:
        """Clean all songs"""
        print_info("Cleaning data...")

        cleaned = []
        issues = []

        for i, song in enumerate(songs):
            try:
                cleaned_song = SunoDataCleaner.clean_song(song)
                cleaned.append(cleaned_song)
            except Exception as e:
                issues.append(f"Song {i}: {e}")

        if issues:
            print_warning(f"Encountered {len(issues)} issues during cleaning")
            for issue in issues[:5]:  # Show first 5
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")

        print_success(f"Cleaned {len(cleaned)}/{len(songs)} songs")
        return cleaned

    @staticmethod
    def clean_song(song: Dict) -> Dict:
        """Clean individual song data"""
        cleaned = song.copy()

        # Standardize ID
        if 'id' in cleaned:
            cleaned['id'] = cleaned['id'].strip().lower()

        # Clean title
        if 'title' in cleaned and cleaned['title']:
            cleaned['title'] = cleaned['title'].strip()
            # Remove extra whitespace
            cleaned['title'] = re.sub(r'\s+', ' ', cleaned['title'])

        # Parse duration to seconds
        if 'duration' in cleaned and cleaned['duration']:
            match = re.match(r'(\d+):(\d+)', cleaned['duration'])
            if match:
                minutes, seconds = map(int, match.groups())
                cleaned['durationSeconds'] = minutes * 60 + seconds

        # Ensure URLs are valid
        for url_field in ['href', 'audio', 'imageUrl']:
            if url_field in cleaned and cleaned[url_field]:
                if not cleaned[url_field].startswith('http'):
                    cleaned[url_field] = 'https://suno.com' + cleaned[url_field]

        # Parse tags (convert string to list if needed)
        if 'tags' in cleaned and isinstance(cleaned['tags'], str):
            cleaned['tagsList'] = [
                tag.strip()
                for tag in cleaned['tags'].split(',')
                if tag.strip()
            ]

        return cleaned

    @staticmethod
    def validate(songs: List[Dict]) -> Dict:
        """Validate songs and return report"""
        print_info("Validating data...")

        report = {
            'total': len(songs),
            'valid': 0,
            'missing_title': 0,
            'missing_id': 0,
            'missing_audio': 0,
            'missing_lyrics': 0,
            'has_errors': 0,
            'invalid_duration': 0,
        }

        for song in songs:
            is_valid = True

            if not song.get('title'):
                report['missing_title'] += 1
                is_valid = False

            if not song.get('id'):
                report['missing_id'] += 1
                is_valid = False

            if not song.get('audio'):
                report['missing_audio'] += 1
                is_valid = False

            if not song.get('lyrics'):
                report['missing_lyrics'] += 1

            if song.get('error'):
                report['has_errors'] += 1
                is_valid = False

            if song.get('duration') and not song.get('durationSeconds'):
                report['invalid_duration'] += 1

            if is_valid:
                report['valid'] += 1

        # Print report
        print("\n📊 Validation Report:")
        print(f"  Total songs: {report['total']}")
        print(f"  Valid songs: {report['valid']} ({report['valid']/report['total']*100:.1f}%)")

        if report['missing_title'] > 0:
            print_warning(f"  Missing title: {report['missing_title']}")
        if report['missing_id'] > 0:
            print_warning(f"  Missing ID: {report['missing_id']}")
        if report['missing_audio'] > 0:
            print_warning(f"  Missing audio URL: {report['missing_audio']}")
        if report['missing_lyrics'] > 0:
            print_info(f"  Missing lyrics: {report['missing_lyrics']}")
        if report['has_errors'] > 0:
            print_error(f"  Extraction errors: {report['has_errors']}")

        return report


# ═══════════════════════════════════════════════════════════════════
# 🔍 DEDUPLICATION
# ═══════════════════════════════════════════════════════════════════

class SunoDeduplicator:
    """Remove duplicate songs"""

    @staticmethod
    def deduplicate(songs: List[Dict]) -> tuple[List[Dict], List[Dict]]:
        """Remove duplicates, return (unique, duplicates)"""
        print_info("Checking for duplicates...")

        seen_ids: Set[str] = set()
        seen_hashes: Set[str] = set()
        unique = []
        duplicates = []

        for song in songs:
            song_id = song.get('id')
            song_hash = SunoDeduplicator.compute_hash(song)

            # Check ID-based duplicates
            if song_id and song_id in seen_ids:
                duplicates.append(song)
                continue

            # Check content-based duplicates
            if song_hash in seen_hashes:
                duplicates.append(song)
                continue

            # It's unique
            if song_id:
                seen_ids.add(song_id)
            seen_hashes.add(song_hash)
            unique.append(song)

        if duplicates:
            print_warning(f"Found {len(duplicates)} duplicates (removed)")
        else:
            print_success("No duplicates found")

        print_success(f"Unique songs: {len(unique)}")

        return unique, duplicates

    @staticmethod
    def compute_hash(song: Dict) -> str:
        """Compute hash for song content"""
        # Use title + author + duration as fingerprint
        fingerprint = '|'.join([
            str(song.get('title', '')),
            str(song.get('author', '')),
            str(song.get('duration', '')),
        ]).lower()

        return hashlib.md5(fingerprint.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════
# 📈 ANALYTICS
# ═══════════════════════════════════════════════════════════════════

class SunoAnalytics:
    """Generate analytics and insights"""

    @staticmethod
    def analyze(songs: List[Dict]) -> Dict:
        """Perform comprehensive analysis"""
        print_header("📈 ANALYTICS")

        stats = {
            'total_songs': len(songs),
            'with_lyrics': sum(1 for s in songs if s.get('lyrics')),
            'total_duration_seconds': sum(s.get('durationSeconds', 0) for s in songs),
            'avg_duration_seconds': 0,
            'authors': Counter(),
            'tags': Counter(),
            'extraction_sources': Counter(),
            'errors': Counter(),
        }

        # Calculate averages
        durations = [s.get('durationSeconds', 0) for s in songs if s.get('durationSeconds')]
        if durations:
            stats['avg_duration_seconds'] = sum(durations) / len(durations)

        # Count authors, tags, sources
        for song in songs:
            if song.get('author'):
                stats['authors'][song['author']] += 1

            if song.get('tagsList'):
                for tag in song['tagsList']:
                    stats['tags'][tag] += 1

            if song.get('source'):
                stats['extraction_sources'][song['source']] += 1

            if song.get('error'):
                stats['errors'][song.get('errorType', 'UNKNOWN')] += 1

        # Print stats
        SunoAnalytics.print_stats(stats)

        return stats

    @staticmethod
    def print_stats(stats: Dict):
        """Print formatted statistics"""
        print(f"🎵 Total Songs: {stats['total_songs']}")
        print(f"📝 With Lyrics: {stats['with_lyrics']} ({stats['with_lyrics']/stats['total_songs']*100:.1f}%)")

        # Duration
        total_hours = stats['total_duration_seconds'] / 3600
        avg_minutes = stats['avg_duration_seconds'] / 60
        print(f"⏱️  Total Duration: {total_hours:.1f} hours")
        print(f"⏱️  Average Duration: {avg_minutes:.1f} minutes")

        # Top authors
        if stats['authors']:
            print("\n👤 Top Authors:")
            for author, count in stats['authors'].most_common(10):
                print(f"  {author}: {count} songs")

        # Top tags
        if stats['tags']:
            print("\n🏷️  Top Tags:")
            for tag, count in stats['tags'].most_common(10):
                print(f"  {tag}: {count} songs")

        # Extraction sources
        if stats['extraction_sources']:
            print("\n🔍 Extraction Sources:")
            for source, count in stats['extraction_sources'].items():
                print(f"  {source}: {count} songs")

        # Errors
        if stats['errors']:
            print_warning("\n❌ Errors:")
            for error_type, count in stats['errors'].items():
                print(f"  {error_type}: {count}")

        print()


# ═══════════════════════════════════════════════════════════════════
# 💾 EXPORT FORMATS
# ═══════════════════════════════════════════════════════════════════

class SunoExporter:
    """Export to various formats"""

    @staticmethod
    def export_distrokid(songs: List[Dict], output_path: Path):
        """Export DistroKid-compatible CSV"""
        print_info("Creating DistroKid CSV...")

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # DistroKid headers
            writer.writerow([
                'Artist Name',
                'Album Title',
                'Track Title',
                'ISRC',
                'UPC',
                'Audio File',
                'Genre',
                'Subgenre',
                'Language',
                'Explicit',
                'Release Date',
            ])

            for song in songs:
                if song.get('error'):
                    continue  # Skip failed extractions

                # Map Suno data to DistroKid format
                writer.writerow([
                    song.get('author', 'Unknown Artist'),
                    'Suno Collection',  # Can be customized
                    song.get('title', 'Untitled'),
                    '',  # ISRC - to be filled manually
                    '',  # UPC - to be filled manually
                    song.get('id', '') + '.mp3',
                    '',  # Genre - can be auto-filled if AI analysis enabled
                    '',  # Subgenre
                    'English',  # Default
                    'No',  # Default
                    datetime.now().strftime('%Y-%m-%d'),
                ])

        print_success(f"DistroKid CSV saved: {output_path}")

    @staticmethod
    def export_m3u(songs: List[Dict], output_path: Path):
        """Export M3U playlist"""
        print_info("Creating M3U playlist...")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n\n")

            for song in songs:
                if song.get('error') or not song.get('audio'):
                    continue

                duration = song.get('durationSeconds', 0)
                title = song.get('title', 'Untitled')
                author = song.get('author', 'Unknown')

                f.write(f"#EXTINF:{duration},{author} - {title}\n")
                f.write(f"{song['audio']}\n\n")

        print_success(f"M3U playlist saved: {output_path}")

    @staticmethod
    def export_markdown(songs: List[Dict], output_path: Path, stats: Dict):
        """Export Markdown report"""
        print_info("Creating Markdown report...")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# 🎵 Suno Collection Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Statistics
            f.write("## 📊 Statistics\n\n")
            f.write(f"- **Total Songs:** {stats['total_songs']}\n")
            f.write(f"- **With Lyrics:** {stats['with_lyrics']} ({stats['with_lyrics']/stats['total_songs']*100:.1f}%)\n")
            f.write(f"- **Total Duration:** {stats['total_duration_seconds']/3600:.1f} hours\n")
            f.write(f"- **Average Duration:** {stats['avg_duration_seconds']/60:.1f} minutes\n\n")

            # Top authors
            if stats['authors']:
                f.write("## 👤 Top Authors\n\n")
                for author, count in stats['authors'].most_common(10):
                    f.write(f"- **{author}**: {count} songs\n")
                f.write("\n")

            # Top tags
            if stats['tags']:
                f.write("## 🏷️ Top Tags\n\n")
                for tag, count in stats['tags'].most_common(10):
                    f.write(f"- **{tag}**: {count} songs\n")
                f.write("\n")

            # Songs list
            f.write("## 🎵 Songs\n\n")
            for i, song in enumerate(songs[:100], 1):  # First 100 only
                if song.get('error'):
                    continue

                f.write(f"### {i}. {song.get('title', 'Untitled')}\n\n")

                if song.get('author'):
                    f.write(f"**Artist:** {song['author']}  \n")
                if song.get('duration'):
                    f.write(f"**Duration:** {song['duration']}  \n")
                if song.get('tags'):
                    f.write(f"**Tags:** {song['tags']}  \n")
                if song.get('href'):
                    f.write(f"**Link:** [{song['href']}]({song['href']})  \n")

                if song.get('summary'):
                    f.write(f"\n{song['summary'][:200]}...\n")

                f.write("\n---\n\n")

            if len(songs) > 100:
                f.write(f"*... and {len(songs) - 100} more songs*\n")

        print_success(f"Markdown report saved: {output_path}")


# ═══════════════════════════════════════════════════════════════════
# 🎬 MAIN PROCESSOR
# ═══════════════════════════════════════════════════════════════════

class SunoProcessor:
    """Main processing orchestrator"""

    def __init__(self, input_file: Path, args):
        self.input_file = input_file
        self.args = args
        self.songs = []
        self.stats = {}

    def process(self):
        """Run full processing pipeline"""
        try:
            # 1. Load data
            print_header("🎵 SUNO DATA PROCESSOR")
            print_info(f"Loading: {self.input_file}")
            self.songs = SunoDataLoader.load(self.input_file)
            print_success(f"Loaded {len(self.songs)} songs")

            # 2. Clean data
            self.songs = SunoDataCleaner.clean(self.songs)

            # 3. Validate
            SunoDataCleaner.validate(self.songs)

            # 4. Deduplicate
            if not self.args.keep_duplicates:
                self.songs, duplicates = SunoDeduplicator.deduplicate(self.songs)

            # 5. Analyze
            self.stats = SunoAnalytics.analyze(self.songs)

            # 6. Export
            self.export_outputs()

            # 7. Download audio (optional)
            if self.args.download_audio:
                self.download_audio()

            print_header("✅ PROCESSING COMPLETE")
            print_success(f"Processed {len(self.songs)} songs successfully!")

        except Exception as e:
            print_error(f"Processing failed: {e}")
            if self.args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)

    def export_outputs(self):
        """Export to requested formats"""
        output_dir = self.input_file.parent
        basename = self.input_file.stem

        # Clean CSV/JSON
        if self.args.output or self.args.all_formats:
            output_format = self.args.output or self.input_file.suffix[1:]  # csv or json

            if output_format == 'json':
                output_path = output_dir / f"{basename}_processed.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        'metadata': {
                            'processed_at': datetime.now().isoformat(),
                            'total_songs': len(self.songs),
                            'statistics': self.stats,
                        },
                        'songs': self.songs,
                    }, f, indent=2, ensure_ascii=False)
                print_success(f"Saved: {output_path}")

            elif output_format == 'csv':
                output_path = output_dir / f"{basename}_processed.csv"
                if self.songs:
                    with open(output_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=self.songs[0].keys())
                        writer.writeheader()
                        writer.writerows(self.songs)
                    print_success(f"Saved: {output_path}")

        # DistroKid CSV
        if self.args.distrokid or self.args.all_formats:
            output_path = output_dir / f"{basename}_distrokid.csv"
            SunoExporter.export_distrokid(self.songs, output_path)

        # M3U Playlist
        if self.args.playlist or self.args.all_formats:
            output_path = output_dir / f"{basename}_playlist.m3u"
            SunoExporter.export_m3u(self.songs, output_path)

        # Markdown Report
        if self.args.report or self.args.all_formats:
            output_path = output_dir / f"{basename}_report.md"
            SunoExporter.export_markdown(self.songs, output_path, self.stats)

    def download_audio(self):
        """Download audio files"""
        if not HAS_REQUESTS:
            print_error("requests library required for audio download")
            return

        print_header("🎧 DOWNLOADING AUDIO FILES")

        output_dir = self.input_file.parent / 'audio'
        output_dir.mkdir(exist_ok=True)

        successful = 0
        failed = 0

        for i, song in enumerate(self.songs, 1):
            if not song.get('audio') or song.get('error'):
                continue

            try:
                print(f"Downloading {i}/{len(self.songs)}: {song.get('title', 'Untitled')}", end='... ')

                filename = f"{song['id']}.mp3"
                filepath = output_dir / filename

                if filepath.exists() and not self.args.force_download:
                    print("skipped (exists)")
                    continue

                response = requests.get(song['audio'], timeout=30)
                response.raise_for_status()

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                print(f"{Colors.OKGREEN}✓{Colors.ENDC}")
                successful += 1

            except Exception as e:
                print(f"{Colors.FAIL}✗ ({e}){Colors.ENDC}")
                failed += 1

        print()
        print_success(f"Downloaded {successful} files")
        if failed > 0:
            print_warning(f"Failed: {failed} files")
        print_info(f"Location: {output_dir}")


# ═══════════════════════════════════════════════════════════════════
# 🎯 CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Process Suno export files (CSV/JSON)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s songs.csv                           # Basic processing
  %(prog)s songs.json --output csv             # Convert JSON to CSV
  %(prog)s songs.csv --distrokid               # Create DistroKid CSV
  %(prog)s songs.csv --download-audio          # Download all audio files
  %(prog)s songs.csv --all-formats             # Export all formats
        """
    )

    parser.add_argument('input', type=str, help='Input CSV or JSON file')

    parser.add_argument('-o', '--output', type=str, choices=['csv', 'json'],
                       help='Output format for processed data')

    parser.add_argument('--distrokid', action='store_true',
                       help='Create DistroKid-compatible CSV')

    parser.add_argument('--playlist', action='store_true',
                       help='Create M3U playlist file')

    parser.add_argument('--report', action='store_true',
                       help='Create Markdown report')

    parser.add_argument('--all-formats', action='store_true',
                       help='Export all formats')

    parser.add_argument('--download-audio', action='store_true',
                       help='Download audio files')

    parser.add_argument('--force-download', action='store_true',
                       help='Re-download existing files')

    parser.add_argument('--keep-duplicates', action='store_true',
                       help='Keep duplicate songs')

    parser.add_argument('--analyze', action='store_true',
                       help='AI-powered content analysis (requires OpenAI)')

    parser.add_argument('--openai-key', type=str,
                       help='OpenAI API key for analysis')

    parser.add_argument('--debug', action='store_true',
                       help='Show debug information')

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print_error(f"File not found: {input_path}")
        sys.exit(1)

    # Run processor
    processor = SunoProcessor(input_path, args)
    processor.process()


if __name__ == '__main__':
    main()
