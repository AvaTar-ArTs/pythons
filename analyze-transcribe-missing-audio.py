#!/usr/bin/env python3
"""
🔍 ANALYZE & TRANSCRIBE MISSING CONTENT
========================================
1. Scan all folders for MP3s
2. Check for existing transcripts
3. Compare against CSV records
4. Transcribe only missing content
"""

import argparse
import csv
import os
from pathlib import Path
from datetime import datetime

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class AnalyzeAndTranscribe:
    """Analyze folders and identify missing transcripts"""
    
    def __init__(self, root_dir: Path):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.root_dir = root_dir
        
        self.output_dir = self.root_dir / f"TRANSCRIPT_ANALYSIS_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'total_folders': 0,
            'total_mp3s': 0,
            'has_transcript': 0,
            'missing_transcript': 0,
            'has_analysis': 0,
            'missing_analysis': 0
        }
        
        self.missing_transcripts = []
        self.missing_analysis = []
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def normalize_filename(self, filename: str) -> str:
        """Normalize filename for matching"""
        name = Path(filename).stem
        name = name.lower()
        for suffix in ['_transcript', '_analysis', '_lyrics', '_metadata']:
            name = name.replace(suffix, '')
        return name
    
    def check_folder_content(self, folder_path: Path):
        """Check one folder for MP3s and their transcripts"""
        if not folder_path.exists() or not folder_path.is_dir():
            return
        
        mp3_files = list(folder_path.glob("*.mp3"))
        if not mp3_files:
            return
            
        self.stats['total_folders'] += 1
        
        # Get all text files (potential transcripts/analysis)
        txt_files = list(folder_path.glob("*.txt"))
        md_files = list(folder_path.glob("*.md"))
        text_files = txt_files + md_files
        
        print(f"\n{Colors.BOLD}{folder_path.relative_to(self.root_dir)}{Colors.END}")
        print(f"  MP3s: {len(mp3_files)} | Text files: {len(text_files)}")
        
        folder_missing_transcript = []
        folder_missing_analysis = []
        
        for mp3 in mp3_files:
            normalized = self.normalize_filename(mp3.name)
            self.stats['total_mp3s'] += 1
            
            has_transcript = any(
                'transcript' in f.name.lower() and normalized in self.normalize_filename(f.name)
                for f in text_files
            )
            
            has_analysis = any(
                'analysis' in f.name.lower() and normalized in self.normalize_filename(f.name)
                for f in text_files
            )
            
            if has_transcript:
                self.stats['has_transcript'] += 1
            else:
                self.stats['missing_transcript'] += 1
                folder_missing_transcript.append(mp3.name)
                self.missing_transcripts.append({
                    'folder': str(folder_path.relative_to(self.root_dir)),
                    'file': mp3.name,
                    'path': str(mp3)
                })
            
            if has_analysis:
                self.stats['has_analysis'] += 1
            else:
                self.stats['missing_analysis'] += 1
                folder_missing_analysis.append(mp3.name)
                self.missing_analysis.append({
                    'folder': str(folder_path.relative_to(self.root_dir)),
                    'file': mp3.name,
                    'path': str(mp3)
                })
        
        if folder_missing_transcript:
            print(f"  {Colors.YELLOW}Missing transcripts: {len(folder_missing_transcript)}{Colors.END}")
        else:
            print(f"  {Colors.GREEN}✅ All have transcripts{Colors.END}")
        
        if folder_missing_analysis:
            print(f"  {Colors.YELLOW}Missing analysis: {len(folder_missing_analysis)}{Colors.END}")
    
    def scan_all_folders(self):
        """Recursively scan all folders starting from root"""
        self.print_header(f"🔍 SCANNING {self.root_dir}")
        
        # Walk directory tree
        for root, dirs, files in os.walk(self.root_dir):
            # Skip hidden folders and the output directory itself
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != self.output_dir.name]
            
            folder_path = Path(root)
            self.check_folder_content(folder_path)
    
    def save_reports(self):
        """Save analysis reports to CSV files"""
        # Save missing transcripts
        if self.missing_transcripts:
            transcript_csv = self.output_dir / "MISSING_TRANSCRIPTS.csv"
            with open(transcript_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['folder', 'file', 'path'])
                writer.writeheader()
                writer.writerows(self.missing_transcripts)
            print(f"{Colors.GREEN}✅ Missing transcripts saved: {transcript_csv.name} ({len(self.missing_transcripts)} files){Colors.END}")
        
        # Save missing analysis
        if self.missing_analysis:
            analysis_csv = self.output_dir / "MISSING_ANALYSIS.csv"
            with open(analysis_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['folder', 'file', 'path'])
                writer.writeheader()
                writer.writerows(self.missing_analysis)
            print(f"{Colors.GREEN}✅ Missing analysis saved: {analysis_csv.name} ({len(self.missing_analysis)} files){Colors.END}")
        
        # Save summary statistics
        summary_txt = self.output_dir / "SUMMARY.txt"
        with open(summary_txt, 'w', encoding='utf-8') as f:
            f.write("📊 TRANSCRIPT & ANALYSIS SUMMARY\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total folders scanned: {self.stats['total_folders']}\n")
            f.write(f"Total MP3s found: {self.stats['total_mp3s']}\n\n")
            f.write("TRANSCRIPTS:\n")
            f.write(f"  ✅ Has transcript: {self.stats['has_transcript']}\n")
            f.write(f"  ❌ Missing: {self.stats['missing_transcript']}\n")
            if self.stats['total_mp3s'] > 0:
                coverage = self.stats['has_transcript']/self.stats['total_mp3s']*100
                f.write(f"  📊 Coverage: {coverage:.1f}%\n\n")
            f.write("ANALYSIS:\n")
            f.write(f"  ✅ Has analysis: {self.stats['has_analysis']}\n")
            f.write(f"  ❌ Missing: {self.stats['missing_analysis']}\n")
            if self.stats['total_mp3s'] > 0:
                coverage = self.stats['has_analysis']/self.stats['total_mp3s']*100
                f.write(f"  📊 Coverage: {coverage:.1f}%\n")
        print(f"{Colors.GREEN}✅ Summary saved: {summary_txt.name}{Colors.END}")

    def run(self):
        """Run analysis"""
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║          🔍 ANALYZE & TRANSCRIBE MISSING CONTENT 🔍                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        self.scan_all_folders()
        self.save_reports()
        
        # Final summary... (rest of run method)
        self.print_header("📊 FINAL SUMMARY", Colors.GREEN)
        
        print(f"{Colors.BOLD}Folders scanned:{Colors.END} {self.stats['total_folders']}")
        print(f"{Colors.BOLD}Total MP3s:{Colors.END} {self.stats['total_mp3s']}\n")
        
        print(f"{Colors.BOLD}TRANSCRIPTS:{Colors.END}")
        print(f"  ✅ Has transcript: {Colors.GREEN}{self.stats['has_transcript']}{Colors.END}")
        print(f"  ❌ Missing: {Colors.RED}{self.stats['missing_transcript']}{Colors.END}")
        if self.stats['total_mp3s'] > 0:
            coverage = self.stats['has_transcript']/self.stats['total_mp3s']*100
            print(f"  📊 Coverage: {coverage:.1f}%\n")
        
        print(f"{Colors.BOLD}ANALYSIS:{Colors.END}")
        print(f"  ✅ Has analysis: {Colors.GREEN}{self.stats['has_analysis']}{Colors.END}")
        print(f"  ❌ Missing: {Colors.RED}{self.stats['missing_analysis']}{Colors.END}")
        if self.stats['total_mp3s'] > 0:
            coverage = self.stats['has_analysis']/self.stats['total_mp3s']*100
            print(f"  📊 Coverage: {coverage:.1f}%\n")
        
        print(f"{Colors.BOLD}📁 Reports saved to:{Colors.END}")
        print(f"  {self.output_dir}\n")


def main():
    parser = argparse.ArgumentParser(description="Analyze and transcribe missing content in audio directories.")
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=str(Path.home() / "Music" / "nocTurneMeLoDieS"),
        help="Root directory to scan for audio files (recursive)."
    )
    
    args = parser.parse_args()
    root_dir = Path(args.directory)
    
    if not root_dir.exists():
        print(f"{Colors.RED}Error: Directory not found: {root_dir}{Colors.END}")
        return

    analyzer = AnalyzeAndTranscribe(root_dir)
    analyzer.run()

if __name__ == "__main__":
    import argparse
    main()
