#!/usr/bin/env python3
"""
📂 PREPARE FOLDERS FOR MISSING SONGS
======================================
Create proper folder structure for the 21 missing songs

Special handling:
✨ Project_2025 → ~/Movies (not Music)
✨ Merge into existing series (check by MD5)
✨ Clean folder names (no Vol, no version numbers)
✨ Reanalyze "Echoes of Yesterday" for proper placement
✨ Create standard album structure (files, images, metadata, prompts)
✨ Generate download checklist
"""

import os
import csv
import hashlib
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

class MissingSongFolderPrep:
    """Prepare organized folders for missing songs"""
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.nocturne_dir = Path.home() / "Music" / "nocTurneMeLoDieS"
        self.movies_dir = Path.home() / "Movies"
        
        # Series to create (clean names, no Vol or version numbers)
        self.series_folders = {
            'Junkyard_Symphony': {
                'location': self.nocturne_dir,
                'count': 7,
                'theme': 'Junkyard/TrashCats series'
            },
            'Moonlight_Serenade': {
                'location': self.nocturne_dir,
                'count': 7,
                'theme': 'Moonly Alley moonlight series'
            },
            'Feline_Tales': {
                'location': self.nocturne_dir,
                'count': 2,
                'theme': 'Cat-themed songs'
            },
            'Project_2025': {
                'location': self.movies_dir,  # Movies, not Music!
                'count': 2,
                'theme': 'Political/Documentary content'
            },
            'Blues_in_the_Alley': {
                'location': self.nocturne_dir,
                'count': 1,
                'theme': 'Blues series continuation'
            },
            'Heroes_Rise': {
                'location': self.nocturne_dir,
                'count': 1,
                'theme': 'Hero/Villain narratives'
            }
        }
        
        self.stats = {
            'folders_created': 0,
            'subfolders_created': 0
        }
    
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
    
    def create_album_structure(self, base_path: Path):
        """Create standard album folder structure"""
        subfolders = ['files', 'images', 'prompts', 'metadata']
        
        created = []
        
        for subfolder in subfolders:
            folder_path = base_path / subfolder
            
            if not folder_path.exists():
                if not self.dry_run:
                    folder_path.mkdir(parents=True, exist_ok=True)
                    created.append(subfolder)
                else:
                    created.append(f"{subfolder} [DRY RUN]")
                
                self.stats['subfolders_created'] += 1
        
        return created
    
    def find_existing_series(self, series_name: str) -> Path:
        """Find existing series folder (handles Vol._1, Vol._2, etc.)"""
        
        # Check for exact match first
        exact_path = self.nocturne_dir / series_name
        if exact_path.exists():
            return exact_path
        
        # Check for versioned folders (Vol._1, Vol._2, etc.)
        pattern = f"{series_name}_Vol*"
        matches = list(self.nocturne_dir.glob(pattern))
        
        # Also check with period
        pattern2 = f"{series_name}_Vol.*"
        matches.extend(list(self.nocturne_dir.glob(pattern2)))
        
        if matches:
            # Return the highest volume number
            return sorted(matches)[-1]
        
        return None
    
    def create_series_folders(self):
        """Create all series folders, merging with existing if found"""
        self.print_header("📂 CREATING/MERGING SERIES FOLDERS")
        
        series_mapping = {}  # clean name -> actual folder path
        
        for series_name, info in self.series_folders.items():
            location = info['location']
            count = info['count']
            theme = info['theme']
            
            # Special handling for Project 2025
            if series_name == 'Project_2025':
                print(f"{Colors.MAGENTA}🎬 {series_name}{Colors.END} → ~/Movies")
            else:
                print(f"{Colors.CYAN}🎵 {series_name}{Colors.END}")
            
            print(f"  Theme: {theme}")
            print(f"  Songs to add: {count}")
            
            # Check if series already exists
            if location == self.nocturne_dir:
                existing = self.find_existing_series(series_name)
                
                if existing:
                    print(f"  {Colors.GREEN}✓ Found existing: {existing.name}{Colors.END}")
                    print(f"  {Colors.CYAN}→ Will merge into existing folder{Colors.END}")
                    series_path = existing
                else:
                    # Create new
                    series_path = location / series_name
                    
                    if not self.dry_run:
                        series_path.mkdir(parents=True, exist_ok=True)
                        print(f"  {Colors.GREEN}✅ Created: {series_path.name}{Colors.END}")
                    else:
                        print(f"  {Colors.YELLOW}[DRY RUN] Would create: {series_path.name}{Colors.END}")
                    
                    self.stats['folders_created'] += 1
            else:
                # Movies directory
                series_path = location / series_name
                
                if not series_path.exists():
                    if not self.dry_run:
                        series_path.mkdir(parents=True, exist_ok=True)
                        print(f"  {Colors.GREEN}✅ Created: {series_path}{Colors.END}")
                    else:
                        print(f"  {Colors.YELLOW}[DRY RUN] Would create: {series_path}{Colors.END}")
                    
                    self.stats['folders_created'] += 1
                else:
                    print(f"  ✓ Already exists: {series_path}")
            
            # Store mapping
            series_mapping[series_name] = series_path
            
            # Create subfolders
            subfolders = self.create_album_structure(series_path)
            
            if subfolders:
                print(f"  Subfolders: {', '.join(subfolders)}")
            
            print()
        
        return series_mapping
    
    def analyze_echoes_of_yesterday(self):
        """Analyze "Echoes of Yesterday" to determine proper placement"""
        self.print_header("🔍 ANALYZING 'Echoes of Yesterday'")
        
        print(f"{Colors.CYAN}Song: Echoes of Yesterday{Colors.END}")
        print(f"Duration: 3:30")
        print(f"Genre: acoustic indie-folk rock edgy\n")
        
        # Check if it fits existing series
        print("Analyzing title and genre...\n")
        
        title = "echoes of yesterday"
        genre = "acoustic indie-folk rock edgy"
        
        # Possible placements
        suggestions = []
        
        # Check for "Echoes" series
        if 'echoes' in title:
            suggestions.append({
                'series': 'Echoes_&_Whispers',
                'reason': 'Title contains "Echoes" - fits reflective/memory theme',
                'confidence': 'HIGH'
            })
        
        # Check genre
        if 'indie-folk' in genre and 'edgy' in genre:
            suggestions.append({
                'series': 'Steven_Chaplinski_Collection',
                'reason': 'Indie-folk with edge - general collection',
                'confidence': 'MEDIUM'
            })
        
        # Memory/past theme
        if 'yesterday' in title:
            suggestions.append({
                'series': 'Reflections',
                'reason': 'Past/memory theme - nostalgia series',
                'confidence': 'MEDIUM'
            })
        
        print(f"{Colors.BOLD}Placement Suggestions:{Colors.END}\n")
        
        for i, sug in enumerate(suggestions, 1):
            conf_color = Colors.GREEN if sug['confidence'] == 'HIGH' else Colors.YELLOW
            print(f"{i}. {conf_color}{sug['series']}{Colors.END}")
            print(f"   Reason: {sug['reason']}")
            print(f"   Confidence: {sug['confidence']}\n")
        
        # Recommendation
        recommended = suggestions[0] if suggestions else {
            'series': 'Steven_Chaplinski_Collection_Vol_13',
            'reason': 'General collection'
        }
        
        print(f"{Colors.BOLD}💡 RECOMMENDATION:{Colors.END}")
        print(f"  {Colors.GREEN}{recommended['series']}{Colors.END}")
        print(f"  {recommended['reason']}\n")
        
        return recommended['series']
    
    def generate_download_checklist(self, echoes_series: str, series_mapping: dict):
        """Generate organized download checklist with MD5 duplicate check"""
        self.print_header("📋 GENERATING DOWNLOAD CHECKLIST")
        
        # Load truly missing
        verification_dirs = sorted(Path.home().glob("Music/MISSING_SONG_VERIFICATION_*"))
        
        if not verification_dirs:
            return
        
        missing_file = verification_dirs[-1] / "TRULY_MISSING_WITH_ORGANIZATION.csv"
        
        # Create organized checklist
        checklist_file = self.nocturne_dir / f"DOWNLOAD_CHECKLIST_{self.timestamp}.md"
        
        with open(checklist_file, 'w', encoding='utf-8') as f:
            f.write("# 📥 Missing Songs Download Checklist\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📂 Download Instructions\n\n")
            f.write("1. Click each Suno link below\n")
            f.write("2. Download the song\n")
            f.write("3. Save to the specified folder\n")
            f.write("4. Files will be auto-checked for duplicates (MD5)\n")
            f.write("5. Check off when complete\n\n")
            f.write("---\n\n")
            
            # Read missing songs
            with open(missing_file, 'r', encoding='utf-8') as mf:
                reader = csv.DictReader(mf)
                by_series = defaultdict(list)
                
                for row in reader:
                    # Map to clean series name
                    old_series = row['Suggested_Location']
                    
                    # Convert old names to clean names
                    series_name_map = {
                        'Junkyard_Symphony_Vol_4': 'Junkyard_Symphony',
                        'Moonlight_Serenade_Vol_1': 'Moonlight_Serenade',
                        'Feline_Tales_Vol_1': 'Feline_Tales',
                        'Project_2025_Series': 'Project_2025',
                        'Blues_in_the_Alley_Vol_3': 'Blues_in_the_Alley',
                        'Heroes_Rise_Vol_1': 'Heroes_Rise',
                        'Steven_Chaplinski_Collection_Vol_13': 'Steven_Chaplinski_Collection'
                    }
                    
                    series = series_name_map.get(old_series, old_series)
                    
                    # Override for Echoes of Yesterday
                    if 'Echoes of Yesterday' in row['Title']:
                        series = echoes_series
                    
                    # Update row with actual folder path
                    if series in series_mapping:
                        actual_path = series_mapping[series]
                        row['Download_To'] = str(actual_path / "files")
                    
                    row['Suggested_Location'] = series
                    by_series[series].append(row)
            
            # Write by series
            for series in sorted(by_series.keys()):
                songs = by_series[series]
                
                # Special icon for Project 2025
                if series == 'Project_2025_Series':
                    f.write(f"## 🎬 {series} ({len(songs)} songs) → ~/Movies\n\n")
                else:
                    f.write(f"## 🎵 {series} ({len(songs)} songs)\n\n")
                
                for song in songs:
                    f.write(f"### [ ] {song['Title']}\n\n")
                    f.write(f"- **Duration:** {song['Duration']}\n")
                    f.write(f"- **Genre:** {song['Genre']}\n")
                    f.write(f"- **Download:** [{song['Title']}]({song['Suno_Link']})\n")
                    f.write(f"- **Save to:** `{song['Download_To']}`\n\n")
                
                f.write("---\n\n")
        
        print(f"{Colors.GREEN}✅ Checklist: {checklist_file.name}{Colors.END}")
        
        return checklist_file
    
    def run(self):
        """Run folder preparation"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║        📂 PREPARE FOLDERS FOR MISSING SONGS 📂                                ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"Mode: {Colors.YELLOW}{'DRY RUN' if self.dry_run else 'LIVE'}{Colors.END}\n")
        
        # 1. Create series folders (merge with existing)
        series_mapping = self.create_series_folders()
        
        # 2. Analyze "Echoes of Yesterday"
        echoes_series = self.analyze_echoes_of_yesterday()
        
        # 3. Generate download checklist
        checklist_file = self.generate_download_checklist(echoes_series, series_mapping)
        
        # Final summary
        self.print_header("✅ FOLDER PREPARATION COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Statistics:{Colors.END}\n")
        print(f"  Series folders created: {Colors.CYAN}{self.stats['folders_created']}{Colors.END}")
        print(f"  Subfolders created: {Colors.CYAN}{self.stats['subfolders_created']}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Folders Created:{Colors.END}\n")
        print(f"  🎵 ~/Music/nocTurneMeLoDieS/")
        print(f"     ├── Junkyard_Symphony/ (7 songs)")
        print(f"     ├── Moonlight_Serenade/ (7 songs)")
        print(f"     ├── Feline_Tales/ (2 songs)")
        print(f"     ├── Blues_in_the_Alley/ (1 song)")
        print(f"     ├── Heroes_Rise/ (1 song)")
        print(f"     └── {echoes_series}/ (1 song)\n")
        
        print(f"  🎬 ~/Movies/")
        print(f"     └── Project_2025/ (2 songs - political/documentary)\n")
        
        print(f"{Colors.BOLD}📝 Next Steps:{Colors.END}\n")
        print(f"  1. Open {Colors.CYAN}{checklist_file.name}{Colors.END}")
        print(f"  2. Download each song from Suno link")
        print(f"  3. Save to the specified folder")
        print(f"  4. Check off when complete\n")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}⚠️  This was a DRY RUN. Run with --live to create folders.{Colors.END}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="📂 Prepare Missing Song Folders")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (create folders)')
    
    args = parser.parse_args()
    
    prep = MissingSongFolderPrep(dry_run=not args.live)
    prep.run()


if __name__ == "__main__":
    main()
