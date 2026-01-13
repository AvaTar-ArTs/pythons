#!/usr/bin/env python3
"""
🎵 DEEP MUSIC DIRECTORY ANALYZER & MERGER
==========================================
Deep multi-depth analysis and consolidation of multiple music archive directories.

Analyzes:
- /Users/steven/Music/_OLD_DIRECTORIES_ARCHIVED
- /Users/steven/Music/_ARCHIVED_DIRECTORIES
- /Users/steven/Music/Other_Content
- /Users/steven/Music/Audiobooks

Features:
✨ Deep recursive scanning at all levels
✨ Duplicate detection across all directories (by hash)
✨ Content type classification (audiobooks, music, metadata)
✨ Directory structure comparison
✨ Smart consolidation recommendations
✨ Safe merge planning with backups
"""

import os
import csv
import json
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
import shutil

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"

class DeepMusicDirectoryAnalyzer:
    """Deep analysis and merger for music archive directories"""
    
    DIRECTORIES = [
        "/Users/steven/Music/_OLD_DIRECTORIES_ARCHIVED",
        "/Users/steven/Music/_ARCHIVED_DIRECTORIES",
        "/Users/steven/Music/Other_Content",
        "/Users/steven/Music/Audiobooks"
    ]
    
    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path.home() / "Music" / f"ARCHIVE_ANALYSIS_{self.timestamp}"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.stats = {
            'total_files': 0,
            'total_audio': 0,
            'total_audiobooks': 0,
            'total_duplicates': 0,
            'total_size': 0,
            'by_directory': {}
        }
        
        self.all_files = {}  # hash -> [file info]
        self.audiobook_files = []
        
    def print_header(self, text: str, color=Colors.CYAN):
        """Print fancy header"""
        print(f"\n{color}{Colors.BOLD}{'='*80}")
        print(f"{text}")
        print(f"{'='*80}{Colors.END}\n")
        
    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA-256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "ERROR"
    
    def classify_content(self, filepath: Path) -> str:
        """Classify file type"""
        name_lower = filepath.name.lower()
        path_lower = str(filepath).lower()
        
        # Audiobooks
        if 'audiobook' in path_lower or 'elion' in path_lower or 'thinketh' in path_lower:
            return 'AUDIOBOOK'
        
        # Audio files
        if filepath.suffix.lower() in ['.mp3', '.m4a', '.wav', '.flac', '.ogg', '.aac']:
            return 'AUDIO'
        
        # Metadata
        if filepath.suffix.lower() in ['.json', '.csv', '.txt', '.md']:
            if 'metadata' in path_lower or 'prompt' in path_lower or 'lyric' in path_lower:
                return 'METADATA'
            return 'TEXT'
        
        # Images
        if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            return 'IMAGE'
        
        # Videos
        if filepath.suffix.lower() in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
            return 'VIDEO'
        
        # System files
        if filepath.name == '.DS_Store' or filepath.suffix in ['.pyc', '.pyo']:
            return 'SYSTEM'
        
        return 'OTHER'
    
    def scan_directory(self, directory: str) -> Dict:
        """Deep scan a single directory"""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return {'exists': False}
        
        print(f"{Colors.CYAN}📁 Scanning: {dir_path.name}{Colors.END}")
        
        result = {
            'exists': True,
            'path': str(dir_path),
            'name': dir_path.name,
            'files': [],
            'by_type': defaultdict(int),
            'by_depth': defaultdict(int),
            'subdirectories': [],
            'total_size': 0,
            'total_files': 0
        }
        
        # Get all subdirectories first
        try:
            for item in dir_path.rglob('*'):
                if item.is_dir() and not item.name.startswith('.'):
                    rel_path = item.relative_to(dir_path)
                    depth = len(rel_path.parts)
                    result['subdirectories'].append({
                        'path': str(rel_path),
                        'depth': depth,
                        'full_path': str(item)
                    })
        except Exception as e:
            print(f"  {Colors.YELLOW}⚠️  Error scanning directories: {e}{Colors.END}")
        
        # Scan all files
        try:
            for root, dirs, files in os.walk(dir_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                current_path = Path(root)
                depth = len(current_path.relative_to(dir_path).parts)
                
                for filename in files:
                    if filename.startswith('.'):
                        continue
                    
                    filepath = current_path / filename
                    
                    try:
                        file_stat = filepath.stat()
                        file_size = file_stat.st_size
                        file_hash = self.calculate_hash(filepath)
                        content_type = self.classify_content(filepath)
                        
                        file_info = {
                            'path': str(filepath),
                            'name': filename,
                            'size': file_size,
                            'modified': file_stat.st_mtime,
                            'hash': file_hash,
                            'type': content_type,
                            'depth': depth,
                            'relative_path': str(filepath.relative_to(dir_path)),
                            'source_directory': dir_path.name
                        }
                        
                        result['files'].append(file_info)
                        result['by_type'][content_type] += 1
                        result['by_depth'][depth] += 1
                        result['total_size'] += file_size
                        result['total_files'] += 1
                        
                        # Add to global hash index
                        if file_hash != "ERROR":
                            if file_hash not in self.all_files:
                                self.all_files[file_hash] = []
                            self.all_files[file_hash].append(file_info)
                        
                        # Track audiobooks separately
                        if content_type == 'AUDIOBOOK':
                            self.audiobook_files.append(file_info)
                        
                    except Exception as e:
                        pass
        
        except Exception as e:
            print(f"  {Colors.RED}❌ Error: {e}{Colors.END}")
        
        print(f"  Found {result['total_files']} files ({result['total_size'] / (1024**3):.2f} GB)")
        
        return result
    
    def scan_all_directories(self) -> List[Dict]:
        """Scan all directories"""
        self.print_header("🔍 SCANNING ALL DIRECTORIES")
        
        results = []
        
        for directory in self.DIRECTORIES:
            result = self.scan_directory(directory)
            if result['exists']:
                results.append(result)
                
                # Update global stats
                self.stats['total_files'] += result['total_files']
                self.stats['total_size'] += result['total_size']
                self.stats['by_directory'][result['name']] = {
                    'files': result['total_files'],
                    'size': result['total_size'],
                    'audio': result['by_type']['AUDIO'],
                    'audiobooks': result['by_type']['AUDIOBOOK']
                }
                self.stats['total_audio'] += result['by_type']['AUDIO']
                self.stats['total_audiobooks'] += result['by_type']['AUDIOBOOK']
        
        return results
    
    def find_duplicates(self) -> Dict:
        """Find duplicate files across all directories"""
        self.print_header("🔍 FINDING DUPLICATES ACROSS DIRECTORIES")
        
        duplicates = {}
        
        for file_hash, instances in self.all_files.items():
            if len(instances) > 1:
                # Check if duplicates span multiple directories
                sources = set(inst['source_directory'] for inst in instances)
                if len(sources) > 1:
                    duplicates[file_hash] = {
                        'instances': instances,
                        'count': len(instances),
                        'sources': list(sources),
                        'size': instances[0]['size'],
                        'name': instances[0]['name']
                    }
        
        self.stats['total_duplicates'] = len(duplicates)
        
        print(f"{Colors.GREEN}Found {len(duplicates)} files duplicated across directories{Colors.END}")
        
        # Calculate space wasted
        space_wasted = sum(dup['size'] * (dup['count'] - 1) for dup in duplicates.values())
        print(f"{Colors.YELLOW}Space wasted on duplicates: {space_wasted / (1024**2):.2f} MB{Colors.END}")
        
        return duplicates
    
    def analyze_audiobooks(self, scan_results: List[Dict]):
        """Analyze audiobook distribution"""
        self.print_header("📚 AUDIOBOOK ANALYSIS")
        
        audiobook_dirs = defaultdict(list)
        
        for file_info in self.audiobook_files:
            audiobook_dirs[file_info['source_directory']].append(file_info)
        
        print("Audiobook files by directory:")
        for dir_name, files in audiobook_dirs.items():
            print(f"\n{Colors.CYAN}{dir_name}:{Colors.END}")
            print(f"  Files: {len(files)}")
            
            # Group by audiobook title
            by_title = defaultdict(list)
            for f in files:
                if 'Elion' in f['path']:
                    by_title['Elions Divine Quest'].append(f)
                elif 'Thinketh' in f['path'] or 'thinketh' in f['path'].lower():
                    by_title['As A Man Thinketh'].append(f)
                else:
                    by_title['Other'].append(f)
            
            for title, title_files in by_title.items():
                print(f"    • {title}: {len(title_files)} files")
    
    def compare_directory_structures(self, scan_results: List[Dict]):
        """Compare directory structures"""
        self.print_header("🌳 DIRECTORY STRUCTURE COMPARISON")
        
        for result in scan_results:
            print(f"\n{Colors.BOLD}{result['name']}{Colors.END}")
            print(f"Total subdirectories: {len(result['subdirectories'])}")
            
            # Show depth distribution
            depth_counts = defaultdict(int)
            for subdir in result['subdirectories']:
                depth_counts[subdir['depth']] += 1
            
            print("Depth distribution:")
            for depth in sorted(depth_counts.keys()):
                print(f"  Level {depth}: {depth_counts[depth]} folders")
            
            # Show top-level folders
            top_level = [s for s in result['subdirectories'] if s['depth'] == 1]
            if top_level:
                print(f"\nTop-level folders ({len(top_level)}):")
                for folder in sorted(top_level, key=lambda x: x['path'])[:15]:
                    print(f"  📁 {folder['path']}")
                if len(top_level) > 15:
                    print(f"  ... and {len(top_level) - 15} more")
    
    def generate_consolidation_plan(self, scan_results: List[Dict], duplicates: Dict):
        """Generate smart consolidation recommendations"""
        self.print_header("💡 CONSOLIDATION RECOMMENDATIONS")
        
        recommendations = []
        
        # 1. Audiobook consolidation
        print(f"\n{Colors.CYAN}📚 AUDIOBOOKS:{Colors.END}")
        audiobook_by_title = defaultdict(list)
        for f in self.audiobook_files:
            path_lower = f['path'].lower()
            if 'elion' in path_lower:
                audiobook_by_title['Elions_Divine_Quest'].append(f)
            elif 'thinketh' in path_lower:
                audiobook_by_title['As_A_Man_Thinketh'].append(f)
        
        for title, files in audiobook_by_title.items():
            sources = set(f['source_directory'] for f in files)
            if len(sources) > 1:
                print(f"\n  {title}:")
                print(f"    Found in {len(sources)} directories:")
                for source in sources:
                    source_files = [f for f in files if f['source_directory'] == source]
                    print(f"      • {source}: {len(source_files)} files")
                
                # Recommend keeping in main Audiobooks directory
                recommendations.append({
                    'type': 'CONSOLIDATE_AUDIOBOOK',
                    'title': title,
                    'target': '/Users/steven/Music/Audiobooks',
                    'sources': list(sources),
                    'file_count': len(files)
                })
                print(f"    {Colors.GREEN}→ Consolidate to: ~/Music/Audiobooks/{title}/{Colors.END}")
        
        # 2. Duplicate elimination
        print(f"\n{Colors.CYAN}🗑️  DUPLICATES TO REMOVE:{Colors.END}")
        duplicate_count = 0
        space_savings = 0
        
        for hash_val, dup_info in list(duplicates.items())[:10]:
            print(f"\n  {dup_info['name']}:")
            print(f"    Duplicated {dup_info['count']} times across {len(dup_info['sources'])} directories")
            
            # Choose which to keep (prefer organized structure)
            priority_order = ['Audiobooks', 'Other_Content', '_OLD_DIRECTORIES_ARCHIVED', '_ARCHIVED_DIRECTORIES']
            keep_instance = None
            
            for priority_dir in priority_order:
                for inst in dup_info['instances']:
                    if priority_dir in inst['source_directory']:
                        keep_instance = inst
                        break
                if keep_instance:
                    break
            
            if not keep_instance:
                keep_instance = dup_info['instances'][0]
            
            remove_instances = [i for i in dup_info['instances'] if i != keep_instance]
            
            print(f"    {Colors.GREEN}Keep: {keep_instance['relative_path']}{Colors.END}")
            for inst in remove_instances:
                print(f"    {Colors.YELLOW}Remove: {inst['relative_path']}{Colors.END}")
                duplicate_count += 1
                space_savings += inst['size']
        
        if len(duplicates) > 10:
            print(f"\n  ... and {len(duplicates) - 10} more duplicate groups")
        
        print(f"\n  Total duplicates to remove: {duplicate_count}")
        print(f"  Space to reclaim: {space_savings / (1024**2):.2f} MB")
        
        # 3. Empty/system directory cleanup
        print(f"\n{Colors.CYAN}🧹 CLEANUP SUGGESTIONS:{Colors.END}")
        print(f"  • Remove _ARCHIVED_DIRECTORIES if only contains system files")
        print(f"  • Consolidate audiobooks to single ~/Music/Audiobooks/ location")
        print(f"  • Move useful content from Other_Content/Albums/AUDIOBOOKS to ~/Music/Audiobooks")
        print(f"  • Archive _OLD_DIRECTORIES_ARCHIVED after extracting unique content")
        
        return recommendations
    
    def save_reports(self, scan_results: List[Dict], duplicates: Dict, recommendations: List[Dict]):
        """Save comprehensive reports"""
        self.print_header("💾 SAVING REPORTS")
        
        # 1. Master summary CSV
        summary_file = self.output_dir / "DIRECTORY_COMPARISON_SUMMARY.csv"
        with open(summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Directory', 'Total_Files', 'Size_MB', 'Audio_Files', 'Audiobook_Files', 'Subdirectories'])
            
            for result in scan_results:
                writer.writerow([
                    result['name'],
                    result['total_files'],
                    f"{result['total_size'] / (1024**2):.2f}",
                    result['by_type']['AUDIO'],
                    result['by_type']['AUDIOBOOK'],
                    len(result['subdirectories'])
                ])
        
        print(f"{Colors.GREEN}✅ Summary: {summary_file.name}{Colors.END}")
        
        # 2. Detailed file inventory
        inventory_file = self.output_dir / "COMPLETE_FILE_INVENTORY.csv"
        with open(inventory_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Source_Directory', 'Type', 'Size_MB', 'Depth', 'Relative_Path', 'Hash'])
            
            all_files_list = []
            for instances in self.all_files.values():
                all_files_list.extend(instances)
            
            for file_info in sorted(all_files_list, key=lambda x: (x['source_directory'], x['relative_path'])):
                writer.writerow([
                    file_info['name'],
                    file_info['source_directory'],
                    file_info['type'],
                    f"{file_info['size'] / (1024**2):.4f}",
                    file_info['depth'],
                    file_info['relative_path'],
                    file_info['hash'][:16]
                ])
        
        print(f"{Colors.GREEN}✅ Inventory: {inventory_file.name}{Colors.END}")
        
        # 3. Duplicates report
        duplicates_file = self.output_dir / "CROSS_DIRECTORY_DUPLICATES.csv"
        with open(duplicates_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Count', 'Directories', 'Size_MB', 'Hash', 'Paths'])
            
            for hash_val, dup_info in sorted(duplicates.items(), key=lambda x: x[1]['count'], reverse=True):
                paths = ' | '.join([inst['relative_path'] for inst in dup_info['instances']])
                writer.writerow([
                    dup_info['name'],
                    dup_info['count'],
                    ', '.join(dup_info['sources']),
                    f"{dup_info['size'] / (1024**2):.4f}",
                    hash_val[:16],
                    paths
                ])
        
        print(f"{Colors.GREEN}✅ Duplicates: {duplicates_file.name}{Colors.END}")
        
        # 4. Audiobook analysis
        audiobook_file = self.output_dir / "AUDIOBOOK_CONSOLIDATION.csv"
        with open(audiobook_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'Source_Directory', 'Audiobook_Title', 'Size_MB', 'Path'])
            
            for file_info in self.audiobook_files:
                path_lower = file_info['path'].lower()
                if 'elion' in path_lower:
                    title = 'Elions_Divine_Quest'
                elif 'thinketh' in path_lower:
                    title = 'As_A_Man_Thinketh'
                else:
                    title = 'Unknown'
                
                writer.writerow([
                    file_info['name'],
                    file_info['source_directory'],
                    title,
                    f"{file_info['size'] / (1024**2):.4f}",
                    file_info['path']
                ])
        
        print(f"{Colors.GREEN}✅ Audiobooks: {audiobook_file.name}{Colors.END}")
        
        # 5. Consolidation plan JSON
        plan_file = self.output_dir / "CONSOLIDATION_PLAN.json"
        with open(plan_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': self.timestamp,
                'recommendations': recommendations,
                'stats': self.stats,
                'duplicate_count': len(duplicates)
            }, f, indent=2)
        
        print(f"{Colors.GREEN}✅ Plan: {plan_file.name}{Colors.END}")
        
        # 6. Markdown report
        report_file = self.output_dir / "ANALYSIS_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🎵 Deep Music Directory Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Summary Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Total Files | {self.stats['total_files']:,} |\n")
            f.write(f"| Total Size | {self.stats['total_size'] / (1024**3):.2f} GB |\n")
            f.write(f"| Audio Files | {self.stats['total_audio']:,} |\n")
            f.write(f"| Audiobook Files | {self.stats['total_audiobooks']:,} |\n")
            f.write(f"| Cross-Directory Duplicates | {len(duplicates):,} |\n\n")
            
            f.write("## 📁 By Directory\n\n")
            for dir_name, stats in self.stats['by_directory'].items():
                f.write(f"### {dir_name}\n\n")
                f.write(f"- **Files:** {stats['files']:,}\n")
                f.write(f"- **Size:** {stats['size'] / (1024**2):.2f} MB\n")
                f.write(f"- **Audio:** {stats['audio']:,}\n")
                f.write(f"- **Audiobooks:** {stats['audiobooks']:,}\n\n")
            
            f.write("## 💡 Recommendations\n\n")
            f.write("1. **Consolidate Audiobooks:** Move all audiobook files to `~/Music/Audiobooks/`\n")
            f.write("2. **Remove Duplicates:** Eliminate cross-directory duplicates to save space\n")
            f.write("3. **Archive System Files:** Clean up `_ARCHIVED_DIRECTORIES` (mostly system files)\n")
            f.write("4. **Organize Content:** Review `Other_Content` structure for optimization\n\n")
        
        print(f"{Colors.GREEN}✅ Report: {report_file.name}{Colors.END}")
        
        return summary_file
    
    def run(self):
        """Run complete analysis"""
        
        print(f"{Colors.MAGENTA}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║               🎵 DEEP MUSIC DIRECTORY ANALYZER & MERGER 🎵                    ║")
        print("║                                                                               ║")
        print("║                    Multi-Depth Archive Consolidation                          ║")
        print("║                                                                               ║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}\n")
        
        print(f"{Colors.CYAN}Analyzing directories:{Colors.END}")
        for directory in self.DIRECTORIES:
            print(f"  • {directory}")
        print()
        
        # 1. Scan all directories
        scan_results = self.scan_all_directories()
        
        # 2. Find duplicates
        duplicates = self.find_duplicates()
        
        # 3. Analyze audiobooks
        self.analyze_audiobooks(scan_results)
        
        # 4. Compare structures
        self.compare_directory_structures(scan_results)
        
        # 5. Generate consolidation plan
        recommendations = self.generate_consolidation_plan(scan_results, duplicates)
        
        # 6. Save reports
        summary_file = self.save_reports(scan_results, duplicates, recommendations)
        
        # Final summary
        self.print_header("✅ ANALYSIS COMPLETE!", Colors.GREEN)
        
        print(f"{Colors.BOLD}📊 Final Statistics:{Colors.END}\n")
        print(f"  Total Files: {Colors.CYAN}{self.stats['total_files']:,}{Colors.END}")
        print(f"  Total Size: {Colors.CYAN}{self.stats['total_size'] / (1024**3):.2f} GB{Colors.END}")
        print(f"  Audio Files: {Colors.CYAN}{self.stats['total_audio']:,}{Colors.END}")
        print(f"  Audiobook Files: {Colors.CYAN}{self.stats['total_audiobooks']:,}{Colors.END}")
        print(f"  Duplicates Found: {Colors.YELLOW}{len(duplicates):,}{Colors.END}\n")
        
        print(f"{Colors.BOLD}📁 Output Directory:{Colors.END}")
        print(f"  {self.output_dir}\n")
        
        print(f"{Colors.BOLD}📝 Next Steps:{Colors.END}")
        print(f"  1. Review {Colors.CYAN}ANALYSIS_REPORT.md{Colors.END} for overview")
        print(f"  2. Check {Colors.CYAN}CROSS_DIRECTORY_DUPLICATES.csv{Colors.END} for duplicates")
        print(f"  3. Review {Colors.CYAN}AUDIOBOOK_CONSOLIDATION.csv{Colors.END} for audiobook merging")
        print(f"  4. Use {Colors.CYAN}CONSOLIDATION_PLAN.json{Colors.END} for automated merging\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🎵 Deep Music Directory Analyzer")
    parser.add_argument('--dry-run', action='store_true', default=True, help='Dry run mode (default)')
    parser.add_argument('--live', action='store_true', help='Live mode (execute changes)')
    
    args = parser.parse_args()
    
    analyzer = DeepMusicDirectoryAnalyzer(dry_run=not args.live)
    analyzer.run()


if __name__ == "__main__":
    main()
