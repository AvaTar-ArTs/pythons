#!/usr/bin/env python3
"""
Find Portfolio & Skill Documentation
Search for HTML, MD, PDF files that reference Python, APIs, and technical skills
"""

import re
from pathlib import Path
from collections import defaultdict

class PortfolioFinder:
    """Find files showcasing skills and projects"""
    
    def __init__(self):
        self.search_locations = [
            Path.home() / 'Documents',
            Path('/Volumes/2T-Xx'),
            Path('/Volumes/DeVonDaTa'),
        ]
        
        self.skill_keywords = [
            # Python & Programming
            'python', 'api', 'automation', 'script', 'developer',
            # AI/ML
            'openai', 'gpt', 'claude', 'ai', 'machine learning', 'llm',
            'leonardo', 'stable diffusion', 'dall-e',
            # Services
            'instagram', 'youtube', 'social media', 'suno',
            # Skills
            'portfolio', 'resume', 'cv', 'experience', 'projects',
            'skills', 'expertise', 'capabilities'
        ]
        
        self.results = defaultdict(list)
    
    def search_file_content(self, filepath, keywords):
        """Search file for skill keywords"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            found_keywords = [kw for kw in keywords if kw in content]
            return found_keywords
        except:
            return []
    
    def analyze_file(self, filepath):
        """Analyze a single file"""
        found = self.search_file_content(filepath, self.skill_keywords)
        
        if len(found) >= 3:  # Must have at least 3 skill keywords
            return {
                'path': str(filepath),
                'name': filepath.name,
                'type': filepath.suffix,
                'size_kb': filepath.stat().st_size / 1024,
                'keywords_found': found,
                'keyword_count': len(found),
                'location': str(filepath.parent)
            }
        return None
    
    def scan_location(self, location, extensions):
        """Scan a location for specific file types"""
        if not location.exists():
            print(f"  ??  {location} not accessible")
            return
        
        print(f"\n?? Scanning: {location}")
        
        for ext in extensions:
            files = list(location.rglob(f'*{ext}'))
            print(f"  {ext}: {len(files)} files")
            
            for filepath in files[:200]:  # Limit per type
                result = self.analyze_file(filepath)
                if result:
                    self.results[ext].append(result)
    
    def generate_report(self):
        """Generate portfolio content report"""
        report_path = self.search_locations[0] / 'pythons' / 'PORTFOLIO_CONTENT_FOUND.md'
        
        content = f"""# ?? Portfolio & Skills Documentation Found

> **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> **Locations Scanned**: Home, 2T-Xx, DeVonDaTa

---

## ?? Summary

"""
        
        total_files = sum(len(files) for files in self.results.values())
        content += f"**Total Relevant Files**: {total_files}\n\n"
        
        for file_type, files in sorted(self.results.items()):
            if files:
                content += f"- **{file_type} files**: {len(files)}\n"
        
        content += "\n---\n"
        
        # Group by type
        for file_type in ['.html', '.md', '.pdf']:
            if file_type not in self.results or not self.results[file_type]:
                continue
            
            files = self.results[file_type]
            content += f"\n## {file_type.upper()} Files ({len(files)})\n\n"
            
            # Sort by keyword count (most relevant first)
            for item in sorted(files, key=lambda x: -x['keyword_count'])[:30]:
                content += f"### {item['name']}\n\n"
                content += f"**Path**: `{item['path']}`\n\n"
                content += f"**Keywords** ({item['keyword_count']}): {', '.join(item['keywords_found'][:10])}\n\n"
                content += f"**Size**: {item['size_kb']:.1f} KB\n\n"
                content += "---\n\n"
        
        # Priority list
        content += "\n## ?? High Priority Files\n\n"
        content += "Files most likely to be portfolio/resume content:\n\n"
        
        all_files = []
        for files in self.results.values():
            all_files.extend(files)
        
        # Find files with portfolio-specific keywords
        priority_keywords = ['portfolio', 'resume', 'cv', 'experience', 'skills']
        priority_files = [
            f for f in all_files
            if any(pk in ' '.join(f['keywords_found']) for pk in priority_keywords)
        ]
        
        for item in sorted(priority_files, key=lambda x: -x['keyword_count'])[:20]:
            content += f"1. **{item['name']}** ({item['type']})\n"
            content += f"   - Path: `{item['path']}`\n"
            content += f"   - Keywords: {', '.join(item['keywords_found'][:8])}\n\n"
        
        with open(report_path, 'w') as f:
            f.write(content)
        
        print(f"\n? Report saved: {report_path}")
        return report_path

def main():
    print("?? Portfolio & Skills Content Finder")
    print("=" * 80)
    
    finder = PortfolioFinder()
    
    # Search for portfolio-related files
    extensions = ['.html', '.md', '.pdf']
    
    for location in finder.search_locations:
        finder.scan_location(location, extensions)
    
    # Generate report
    report = finder.generate_report()
    
    print("\n" + "=" * 80)
    print("? SEARCH COMPLETE")
    print("=" * 80)
    
    total = sum(len(files) for files in finder.results.values())
    print(f"\n?? Found {total} relevant files")
    
    for file_type, files in sorted(finder.results.items()):
        if files:
            print(f"  ? {file_type}: {len(files)} files")
    
    print(f"\n?? Full report: {report}")

if __name__ == "__main__":
    main()
