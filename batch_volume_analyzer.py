#!/usr/bin/env python3
"""
BATCH VOLUME ANALYZER
Analyzes volumes one at a time to avoid resource overload
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class BatchVolumeAnalyzer:
    """Analyzes one volume/folder at a time"""
    
    def __init__(self, max_files_per_batch: int = 50):
        self.max_files_per_batch = max_files_per_batch
        self.results = {
            'volumes': {},
            'summary': {},
        }
        self.stats = {
            'files_analyzed': 0,
            'python_files': 0,
            'html_files': 0,
            'json_files': 0,
            'markdown_files': 0,
            'image_files': 0,
            'audio_files': 0,
            'video_files': 0,
        }
        self.findings = {
            'apis_integrated': set(),
            'technologies': set(),
            'projects': [],
        }
    
    def analyze_volume(self, volume_path: str, max_depth: int = 4) -> Dict[str, Any]:
        """Analyze a single volume"""
        volume = Path(volume_path)
        
        if not volume.exists():
            return {'error': f'Volume not found: {volume_path}'}
        
        print(f"\n{'='*60}")
        print(f"📦 ANALYZING: {volume_path}")
        print(f"{'='*60}\n")
        
        volume_data = {
            'path': str(volume),
            'name': volume.name,
            'directories': {},
            'key_findings': [],
            'total_files': 0,
            'total_size': 0,
            'file_types': defaultdict(int),
            'projects': [],
            'technologies': set(),
            'apis': set(),
        }
        
        # Step 1: Identify key directories
        print("🔍 Step 1: Identifying key directories...")
        key_dirs = self._find_key_directories(volume, max_depth)
        print(f"   Found {len(key_dirs)} key directories\n")
        
        # Step 2: Analyze each directory
        for i, dir_path in enumerate(key_dirs[:30], 1):  # Limit to 30 directories
            rel_path = str(dir_path.relative_to(volume))
            print(f"   [{i}/{min(30, len(key_dirs))}] Analyzing: {rel_path}")
            
            dir_analysis = self._analyze_directory(dir_path)
            if dir_analysis:
                volume_data['directories'][rel_path] = dir_analysis
                
                # Collect findings
                if dir_analysis.get('technologies'):
                    volume_data['technologies'].update(dir_analysis['technologies'])
                if dir_analysis.get('apis'):
                    volume_data['apis'].update(dir_analysis['apis'])
                if dir_analysis.get('project_type'):
                    volume_data['projects'].append({
                        'path': rel_path,
                        'type': dir_analysis['project_type'],
                        'purpose': dir_analysis.get('purpose', 'unknown'),
                    })
        
        # Step 3: Count files
        print("\n📊 Step 2: Counting files...")
        for root, dirs, files in os.walk(volume):
            depth = len(Path(root).relative_to(volume).parts)
            if depth > max_depth:
                dirs.clear()
                continue
            
            for file in files:
                filepath = Path(root) / file
                try:
                    volume_data['total_files'] += 1
                    volume_data['total_size'] += filepath.stat().st_size
                    
                    ext = filepath.suffix.lower()
                    if ext:
                        volume_data['file_types'][ext] += 1
                except:
                    pass
        
        # Convert sets to lists for JSON
        volume_data['technologies'] = sorted(list(volume_data['technologies']))
        volume_data['apis'] = sorted(list(volume_data['apis']))
        
        print("\n✅ Volume analysis complete!")
        print(f"   Total files: {volume_data['total_files']:,}")
        print(f"   Total size: {volume_data['total_size'] / (1024**3):.2f} GB")
        print(f"   Projects found: {len(volume_data['projects'])}")
        print(f"   Technologies: {len(volume_data['technologies'])}")
        
        return volume_data
    
    def _find_key_directories(self, volume: Path, max_depth: int) -> List[Path]:
        """Find important directories to analyze"""
        key_dirs = []
        
        # Priority patterns (most important first)
        priority_patterns = [
            ('**/ai-sites/**', 10),
            ('**/steven/**', 10),
            ('**/projects/**', 5),
            ('**/code/**', 5),
            ('**/scripts/**', 5),
            ('**/content/**', 5),
            ('**/gallery/**', 5),
            ('**/music/**', 5),
            ('**/images/**', 5),
            ('**/archives/**', 3),
            ('**/AvaTarArTs/**', 5),
            ('**/leonardo/**', 3),
            ('**/all/**', 3),
        ]
        
        for pattern, limit in priority_patterns:
            try:
                matches = list(volume.glob(pattern))
                key_dirs.extend(matches[:limit])
            except:
                pass
        
        # Also get top-level directories
        try:
            for item in volume.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    if item not in key_dirs:
                        key_dirs.append(item)
        except:
            pass
        
        # Remove duplicates and sort
        key_dirs = sorted(set(key_dirs), key=lambda x: str(x))
        
        return key_dirs[:50]  # Max 50 directories
    
    def _analyze_directory(self, dir_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single directory"""
        if not dir_path.exists() or not dir_path.is_dir():
            return None
        
        dir_analysis = {
            'path': str(dir_path),
            'files': [],
            'file_count': 0,
            'project_type': None,
            'technologies': [],
            'apis': [],
            'purpose': None,
            'key_files': [],
        }
        
        files_analyzed = 0
        for item in dir_path.iterdir():
            if files_analyzed >= self.max_files_per_batch:
                break
            
            if item.is_file():
                analysis = self._analyze_file(item)
                if analysis:
                    dir_analysis['files'].append(analysis)
                    dir_analysis['file_count'] += 1
                    files_analyzed += 1
                    
                    # Extract technologies and APIs
                    if 'technologies' in analysis:
                        dir_analysis['technologies'].extend(analysis['technologies'])
                    if 'apis_used' in analysis:
                        dir_analysis['apis'].extend(analysis['apis_used'])
                    
                    # Determine project type
                    if analysis.get('type') == 'python' and not dir_analysis['project_type']:
                        dir_analysis['project_type'] = 'Python Project'
                        if analysis.get('purpose'):
                            dir_analysis['purpose'] = analysis['purpose']
                    
                    # Key files
                    if analysis.get('type') in ['python', 'html', 'json', 'markdown']:
                        dir_analysis['key_files'].append({
                            'name': item.name,
                            'type': analysis.get('type'),
                            'purpose': analysis.get('purpose'),
                        })
        
        # Deduplicate
        dir_analysis['technologies'] = list(set(dir_analysis['technologies']))
        dir_analysis['apis'] = list(set(dir_analysis['apis']))
        
        return dir_analysis
    
    def _analyze_file(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Quick file analysis"""
        try:
            if not filepath.exists() or not filepath.is_file():
                return None
            
            if filepath.name.startswith('.') or filepath.name.startswith('__'):
                return None
            
            size = filepath.stat().st_size
            if size > 10 * 1024 * 1024 or size == 0:  # 10MB limit
                return None
            
            ext = filepath.suffix.lower()
            analysis = {
                'name': filepath.name,
                'extension': ext,
                'size': size,
            }
            
            # Python files
            if ext == '.py':
                analysis.update(self._analyze_python_quick(filepath))
                self.stats['python_files'] += 1
            
            # HTML files
            elif ext in ['.html', '.htm']:
                analysis.update(self._analyze_html_quick(filepath))
                self.stats['html_files'] += 1
            
            # JSON files
            elif ext == '.json':
                analysis.update(self._analyze_json_quick(filepath))
                self.stats['json_files'] += 1
            
            # Markdown files
            elif ext in ['.md', '.markdown']:
                analysis.update(self._analyze_markdown_quick(filepath))
                self.stats['markdown_files'] += 1
            
            # Images
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                analysis['type'] = 'image'
                self.stats['image_files'] += 1
            
            # Audio
            elif ext in ['.mp3', '.wav', '.flac', '.m4a']:
                analysis['type'] = 'audio'
                self.stats['audio_files'] += 1
            
            # Video
            elif ext in ['.mp4', '.mov', '.avi', '.mkv']:
                analysis['type'] = 'video'
                self.stats['video_files'] += 1
            
            self.stats['files_analyzed'] += 1
            return analysis
            
        except Exception:
            return None
    
    def _analyze_python_quick(self, filepath: Path) -> Dict[str, Any]:
        """Quick Python analysis"""
        result = {
            'type': 'python',
            'classes': [],
            'functions': [],
            'imports': [],
            'apis_used': [],
            'technologies': [],
            'purpose': 'unknown',
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(50000)  # First 50KB only
            
            # Quick import detection
            import_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(\S+)'
            imports = re.findall(import_pattern, content, re.MULTILINE)
            for from_mod, imp in imports:
                module = from_mod or imp.split('.')[0]
                result['imports'].append(module)
                
                # Detect APIs
                api_map = {
                    'openai': 'OpenAI',
                    'anthropic': 'Anthropic Claude',
                    'google.generativeai': 'Google Gemini',
                    'groq': 'Groq',
                    'xai': 'Grok/XAI',
                    'perplexity': 'Perplexity',
                    'selenium': 'Selenium',
                    'requests': 'HTTP Requests',
                    'beautifulsoup': 'BeautifulSoup',
                    'pandas': 'Pandas',
                }
                
                for key, api_name in api_map.items():
                    if key in module.lower():
                        result['apis_used'].append(api_name)
                        result['technologies'].append(api_name)
            
            # Purpose detection
            content_lower = content.lower()
            if any(w in content_lower for w in ['trend', 'seo', 'optimize']):
                result['purpose'] = 'SEO/Content Optimization'
            elif any(w in content_lower for w in ['extract', 'scrape', 'grab']):
                result['purpose'] = 'Content Extraction'
            elif any(w in content_lower for w in ['orchestrat', 'route', 'multi']):
                result['purpose'] = 'AI Orchestration'
            elif any(w in content_lower for w in ['audio', 'music', 'transcribe']):
                result['purpose'] = 'Audio Processing'
            elif any(w in content_lower for w in ['image', 'gallery', 'visual']):
                result['purpose'] = 'Image Processing'
            elif any(w in content_lower for w in ['automate', 'workflow']):
                result['purpose'] = 'Automation'
            elif any(w in content_lower for w in ['youtube', 'video']):
                result['purpose'] = 'YouTube/Video Content'
        
        except:
            pass
        
        return result
    
    def _analyze_html_quick(self, filepath: Path) -> Dict[str, Any]:
        """Quick HTML analysis"""
        result = {
            'type': 'html',
            'title': None,
            'is_gallery': False,
            'is_landing_page': False,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(20000)  # First 20KB
            
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                result['title'] = title_match.group(1).strip()[:100]
            
            content_lower = content.lower()
            if any(w in content_lower for w in ['gallery', 'image', 'photo', 'portfolio']):
                result['is_gallery'] = True
            if any(w in content_lower for w in ['landing', 'hero', 'cta']):
                result['is_landing_page'] = True
        
        except:
            pass
        
        return result
    
    def _analyze_json_quick(self, filepath: Path) -> Dict[str, Any]:
        """Quick JSON analysis"""
        result = {
            'type': 'json',
            'structure': 'unknown',
            'purpose': None,
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10000)  # First 10KB
                data = json.loads(content)
            
            if isinstance(data, dict):
                result['structure'] = 'object'
                keys = list(data.keys())[:10]
                json_str = json.dumps(data).lower()
                
                if 'workflow' in json_str or 'blueprint' in json_str:
                    result['purpose'] = 'Workflow/Blueprint'
                elif 'api' in json_str or 'endpoint' in json_str:
                    result['purpose'] = 'API Configuration'
            elif isinstance(data, list):
                result['structure'] = 'array'
        
        except:
            pass
        
        return result
    
    def _analyze_markdown_quick(self, filepath: Path) -> Dict[str, Any]:
        """Quick Markdown analysis"""
        result = {
            'type': 'markdown',
            'headings': [],
            'topics': [],
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(10000)  # First 10KB
            
            headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
            result['headings'] = headings[:10]
            
            content_lower = content.lower()
            topics = []
            if any(w in content_lower for w in ['seo', 'optimize', 'keyword']):
                topics.append('SEO')
            if any(w in content_lower for w in ['ai', 'llm', 'machine learning']):
                topics.append('AI/ML')
            if any(w in content_lower for w in ['trend', 'trending']):
                topics.append('Trending Content')
            result['topics'] = topics
        
        except:
            pass
        
        return result


def main():
    """Main execution - analyze volumes one at a time"""
    volumes = [
        '/Volumes/2T-Xx',
        '/Volumes/DeVonDaTa',
    ]
    
    analyzer = BatchVolumeAnalyzer(max_files_per_batch=50)
    all_results = {}
    
    for i, volume_path in enumerate(volumes, 1):
        print(f"\n{'#'*60}")
        print(f"# BATCH {i}/{len(volumes)}: {volume_path}")
        print(f"{'#'*60}\n")
        
        try:
            volume_data = analyzer.analyze_volume(volume_path, max_depth=4)
            all_results[volume_path] = volume_data
            
            # Save intermediate results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            batch_file = Path.home() / f'VOLUME_ANALYSIS_{Path(volume_path).name}_{timestamp}.json'
            
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(volume_data, f, indent=2, default=str)
            
            print(f"\n💾 Batch saved: {batch_file}")
            
        except Exception as e:
            print(f"\n❌ Error analyzing {volume_path}: {e}")
            all_results[volume_path] = {'error': str(e)}
    
    # Generate final report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    final_file = Path.home() / f'COMPLETE_VOLUMES_ANALYSIS_{timestamp}.json'
    
    with open(final_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    # Generate markdown report
    report_file = Path.home() / f'VOLUMES_ANALYSIS_REPORT_{timestamp}.md'
    generate_report(all_results, report_file, analyzer.stats)
    
    print(f"\n{'='*60}")
    print("✅ COMPLETE ANALYSIS FINISHED")
    print(f"{'='*60}")
    print(f"📄 Final JSON: {final_file}")
    print(f"📝 Markdown Report: {report_file}")
    print(f"\n📊 Total Files Analyzed: {analyzer.stats['files_analyzed']}")
    print(f"   Python: {analyzer.stats['python_files']}")
    print(f"   HTML: {analyzer.stats['html_files']}")
    print(f"   JSON: {analyzer.stats['json_files']}")
    print(f"   Markdown: {analyzer.stats['markdown_files']}")


def generate_report(results: Dict, output_file: Path, stats: Dict):
    """Generate comprehensive markdown report"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🔍 DEEP MULTI-VOLUME CONTENT-AWARE ANALYSIS REPORT\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 📊 Executive Summary\n\n")
        f.write(f"- **Volumes Analyzed:** {len(results)}\n")
        f.write(f"- **Total Files Analyzed:** {stats['files_analyzed']}\n")
        f.write(f"- **Python Files:** {stats['python_files']}\n")
        f.write(f"- **HTML Files:** {stats['html_files']}\n")
        f.write(f"- **JSON Files:** {stats['json_files']}\n")
        f.write(f"- **Markdown Files:** {stats['markdown_files']}\n\n")
        
        # Volume details
        f.write("## 📦 Volume Analysis\n\n")
        for volume_path, volume_data in results.items():
            if 'error' in volume_data:
                f.write(f"### {volume_path}\n\n")
                f.write(f"❌ Error: {volume_data['error']}\n\n")
                continue
            
            f.write(f"### {volume_data.get('name', Path(volume_path).name)}\n\n")
            f.write(f"**Path:** `{volume_path}`\n\n")
            f.write(f"- **Total Files:** {volume_data.get('total_files', 0):,}\n")
            f.write(f"- **Total Size:** {volume_data.get('total_size', 0) / (1024**3):.2f} GB\n")
            f.write(f"- **Directories Analyzed:** {len(volume_data.get('directories', {}))}\n")
            f.write(f"- **Projects Found:** {len(volume_data.get('projects', []))}\n")
            f.write(f"- **Technologies:** {len(volume_data.get('technologies', []))}\n")
            f.write(f"- **APIs:** {len(volume_data.get('apis', []))}\n\n")
            
            # Projects
            if volume_data.get('projects'):
                f.write("#### 🎯 Projects Identified\n\n")
                for proj in volume_data['projects'][:10]:
                    f.write(f"- **{proj['path']}**\n")
                    f.write(f"  - Type: {proj['type']}\n")
                    f.write(f"  - Purpose: {proj.get('purpose', 'unknown')}\n\n")
            
            # Technologies
            if volume_data.get('technologies'):
                f.write("#### 🔧 Technologies\n\n")
                for tech in volume_data['technologies'][:20]:
                    f.write(f"- {tech}\n")
                f.write("\n")
            
            # APIs
            if volume_data.get('apis'):
                f.write("#### 🔌 APIs Integrated\n\n")
                for api in volume_data['apis'][:20]:
                    f.write(f"- {api}\n")
                f.write("\n")
            
            # Key directories
            if volume_data.get('directories'):
                f.write("#### 📁 Key Directories\n\n")
                for dir_path, dir_info in list(volume_data['directories'].items())[:15]:
                    f.write(f"**{dir_path}**\n")
                    if dir_info.get('project_type'):
                        f.write(f"- Type: {dir_info['project_type']}\n")
                    if dir_info.get('purpose'):
                        f.write(f"- Purpose: {dir_info['purpose']}\n")
                    if dir_info.get('file_count'):
                        f.write(f"- Files: {dir_info['file_count']}\n")
                    if dir_info.get('key_files'):
                        f.write(f"- Key Files: {len(dir_info['key_files'])}\n")
                    f.write("\n")


if __name__ == '__main__':
    main()

