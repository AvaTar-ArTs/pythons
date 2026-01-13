#!/usr/bin/env python3
"""
🎵 COMPREHENSIVE MUSIC CONTENT SCANNER
=======================================
Deep scan of ALL MP3s and associated content before any cleanup

Features:
✨ Scan every MP3/audio file in ~/Music
✨ Find transcripts, lyrics, metadata, prompts for each audio
✨ Cross-reference with ~/Documents content
✨ Identify orphaned audio (no content)
✨ Identify orphaned content (no audio)
✨ Ensure nothing is lost before cleanup
✨ Generate comprehensive preservation report
"""

import os
import csv
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from difflib import SequenceMatcher
from typing import Dict, List, Tuple
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class ComprehensiveMusicContentScanner:
    """Deep scan of all music and associated content"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Directories to scan
        self.music_dir = Path.home() / "Music"
        self.docs_dir = Path.home() / "Documents"
        
        # Output directory
        self.output_dir = self.music_dir / f"COMPREHENSIVE_SCAN_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Storage
        self.audio_files = []
        self.content_files = {
            'transcripts': [],
            'lyrics': [],
            'metadata': [],
            'prompts': [],
            'json': [],
            'text': []
        }
        
        self.audio_content_map = {}  # audio -> associated content
        self.orphaned_audio = []
        self.orphaned_content = []
        
        self.stats = {
            'total_audio': 0,
            'total_content': 0,
            'audio_with_content': 0,
            'audio_without_content': 0,
            'content_with_audio': 0,
            'content_without_audio': 0,
            'total_size_gb': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def normalize_name(self, name: str) -> str:
        """Normalize filename for matching"""
        name = Path(name).stem.lower()
        # Remove common patterns
        name = re.sub(r'\s*\(remix\)\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*\(remastered\)\s*', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s*\(.*?\)\s*', '', name)  # Remove parentheticals
        name = re.sub(r'\s*-\s*\d+$', '', name)  # Remove trailing numbers
        name = re.sub(r'[-_]+', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def get_audio_metadata(self, filepath: Path) -> Dict:
        """Extract metadata from audio file"""
        metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'duration': 0,
            'bitrate': 0,
            'has_embedded_lyrics': False
        }
        
        try:
            if filepath.suffix.lower() == '.mp3':
                audio = MP3(filepath, ID3=ID3)
                metadata['duration'] = audio.info.length
                metadata['bitrate'] = audio.info.bitrate
                
                # Try to get ID3 tags
                try:
                    tags = ID3(filepath)
                    
                    # Title
                    if 'TIT2' in tags:
                        metadata['title'] = str(tags['TIT2'])
                    
                    # Artist
                    if 'TPE1' in tags:
                        metadata['artist'] = str(tags['TPE1'])
                    
                    # Album
                    if 'TALB' in tags:
                        metadata['album'] = str(tags['TALB'])
                    
                    # Lyrics
                    if 'USLT' in tags or 'SYLT' in tags:
                        metadata['has_embedded_lyrics'] = True
                        
                except Exception:
                    pass
            
            elif filepath.suffix.lower() in ['.m4a', '.wav', '.flac']:
                audio = mutagen.File(filepath)
                if audio:
                    metadata['duration'] = audio.info.length if hasattr(audio.info, 'length') else 0
                    
        except Exception as e:
            pass
        
        return metadata
    
    def classify_content_file(self, filepath: Path) -> str:
        """Classify content file type"""
        name_lower = filepath.name.lower()
        
        # Check filename
        if 'transcript' in name_lower:
            return 'transcripts'
        if 'lyric' in name_lower or 'lyrics' in name_lower:
            return 'lyrics'
        if 'prompt' in name_lower or 'dalle' in name_lower or 'sora' in name_lower:
            return 'prompts'
        if 'metadata' in name_lower or 'info' in name_lower:
            return 'metadata'
        
        # Check file extension
        if filepath.suffix.lower() == '.json':
            return 'json'
        
        # Read first few lines
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = ''.join(f.readlines()[:10]).lower()
                
                if 'transcript' in first_lines or 'speaker' in first_lines:
                    return 'transcripts'
                if '[verse' in first_lines or '[chorus' in first_lines:
                    return 'lyrics'
                if 'prompt' in first_lines or 'generate' in first_lines:
                    return 'prompts'
        except Exception:
            pass
        
        return 'text'
    
    def scan_audio_files(self):
        """Scan all audio files in ~/Music"""
        self.print_header("🎵 SCANNING ALL AUDIO FILES IN ~/Music")
        
        audio_extensions = {'.mp3', '.m4a', '.wav', '.flac', '.ogg', '.aac'}
        
        print(f"Scanning: {self.music_dir}\n")
        
        scanned_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.music_dir):
            # Skip backup and analysis directories
            dirs[:] = [d for d in dirs if not d.startswith(('ARCHIVE_', 'CONSOLIDATION_', 
                                                           'CONTENT_CROSS_', '.', 'merge_backup'))]
            
            for filename in files:
                if Path(filename).suffix.lower() in audio_extensions:
                    filepath = Path(root) / filename
                    
                    try:
                        file_stat = filepath.stat()
                        file_size = file_stat.st_size
                        total_size += file_size
                        
                        # Get metadata
                        metadata = self.get_audio_metadata(filepath)
                        
                        audio_info = {
                            'path': str(filepath),
                            'filename': filename,
                            'relative_path': str(filepath.relative_to(self.music_dir)),
                            'size': file_size,
                            'normalized_name': self.normalize_name(filename),
                            'metadata': metadata,
                            'directory': filepath.parent.name
                        }
                        
                        self.audio_files.append(audio_info)
                        self.stats['total_audio'] += 1
                        scanned_count += 1
                        
                        if scanned_count % 100 == 0:
                            print(f"  Scanned {scanned_count} audio files...", end='\r')
                        
                    except Exception as e:
                        pass
        
        self.stats['total_size_gb'] = total_size / (1024**3)
        
        print(f"\n{Colors.GREEN}✅ Scanned {self.stats['total_audio']} audio files{Colors.END}")
        print(f"{Colors.CYAN}Total size: {self.stats['total_size_gb']:.2f} GB{Colors.END}\n")
    
    def scan_content_files(self):
        """Scan content files in ~/Music and ~/Documents"""
        self.print_header("📄 SCANNING CONTENT FILES (Transcripts, Lyrics, Metadata)")
        
        text_extensions = {'.txt', '.md', '.json', '.lrc', '.srt', '.vtt'}
        
        # Scan ~/Music
        print(f"{Colors.CYAN}Scanning ~/Music for content...{Colors.END}\n")
        
        for root, dirs, files in os.walk(self.music_dir):
            dirs[:] = [d for d in dirs if not d.startswith(('ARCHIVE_', 'CONSOLIDATION_', 
                                                           'CONTENT_CROSS_', '.', 'merge_backup'))]
            
            for filename in files:
                if Path(filename).suffix.lower() in text_extensions:
                    filepath = Path(root) / filename
                    
                    try:
                        file_size = filepath.stat().st_size
                        content_type = self.classify_content_file(filepath)
                        
                        content_info = {
                            'path': str(filepath),
                            'filename': filename,
                            'relative_path': str(filepath.relative_to(self.music_dir)),
                            'size': file_size,
                            'type': content_type,
                            'normalized_name': self.normalize_name(filename),
                            'location': 'Music'
                        }
                        
                        self.content_files[content_type].append(content_info)
                        self.stats['total_content'] += 1
                        
                    except Exception:
                        pass
        
        # Scan ~/Documents (max 3 levels for performance)
        print(f"{Colors.CYAN}Scanning ~/Documents for content...{Colors.END}\n")
        
        for root, dirs, files in os.walk(self.docs_dir):
            # Calculate depth
            try:
                depth = len(Path(root).relative_to(self.docs_dir).parts)
            except ValueError:
                continue
            
            if depth > 3:
                dirs.clear()
                continue
            
            # Skip system directories
            dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules', 
                                                     '.Trash', 'Library', '.cache'}]
            
            for filename in files:
                if Path(filename).suffix.lower() in text_extensions:
                    filepath = Path(root) / filename
                    
                    try:
                        file_size = filepath.stat().st_size
                        
                        # Skip very large files
                        if file_size > 10 * 1024 * 1024:
                            continue
                        
                        content_type = self.classify_content_file(filepath)
                        
                        # Only include if likely related to music
                        name_lower = filename.lower()
                        if any(word in name_lower for word in ['song', 'music', 'lyric', 
                                                                 'transcript', 'audio', 'suno']):
                            content_info = {
                                'path': str(filepath),
                                'filename': filename,
                                'relative_path': str(filepath.relative_to(self.docs_dir)),
                                'size': file_size,
                                'type': content_type,
                                'normalized_name': self.normalize_name(filename),
                                'location': 'Documents'
                            }
                            
                            self.content_files[content_type].append(content_info)
                            self.stats['total_content'] += 1
                        
                    except Exception:
                        pass
        
        print(f"{Colors.GREEN}✅ Found {self.stats['total_content']} content files{Colors.END}\n")
        
        print("Content by type:")
        for content_type, files in self.content_files.items():
            if files:
                print(f"  {content_type:15} {len(files):5} files")
        print()
    
    def cross_reference_audio_content(self):
        """Match audio files with their content"""
        self.print_header("🔗 CROSS-REFERENCING AUDIO ↔ CONTENT")
        
        print(f"Matching {self.stats['total_audio']} audio files with {self.stats['total_content']} content files...\n")
        
        # Build content index
        content_index = defaultdict(list)
        for content_type, files in self.content_files.items():
            for file_info in files:
                content_index[file_info['normalized_name']].append(file_info)
        
        # Match each audio file
        matched_audio = set()
        matched_content = set()
        
        for audio in self.audio_files:
            audio_norm = audio['normalized_name']
            matches = []
            
            # Exact match
            if audio_norm in content_index:
                for content in content_index[audio_norm]:
                    matches.append({
                        **content,
                        'match_type': 'EXACT',
                        'similarity': 1.0
                    })
                    matched_content.add(content['path'])
            
            # Fuzzy match
            else:
                for content_type, files in self.content_files.items():
                    for content in files:
                        score = self.similarity_score(audio_norm, content['normalized_name'])
                        
                        if score > 0.75:  # 75% threshold
                            matches.append({
                                **content,
                                'match_type': 'FUZZY',
                                'similarity': score
                            })
                            matched_content.add(content['path'])
            
            if matches:
                self.audio_content_map[audio['path']] = {
                    'audio': audio,
                    'content': matches
                }
                matched_audio.add(audio['path'])
                self.stats['audio_with_content'] += 1
            else:
                self.orphaned_audio.append(audio)
                self.stats['audio_without_content'] += 1
        
        # Find orphaned content
        for content_type, files in self.content_files.items():
            for content in files:
                if content['path'] not in matched_content:
                    self.orphaned_content.append(content)
                    self.stats['content_without_audio'] += 1
        
        self.stats['content_with_audio'] = len(matched_content)
        
        print(f"{Colors.GREEN}✅ Matched {len(self.audio_content_map)} audio files with content{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  {len(self.orphaned_audio)} audio files WITHOUT content{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  {len(self.orphaned_content)} content files WITHOUT audio{Colors.END}\n")
    
    def save_comprehensive_reports(self):
        """Save detailed reports"""
        self.print_header("💾 SAVING COMPREHENSIVE REPORTS")
        
        # 1. Audio-Content Map
        map_file = self.output_dir / "AUDIO_CONTENT_MAP.csv"
        with open(map_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Audio_File', 'Audio_Path', 'Directory', 'Size_MB', 'Duration', 
                'Has_Embedded_Lyrics', 'Content_Files', 'Content_Types', 
                'Match_Types', 'Content_Locations'
            ])
            
            for audio_path, mapping in sorted(self.audio_content_map.items()):
                audio = mapping['audio']
                content_list = mapping['content']
                
                content_files = ' | '.join([c['filename'] for c in content_list])
                content_types = ' | '.join([c['type'] for c in content_list])
                match_types = ' | '.join([c['match_type'] for c in content_list])
                content_locs = ' | '.join([c['location'] for c in content_list])
                
                writer.writerow([
                    audio['filename'],
                    audio['relative_path'],
                    audio['directory'],
                    f"{audio['size'] / (1024**2):.2f}",
                    f"{audio['metadata']['duration']:.0f}s",
                    'YES' if audio['metadata']['has_embedded_lyrics'] else 'NO',
                    content_files,
                    content_types,
                    match_types,
                    content_locs
                ])
        
        print(f"{Colors.GREEN}✅ Audio-Content Map: {map_file.name}{Colors.END}")
        
        # 2. Orphaned Audio
        orphaned_audio_file = self.output_dir / "ORPHANED_AUDIO_NO_CONTENT.csv"
        with open(orphaned_audio_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Filename', 'Path', 'Directory', 'Size_MB', 'Duration', 
                'Has_Embedded_Lyrics', 'Recommendation'
            ])
            
            for audio in sorted(self.orphaned_audio, key=lambda x: x['relative_path']):
                recommendation = 'May need transcript/lyrics' if not audio['metadata']['has_embedded_lyrics'] else 'Has embedded lyrics'
                
                writer.writerow([
                    audio['filename'],
                    audio['relative_path'],
                    audio['directory'],
                    f"{audio['size'] / (1024**2):.2f}",
                    f"{audio['metadata']['duration']:.0f}s",
                    'YES' if audio['metadata']['has_embedded_lyrics'] else 'NO',
                    recommendation
                ])
        
        print(f"{Colors.GREEN}✅ Orphaned Audio: {orphaned_audio_file.name}{Colors.END}")
        
        # 3. Orphaned Content
        orphaned_content_file = self.output_dir / "ORPHANED_CONTENT_NO_AUDIO.csv"
        with open(orphaned_content_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Filename', 'Path', 'Type', 'Location', 'Size_KB', 'Recommendation'
            ])
            
            for content in sorted(self.orphaned_content, key=lambda x: x['path']):
                recommendation = 'Review before deleting - may be draft/standalone'
                
                writer.writerow([
                    content['filename'],
                    content['relative_path'] if content['location'] == 'Music' else content['path'],
                    content['type'],
                    content['location'],
                    f"{content['size'] / 1024:.2f}",
                    recommendation
                ])
        
        print(f"{Colors.GREEN}✅ Orphaned Content: {orphaned_content_file.name}{Colors.END}")
        
        # 4. Summary Report
        summary_file = self.output_dir / "COMPREHENSIVE_SCAN_REPORT.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 🎵 Comprehensive Music Content Scan Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Audio Files | {self.stats['total_audio']:,} |\n")
            f.write(f"| Total Content Files | {self.stats['total_content']:,} |\n")
            f.write(f"| Total Music Size | {self.stats['total_size_gb']:.2f} GB |\n")
            f.write(f"| **Audio WITH Content** | **{self.stats['audio_with_content']:,}** |\n")
            f.write(f"| **Audio WITHOUT Content** | **{self.stats['audio_without_content']:,}** |\n")
            f.write(f"| Content WITH Audio | {self.stats['content_with_audio']:,} |\n")
            f.write(f"| Content WITHOUT Audio | {self.stats['content_without_audio']:,} |\n\n")
            
            f.write("## 🎯 Content Coverage\n\n")
            coverage = (self.stats['audio_with_content'] / self.stats['total_audio'] * 100) if self.stats['total_audio'] > 0 else 0
            f.write(f"**{coverage:.1f}%** of audio files have associated content\n\n")
            
            f.write("## ⚠️ Critical Findings\n\n")
            f.write(f"### Audio Without Content ({self.stats['audio_without_content']} files)\n\n")
            f.write("These audio files have NO associated transcripts, lyrics, or metadata.\n")
            f.write("Review before cleanup to ensure you don't need this content.\n\n")
            
            f.write(f"### Content Without Audio ({self.stats['content_without_audio']} files)\n\n")
            f.write("These content files have NO associated audio.\n")
            f.write("**IMPORTANT:** Review before deleting - may be drafts or standalone stories.\n\n")
            
            f.write("## 📁 Content Types Found\n\n")
            for content_type, files in self.content_files.items():
                if files:
                    f.write(f"- **{content_type}:** {len(files)} files\n")
            f.write("\n")
            
            f.write("## ✅ Safe to Proceed with Cleanup?\n\n")
            if self.stats['content_without_audio'] == 0:
                f.write("✅ **YES** - No orphaned content found. All content is matched to audio.\n\n")
            else:
                f.write(f"⚠️ **REVIEW FIRST** - {self.stats['content_without_audio']} orphaned content files found.\n")
                f.write("Check `ORPHANED_CONTENT_NO_AUDIO.csv` before proceeding.\n\n")
        
        print(f"{Colors.GREEN}✅ Summary Report: {summary_file.name}{Colors.END}")
        
        return summary_file
    
    def run(self):
        """Run comprehensive scan"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║        🎵 COMPREHENSIVE MUSIC CONTENT SCANNER 🎵                              ║")
        print("║                                                                               ║")
        print("║      Scan Every MP3 → Find All Content → Ensure Nothing Lost                 ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # 1. Scan audio files
        self.scan_audio_files()
        
        # 2. Scan content files
        self.scan_content_files()
        
        # 3. Cross-reference
        self.cross_reference_audio_content()
        
        # 4. Save reports
        summary_file = self.save_comprehensive_reports()
        
        # Final summary
        self.print_header("✅ COMPREHENSIVE SCAN COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Audio files: {Colors.CYAN}{self.stats['total_audio']:,}{Colors.END}")
        print(f"  Content files: {Colors.CYAN}{self.stats['total_content']:,}{Colors.END}")
        print(f"  Total size: {Colors.CYAN}{self.stats['total_size_gb']:.2f} GB{Colors.END}")
        print(f"  Audio WITH content: {Colors.GREEN}{self.stats['audio_with_content']:,}{Colors.END}")
        print(f"  Audio WITHOUT content: {Colors.YELLOW}{self.stats['audio_without_content']:,}{Colors.END}")
        print(f"  Orphaned content: {Colors.YELLOW}{self.stats['content_without_audio']:,}{Colors.END}\n")
        
        coverage = (self.stats['audio_with_content'] / self.stats['total_audio'] * 100) if self.stats['total_audio'] > 0 else 0
        print(f"{Colors.BOLD}Coverage: {Colors.CYAN}{coverage:.1f}%{Colors.END} of audio has associated content{Colors.BOLD}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Reports Directory:{Colors.END}")
        print(f"  {self.output_dir}\n")
        
        print(f"{Colors.BOLD}📝 Key Reports:{Colors.END}")
        print(f"  1. AUDIO_CONTENT_MAP.csv - Complete audio→content mapping")
        print(f"  2. ORPHANED_AUDIO_NO_CONTENT.csv - Audio without transcripts/lyrics")
        print(f"  3. ORPHANED_CONTENT_NO_AUDIO.csv - Content to review before cleanup")
        print(f"  4. COMPREHENSIVE_SCAN_REPORT.md - Full analysis\n")
        
        if self.stats['content_without_audio'] > 0:
            print(f"{Colors.YELLOW}⚠️  IMPORTANT: {self.stats['content_without_audio']} orphaned content files found!{Colors.END}")
            print(f"{Colors.YELLOW}Review ORPHANED_CONTENT_NO_AUDIO.csv before any cleanup.{Colors.END}\n")
        
        print(f"{Colors.GREEN}✅ Safe to proceed with cleanup after reviewing orphaned content.{Colors.END}\n")


def main():
    # Check for mutagen
    try:
        import mutagen
    except ImportError:
        print(f"{Colors.RED}❌ Mutagen is required. Install with:{Colors.END}")
        print(f"{Colors.CYAN}pip install mutagen{Colors.END}\n")
        return
    
    scanner = ComprehensiveMusicContentScanner()
    scanner.run()


if __name__ == "__main__":
    main()
