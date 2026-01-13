#!/usr/bin/env python3
"""
?? Search Documents for InVideo & 2025 Proofs
==============================================

Searches ~/Documents for:
- InVideo AI content
- Project 2025 proofs
- AI-generated videos
- Content scripts
- Audio files
- Documentation

Author: Steven Chaplinski
Date: November 4, 2025
"""

import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class InVideoProofSearcher:
    """Search for InVideo and proof content"""
    
    def __init__(self):
        self.docs_dir = Path.home() / 'Documents'
        self.workspace = Path.home() / 'workspace' / 'music-empire'
        
        self.findings = {
            'invideo': [],
            'project_2025': [],
            'ai_videos': [],
            'scripts': [],
            'audio': [],
            'documents': [],
            'other': []
        }
        
        self.file_types = {
            'video': {'.mp4', '.mov', '.avi', '.mkv', '.webm'},
            'audio': {'.mp3', '.wav', '.m4a', '.flac', '.aac'},
            'document': {'.pdf', '.md', '.txt', '.doc', '.docx'},
            'script': {'.py', '.sh', '.js'},
            'data': {'.csv', '.json', '.xml'}
        }
        
        self.total_found = 0
    
    def categorize_file(self, filepath: Path) -> str:
        """Categorize file"""
        
        filename_lower = filepath.name.lower()
        path_lower = str(filepath).lower()
        
        # InVideo content
        if 'invideo' in filename_lower or 'invideo' in path_lower:
            return 'invideo'
        
        # Project 2025
        if any(term in filename_lower for term in ['2025', 'project 2025', 'trump', 'disaster']):
            if any(term in filename_lower for term in ['project', 'proof', 'american', 'disaster']):
                return 'project_2025'
        
        # AI video indicators
        if any(term in filename_lower for term in ['ai-generated', 'ai-480', 'runway', 'gen-', 'leonardo']):
            return 'ai_videos'
        
        # Scripts
        if filepath.suffix.lower() in self.file_types['script']:
            return 'scripts'
        
        # Audio
        if filepath.suffix.lower() in self.file_types['audio']:
            return 'audio'
        
        # Documents
        if filepath.suffix.lower() in self.file_types['document']:
            return 'documents'
        
        return 'other'
    
    def search_documents(self):
        """Search Documents directory"""
        
        print("?? SEARCHING ~/Documents")
        print("=" * 70)
        print()
        print("Looking for:")
        print("  ? InVideo AI content")
        print("  ? Project 2025 proofs")
        print("  ? AI-generated videos")
        print("  ? Related scripts & docs")
        print()
        print("??  Scanning...")
        print()
        
        scanned = 0
        
        for root, dirs, files in os.walk(self.docs_dir):
            # Skip hidden and cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
            
            scanned += 1
            if scanned % 100 == 0:
                print(f"   Scanned {scanned} directories, found {self.total_found} files...", end='\r')
            
            for filename in files:
                filepath = Path(root) / filename
                
                try:
                    if filepath.is_file():
                        category = self.categorize_file(filepath)
                        
                        if category != 'other':
                            self.total_found += 1
                            
                            self.findings[category].append({
                                'filename': filename,
                                'path': str(filepath),
                                'size_mb': round(filepath.stat().st_size / (1024**2), 2),
                                'location': str(Path(root).relative_to(self.docs_dir)),
                                'type': filepath.suffix.lower()
                            })
                except:
                    pass
        
        print(f"   ? Scanned {scanned} directories, found {self.total_found} files" + " " * 20)
    
    def generate_report(self):
        """Generate detailed report"""
        
        print(f"\n?? Generating report...\n")
        
        report_file = self.workspace / f'INVIDEO_PROOFS_SEARCH_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# ?? InVideo & 2025 Proofs Search Results\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Searched:** ~/Documents\n\n")
            f.write("---\n\n")
            
            # Summary
            f.write("## ?? Summary\n\n")
            f.write(f"**Total files found:** {self.total_found}\n\n")
            
            for category, files in self.findings.items():
                if files:
                    total_size = sum(f['size_mb'] for f in files)
                    f.write(f"- **{category.replace('_', ' ').title()}:** {len(files)} files ({total_size / 1024:.2f} GB)\n")
            
            f.write("\n---\n\n")
            
            # Details for each category
            for category, files in self.findings.items():
                if files:
                    f.write(f"## {category.replace('_', ' ').title()} ({len(files)} files)\n\n")
                    
                    # Group by location
                    by_location = defaultdict(list)
                    for file_info in files:
                        by_location[file_info['location']].append(file_info)
                    
                    for location, loc_files in sorted(by_location.items(), key=lambda x: len(x[1]), reverse=True):
                        f.write(f"### {location if location != '.' else '[Root]'}\n")
                        f.write(f"**{len(loc_files)} files**\n\n")
                        
                        # Group by type
                        by_type = defaultdict(list)
                        for file_info in loc_files:
                            by_type[file_info['type']].append(file_info)
                        
                        for file_type, type_files in sorted(by_type.items()):
                            f.write(f"**{file_type} files ({len(type_files)}):**\n")
                            for file_info in type_files[:20]:
                                f.write(f"- `{file_info['filename']}` ({file_info['size_mb']} MB)\n")
                            
                            if len(type_files) > 20:
                                f.write(f"  ... and {len(type_files) - 20} more\n")
                            
                            f.write("\n")
                        
                        f.write("\n")
                    
                    f.write("---\n\n")
            
            # Action items
            f.write("## ?? Action Items\n\n")
            
            if self.findings['invideo']:
                f.write(f"### InVideo Content ({len(self.findings['invideo'])} files)\n")
                f.write("- These are YOUR AI-generated videos\n")
                f.write("- Can use for YouTube, social media\n")
                f.write("- May contain audio tracks for albums\n\n")
            
            if self.findings['project_2025']:
                f.write(f"### Project 2025 Content ({len(self.findings['project_2025'])} files)\n")
                f.write("- Your research/proof content\n")
                f.write("- Documentary material\n")
                f.write("- Can be repurposed for content\n\n")
            
            if self.findings['audio']:
                f.write(f"### Audio Files ({len(self.findings['audio'])} files)\n")
                f.write("- Check if these are YOUR music\n")
                f.write("- Move to organized collection if yours\n\n")
        
        print(f"   ? Report: {report_file.name}\n")
        return report_file
    
    def print_summary(self):
        """Print summary"""
        
        print("=" * 70)
        print("?? SEARCH RESULTS")
        print("=" * 70)
        
        print(f"\n   Total files found: {self.total_found}")
        
        print(f"\n   By category:")
        for category, files in sorted(self.findings.items(), key=lambda x: len(x[1]), reverse=True):
            if files:
                print(f"      {category.replace('_', ' ').title()}: {len(files)} files")
        
        # Show InVideo samples
        if self.findings['invideo']:
            print(f"\n   ?? InVideo files found:")
            for i, file_info in enumerate(self.findings['invideo'][:10], 1):
                print(f"      {i:2d}. {file_info['filename']}")
        
        # Show Project 2025 samples
        if self.findings['project_2025']:
            print(f"\n   ?? Project 2025 files found:")
            for i, file_info in enumerate(self.findings['project_2025'][:10], 1):
                print(f"      {i:2d}. {file_info['filename']}")
        
        # Show audio files
        if self.findings['audio']:
            print(f"\n   ?? Audio files found:")
            for i, file_info in enumerate(self.findings['audio'][:10], 1):
                print(f"      {i:2d}. {file_info['filename']}")
    
    def run(self):
        """Run the search"""
        
        # Search
        self.search_documents()
        
        # Report
        report_file = self.generate_report()
        
        # Summary
        self.print_summary()
        
        print(f"\n{'=' * 70}")
        print("? SEARCH COMPLETE!")
        print("=" * 70)
        
        print(f"\n?? Full report: {report_file.name}")


def main():
    searcher = InVideoProofSearcher()
    searcher.run()


if __name__ == '__main__':
    main()
