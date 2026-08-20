#!/usr/bin/env python3
"""
🔍 EXTRACT & PRESERVE ARCHIVED CONTENT
========================================
Extract valuable content from _ARCHIVED_DIRECTORIES before cleanup

Features:
✨ Extract and preserve CSV, MD, and HTML files
✨ Compare CSV song list with current music collection
✨ Parse HTML files for song metadata
✨ Identify gaps in your music collection
✨ Safe preservation with backups
"""

import os
import re
import csv
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from difflib import SequenceMatcher
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class ArchivedContentExtractor:
    """Extract and preserve valuable archived content"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Source directory
        self.archive_dir = Path("/Users/steven/Music/_ARCHIVED_DIRECTORIES/Song-origins-html")
        
        # Target preservation directories
        self.music_data_dir = Path.home() / "Music" / "nocTurneMeLoDieS" / "DATA"
        self.docs_dir = Path.home() / "Documents" / "PRESERVED_ARCHIVES"
        self.extraction_report_dir = Path.home() / "Music" / f"ARCHIVE_EXTRACTION_{self.timestamp}"
        
        # Create directories
        for directory in [self.music_data_dir, self.docs_dir, self.extraction_report_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'csv_files': 0,
            'md_files': 0,
            'html_files': 0,
            'songs_in_csv': 0,
            'songs_in_html': 0,
            'songs_in_collection': 0,
            'missing_songs': 0
        }
        
        self.csv_songs = []
        self.html_songs = []
        self.collection_songs = []
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def normalize_title(self, title: str) -> str:
        """Normalize song title for comparison"""
        # Remove common suffixes and clean up
        title = re.sub(r'\s*\(Remix\)\s*', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*\(Remastered\)\s*', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*\d+$', '', title)  # Remove trailing numbers
        title = title.lower().strip()
        return title
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def extract_csv_files(self):
        """Extract and analyze CSV files"""
        self.print_header("📊 EXTRACTING CSV FILES")
        
        csv_files = list(self.archive_dir.glob("*.csv"))
        
        for csv_file in csv_files:
            print(f"{Colors.CYAN}Found CSV: {csv_file.name}{Colors.END}")
            
            # Read CSV content
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    
                    for row in rows:
                        song_info = {
                            'title': row.get('Track Title', ''),
                            'duration': row.get('x', ''),  # Duration column
                            'genre': row.get('Music Genre', ''),
                            'link': row.get('Track Link', ''),
                            'source': csv_file.name
                        }
                        
                        if song_info['title']:
                            self.csv_songs.append(song_info)
                            self.stats['songs_in_csv'] += 1
                
                print(f"  Found {len(rows)} songs in CSV\n")
                
                # Copy to preservation directory
                target = self.music_data_dir / f"{csv_file.stem}_{self.timestamp}.csv"
                
                if not self.dry_run:
                    shutil.copy2(csv_file, target)
                    print(f"  {Colors.GREEN}✅ Preserved to: {target}{Colors.END}")
                else:
                    print(f"  {Colors.YELLOW}[DRY RUN] Would preserve to: {target}{Colors.END}")
                
                self.stats['csv_files'] += 1
                
            except Exception as e:
                print(f"  {Colors.RED}❌ Error reading CSV: {e}{Colors.END}")
        
        print(f"\n{Colors.BOLD}CSV Summary:{Colors.END}")
        print(f"  CSV files found: {self.stats['csv_files']}")
        print(f"  Total songs: {self.stats['songs_in_csv']}")
    
    def extract_markdown_files(self):
        """Extract and preserve markdown files"""
        self.print_header("📝 EXTRACTING MARKDOWN FILES")
        
        md_files = list(self.archive_dir.glob("*.md"))
        
        for md_file in md_files:
            file_size = md_file.stat().st_size / 1024  # KB
            
            print(f"{Colors.CYAN}Found MD: {md_file.name}{Colors.END}")
            print(f"  Size: {file_size:.1f} KB")
            
            # Read first few lines to show content type
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    first_lines = ''.join(f.readlines()[:5])
                    
                    # Detect content type
                    if 'prompt' in first_lines.lower():
                        content_type = 'PROMPT_TEMPLATES'
                    elif 'professional' in first_lines.lower() or 'career' in first_lines.lower():
                        content_type = 'PROFESSIONAL_DOCS'
                    else:
                        content_type = 'GENERAL'
                    
                    print(f"  Type: {content_type}")
            except Exception:
                content_type = 'UNKNOWN'
            
            # Copy to docs directory
            target = self.docs_dir / f"{md_file.stem}_{self.timestamp}.md"
            
            if not self.dry_run:
                shutil.copy2(md_file, target)
                print(f"  {Colors.GREEN}✅ Preserved to: {target}{Colors.END}\n")
            else:
                print(f"  {Colors.YELLOW}[DRY RUN] Would preserve to: {target}{Colors.END}\n")
            
            self.stats['md_files'] += 1
        
        print(f"{Colors.BOLD}Markdown Summary:{Colors.END}")
        print(f"  MD files found: {self.stats['md_files']}")
    
    def parse_html_files(self):
        """Parse HTML files for song metadata"""
        self.print_header("🌐 PARSING HTML FILES FOR SONG DATA")
        
        html_files = list(self.archive_dir.glob("*.html"))
        
        print(f"Found {len(html_files)} HTML file(s)\n")
        
        for html_file in html_files:
            file_size = html_file.stat().st_size / (1024*1024)  # MB
            
            print(f"{Colors.CYAN}Parsing: {html_file.name}{Colors.END}")
            print(f"  Size: {file_size:.1f} MB")
            
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    
                    # Try to find song titles in various HTML structures
                    # Look for common Suno.com patterns
                    
                    # Pattern 1: Look for song titles in links
                    song_links = soup.find_all('a', href=re.compile(r'/song/'))
                    
                    # Pattern 2: Look for song titles in spans/divs with title attributes
                    song_titles = soup.find_all(attrs={'title': True})
                    
                    # Pattern 3: Look for duration stamps (indicates song)
                    durations = soup.find_all(text=re.compile(r'\d+:\d+'))
                    
                    songs_found = set()
                    
                    # Extract from links
                    for link in song_links:
                        title = link.get_text().strip()
                        if title and len(title) > 2:
                            songs_found.add(title)
                    
                    # Extract from title attributes
                    for element in song_titles:
                        title = element.get('title', '').strip()
                        # Filter to likely song titles
                        if title and 3 < len(title) < 100 and not title.startswith('http'):
                            songs_found.add(title)
                    
                    # Store songs
                    for song_title in songs_found:
                        self.html_songs.append({
                            'title': song_title,
                            'source': html_file.name
                        })
                    
                    self.stats['songs_in_html'] += len(songs_found)
                    print(f"  Found {len(songs_found)} potential song titles\n")
                
                self.stats['html_files'] += 1
                
            except Exception as e:
                print(f"  {Colors.RED}❌ Error parsing HTML: {e}{Colors.END}\n")
        
        print(f"{Colors.BOLD}HTML Parsing Summary:{Colors.END}")
        print(f"  HTML files parsed: {self.stats['html_files']}")
        print(f"  Song titles extracted: {self.stats['songs_in_html']}")
    
    def scan_music_collection(self):
        """Scan current music collection"""
        self.print_header("🎵 SCANNING CURRENT MUSIC COLLECTION")
        
        music_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        
        print(f"Scanning: {music_dir}\n")
        
        # Scan all MP3 files
        audio_extensions = {'.mp3', '.m4a', '.wav', '.flac'}
        
        for audio_file in music_dir.rglob('*'):
            if audio_file.suffix.lower() in audio_extensions:
                self.collection_songs.append({
                    'title': audio_file.stem,
                    'path': str(audio_file.relative_to(music_dir)),
                    'filename': audio_file.name
                })
                self.stats['songs_in_collection'] += 1
        
        print(f"{Colors.GREEN}✅ Found {self.stats['songs_in_collection']} songs in collection{Colors.END}")
    
    def compare_and_find_gaps(self):
        """Compare CSV/HTML songs with current collection"""
        self.print_header("🔍 COMPARING & FINDING GAPS")
        
        # Build normalized collection index
        collection_index = {}
        for song in self.collection_songs:
            normalized = self.normalize_title(song['title'])
            collection_index[normalized] = song
        
        print(f"Collection index: {len(collection_index)} unique titles\n")
        
        # Check CSV songs
        print(f"{Colors.BOLD}Checking CSV songs...{Colors.END}\n")
        
        csv_missing = []
        csv_found = []
        
        for song in self.csv_songs:
            title = song['title']
            normalized = self.normalize_title(title)
            
            # Check exact match
            if normalized in collection_index:
                csv_found.append({
                    **song,
                    'match_type': 'EXACT',
                    'found_in': collection_index[normalized]['path']
                })
            else:
                # Try fuzzy match
                best_match = None
                best_score = 0
                
                for col_norm, col_song in collection_index.items():
                    score = self.similarity_score(normalized, col_norm)
                    if score > best_score:
                        best_score = score
                        best_match = col_song
                
                if best_score > 0.8:  # 80% similar
                    csv_found.append({
                        **song,
                        'match_type': 'FUZZY',
                        'similarity': best_score,
                        'found_in': best_match['path']
                    })
                else:
                    csv_missing.append(song)
                    self.stats['missing_songs'] += 1
        
        print(f"{Colors.GREEN}✅ Found in collection: {len(csv_found)}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Missing from collection: {len(csv_missing)}{Colors.END}\n")
        
        # Show missing songs
        if csv_missing:
            print(f"{Colors.BOLD}Missing Songs from CSV:{Colors.END}\n")
            for i, song in enumerate(csv_missing[:20], 1):
                print(f"{i}. {song['title']}")
                print(f"   Duration: {song['duration']} | Genre: {song['genre']}")
                if song.get('link'):
                    print(f"   Link: {song['link']}")
                print()
            
            if len(csv_missing) > 20:
                print(f"... and {len(csv_missing) - 20} more\n")
        
        return csv_found, csv_missing
    
    def save_reports(self, csv_found: List, csv_missing: List):
        """Save comprehensive reports"""
        self.print_header("💾 SAVING REPORTS")
        
        # 1. Missing songs report
        missing_file = self.extraction_report_dir / "MISSING_SONGS.csv"
        with open(missing_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Duration', 'Genre', 'Suno_Link', 'Source'])
            
            for song in csv_missing:
                writer.writerow([
                    song['title'],
                    song.get('duration', ''),
                    song.get('genre', ''),
                    song.get('link', ''),
                    song.get('source', '')
                ])
        
        print(f"{Colors.GREEN}✅ Missing songs: {missing_file.name}{Colors.END}")
        
        # 2. Found songs report
        found_file = self.extraction_report_dir / "FOUND_SONGS.csv"
        with open(found_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Match_Type', 'Similarity', 'Found_In', 'Duration', 'Genre'])
            
            for song in csv_found:
                writer.writerow([
                    song['title'],
                    song.get('match_type', ''),
                    f"{song.get('similarity', 1.0):.2%}",
                    song.get('found_in', ''),
                    song.get('duration', ''),
                    song.get('genre', '')
                ])
        
        print(f"{Colors.GREEN}✅ Found songs: {found_file.name}{Colors.END}")
        
        # 3. HTML songs report
        html_songs_file = self.extraction_report_dir / "HTML_EXTRACTED_SONGS.csv"
        with open(html_songs_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Source_HTML'])
            
            for song in self.html_songs:
                writer.writerow([song['title'], song['source']])
        
        print(f"{Colors.GREEN}✅ HTML songs: {html_songs_file.name}{Colors.END}")
        
        # 4. Master summary
        summary_file = self.extraction_report_dir / "EXTRACTION_SUMMARY.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 🔍 Archived Content Extraction Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE EXTRACTION'}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| CSV Files Extracted | {self.stats['csv_files']} |\n")
            f.write(f"| Markdown Files Extracted | {self.stats['md_files']} |\n")
            f.write(f"| HTML Files Parsed | {self.stats['html_files']} |\n")
            f.write(f"| Songs in CSV | {self.stats['songs_in_csv']} |\n")
            f.write(f"| Songs in HTML | {self.stats['songs_in_html']} |\n")
            f.write(f"| Songs in Collection | {self.stats['songs_in_collection']} |\n")
            f.write(f"| **Missing Songs** | **{self.stats['missing_songs']}** |\n\n")
            
            f.write("## 📁 Preserved Files\n\n")
            f.write(f"### CSV Files\n")
            f.write(f"- Preserved to: `{self.music_data_dir}`\n\n")
            
            f.write(f"### Markdown Files\n")
            f.write(f"- Preserved to: `{self.docs_dir}`\n\n")
            
            f.write("## ⚠️ Missing Songs\n\n")
            f.write(f"Found {len(csv_missing)} songs in CSV that are NOT in your current collection.\n")
            f.write(f"See `MISSING_SONGS.csv` for full list with Suno links.\n\n")
            
            f.write("## ✅ Next Steps\n\n")
            f.write("1. Review `MISSING_SONGS.csv` to identify songs to download\n")
            f.write("2. Check Suno links to retrieve missing tracks\n")
            f.write("3. Verify `FOUND_SONGS.csv` for fuzzy matches that might need renaming\n")
            f.write("4. Review preserved markdown files in ~/Documents/PRESERVED_ARCHIVES\n\n")
        
        print(f"{Colors.GREEN}✅ Summary: {summary_file.name}{Colors.END}")
        
        return summary_file
    
    def run(self):
        """Run complete extraction and analysis"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           🔍 ARCHIVED CONTENT EXTRACTION & PRESERVATION 🔍                    ║")
        print("║                                                                               ║")
        print("║              Extract → Analyze → Compare → Report                            ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE EXTRACTION'}{Colors.END}")
        print(f"Source: {self.archive_dir}")
        print(f"Target: {self.music_data_dir}\n")
        
        # 1. Extract CSV files
        self.extract_csv_files()
        
        # 2. Extract markdown files
        self.extract_markdown_files()
        
        # 3. Parse HTML files
        self.parse_html_files()
        
        # 4. Scan music collection
        self.scan_music_collection()
        
        # 5. Compare and find gaps
        csv_found, csv_missing = self.compare_and_find_gaps()
        
        # 6. Save reports
        summary_file = self.save_reports(csv_found, csv_missing)
        
        # Final summary
        self.print_header("✅ EXTRACTION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  CSV files: {Colors.CYAN}{self.stats['csv_files']}{Colors.END}")
        print(f"  Markdown files: {Colors.CYAN}{self.stats['md_files']}{Colors.END}")
        print(f"  HTML files: {Colors.CYAN}{self.stats['html_files']}{Colors.END}")
        print(f"  Songs in CSV: {Colors.CYAN}{self.stats['songs_in_csv']}{Colors.END}")
        print(f"  Songs in HTML: {Colors.CYAN}{self.stats['songs_in_html']}{Colors.END}")
        print(f"  Songs in collection: {Colors.CYAN}{self.stats['songs_in_collection']}{Colors.END}")
        print(f"  Missing songs: {Colors.YELLOW}{self.stats['missing_songs']}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Preserved Files:{Colors.END}")
        print(f"  CSV: {self.music_data_dir}")
        print(f"  Markdown: {self.docs_dir}")
        print(f"  Reports: {self.extraction_report_dir}\n")
        
        print(f"{Colors.BOLD}📝 Key Reports:{Colors.END}")
        print(f"  {summary_file}")
        print(f"  MISSING_SONGS.csv - Songs to download")
        print(f"  FOUND_SONGS.csv - Songs already in collection")
        print(f"  HTML_EXTRACTED_SONGS.csv - Songs from HTML files\n")
        
        if self.stats['missing_songs'] > 0:
            print(f"{Colors.YELLOW}⚠️  IMPORTANT: {self.stats['missing_songs']} songs from CSV are NOT in your collection!{Colors.END}")
            print(f"{Colors.YELLOW}Review MISSING_SONGS.csv and use the Suno links to download them.{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to actually preserve files.{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🔍 Extract & Preserve Archived Content")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (actually preserve files)')
    
    args = parser.parse_args()
    
    # Check if BeautifulSoup is installed
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print(f"{Colors.RED}❌ BeautifulSoup4 is required. Install with:{Colors.END}")
        print(f"{Colors.CYAN}pip install beautifulsoup4{Colors.END}\n")
        return
    
    extractor = ArchivedContentExtractor(dry_run=not args.live)
    extractor.run()


if __name__ == "__main__":
    main()
