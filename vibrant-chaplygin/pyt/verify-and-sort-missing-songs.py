#!/usr/bin/env python3
"""
🔍 VERIFY & SORT MISSING SONGS
================================
Deep comparison of "missing" songs against ~/Music collection
Then provide proper sorting recommendations

Features:
✨ Fuzzy match against all audio files
✨ Check by title AND duration
✨ Identify truly missing vs. misnamed files
✨ Suggest proper volume/series placement
✨ Auto-organize into existing structure
"""

import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from difflib import SequenceMatcher
from typing import Dict, List
import re
import mutagen

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class MissingSongVerifier:
    """Verify and sort missing songs"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.music_dir = Path.home() / "Music"
        self.nocturne_dir = self.music_dir / "nocTurneMeLoDieS"
        
        self.output_dir = self.music_dir / f"MISSING_SONG_VERIFICATION_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.collection_files = []
        self.missing_songs = []
        
        self.truly_missing = []
        self.found_with_diff_name = []
        
        self.stats = {
            'missing_claimed': 0,
            'truly_missing': 0,
            'found_different_name': 0,
            'organized': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def normalize_title(self, title: str) -> str:
        """Normalize for matching"""
        title = title.lower()
        # Remove punctuation and special chars
        title = re.sub(r'[^\w\s]', ' ', title)
        # Remove multiple spaces
        title = re.sub(r'\s+', ' ', title)
        return title.strip()
    
    def parse_duration(self, duration_str: str) -> int:
        """Parse duration string to seconds"""
        if ':' not in duration_str:
            return 0
        
        try:
            parts = duration_str.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            return 0
        except Exception:
            return 0
    
    def get_audio_duration(self, filepath: Path) -> int:
        """Get audio file duration in seconds"""
        try:
            audio = mutagen.File(filepath)
            if audio and hasattr(audio.info, 'length'):
                return int(audio.info.length)
        except Exception:
            pass
        return 0
    
    def similarity_score(self, str1: str, str2: str) -> float:
        """Calculate similarity"""
        norm1 = self.normalize_title(str1)
        norm2 = self.normalize_title(str2)
        return SequenceMatcher(None, norm1, norm2).ratio()
    
    def scan_collection(self):
        """Scan ~/Music collection"""
        self.print_header("🎵 SCANNING ~/Music COLLECTION")
        
        print(f"Scanning: {self.music_dir}\n")
        
        audio_extensions = {'.mp3', '.m4a', '.wav', '.flac', '.ogg'}
        scanned = 0
        
        for audio_file in self.music_dir.rglob('*'):
            if audio_file.suffix.lower() in audio_extensions:
                # Skip analysis/backup directories
                if any(x in str(audio_file) for x in ['ARCHIVE_', 'BACKUP_', 'CONSOLIDATION_', 'SCAN_']):
                    continue
                
                duration = self.get_audio_duration(audio_file)
                
                self.collection_files.append({
                    'path': audio_file,
                    'filename': audio_file.name,
                    'stem': audio_file.stem,
                    'duration': duration,
                    'relative_path': str(audio_file.relative_to(self.music_dir)),
                    'normalized': self.normalize_title(audio_file.stem)
                })
                
                scanned += 1
                if scanned % 100 == 0:
                    print(f"  Scanned {scanned} files...", end='\r')
        
        print(f"\n{Colors.GREEN}✅ Scanned {len(self.collection_files)} audio files{Colors.END}\n")
    
    def load_missing_songs(self):
        """Load the 27 missing songs"""
        self.print_header("📋 LOADING MISSING SONGS LIST")
        
        # Find latest extraction
        extraction_dirs = sorted(self.music_dir.glob("ARCHIVE_EXTRACTION_*"))
        
        if not extraction_dirs:
            print(f"{Colors.RED}❌ No extraction report found{Colors.END}")
            return
        
        missing_file = extraction_dirs[-1] / "MISSING_SONGS.csv"
        
        with open(missing_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.missing_songs.append({
                    'title': row['Title'],
                    'duration_str': row['Duration'],
                    'duration_sec': self.parse_duration(row['Duration']),
                    'genre': row['Genre'],
                    'link': row['Suno_Link'],
                    'normalized': self.normalize_title(row['Title'])
                })
        
        self.stats['missing_claimed'] = len(self.missing_songs)
        print(f"{Colors.CYAN}Loaded {len(self.missing_songs)} claimed missing songs{Colors.END}\n")
    
    def verify_missing_songs(self):
        """Verify which songs are truly missing"""
        self.print_header("🔍 VERIFYING MISSING SONGS")
        
        print(f"Comparing {len(self.missing_songs)} songs against {len(self.collection_files)} collection files...\n")
        
        for missing in self.missing_songs:
            title = missing['title']
            duration = missing['duration_sec']
            
            # Try to find match
            best_match = None
            best_score = 0
            best_duration_diff = 999
            
            for collection_file in self.collection_files:
                # Title similarity
                title_score = self.similarity_score(title, collection_file['stem'])
                
                # Duration match (within 3 seconds)
                duration_diff = abs(duration - collection_file['duration'])
                
                # Combined matching
                if title_score > 0.7 or (title_score > 0.5 and duration_diff <= 3):
                    if title_score > best_score or (title_score == best_score and duration_diff < best_duration_diff):
                        best_score = title_score
                        best_match = collection_file
                        best_duration_diff = duration_diff
            
            if best_match and best_score > 0.75:
                # Found with different name
                self.found_with_diff_name.append({
                    'missing_title': title,
                    'missing_duration': duration,
                    'found_title': best_match['stem'],
                    'found_duration': best_match['duration'],
                    'found_path': best_match['relative_path'],
                    'similarity': best_score,
                    'duration_diff': best_duration_diff,
                    'genre': missing['genre']
                })
                self.stats['found_different_name'] += 1
            else:
                # Truly missing
                self.truly_missing.append(missing)
                self.stats['truly_missing'] += 1
        
        print(f"{Colors.GREEN}✅ Found with different names: {len(self.found_with_diff_name)}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Truly missing: {len(self.truly_missing)}{Colors.END}\n")
    
    def suggest_organization(self):
        """Suggest where missing songs should go"""
        self.print_header("📂 ORGANIZATION SUGGESTIONS")
        
        if not self.truly_missing:
            print(f"{Colors.GREEN}✅ No truly missing songs to organize!{Colors.END}")
            return {}
        
        # Categorize by theme
        by_series = defaultdict(list)
        
        for song in self.truly_missing:
            title_lower = song['title'].lower()
            genre = song['genre'].lower()
            
            # Determine series based on title/genre
            if 'moonly' in title_lower or 'moonlit' in title_lower or 'moonlight' in title_lower:
                by_series['Moonlight_Serenade_Vol_1'].append(song)
            elif 'alley' in title_lower and ('blues' in title_lower or 'blues' in genre):
                by_series['Blues_in_the_Alley_Vol_3'].append(song)
            elif 'junkyard' in title_lower or 'trash' in title_lower or 'rubbish' in title_lower:
                by_series['Junkyard_Symphony_Vol_4'].append(song)
            elif 'king' in title_lower or 'queen' in title_lower or 'royalty' in title_lower:
                by_series['Junkyard_Symphony_Vol_4'].append(song)
            elif 'howl' in title_lower or 'cat' in title_lower:
                by_series['Feline_Tales_Vol_1'].append(song)
            elif 'project 2025' in title_lower:
                by_series['Project_2025_Series'].append(song)
            elif 'hero' in title_lower or 'villain' in title_lower:
                by_series['Heroes_Rise_Vol_1'].append(song)
            elif 'dance' in title_lower:
                by_series['Upbeat_Collection_Vol_1'].append(song)
            else:
                by_series['Steven_Chaplinski_Collection_Vol_13'].append(song)
        
        print("Suggested organization:\n")
        
        for series, songs in sorted(by_series.items()):
            print(f"{Colors.BOLD}{series}:{Colors.END} {len(songs)} songs")
            for song in songs:
                print(f"  • {song['title']} ({song['duration_str']})")
            print()
        
        return by_series
    
    def save_reports(self, by_series: Dict):
        """Save verification and organization reports"""
        self.print_header("💾 SAVING REPORTS")
        
        # 1. Found with different names
        if self.found_with_diff_name:
            found_file = self.output_dir / "FOUND_WITH_DIFFERENT_NAMES.csv"
            with open(found_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Missing_Title', 'Missing_Duration', 'Found_As', 
                    'Found_Duration', 'Found_Path', 'Similarity', 
                    'Duration_Diff', 'Recommendation'
                ])
                
                for match in self.found_with_diff_name:
                    writer.writerow([
                        match['missing_title'],
                        match['missing_duration'],
                        match['found_title'],
                        match['found_duration'],
                        match['found_path'],
                        f"{match['similarity']:.2%}",
                        f"{match['duration_diff']}s",
                        'Already in collection (different name)'
                    ])
            
            print(f"{Colors.GREEN}✅ Found songs: {found_file.name}{Colors.END}")
        
        # 2. Truly missing with organization plan
        if self.truly_missing:
            missing_file = self.output_dir / "TRULY_MISSING_WITH_ORGANIZATION.csv"
            with open(missing_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Title', 'Duration', 'Genre', 'Suno_Link', 
                    'Suggested_Location', 'Download_To'
                ])
                
                for series, songs in by_series.items():
                    target_dir = self.nocturne_dir / series / "files"
                    
                    for song in songs:
                        writer.writerow([
                            song['title'],
                            song['duration_str'],
                            song['genre'],
                            song['link'],
                            series,
                            str(target_dir)
                        ])
            
            print(f"{Colors.GREEN}✅ Truly missing: {missing_file.name}{Colors.END}")
        
        # 3. Summary report
        summary_file = self.output_dir / "VERIFICATION_SUMMARY.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("# 🔍 Missing Songs Verification Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Claimed Missing | {self.stats['missing_claimed']} |\n")
            f.write(f"| **Truly Missing** | **{self.stats['truly_missing']}** |\n")
            f.write(f"| Found (Different Name) | {self.stats['found_different_name']} |\n\n")
            
            if self.found_with_diff_name:
                f.write("## ✅ Found in Collection (Different Names)\n\n")
                f.write("These songs ARE in your collection with different filenames:\n\n")
                for match in self.found_with_diff_name:
                    f.write(f"### {match['missing_title']}\n")
                    f.write(f"- **Found as:** `{match['found_title']}`\n")
                    f.write(f"- **Location:** `{match['found_path']}`\n")
                    f.write(f"- **Similarity:** {match['similarity']:.1%}\n")
                    f.write(f"- **Duration match:** {match['missing_duration']}s vs {match['found_duration']}s (diff: {match['duration_diff']}s)\n\n")
            
            if self.truly_missing:
                f.write("## ❌ Truly Missing Songs\n\n")
                f.write("These songs need to be downloaded:\n\n")
                
                for series, songs in by_series.items():
                    f.write(f"### {series}\n\n")
                    for song in songs:
                        f.write(f"- **{song['title']}** ({song['duration_str']}) - {song['genre']}\n")
                        f.write(f"  - [Download from Suno]({song['link']})\n")
                    f.write("\n")
        
        print(f"{Colors.GREEN}✅ Summary: {summary_file.name}{Colors.END}")
    
    def run(self):
        """Run verification"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║        🔍 VERIFY & SORT MISSING SONGS 🔍                                      ║")
        print("║                                                                               ║")
        print("║   Compare → Verify → Organize → Sort                                         ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        # 1. Scan collection
        self.scan_collection()
        
        # 2. Load missing songs
        self.load_missing_songs()
        
        # 3. Verify
        self.verify_missing_songs()
        
        # 4. Suggest organization
        by_series = self.suggest_organization()
        
        # 5. Save reports
        self.save_reports(by_series)
        
        # Final summary
        self.print_header("✅ VERIFICATION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Results:{Colors.END}\n")
        print(f"  Claimed missing: {Colors.CYAN}{self.stats['missing_claimed']}{Colors.END}")
        print(f"  Found (different names): {Colors.GREEN}{self.stats['found_different_name']}{Colors.END}")
        print(f"  Truly missing: {Colors.YELLOW}{self.stats['truly_missing']}{Colors.END}\n")
        
        if self.found_with_diff_name:
            print(f"{Colors.GREEN}✅ Good news! {len(self.found_with_diff_name)} songs are already in your collection!{Colors.END}")
            print(f"{Colors.GREEN}They just have different filenames.{Colors.END}\n")
        
        if self.truly_missing:
            print(f"{Colors.YELLOW}📥 {len(self.truly_missing)} songs need to be downloaded from Suno{Colors.END}")
            print(f"{Colors.CYAN}See TRULY_MISSING_WITH_ORGANIZATION.csv for download links and locations{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Reports:{Colors.END}")
        print(f"  {self.output_dir}\n")


def main():
    verifier = MissingSongVerifier()
    verifier.run()


if __name__ == "__main__":
    main()
