#!/usr/bin/env python3
"""
🔍 ANALYZE & TRANSCRIBE MISSING CONTENT
========================================
1. Scan all folders for MP3s
2. Check for existing transcripts
3. Compare against CSV records
4. Transcribe only missing content
"""

import os
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

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
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.output_dir = self.nocturne_dir / f"TRANSCRIPT_ANALYSIS_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'total_folders': 0,
            'total_mp3s': 0,
            'has_transcript': 0,
            'missing_transcript': 0,
            'has_analysis': 0,
            'missing_analysis': 0
        }
        
        self.folders_to_scan = []
        self.missing_transcripts = []
        self.missing_analysis = []
    
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def normalize_filename(self, filename: str) -> str:
        """Normalize filename for matching"""
        # Remove extension
        name = Path(filename).stem
        # Lowercase
        name = name.lower()
        # Remove common suffixes
        for suffix in ['_transcript', '_analysis', '_lyrics', '_metadata']:
            name = name.replace(suffix, '')
        return name
    
    def check_folder_content(self, folder_path: Path):
        """Check one folder for MP3s and their transcripts"""
        
        if not folder_path.exists() or not folder_path.is_dir():
            return
        
        # Get all MP3s
        mp3_files = list(folder_path.glob("*.mp3"))
        
        if not mp3_files:
            return
        
        # Get all text files (potential transcripts/analysis)
        txt_files = list(folder_path.glob("*.txt"))
        md_files = list(folder_path.glob("*.md"))
        
        text_files = txt_files + md_files
        
        # Create normalized lookup
        text_lookup = {self.normalize_filename(f.name): f for f in text_files}
        
        print(f"\n{Colors.BOLD}{folder_path.name}{Colors.END}")
        print(f"  MP3s: {len(mp3_files)} | Text files: {len(text_files)}")
        
        folder_missing_transcript = []
        folder_missing_analysis = []
        
        for mp3 in mp3_files:
            normalized = self.normalize_filename(mp3.name)
            
            self.stats['total_mp3s'] += 1
            
            # Check for transcript
            has_transcript = any(
                'transcript' in f.name.lower() and normalized in self.normalize_filename(f.name)
                for f in text_files
            )
            
            # Check for analysis
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
                    'folder': folder_path.name,
                    'file': mp3.name,
                    'path': str(mp3)
                })
            
            if has_analysis:
                self.stats['has_analysis'] += 1
            else:
                self.stats['missing_analysis'] += 1
                folder_missing_analysis.append(mp3.name)
                self.missing_analysis.append({
                    'folder': folder_path.name,
                    'file': mp3.name,
                    'path': str(mp3)
                })
        
        # Show summary for this folder
        if folder_missing_transcript:
            print(f"  {Colors.YELLOW}Missing transcripts: {len(folder_missing_transcript)}{Colors.END}")
            if len(folder_missing_transcript) <= 5:
                for f in folder_missing_transcript:
                    print(f"    • {f}")
            else:
                for f in folder_missing_transcript[:3]:
                    print(f"    • {f}")
                print(f"    ... and {len(folder_missing_transcript) - 3} more")
        else:
            print(f"  {Colors.GREEN}✅ All have transcripts{Colors.END}")
        
        if folder_missing_analysis:
            print(f"  {Colors.YELLOW}Missing analysis: {len(folder_missing_analysis)}{Colors.END}")
    
    def scan_all_folders(self, folder_paths):
        """Scan all provided folders"""
        self.print_header("🔍 SCANNING FOLDERS FOR MP3s & TRANSCRIPTS")
        
        for folder_str in folder_paths:
            folder_path = Path(folder_str)
            
            if folder_path.exists() and folder_path.is_dir():
                self.stats['total_folders'] += 1
                self.check_folder_content(folder_path)
    
    def save_reports(self):
        """Save missing content reports"""
        self.print_header("💾 SAVING REPORTS")
        
        # Missing transcripts CSV
        transcript_csv = self.output_dir / "MISSING_TRANSCRIPTS.csv"
        with open(transcript_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Folder', 'File', 'Full_Path'])
            
            for item in self.missing_transcripts:
                writer.writerow([item['folder'], item['file'], item['path']])
        
        print(f"{Colors.GREEN}✅ Missing transcripts: {transcript_csv.name}{Colors.END}")
        
        # Missing analysis CSV
        analysis_csv = self.output_dir / "MISSING_ANALYSIS.csv"
        with open(analysis_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Folder', 'File', 'Full_Path'])
            
            for item in self.missing_analysis:
                writer.writerow([item['folder'], item['file'], item['path']])
        
        print(f"{Colors.GREEN}✅ Missing analysis: {analysis_csv.name}{Colors.END}")
        
        # Summary report
        summary_file = self.output_dir / "SUMMARY.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("TRANSCRIPT & ANALYSIS SUMMARY\n")
            f.write("="*80 + "\n\n")
            f.write(f"Folders scanned: {self.stats['total_folders']}\n")
            f.write(f"Total MP3s: {self.stats['total_mp3s']}\n\n")
            
            f.write("TRANSCRIPTS:\n")
            f.write(f"  Has transcript: {self.stats['has_transcript']}\n")
            f.write(f"  Missing transcript: {self.stats['missing_transcript']}\n")
            f.write(f"  Coverage: {self.stats['has_transcript']/self.stats['total_mp3s']*100:.1f}%\n\n")
            
            f.write("ANALYSIS:\n")
            f.write(f"  Has analysis: {self.stats['has_analysis']}\n")
            f.write(f"  Missing analysis: {self.stats['missing_analysis']}\n")
            f.write(f"  Coverage: {self.stats['has_analysis']/self.stats['total_mp3s']*100:.1f}%\n\n")
        
        print(f"{Colors.GREEN}✅ Summary: {summary_file.name}{Colors.END}\n")
    
    def run(self, folder_paths):
        """Run analysis"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║          🔍 ANALYZE & TRANSCRIBE MISSING CONTENT 🔍                           ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # Scan all folders
        self.scan_all_folders(folder_paths)
        
        # Save reports
        self.save_reports()
        
        # Final summary
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
        
        if self.stats['missing_transcript'] > 0:
            print(f"{Colors.YELLOW}⚠️  {self.stats['missing_transcript']} MP3s need transcripts{Colors.END}")
            print(f"{Colors.CYAN}💡 Review MISSING_TRANSCRIPTS.csv for details{Colors.END}\n")
        else:
            print(f"{Colors.GREEN}✅ All MP3s have transcripts!{Colors.END}\n")


def main():
    # All folder paths from user
    folders = [
        "/Users/steven/Music/nocTurneMeLoDieS/A_New_Dawn",
        "/Users/steven/Music/nocTurneMeLoDieS/Acapela Box_Create Your Text to Speech Messages",
        "/Users/steven/Music/nocTurneMeLoDieS/All_I_Wanna_Do",
        "/Users/steven/Music/nocTurneMeLoDieS/Audio",
        "/Users/steven/Music/nocTurneMeLoDieS/Avatar ArTs_The Shadow Syndicate Metrovales",
        "/Users/steven/Music/nocTurneMeLoDieS/avatararts",
        "/Users/steven/Music/nocTurneMeLoDieS/Beautiful_Mess_Indie_Folk_Acoustic",
        "/Users/steven/Music/nocTurneMeLoDieS/Bite_in_the_Night",
        "/Users/steven/Music/nocTurneMeLoDieS/Blues_in_the_Alley",
        "/Users/steven/Music/nocTurneMeLoDieS/Cannon_Busters_(Netflix_Original_Series_Soundtrack)",
        "/Users/steven/Music/nocTurneMeLoDieS/Canyon_Songs",
        "/Users/steven/Music/nocTurneMeLoDieS/Classically_Trained",
        "/Users/steven/Music/nocTurneMeLoDieS/Cover_Collaborations,_Vol._4",
        "/Users/steven/Music/nocTurneMeLoDieS/Dance_Like_Nobodys_Watching",
        "/Users/steven/Music/nocTurneMeLoDieS/Enchanted_Woods",
        "/Users/steven/Music/nocTurneMeLoDieS/FINAL_ORGANIZED",
        "/Users/steven/Music/nocTurneMeLoDieS/Junkyard_Symphony",
        "/Users/steven/Music/nocTurneMeLoDieS/STEVEN_CHAPLINSKI",
        "/Users/steven/Music/nocTurneMeLoDieS/Uncategorized",
        "/Users/steven/Music/nocTurneMeLoDieS/SONG_BUNDLES",
    ]
    
    analyzer = AnalyzeAndTranscribe()
    analyzer.run(folders)


if __name__ == "__main__":
    main()
