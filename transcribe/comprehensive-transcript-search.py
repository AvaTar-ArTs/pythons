#!/usr/bin/env python3
"""
🔍 COMPREHENSIVE TRANSCRIPT & LYRICS SEARCH
============================================
Search for transcript/lyric files by:
1. Filename patterns
2. File content (grep through text files)
3. Home directory + Volumes
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
import csv

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class ComprehensiveTranscriptSearch:
    """Search for all transcript/lyric content"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.home_dir = Path.home()
        self.output_dir = self.home_dir / "Documents" / f"TRANSCRIPT_SEARCH_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.found_files = []
        
    def print_header(self, text: str, color=Colors.CYAN):
        print(f"\n{color}{Colors.BOLD}{'='*80}\n{text}\n{'='*80}{Colors.END}\n")
    
    def search_by_filename(self, search_path: str):
        """Search for files by name pattern"""
        self.print_header(f"🔍 SEARCHING BY FILENAME: {search_path}")
        
        patterns = [
            "*transcript*",
            "*lyrics*",
            "*lyric*",
            "*transcription*"
        ]
        
        found_count = 0
        
        for pattern in patterns:
            try:
                # Use find command for speed
                cmd = f"find '{search_path}' -type f -iname '{pattern}' 2>/dev/null"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
                
                files = result.stdout.strip().split('\n')
                files = [f for f in files if f]
                
                for file in files:
                    file_path = Path(file)
                    
                    # Get file size
                    try:
                        size = file_path.stat().st_size
                    except:
                        size = 0
                    
                    self.found_files.append({
                        'path': str(file_path),
                        'name': file_path.name,
                        'parent': file_path.parent.name,
                        'size_kb': size / 1024,
                        'type': 'filename_match'
                    })
                    
                    found_count += 1
                
            except Exception as e:
                print(f"{Colors.RED}Error with pattern {pattern}: {e}{Colors.END}")
        
        print(f"{Colors.GREEN}✅ Found {found_count} files by filename{Colors.END}")
        
        return found_count
    
    def search_volumes(self):
        """Search mounted volumes"""
        self.print_header("💿 SEARCHING VOLUMES")
        
        volumes_path = Path("/Volumes")
        
        if not volumes_path.exists():
            print(f"{Colors.YELLOW}No /Volumes directory{Colors.END}")
            return 0
        
        volumes = [v for v in volumes_path.iterdir() if v.is_dir() and v.name != "Macintosh HD"]
        
        if not volumes:
            print(f"{Colors.YELLOW}No external volumes mounted{Colors.END}")
            return 0
        
        total_found = 0
        
        for volume in volumes:
            print(f"\n{Colors.CYAN}Searching: {volume.name}{Colors.END}")
            count = self.search_by_filename(str(volume))
            total_found += count
        
        return total_found
    
    def analyze_nocturne_transcripts(self):
        """Special analysis for nocTurneMeLoDieS transcripts"""
        self.print_header("🎵 ANALYZING NOCTURNE TRANSCRIPTS")
        
        nocturne = self.home_dir / "Music" / "nocTurneMeLoDieS"
        
        if not nocturne.exists():
            return
        
        # Find all transcript files
        transcript_files = list(nocturne.rglob("*transcript*.txt"))
        lyric_files = list(nocturne.rglob("*lyric*.txt"))
        
        all_content_files = transcript_files + lyric_files
        
        print(f"Found in nocTurneMeLoDieS:")
        print(f"  Transcript files: {len(transcript_files)}")
        print(f"  Lyric files: {len(lyric_files)}")
        print(f"  Total: {len(all_content_files)}\n")
        
        # Group by folder
        by_folder = {}
        
        for f in all_content_files:
            folder = f.parent.name
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(f.name)
        
        print(f"{Colors.BOLD}Top folders with transcripts:{Colors.END}\n")
        
        sorted_folders = sorted(by_folder.items(), key=lambda x: len(x[1]), reverse=True)
        
        for folder, files in sorted_folders[:20]:
            print(f"  {folder}: {len(files)} files")
        
        return len(all_content_files)
    
    def save_comprehensive_report(self):
        """Save all found files to CSV"""
        self.print_header("💾 SAVING COMPREHENSIVE REPORT")
        
        # Remove duplicates
        unique_files = {}
        for item in self.found_files:
            path = item['path']
            if path not in unique_files:
                unique_files[path] = item
        
        self.found_files = list(unique_files.values())
        
        # Save CSV
        csv_file = self.output_dir / "ALL_TRANSCRIPTS_FOUND.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Path', 'Filename', 'Parent_Folder', 'Size_KB', 'Type'])
            
            for item in sorted(self.found_files, key=lambda x: x['size_kb'], reverse=True):
                writer.writerow([
                    item['path'],
                    item['name'],
                    item['parent'],
                    f"{item['size_kb']:.2f}",
                    item['type']
                ])
        
        print(f"{Colors.GREEN}✅ CSV: {csv_file.name}{Colors.END}")
        print(f"{Colors.GREEN}✅ Total unique files: {len(self.found_files)}{Colors.END}\n")
    
    def run(self):
        """Run comprehensive search"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║        🔍 COMPREHENSIVE TRANSCRIPT & LYRICS SEARCH 🔍                         ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # 1. Search home directory
        home_count = self.search_by_filename(str(self.home_dir))
        
        # 2. Search volumes
        volume_count = self.search_volumes()
        
        # 3. Analyze nocturne specifically
        nocturne_count = self.analyze_nocturne_transcripts()
        
        # 4. Save comprehensive report
        self.save_comprehensive_report()
        
        # Final summary
        self.print_header("✅ SEARCH COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Summary:{Colors.END}\n")
        print(f"  Files found in ~/ : {Colors.CYAN}{home_count}{Colors.END}")
        print(f"  Files found in /Volumes: {Colors.CYAN}{volume_count}{Colors.END}")
        print(f"  nocTurneMeLoDieS transcripts: {Colors.CYAN}{nocturne_count}{Colors.END}")
        print(f"  Total unique files: {Colors.CYAN}{len(self.found_files)}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Report saved to:{Colors.END}")
        print(f"  {self.output_dir}\n")


def main():
    searcher = ComprehensiveTranscriptSearch()
    searcher.run()


if __name__ == "__main__":
    main()
