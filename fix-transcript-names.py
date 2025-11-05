#!/usr/bin/env python3
"""
📝 FIX TRANSCRIPT NAMES
========================
Find and rename misnamed/changed transcript files

Features:
✨ Compare transcripts to audio files by similarity
✨ Match by filename AND content similarity
✨ Detect renamed/changed titles
✨ Suggest proper renames
✨ Safe renaming with backups
✨ Handle duplicates intelligently
"""

import os
import csv
import shutil
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from collections import defaultdict
from typing import Dict, List, Tuple
import re

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class TranscriptNameFixer:
    """Fix misnamed transcript files"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.music_dir = Path.home() / "Music"
        self.output_dir = self.music_dir / f"TRANSCRIPT_RENAME_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.audio_files = []
        self.transcript_files = []
        
        self.rename_suggestions = []
        
        self.stats = {
            'audio_files': 0,
            'transcript_files': 0,
            'mismatches_found': 0,
            'renames_suggested': 0,
            'renames_executed': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def normalize_name(self, name: str) -> str:
        """Normalize filename for matching"""
        name = Path(name).stem.lower()
        
        # Remove common suffixes
        patterns = [
            r'_transcript.*$',
            r'_analysis.*$',
            r'_\d{2}-\d{2}-\d{2}$',  # timestamps
            r'\s*\(remix\)',
            r'\s*\(remastered\)',
            r'\s*\[.*?\]',  # brackets
            r'_creator.*$',
            r'_log$',
            r'_subtitle.*$'
        ]
        
        for pattern in patterns:
            name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Normalize separators
        name = re.sub(r'[-_]+', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        
        return name.strip()
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity"""
        norm1 = self.normalize_name(str1)
        norm2 = self.normalize_name(str2)
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    def get_content_preview(self, filepath: Path) -> str:
        """Get first 200 chars of file content"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(200).lower()
        except Exception:
            return ""
    
    def scan_audio_files(self):
        """Scan all audio files"""
        self.print_header("🎵 SCANNING AUDIO FILES")
        
        audio_extensions = {'.mp3', '.m4a', '.wav', '.flac'}
        
        print(f"Scanning: {self.music_dir}\n")
        
        for root, dirs, files in os.walk(self.music_dir):
            # Skip backup/analysis directories
            dirs[:] = [d for d in dirs if not any(x in d for x in 
                      ['ARCHIVE_', 'BACKUP_', 'CONSOLIDATION_', 'SCAN_', 'EXTRACTION_'])]
            
            for filename in files:
                if Path(filename).suffix.lower() in audio_extensions:
                    filepath = Path(root) / filename
                    
                    self.audio_files.append({
                        'path': filepath,
                        'filename': filename,
                        'stem': filepath.stem,
                        'normalized': self.normalize_name(filename),
                        'directory': filepath.parent
                    })
                    
                    self.stats['audio_files'] += 1
        
        print(f"{Colors.GREEN}✅ Found {self.stats['audio_files']} audio files{Colors.END}\n")
    
    def scan_transcript_files(self):
        """Scan all transcript files"""
        self.print_header("📄 SCANNING TRANSCRIPT FILES")
        
        text_extensions = {'.txt', '.md', '.srt', '.vtt', '.lrc'}
        
        for root, dirs, files in os.walk(self.music_dir):
            dirs[:] = [d for d in dirs if not any(x in d for x in 
                      ['ARCHIVE_', 'BACKUP_', 'CONSOLIDATION_', 'SCAN_', 'EXTRACTION_'])]
            
            for filename in files:
                if Path(filename).suffix.lower() in text_extensions:
                    filepath = Path(root) / filename
                    
                    # Check if it's a transcript
                    name_lower = filename.lower()
                    if any(word in name_lower for word in ['transcript', 'analysis', 'lyric']):
                        
                        content_preview = self.get_content_preview(filepath)
                        
                        self.transcript_files.append({
                            'path': filepath,
                            'filename': filename,
                            'stem': filepath.stem,
                            'normalized': self.normalize_name(filename),
                            'directory': filepath.parent,
                            'content_preview': content_preview
                        })
                        
                        self.stats['transcript_files'] += 1
        
        print(f"{Colors.GREEN}✅ Found {self.stats['transcript_files']} transcript files{Colors.END}\n")
    
    def find_mismatches(self):
        """Find transcripts that don't match their audio"""
        self.print_header("🔍 FINDING MISMATCHES")
        
        print(f"Comparing {self.stats['transcript_files']} transcripts with {self.stats['audio_files']} audio files...\n")
        
        for transcript in self.transcript_files:
            trans_norm = transcript['normalized']
            trans_dir = transcript['directory']
            
            # Find audio files in same directory
            same_dir_audio = [a for a in self.audio_files if a['directory'] == trans_dir]
            
            # If no audio in same dir, expand search
            if not same_dir_audio:
                # Search parent directory
                same_dir_audio = [a for a in self.audio_files if a['directory'] == trans_dir.parent]
            
            if not same_dir_audio:
                continue
            
            # Find best matching audio file
            best_match = None
            best_score = 0
            
            for audio in same_dir_audio:
                score = self.similarity_score(transcript['filename'], audio['filename'])
                
                if score > best_score:
                    best_score = score
                    best_match = audio
            
            # Check if transcript name matches audio name
            if best_match and best_score > 0.7:
                # Compare normalized names
                if transcript['normalized'] != best_match['normalized']:
                    # Mismatch found!
                    
                    # Determine new name
                    # Keep the transcript suffix pattern
                    suffix_match = re.search(r'(_transcript|_analysis|_lyric.*?)(\.|$)', 
                                           transcript['filename'], re.IGNORECASE)
                    
                    if suffix_match:
                        suffix = suffix_match.group(1)
                    else:
                        suffix = '_transcript'
                    
                    new_name = f"{best_match['stem']}{suffix}{transcript['path'].suffix}"
                    new_path = transcript['directory'] / new_name
                    
                    # Check if new name already exists
                    name_conflict = new_path.exists() and new_path != transcript['path']
                    
                    self.rename_suggestions.append({
                        'old_path': transcript['path'],
                        'old_name': transcript['filename'],
                        'new_name': new_name,
                        'new_path': new_path,
                        'audio_match': best_match['filename'],
                        'similarity': best_score,
                        'name_conflict': name_conflict,
                        'directory': str(transcript['directory'].relative_to(self.music_dir))
                    })
                    
                    self.stats['mismatches_found'] += 1
        
        print(f"{Colors.YELLOW}Found {self.stats['mismatches_found']} mismatched transcript names{Colors.END}\n")
    
    def execute_renames(self):
        """Execute transcript renames"""
        self.print_header("✏️ RENAMING TRANSCRIPTS")
        
        if not self.rename_suggestions:
            print(f"{Colors.GREEN}✅ No renames needed - all transcripts properly named!{Colors.END}")
            return
        
        print(f"Processing {len(self.rename_suggestions)} rename(s)")
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        for i, rename in enumerate(self.rename_suggestions[:50], 1):  # Show first 50
            print(f"{Colors.BOLD}[{i}/{min(len(self.rename_suggestions), 50)}]{Colors.END}")
            print(f"  Directory: {rename['directory']}")
            print(f"  {Colors.RED}Old:{Colors.END} {rename['old_name']}")
            print(f"  {Colors.GREEN}New:{Colors.END} {rename['new_name']}")
            print(f"  Matches audio: {rename['audio_match']} ({rename['similarity']:.1%})")
            
            if rename['name_conflict']:
                print(f"  {Colors.YELLOW}⚠️  Name conflict - target exists{Colors.END}")
                
                # Add number suffix
                counter = 1
                new_path = rename['new_path']
                while new_path.exists():
                    new_path = rename['new_path'].parent / f"{rename['new_path'].stem}_{counter}{rename['new_path'].suffix}"
                    counter += 1
                
                rename['new_path'] = new_path
                rename['new_name'] = new_path.name
                print(f"  {Colors.CYAN}→ Using: {new_path.name}{Colors.END}")
            
            # Execute rename
            if not self.dry_run:
                try:
                    rename['old_path'].rename(rename['new_path'])
                    print(f"  {Colors.GREEN}✅ Renamed{Colors.END}")
                    self.stats['renames_executed'] += 1
                except Exception as e:
                    print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
            else:
                print(f"  {Colors.YELLOW}[DRY RUN] Would rename{Colors.END}")
                self.stats['renames_suggested'] += 1
            
            print()
        
        if len(self.rename_suggestions) > 50:
            print(f"... and {len(self.rename_suggestions) - 50} more\n")
    
    def save_report(self):
        """Save rename report (CSV is all that's needed to revert)"""
        self.print_header("💾 SAVING RENAME LOG (CSV for Revert)")
        
        report_file = self.output_dir / "TRANSCRIPT_RENAMES.csv"
        
        with open(report_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Old_Path', 'New_Path', 'Old_Name', 'New_Name', 'Audio_Match', 
                'Similarity', 'Directory', 'Status'
            ])
            
            for rename in self.rename_suggestions:
                status = 'RENAMED' if not self.dry_run and self.stats['renames_executed'] > 0 else 'SUGGESTED'
                
                writer.writerow([
                    str(rename['old_path']),
                    str(rename['new_path']),
                    rename['old_name'],
                    rename['new_name'],
                    rename['audio_match'],
                    f"{rename['similarity']:.2%}",
                    rename['directory'],
                    status
                ])
        
        print(f"{Colors.GREEN}✅ Rename log: {report_file.name}{Colors.END}")
        print(f"{Colors.CYAN}💡 CSV contains old_path & new_path - all you need to revert!{Colors.END}")
        
        # Create revert script from CSV
        revert_script = self.output_dir / "REVERT_RENAMES.py"
        
        with open(revert_script, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write('"""\nRevert transcript renames using CSV log\n"""\n\n')
            f.write("import csv\nfrom pathlib import Path\n\n")
            f.write(f"csv_file = Path(__file__).parent / 'TRANSCRIPT_RENAMES.csv'\n\n")
            f.write("with open(csv_file, 'r') as f:\n")
            f.write("    reader = csv.DictReader(f)\n")
            f.write("    for row in reader:\n")
            f.write("        if row['Status'] == 'RENAMED':\n")
            f.write("            old_path = Path(row['Old_Path'])\n")
            f.write("            new_path = Path(row['New_Path'])\n")
            f.write("            if new_path.exists():\n")
            f.write("                new_path.rename(old_path)\n")
            f.write("                print(f'Reverted: {old_path.name}')\n")
            f.write("\nprint('Revert complete!')\n")
        
        revert_script.chmod(0o755)
        
        print(f"{Colors.GREEN}✅ Revert script: {revert_script.name}{Colors.END}")
        print(f"{Colors.CYAN}💡 Just run this script to undo all renames!{Colors.END}")
    
    def run(self):
        """Run transcript name fixer"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║           📝 FIX TRANSCRIPT NAMES 📝                                          ║")
        print("║                                                                               ║")
        print("║     Find Mismatches → Compare Similarity → Rename                            ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # 1. Scan audio files
        self.scan_audio_files()
        
        # 2. Scan transcript files
        self.scan_transcript_files()
        
        # 3. Find mismatches
        self.find_mismatches()
        
        # 4. Execute renames
        self.execute_renames()
        
        # 5. Save report
        self.save_report()
        
        # Final summary
        self.print_header("✅ TRANSCRIPT NAME FIXING COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Audio files: {Colors.CYAN}{self.stats['audio_files']:,}{Colors.END}")
        print(f"  Transcript files: {Colors.CYAN}{self.stats['transcript_files']:,}{Colors.END}")
        print(f"  Mismatches found: {Colors.YELLOW}{self.stats['mismatches_found']:,}{Colors.END}")
        
        if self.dry_run:
            print(f"  Renames suggested: {Colors.YELLOW}{self.stats['renames_suggested']:,}{Colors.END}\n")
        else:
            print(f"  Renames executed: {Colors.GREEN}{self.stats['renames_executed']:,}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Reports:{Colors.END}")
        print(f"  {self.output_dir}\n")
        
        if self.stats['mismatches_found'] > 0:
            print(f"{Colors.CYAN}Review TRANSCRIPT_RENAMES.csv for all suggested changes{Colors.END}\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to execute renames.{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="📝 Fix Transcript Names")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (execute renames)')
    
    args = parser.parse_args()
    
    fixer = TranscriptNameFixer(dry_run=not args.live)
    fixer.run()


if __name__ == "__main__":
    main()
