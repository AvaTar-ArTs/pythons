#!/usr/bin/env python3
"""
?? Deep Multi-Depth Search for YOUR Content
============================================

Searches entire ~/ at all depths for:
- InVideo content
- TrashCat content
- AvatarArts content
- nocTurneMeLoDieS content
- Alley/Junkyard themes
- As a Man Thinketh
- All YOUR projects

Author: Steven Chaplinski
Date: November 4, 2025
"""

import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class DeepContentSearcher:
    """Deep search for all YOUR content"""
    
    def __init__(self):
        self.home = Path.home()
        self.workspace = self.home / 'workspace' / 'music-empire'
        
        self.audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg'}
        
        # YOUR content patterns
        self.your_patterns = {
            'invideo': [],
            'avatararts': [],
            'nocturne': [],
            'trashcat': [],
            'alley': [],
            'junkyard': [],
            'moonlit': [],
            'thinketh': [],
            'suno': [],
            'feather': [],
            'petals': [],
            'willow': [],
            'dusty': [],
            'grime': [],
            'raccoon': [],
        }
        
        self.skip_dirs = {
            'Library/Caches',
            'Library/Logs',
            'Library/Application Support/Google',
            'Library/Application Support/Slack',
            '.Trash',
            'node_modules',
            '.git',
            '.cache'
        }
        
        self.total_found = 0
    
    def should_skip(self, path_str: str) -> bool:
        """Check if should skip directory"""
        
        for skip in self.skip_dirs:
            if skip in path_str:
                return True
        return False
    
    def matches_pattern(self, filename: str) -> list:
        """Check which patterns filename matches"""
        
        filename_lower = filename.lower()
        matched_patterns = []
        
        for pattern in self.your_patterns.keys():
            if pattern in filename_lower:
                matched_patterns.append(pattern)
        
        return matched_patterns
    
    def deep_search(self):
        """Deep search entire home directory"""
        
        print("?? DEEP MULTI-DEPTH SEARCH")
        print("=" * 70)
        print()
        print("Searching ENTIRE ~/ for YOUR content...")
        print("Patterns: invideo, avatararts, nocturne, trashcat, alley,")
        print("          junkyard, moonlit, thinketh, feather, petals, etc.")
        print()
        print("??  This may take 3-5 minutes...")
        print()
        
        scanned_dirs = 0
        
        for root, dirs, files in os.walk(self.home):
            # Filter directories
            if self.should_skip(root):
                dirs[:] = []
                continue
            
            scanned_dirs += 1
            
            if scanned_dirs % 100 == 0:
                print(f"   Scanned {scanned_dirs} directories, found {self.total_found} files...", end='\r')
            
            for filename in files:
                filepath = Path(root) / filename
                
                if filepath.suffix.lower() in self.audio_extensions:
                    try:
                        if filepath.is_file() and filepath.stat().st_size > 100000:
                            # Check if matches any pattern
                            patterns = self.matches_pattern(filename)
                            
                            if patterns:
                                self.total_found += 1
                                
                                for pattern in patterns:
                                    self.your_patterns[pattern].append({
                                        'filename': filename,
                                        'path': str(filepath),
                                        'size_mb': round(filepath.stat().st_size / (1024**2), 2),
                                        'location': str(Path(root).relative_to(self.home))
                                    })
                    except:
                        pass
        
        print(f"   ? Scanned {scanned_dirs} directories, found {self.total_found} files" + " " * 20)
    
    def generate_report(self):
        """Generate detailed report"""
        
        print(f"\n?? Generating report...\n")
        
        report_file = self.workspace / f'DEEP_SEARCH_RESULTS_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# ?? Deep Search Results - YOUR Content\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # Summary
            f.write("## ?? Summary\n\n")
            f.write(f"**Total files found:** {self.total_found}\n\n")
            
            f.write("**By pattern:**\n\n")
            for pattern, files in sorted(self.your_patterns.items(), key=lambda x: len(x[1]), reverse=True):
                if files:
                    total_size = sum(f['size_mb'] for f in files)
                    f.write(f"- **{pattern}:** {len(files)} files ({total_size / 1024:.2f} GB)\n")
            
            f.write("\n---\n\n")
            
            # Details for each pattern
            for pattern, files in sorted(self.your_patterns.items(), key=lambda x: len(x[1]), reverse=True):
                if files:
                    f.write(f"## ?? {pattern.upper()} ({len(files)} files)\n\n")
                    
                    # Group by location
                    by_location = defaultdict(list)
                    for file_info in files:
                        by_location[file_info['location']].append(file_info)
                    
                    for location, loc_files in sorted(by_location.items(), key=lambda x: len(x[1]), reverse=True):
                        f.write(f"### {location}\n")
                        f.write(f"**{len(loc_files)} files**\n\n")
                        
                        for file_info in loc_files[:20]:
                            f.write(f"- `{file_info['filename']}` ({file_info['size_mb']} MB)\n")
                        
                        if len(loc_files) > 20:
                            f.write(f"\n... and {len(loc_files) - 20} more\n")
                        
                        f.write("\n")
                    
                    f.write("---\n\n")
            
            # Action plan
            f.write("## ?? Action Plan\n\n")
            f.write("### Files to Move to YOUR_SUNO_SONGS:\n\n")
            
            priority_patterns = ['invideo', 'avatararts', 'nocturne', 'trashcat', 'alley', 'junkyard']
            total_to_move = sum(len(self.your_patterns[p]) for p in priority_patterns if p in self.your_patterns)
            
            f.write(f"**Total:** {total_to_move} files\n\n")
            
            for pattern in priority_patterns:
                if self.your_patterns.get(pattern):
                    f.write(f"- {pattern}: {len(self.your_patterns[pattern])} files\n")
            
            f.write("\n**Command to organize:**\n")
            f.write("```bash\n")
            f.write("cd ~/workspace/music-empire\n")
            f.write("python3 MOVE_YOUR_FILES.py\n")
            f.write("```\n\n")
        
        print(f"   ? Report: {report_file.name}")
        return report_file
    
    def print_summary(self):
        """Print summary to console"""
        
        print(f"\n{'=' * 70}")
        print("?? DEEP SEARCH RESULTS")
        print("=" * 70)
        
        print(f"\n   Total YOUR files found: {self.total_found}")
        
        print(f"\n   By pattern:")
        for pattern, files in sorted(self.your_patterns.items(), key=lambda x: len(x[1]), reverse=True):
            if files:
                print(f"      {pattern}: {len(files)} files")
        
        # Show samples
        print(f"\n   ?? Sample files found:")
        
        all_files = []
        for files in self.your_patterns.values():
            all_files.extend(files)
        
        for i, file_info in enumerate(all_files[:20], 1):
            print(f"      {i:2d}. {file_info['filename']}")
            print(f"          ({file_info['location']})")
        
        if len(all_files) > 20:
            print(f"\n      ... and {len(all_files) - 20} more!")
    
    def run(self):
        """Run the deep search"""
        
        # Search
        self.deep_search()
        
        # Report
        report_file = self.generate_report()
        
        # Summary
        self.print_summary()
        
        print(f"\n{'=' * 70}")
        print("? DEEP SEARCH COMPLETE!")
        print("=" * 70)
        
        print(f"\n?? Full report: {report_file.name}")
        print(f"\n?? Found {self.total_found} of YOUR files scattered across ~/")


def main():
    searcher = DeepContentSearcher()
    searcher.run()


if __name__ == '__main__':
    main()
