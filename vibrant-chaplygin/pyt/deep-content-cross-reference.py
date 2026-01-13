#!/usr/bin/env python3
"""
📚 DEEP CONTENT CROSS-REFERENCE SCANNER
========================================
Multi-depth scan of ~/Documents for stories, lyrics, transcripts, and prompts
Cross-reference with music archives to ensure nothing is lost

Features:
✨ Deep recursive scan of ~/Documents (all depths)
✨ Find lyrics, transcripts, stories, prompts, metadata
✨ Match content to audio files by name similarity
✨ Identify orphaned content (content without audio)
✨ Identify orphaned audio (audio without content)
✨ Safe consolidation recommendations
"""

import os
import csv
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from difflib import SequenceMatcher
from typing import Dict, List, Tuple

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class DeepContentCrossReference:
    """Deep content scanner and cross-referencer"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path.home() / "Music" / f"CONTENT_CROSS_REFERENCE_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Content storage
        self.content_files = {
            'lyrics': [],
            'transcripts': [],
            'stories': [],
            'prompts': [],
            'metadata': [],
            'text': []
        }
        
        self.audio_files = []
        self.matches = []
        
        self.stats = {
            'documents_scanned': 0,
            'audio_files': 0,
            'lyrics_found': 0,
            'transcripts_found': 0,
            'stories_found': 0,
            'prompts_found': 0,
            'matched_pairs': 0,
            'orphaned_content': 0,
            'orphaned_audio': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def normalize_name(self, name: str) -> str:
        """Normalize filename for matching"""
        # Remove extension
        name = Path(name).stem
        
        # Convert to lowercase
        name = name.lower()
        
        # Remove common prefixes/suffixes
        patterns_to_remove = [
            r'^audio[_\s-]*',
            r'^song[_\s-]*',
            r'^track[_\s-]*',
            r'[_\s-]*lyrics?$',
            r'[_\s-]*transcript$',
            r'[_\s-]*story$',
            r'[_\s-]*prompt$',
            r'[_\s-]*\d+$',  # trailing numbers
            r'^\d+[_\s-]*',  # leading numbers
        ]
        
        for pattern in patterns_to_remove:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Normalize separators
        name = re.sub(r'[_\s-]+', ' ', name)
        
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        norm1 = self.normalize_name(str1)
        norm2 = self.normalize_name(str2)
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    def classify_content_file(self, filepath: Path) -> str:
        """Classify text file type"""
        name_lower = filepath.name.lower()
        
        # Read first few lines to help classify
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = ''.join(f.readlines()[:10]).lower()
        except Exception:
            first_lines = ""
        
        # Lyrics
        if 'lyric' in name_lower or 'lyrics' in name_lower:
            return 'lyrics'
        if '[verse' in first_lines or '[chorus' in first_lines:
            return 'lyrics'
        
        # Transcripts
        if 'transcript' in name_lower or 'transcription' in name_lower:
            return 'transcripts'
        if 'speaker' in first_lines or 'timestamp' in first_lines:
            return 'transcripts'
        
        # Stories
        if 'story' in name_lower or 'tale' in name_lower or 'narrative' in name_lower:
            return 'stories'
        if 'chapter' in first_lines or 'once upon' in first_lines:
            return 'stories'
        
        # Prompts
        if 'prompt' in name_lower or 'dalle' in name_lower or 'sora' in name_lower:
            return 'prompts'
        if 'generate' in first_lines or 'create an image' in first_lines:
            return 'prompts'
        
        # Metadata
        if 'metadata' in name_lower or 'info' in name_lower or 'data' in name_lower:
            return 'metadata'
        
        # Generic text
        return 'text'
    
    def scan_documents_for_content(self):
        """Deep scan ~/Documents for all text content"""
        self.print_header("📚 SCANNING ~/Documents FOR CONTENT")
        
        docs_dir = Path.home() / "Documents"
        
        print(f"Scanning {docs_dir} (all depths)...\n")
        
        # Text file extensions to scan
        text_extensions = {'.txt', '.md', '.text', '.lrc', '.srt', '.vtt', '.json'}
        
        skip_dirs = {
            '.git', '__pycache__', 'node_modules', '.Trash', 'Library',
            '.cache', 'cache', 'Cache', 'Caches', '.vscode', '.idea'
        }
        
        for root, dirs, files in os.walk(docs_dir):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
            
            current_path = Path(root)
            
            try:
                depth = len(current_path.relative_to(docs_dir).parts)
            except ValueError:
                continue
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                
                filepath = current_path / filename
                
                # Check if text file
                if filepath.suffix.lower() in text_extensions:
                    try:
                        file_size = filepath.stat().st_size
                        
                        # Skip very large files (>10MB)
                        if file_size > 10 * 1024 * 1024:
                            continue
                        
                        # Classify content type
                        content_type = self.classify_content_file(filepath)
                        
                        file_info = {
                            'path': str(filepath),
                            'name': filename,
                            'size': file_size,
                            'depth': depth,
                            'relative_path': str(filepath.relative_to(docs_dir)),
                            'type': content_type,
                            'normalized_name': self.normalize_name(filename)
                        }
                        
                        self.content_files[content_type].append(file_info)
                        self.stats['documents_scanned'] += 1
                        
                        if content_type == 'lyrics':
                            self.stats['lyrics_found'] += 1
                        elif content_type == 'transcripts':
                            self.stats['transcripts_found'] += 1
                        elif content_type == 'stories':
                            self.stats['stories_found'] += 1
                        elif content_type == 'prompts':
                            self.stats['prompts_found'] += 1
                        
                    except Exception as e:
                        pass
        
        # Summary
        print(f"{Colors.GREEN}✅ Scanned {self.stats['documents_scanned']} text files{Colors.END}\n")
        
        print("Content found:")
        for content_type, files in self.content_files.items():
            if files:
                print(f"  {content_type:15} {len(files):5} files")
        print()
    
    def load_audio_files_from_analysis(self):
        """Load audio files from previous analysis"""
        self.print_header("🎵 LOADING AUDIO FILES FROM ANALYSIS")
        
        # Find latest analysis
        music_dir = Path.home() / "Music"
        analysis_dirs = sorted(music_dir.glob("ARCHIVE_ANALYSIS_*"))
        
        if not analysis_dirs:
            print(f"{Colors.RED}❌ No previous analysis found{Colors.END}")
            return
        
        latest_analysis = analysis_dirs[-1]
        print(f"Using: {latest_analysis.name}\n")
        
        # Load file inventory
        inventory_file = latest_analysis / "COMPLETE_FILE_INVENTORY.csv"
        
        if not inventory_file.exists():
            print(f"{Colors.RED}❌ Inventory file not found{Colors.END}")
            return
        
        with open(inventory_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Type'] in ['AUDIO', 'AUDIOBOOK']:
                    self.audio_files.append({
                        'name': row['Filename'],
                        'path': row['Relative_Path'],
                        'source': row['Source_Directory'],
                        'type': row['Type'],
                        'normalized_name': self.normalize_name(row['Filename'])
                    })
        
        self.stats['audio_files'] = len(self.audio_files)
        print(f"{Colors.GREEN}✅ Loaded {len(self.audio_files)} audio files{Colors.END}\n")
    
    def cross_reference_content(self):
        """Match content files to audio files"""
        self.print_header("🔗 CROSS-REFERENCING CONTENT WITH AUDIO")
        
        print(f"Matching {self.stats['documents_scanned']} content files with {len(self.audio_files)} audio files...\n")
        
        # Build content index by normalized name
        content_index = defaultdict(list)
        for content_type, files in self.content_files.items():
            for file_info in files:
                content_index[file_info['normalized_name']].append({
                    **file_info,
                    'content_type': content_type
                })
        
        # Match audio to content
        matched_audio = set()
        matched_content = set()
        
        for audio_file in self.audio_files:
            audio_norm = audio_file['normalized_name']
            
            # Look for exact matches first
            if audio_norm in content_index:
                for content_file in content_index[audio_norm]:
                    match = {
                        'audio_name': audio_file['name'],
                        'audio_path': audio_file['path'],
                        'audio_source': audio_file['source'],
                        'content_name': content_file['name'],
                        'content_path': content_file['path'],
                        'content_type': content_file['content_type'],
                        'match_type': 'EXACT',
                        'similarity': 1.0
                    }
                    self.matches.append(match)
                    matched_audio.add(audio_file['name'])
                    matched_content.add(content_file['path'])
            
            else:
                # Fuzzy matching
                best_match = None
                best_score = 0
                
                for content_type, files in self.content_files.items():
                    for content_file in files:
                        score = self.similarity_score(audio_file['name'], content_file['name'])
                        
                        if score > best_score and score > 0.7:  # 70% threshold
                            best_score = score
                            best_match = content_file
                
                if best_match:
                    match = {
                        'audio_name': audio_file['name'],
                        'audio_path': audio_file['path'],
                        'audio_source': audio_file['source'],
                        'content_name': best_match['name'],
                        'content_path': best_match['path'],
                        'content_type': best_match['type'],
                        'match_type': 'FUZZY',
                        'similarity': best_score
                    }
                    self.matches.append(match)
                    matched_audio.add(audio_file['name'])
                    matched_content.add(best_match['path'])
        
        self.stats['matched_pairs'] = len(self.matches)
        
        # Find orphans
        orphaned_audio = [a for a in self.audio_files if a['name'] not in matched_audio]
        self.stats['orphaned_audio'] = len(orphaned_audio)
        
        orphaned_content = []
        for content_type, files in self.content_files.items():
            for file_info in files:
                if file_info['path'] not in matched_content:
                    orphaned_content.append({**file_info, 'content_type': content_type})
        self.stats['orphaned_content'] = len(orphaned_content)
        
        print(f"{Colors.GREEN}✅ Matched {len(self.matches)} audio-content pairs{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Orphaned audio (no content): {len(orphaned_audio)}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Orphaned content (no audio): {len(orphaned_content)}{Colors.END}\n")
        
        return orphaned_audio, orphaned_content
    
    def save_reports(self, orphaned_audio: List, orphaned_content: List):
        """Save comprehensive reports"""
        self.print_header("💾 SAVING REPORTS")
        
        # 1. Matched pairs
        matches_file = self.output_dir / "MATCHED_AUDIO_CONTENT_PAIRS.csv"
        with open(matches_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Audio_File', 'Audio_Path', 'Audio_Source',
                'Content_File', 'Content_Path', 'Content_Type',
                'Match_Type', 'Similarity'
            ])
            
            for match in sorted(self.matches, key=lambda x: -x['similarity']):
                writer.writerow([
                    match['audio_name'],
                    match['audio_path'],
                    match['audio_source'],
                    match['content_name'],
                    match['content_path'],
                    match['content_type'],
                    match['match_type'],
                    f"{match['similarity']:.2%}"
                ])
        
        print(f"{Colors.GREEN}✅ Matched pairs: {matches_file.name}{Colors.END}")
        
        # 2. Orphaned audio
        orphaned_audio_file = self.output_dir / "ORPHANED_AUDIO_NO_CONTENT.csv"
        with open(orphaned_audio_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Audio_File', 'Path', 'Source', 'Type', 'Recommendation'])
            
            for audio in orphaned_audio:
                recommendation = 'May be safe to archive - no associated content found'
                writer.writerow([
                    audio['name'],
                    audio['path'],
                    audio['source'],
                    audio['type'],
                    recommendation
                ])
        
        print(f"{Colors.GREEN}✅ Orphaned audio: {orphaned_audio_file.name}{Colors.END}")
        
        # 3. Orphaned content
        orphaned_content_file = self.output_dir / "ORPHANED_CONTENT_NO_AUDIO.csv"
        with open(orphaned_content_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Content_File', 'Path', 'Type', 'Size_KB', 'Depth', 'Recommendation'])
            
            for content in orphaned_content:
                recommendation = 'Content without audio - review before removing'
                writer.writerow([
                    content['name'],
                    content['path'],
                    content['content_type'],
                    f"{content['size'] / 1024:.2f}",
                    content['depth'],
                    recommendation
                ])
        
        print(f"{Colors.GREEN}✅ Orphaned content: {orphaned_content_file.name}{Colors.END}")
        
        # 4. Content by type summary
        by_type_file = self.output_dir / "CONTENT_BY_TYPE_SUMMARY.csv"
        with open(by_type_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Content_Type', 'Total_Files', 'Matched_to_Audio', 'Orphaned'])
            
            for content_type, files in self.content_files.items():
                if not files:
                    continue
                
                matched = sum(1 for m in self.matches if m['content_type'] == content_type)
                orphaned = len(files) - matched
                
                writer.writerow([
                    content_type,
                    len(files),
                    matched,
                    orphaned
                ])
        
        print(f"{Colors.GREEN}✅ Summary by type: {by_type_file.name}{Colors.END}")
        
        # 5. Markdown report
        report_file = self.output_dir / "CROSS_REFERENCE_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 📚 Deep Content Cross-Reference Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Documents Scanned | {self.stats['documents_scanned']:,} |\n")
            f.write(f"| Audio Files | {self.stats['audio_files']:,} |\n")
            f.write(f"| Lyrics Found | {self.stats['lyrics_found']:,} |\n")
            f.write(f"| Transcripts Found | {self.stats['transcripts_found']:,} |\n")
            f.write(f"| Stories Found | {self.stats['stories_found']:,} |\n")
            f.write(f"| Prompts Found | {self.stats['prompts_found']:,} |\n")
            f.write(f"| **Matched Pairs** | **{self.stats['matched_pairs']:,}** |\n")
            f.write(f"| Orphaned Audio | {self.stats['orphaned_audio']:,} |\n")
            f.write(f"| Orphaned Content | {self.stats['orphaned_content']:,} |\n\n")
            
            f.write("## ⚠️ Important Findings\n\n")
            f.write(f"### Audio Files Without Content\n\n")
            f.write(f"Found **{self.stats['orphaned_audio']}** audio files with no associated content.\n")
            f.write(f"These may be safe to archive/remove.\n\n")
            
            f.write(f"### Content Without Audio\n\n")
            f.write(f"Found **{self.stats['orphaned_content']}** content files with no associated audio.\n")
            f.write(f"Review these before removing any content - they may be:\n")
            f.write(f"- Drafts for future songs\n")
            f.write(f"- Story fragments\n")
            f.write(f"- Standalone creative writing\n\n")
            
            f.write("## 🎯 Recommendations\n\n")
            f.write("1. **Review Orphaned Content** - Check `ORPHANED_CONTENT_NO_AUDIO.csv` before removing anything\n")
            f.write("2. **Preserve Matched Pairs** - Ensure audio-content pairs stay together during consolidation\n")
            f.write("3. **Archive Safely** - When archiving duplicates, verify content files are preserved\n\n")
        
        print(f"{Colors.GREEN}✅ Full report: {report_file.name}{Colors.END}")
        
        return report_file
    
    def run(self):
        """Run complete cross-reference analysis"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           📚 DEEP CONTENT CROSS-REFERENCE SCANNER 📚                          ║")
        print("║                                                                               ║")
        print("║        Stories · Lyrics · Transcripts · Prompts → Audio Matching             ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # 1. Scan ~/Documents for content
        self.scan_documents_for_content()
        
        # 2. Load audio files from analysis
        self.load_audio_files_from_analysis()
        
        # 3. Cross-reference
        orphaned_audio, orphaned_content = self.cross_reference_content()
        
        # 4. Save reports
        report_file = self.save_reports(orphaned_audio, orphaned_content)
        
        # Final summary
        self.print_header("✅ CROSS-REFERENCE COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Content files scanned: {Colors.CYAN}{self.stats['documents_scanned']:,}{Colors.END}")
        print(f"  Audio files analyzed: {Colors.CYAN}{self.stats['audio_files']:,}{Colors.END}")
        print(f"  Matched pairs: {Colors.GREEN}{self.stats['matched_pairs']:,}{Colors.END}")
        print(f"  Orphaned audio: {Colors.YELLOW}{self.stats['orphaned_audio']:,}{Colors.END}")
        print(f"  Orphaned content: {Colors.YELLOW}{self.stats['orphaned_content']:,}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Output Directory:{Colors.END}")
        print(f"  {self.output_dir}\n")
        
        print(f"{Colors.BOLD}📝 Key Reports:{Colors.END}")
        print(f"  1. MATCHED_AUDIO_CONTENT_PAIRS.csv - Audio with associated content")
        print(f"  2. ORPHANED_AUDIO_NO_CONTENT.csv - Audio without content (may be safe to archive)")
        print(f"  3. ORPHANED_CONTENT_NO_AUDIO.csv - Content without audio (REVIEW before removing!)")
        print(f"  4. CROSS_REFERENCE_REPORT.md - Full analysis\n")
        
        print(f"{Colors.YELLOW}⚠️  IMPORTANT:{Colors.END}")
        print(f"{Colors.YELLOW}Review ORPHANED_CONTENT_NO_AUDIO.csv before removing any duplicates!{Colors.END}")
        print(f"{Colors.YELLOW}This ensures stories/lyrics aren't lost during consolidation.{Colors.END}\n")


def main():
    scanner = DeepContentCrossReference()
    scanner.run()


if __name__ == "__main__":
    main()
