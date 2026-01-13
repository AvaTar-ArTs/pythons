#!/usr/bin/env python3
"""
Analyze Scattered Python Code by Content
Check actual code functionality, imports, and purpose
"""

import ast
import re
from pathlib import Path
from collections import defaultdict
import hashlib

class CodeContentAnalyzer:
    """Analyze Python files by their actual content"""
    
    def __init__(self):
        self.locations = [
            Path.home() / 'Documents' / 'pythons',
            Path('/Volumes/2T-Xx'),
            Path('/Volumes/DeVonDaTa'),
        ]
        self.analyzed = []
        self.duplicates = defaultdict(list)
        self.categories = defaultdict(list)
        
    def get_file_hash(self, filepath):
        """Get MD5 hash of file content"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def analyze_imports(self, filepath):
        """Extract and categorize imports"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            tree = ast.parse(content)
            imports = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
            
            return list(imports)
        except:
            # Fallback to regex if AST fails
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                imports = set()
                for match in re.finditer(r'^(?:from|import)\s+(\w+)', content, re.MULTILINE):
                    imports.add(match.group(1))
                return list(imports)
            except:
                return []
    
    def detect_functionality(self, filepath, imports):
        """Detect what the script does based on content"""
        functionality = {
            'type': 'utility',
            'services': [],
            'operations': [],
            'ai_powered': False
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().lower()
            
            # Detect services
            services = {
                'openai': ['openai', 'gpt', 'dall-e', 'whisper'],
                'anthropic': ['anthropic', 'claude'],
                'leonardo': ['leonardo'],
                'stability': ['stability', 'stablediffusion'],
                'instagram': ['instagram', 'instabot'],
                'youtube': ['youtube', 'pytube'],
                'suno': ['suno'],
                'elevenlabs': ['elevenlabs'],
                'assemblyai': ['assemblyai'],
                'replicate': ['replicate'],
                'aws': ['boto3', 'aws'],
                'supabase': ['supabase'],
            }
            
            for service, keywords in services.items():
                if any(kw in content for kw in keywords) or any(kw in imports for kw in keywords):
                    functionality['services'].append(service)
            
            # Detect operations
            operations = {
                'image_processing': ['pillow', 'pil', 'image', 'opencv', 'cv2'],
                'video_processing': ['ffmpeg', 'moviepy', 'video'],
                'audio_processing': ['audio', 'pydub', 'librosa', 'soundfile'],
                'data_analysis': ['pandas', 'numpy', 'dataframe'],
                'web_scraping': ['beautifulsoup', 'selenium', 'scrapy', 'requests'],
                'automation': ['schedule', 'cron', 'automate'],
                'api_integration': ['requests', 'http', 'api'],
                'database': ['sqlite', 'mysql', 'postgres', 'mongodb'],
                'file_management': ['shutil', 'glob', 'pathlib'],
            }
            
            for op, keywords in operations.items():
                if any(kw in content for kw in keywords) or any(kw in imports for kw in keywords):
                    functionality['operations'].append(op)
            
            # Check if AI-powered
            ai_keywords = ['gpt', 'claude', 'gemini', 'llm', 'ai', 'machine learning', 'neural']
            functionality['ai_powered'] = any(kw in content for kw in ai_keywords)
            
            # Determine type
            if functionality['services']:
                functionality['type'] = 'api_integration'
            elif 'automation' in functionality['operations']:
                functionality['type'] = 'automation'
            elif 'data_analysis' in functionality['operations']:
                functionality['type'] = 'data_processing'
            
            return functionality
            
        except Exception as e:
            return functionality
    
    def extract_docstring(self, filepath):
        """Extract module docstring"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            return docstring[:200] if docstring else None
        except:
            return None
    
    def analyze_file(self, filepath):
        """Comprehensive file analysis"""
        result = {
            'path': str(filepath),
            'name': filepath.name,
            'location': str(filepath.parent),
            'size_kb': filepath.stat().st_size / 1024,
            'hash': self.get_file_hash(filepath),
        }
        
        # Analyze content
        result['imports'] = self.analyze_imports(filepath)
        result['functionality'] = self.detect_functionality(filepath, result['imports'])
        result['docstring'] = self.extract_docstring(filepath)
        
        # Count lines
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                result['lines'] = len(f.readlines())
        except:
            result['lines'] = 0
        
        return result
    
    def scan_all_locations(self):
        """Scan all locations for Python files"""
        print("?? Scanning for Python files...")
        print("=" * 80)
        
        all_files = []
        
        for location in self.locations:
            if not location.exists():
                print(f"??  {location} not accessible")
                continue
            
            print(f"\n?? Scanning: {location}")
            
            # Find all .py files
            py_files = list(location.rglob('*.py'))
            print(f"  Found {len(py_files)} Python files")
            
            all_files.extend(py_files)
        
        print(f"\n?? Total Python files found: {len(all_files)}")
        return all_files
    
    def analyze_all(self, files, limit=None):
        """Analyze all files"""
        print(f"\n?? Analyzing file contents...")
        print("=" * 80)
        
        if limit:
            files = files[:limit]
        
        for i, filepath in enumerate(files, 1):
            if i % 50 == 0:
                print(f"  Progress: {i}/{len(files)}")
            
            try:
                analysis = self.analyze_file(filepath)
                self.analyzed.append(analysis)
                
                # Track duplicates by hash
                if analysis['hash']:
                    self.duplicates[analysis['hash']].append(analysis)
                
                # Categorize by functionality
                func_type = analysis['functionality']['type']
                self.categories[func_type].append(analysis)
                
            except Exception as e:
                print(f"  ??  Error analyzing {filepath.name}: {e}")
        
        print(f"? Analyzed {len(self.analyzed)} files")
    
    def find_duplicates(self):
        """Find duplicate files by content"""
        print("\n?? Finding Duplicates...")
        print("=" * 80)
        
        dupes = {k: v for k, v in self.duplicates.items() if len(v) > 1}
        
        if not dupes:
            print("  No duplicates found!")
            return
        
        print(f"\n  Found {len(dupes)} sets of duplicates:")
        
        for hash_val, files in sorted(dupes.items(), key=lambda x: -len(x[1]))[:10]:
            print(f"\n  ?? {len(files)} identical copies:")
            for f in files:
                location = 'pythons' if 'pythons' in f['location'] else '2T-Xx' if '2T-Xx' in f['location'] else 'DeVonDaTa'
                print(f"    ? {f['name']} ({location}) - {f['size_kb']:.1f}KB")
    
    def generate_recommendations(self):
        """Generate smart recommendations"""
        print("\n?? Recommendations")
        print("=" * 80)
        
        # Find duplicates to remove
        dupes = {k: v for k, v in self.duplicates.items() if len(v) > 1}
        
        if dupes:
            print(f"\n???  Duplicates to Remove:")
            for hash_val, files in list(dupes.items())[:5]:
                # Keep the one in ~/Documents/pythons, remove others
                keep = None
                remove = []
                
                for f in files:
                    if 'pythons' in f['location']:
                        keep = f
                    else:
                        remove.append(f)
                
                if keep and remove:
                    print(f"\n  Keep: {keep['name']} (pythons)")
                    for r in remove:
                        loc = '2T-Xx' if '2T-Xx' in r['location'] else 'DeVonDaTa'
                        print(f"  Remove: {r['path']}")
        
        # Find valuable scripts on external drives
        print(f"\n? Valuable Scripts on External Drives:")
        external_valuable = [
            a for a in self.analyzed 
            if ('2T-Xx' in a['location'] or 'DeVonDaTa' in a['location'])
            and a['functionality']['ai_powered']
            and a['size_kb'] > 5  # Not trivial
        ]
        
        for script in sorted(external_valuable, key=lambda x: -x['size_kb'])[:10]:
            loc = '2T-Xx' if '2T-Xx' in script['location'] else 'DeVonDaTa'
            services = ', '.join(script['functionality']['services'][:3]) or 'General'
            print(f"  ? {script['name']} ({loc})")
            print(f"    Services: {services}")
            print(f"    Size: {script['size_kb']:.1f}KB | Lines: {script['lines']}")
    
    def generate_report(self):
        """Generate comprehensive report"""
        report_path = Path.home() / 'Documents' / 'pythons' / 'CODE_ANALYSIS_REPORT.md'
        
        content = f"""# ?? Scattered Code Content Analysis Report

> **Generated**: {Path.home() / 'Documents' / 'pythons'}
> **Files Analyzed**: {len(self.analyzed)}

## ?? Summary

### By Location
"""
        # Count by location
        locations = defaultdict(int)
        for a in self.analyzed:
            if 'pythons' in a['location']:
                locations['~/Documents/pythons'] += 1
            elif '2T-Xx' in a['location']:
                locations['/Volumes/2T-Xx'] += 1
            elif 'DeVonDaTa' in a['location']:
                locations['/Volumes/DeVonDaTa'] += 1
        
        for loc, count in sorted(locations.items(), key=lambda x: -x[1]):
            content += f"- **{loc}**: {count} files\n"
        
        content += "\n### By Type\n"
        for cat_type, files in sorted(self.categories.items(), key=lambda x: -len(x[1])):
            content += f"- **{cat_type}**: {len(files)} files\n"
        
        # AI-powered scripts
        ai_scripts = [a for a in self.analyzed if a['functionality']['ai_powered']]
        content += f"\n### AI-Powered Scripts: {len(ai_scripts)}\n\n"
        
        # Most used services
        all_services = []
        for a in self.analyzed:
            all_services.extend(a['functionality']['services'])
        
        from collections import Counter
        service_counts = Counter(all_services)
        
        content += "\n### Top Services Used\n"
        for service, count in service_counts.most_common(10):
            content += f"- **{service}**: {count} scripts\n"
        
        # Duplicates section
        dupes = {k: v for k, v in self.duplicates.items() if len(v) > 1}
        content += f"\n## ?? Duplicates Found: {len(dupes)} sets\n\n"
        
        for i, (hash_val, files) in enumerate(sorted(dupes.items(), key=lambda x: -len(x[1]))[:20], 1):
            content += f"\n### {i}. {files[0]['name']} ({len(files)} copies)\n"
            for f in files:
                loc = 'pythons' if 'pythons' in f['location'] else '2T-Xx' if '2T-Xx' in f['location'] else 'DeVonDaTa'
                content += f"- `{f['path']}`\n"
        
        # Save report
        with open(report_path, 'w') as f:
            f.write(content)
        
        print(f"\n?? Report saved: {report_path}")
        return report_path
    
    def run(self, limit=None):
        """Run full analysis"""
        print("?? Scattered Code Content Analyzer")
        print("=" * 80)
        
        # Scan
        files = self.scan_all_locations()
        
        # Analyze
        self.analyze_all(files, limit=limit)
        
        # Find duplicates
        self.find_duplicates()
        
        # Recommendations
        self.generate_recommendations()
        
        # Generate report
        report = self.generate_report()
        
        print("\n" + "=" * 80)
        print("? Analysis Complete!")
        print("=" * 80)

def main():
    import sys
    
    # Limit for testing
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    
    print(f"Analyzing up to {limit} files (pass number as argument to change)\n")
    
    analyzer = CodeContentAnalyzer()
    analyzer.run(limit=limit)

if __name__ == "__main__":
    main()
