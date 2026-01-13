#!/usr/bin/env python3
"""
Master Intelligent Content-Awareness System
Processes all directories with unified intelligence layer

Usage:
    python master_content_analyzer.py [--dir DIR] [--all] [--search "query"] [--config]
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict
import hashlib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'Documents' / '.intelligence'))

# Try to import the base analyzer
try:
    from intelligent_documents_analyzer import IntelligentDocumentsAnalyzer
    BASE_ANALYZER_AVAILABLE = True
except ImportError:
    BASE_ANALYZER_AVAILABLE = False
    print("⚠️  Base analyzer not found, using standalone mode")


class MasterContentAnalyzer:
    """Master analyzer for all directories"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.home = Path.home()
        self.intelligence_dir = self.home / '.intelligence'
        self.intelligence_dir.mkdir(exist_ok=True)
        
        self.config_path = config_path or self.intelligence_dir / 'directories_config.json'
        self.metadata_path = self.intelligence_dir / 'master_metadata.json'
        self.results_dir = self.intelligence_dir / 'results'
        self.results_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self.config = self.load_config()
        
        # Processing state
        self.processed_files = self.load_processed_files()
        self.directory_stats = defaultdict(lambda: {
            'total_files': 0,
            'processed': 0,
            'errors': 0,
            'last_processed': None
        })
        
        # Initialize base analyzer if available
        self.base_analyzer = None
        if BASE_ANALYZER_AVAILABLE:
            try:
                self.base_analyzer = IntelligentDocumentsAnalyzer()
            except Exception as e:
                print(f"⚠️  Could not initialize base analyzer: {e}")
    
    def load_config(self) -> Dict:
        """Load directory configuration"""
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text())
            except:
                pass
        
        # Default configuration
        return {
            'directories': self.get_default_directories(),
            'settings': {
                'batch_size': 100,
                'max_file_size_mb': 100,
                'enable_embeddings': True,
                'enable_summaries': True,
            }
        }
    
    def get_default_directories(self) -> List[Dict]:
        """Get default directory list"""
        directories = [
            {
                'path': str(self.home / 'claude'),
                'name': 'Claude Conversations',
                'type': 'conversations',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'Documents'),
                'name': 'Documents',
                'type': 'mixed',
                'priority': 'high',
                'enabled': True,
            },
            {
                'path': str(self.home / 'Downloads'),
                'name': 'Downloads',
                'type': 'temporary',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'GitHub'),
                'name': 'GitHub Repositories',
                'type': 'code',
                'priority': 'high',
                'enabled': True,
            },
            {
                'path': str(self.home / 'Movies'),
                'name': 'Movies',
                'type': 'video',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'Music'),
                'name': 'Music',
                'type': 'audio',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'Pictures'),
                'name': 'Pictures',
                'type': 'images',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'pythons'),
                'name': 'Python Projects',
                'type': 'code',
                'priority': 'high',
                'enabled': True,
            },
            {
                'path': str(self.home / 'workspace'),
                'name': 'Workspace',
                'type': 'projects',
                'priority': 'high',
                'enabled': True,
            },
            {
                'path': str(self.home / 'advanced_toolkit'),
                'name': 'Advanced Toolkit',
                'type': 'tools',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'ai-sites'),
                'name': 'AI Sites',
                'type': 'projects',
                'priority': 'high',
                'enabled': True,
            },
            {
                'path': str(self.home / 'analysis_reports'),
                'name': 'Analysis Reports',
                'type': 'reports',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'clean'),
                'name': 'Clean',
                'type': 'organized',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'clipboard_items'),
                'name': 'Clipboard Items',
                'type': 'misc',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'docs'),
                'name': 'Documentation',
                'type': 'docs',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'docs_docsify'),
                'name': 'Docsify Docs',
                'type': 'docs',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'docs_mkdocs'),
                'name': 'MkDocs',
                'type': 'docs',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'docs_pdoc'),
                'name': 'Pdoc',
                'type': 'docs',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'docs_seo'),
                'name': 'SEO Docs',
                'type': 'docs',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'gemini'),
                'name': 'Gemini Conversations',
                'type': 'conversations',
                'priority': 'medium',
                'enabled': True,
            },
            {
                'path': str(self.home / 'organize'),
                'name': 'Organize',
                'type': 'tools',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'pydocs'),
                'name': 'Python Docs',
                'type': 'docs',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'sites-navigator'),
                'name': 'Sites Navigator',
                'type': 'tools',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'sphinx-docs'),
                'name': 'Sphinx Docs',
                'type': 'docs',
                'priority': 'low',
                'enabled': True,
            },
            {
                'path': str(self.home / 'tests'),
                'name': 'Tests',
                'type': 'code',
                'priority': 'low',
                'enabled': True,
            },
        ]
        
        return directories
    
    def save_config(self):
        """Save configuration"""
        self.config_path.write_text(json.dumps(self.config, indent=2))
    
    def load_processed_files(self) -> Dict[str, datetime]:
        """Load processed files metadata"""
        if self.metadata_path.exists():
            try:
                data = json.loads(self.metadata_path.read_text())
                return {
                    k: datetime.fromisoformat(v) 
                    for k, v in data.get('processed_files', {}).items()
                }
            except:
                return {}
        return {}
    
    def save_processed_files(self):
        """Save processed files metadata"""
        data = {
            'processed_files': {
                k: v.isoformat() 
                for k, v in self.processed_files.items()
            },
            'directory_stats': {
                k: {
                    **v,
                    'last_processed': v['last_processed'].isoformat() if v['last_processed'] else None
                }
                for k, v in self.directory_stats.items()
            },
            'last_updated': datetime.now().isoformat()
        }
        self.metadata_path.write_text(json.dumps(data, indent=2))
    
    def analyze_directory(self, dir_config: Dict, limit: Optional[int] = None) -> List[Dict]:
        """Analyze a single directory"""
        dir_path = Path(dir_config['path'])
        dir_name = dir_config['name']
        
        if not dir_path.exists():
            print(f"⚠️  Directory not found: {dir_path}")
            return []
        
        print(f"\n{'='*70}")
        print(f"📁 Analyzing: {dir_name}")
        print(f"   Path: {dir_path}")
        print(f"   Type: {dir_config.get('type', 'unknown')}")
        print(f"{'='*70}\n")
        
        # Get files
        all_files = []
        for file_path in dir_path.rglob('*'):
            if file_path.is_file():
                # Check ignore patterns
                if self.should_ignore(file_path, dir_config):
                    continue
                all_files.append(file_path)
        
        total_files = len(all_files)
        self.directory_stats[dir_name]['total_files'] = total_files
        
        print(f"📊 Found {total_files} files")
        
        if limit:
            all_files = all_files[:limit]
            print(f"   Processing first {limit} files")
        
        # Process files
        analyses = []
        processed = 0
        errors = 0
        
        for i, file_path in enumerate(all_files, 1):
            try:
                # Use base analyzer if available
                if self.base_analyzer:
                    analysis = self.base_analyzer.analyze_document(file_path)
                else:
                    analysis = self.analyze_file_basic(file_path, dir_config)
                
                if analysis:
                    analysis['directory'] = dir_name
                    analysis['directory_path'] = str(dir_path)
                    analyses.append(analysis)
                    processed += 1
                    self.processed_files[str(file_path)] = datetime.now()
                    
                    if i % 10 == 0:
                        print(f"  ✅ Processed {i}/{len(all_files)} files...")
            except Exception as e:
                errors += 1
                if errors <= 5:  # Only show first 5 errors
                    print(f"  ⚠️  Error processing {file_path.name}: {e}")
        
        # Update stats
        self.directory_stats[dir_name]['processed'] = processed
        self.directory_stats[dir_name]['errors'] = errors
        self.directory_stats[dir_name]['last_processed'] = datetime.now()
        
        print(f"\n✅ Completed: {processed} processed, {errors} errors")
        
        # Save results
        results_file = self.results_dir / f"{dir_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        results_file.write_text(json.dumps(analyses, indent=2))
        print(f"📄 Results saved: {results_file.name}")
        
        return analyses
    
    def should_ignore(self, file_path: Path, dir_config: Dict) -> bool:
        """Check if file should be ignored"""
        ignore_patterns = [
            '.DS_Store', '__pycache__', '.pyc', '.pyo', '.git',
            'node_modules', '.intelligence', '.env', '.env.d',
            '.DS_Store', 'Thumbs.db'
        ]
        
        # Add directory-specific ignores
        ignore_patterns.extend(dir_config.get('ignore_patterns', []))
        
        file_str = str(file_path)
        return any(pattern in file_str for pattern in ignore_patterns)
    
    def analyze_file_basic(self, file_path: Path, dir_config: Dict) -> Optional[Dict]:
        """Basic file analysis (fallback)"""
        try:
            stat = file_path.stat()
            
            analysis = {
                'file': str(file_path),
                'name': file_path.name,
                'extension': file_path.suffix,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': self.detect_file_type(file_path),
            }
            
            # Try to read text content for small files
            if stat.st_size < 1024 * 1024:  # < 1MB
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    analysis['line_count'] = len(content.split('\n'))
                    analysis['word_count'] = len(content.split())
                    analysis['content_preview'] = content[:500]
                except:
                    pass
            
            return analysis
        except Exception as e:
            return None
    
    def detect_file_type(self, file_path: Path) -> str:
        """Detect file type"""
        ext = file_path.suffix.lower()
        
        type_map = {
            '.md': 'markdown',
            '.txt': 'text',
            '.py': 'python',
            '.js': 'javascript',
            '.json': 'json',
            '.csv': 'csv',
            '.pdf': 'pdf',
            '.mp3': 'audio',
            '.mp4': 'video',
            '.jpg': 'image',
            '.png': 'image',
        }
        
        return type_map.get(ext, 'unknown')
    
    def process_all_directories(self, limit_per_dir: Optional[int] = None):
        """Process all enabled directories"""
        print("🧠 Master Content Analyzer")
        print("=" * 70)
        print(f"📊 Processing {len(self.config['directories'])} directories\n")
        
        all_analyses = []
        
        # Sort by priority
        directories = sorted(
            [d for d in self.config['directories'] if d.get('enabled', True)],
            key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x.get('priority', 'low'), 2)
        )
        
        for dir_config in directories:
            try:
                analyses = self.analyze_directory(dir_config, limit=limit_per_dir)
                all_analyses.extend(analyses)
            except Exception as e:
                print(f"⚠️  Error processing {dir_config['name']}: {e}")
        
        # Save master results
        master_results = self.results_dir / f"master_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        master_results.write_text(json.dumps(all_analyses, indent=2))
        
        # Save metadata
        self.save_processed_files()
        
        print(f"\n{'='*70}")
        print("✅ Master Analysis Complete")
        print(f"📊 Total files analyzed: {len(all_analyses)}")
        print(f"📄 Master results: {master_results.name}")
        print(f"{'='*70}\n")
        
        return all_analyses
    
    def process_directory(self, dir_name: str, limit: Optional[int] = None):
        """Process a specific directory"""
        dir_config = next(
            (d for d in self.config['directories'] if d['name'] == dir_name),
            None
        )
        
        if not dir_config:
            print(f"⚠️  Directory not found in config: {dir_name}")
            return []
        
        return self.analyze_directory(dir_config, limit=limit)
    
    def generate_master_report(self):
        """Generate master report"""
        print("📊 Generating Master Report...\n")
        
        # Load latest results
        result_files = sorted(self.results_dir.glob('master_analysis_*.json'))
        if not result_files:
            print("⚠️  No master analysis found. Run --all first.")
            return
        
        latest = json.loads(result_files[-1].read_text())
        
        # Generate statistics
        stats = {
            'total_files': len(latest),
            'by_directory': defaultdict(int),
            'by_type': defaultdict(int),
            'by_extension': defaultdict(int),
        }
        
        for analysis in latest:
            stats['by_directory'][analysis.get('directory', 'unknown')] += 1
            stats['by_type'][analysis.get('type', 'unknown')] += 1
            stats['by_extension'][analysis.get('extension', 'unknown')] += 1
        
        print("📈 Master Statistics")
        print("=" * 70)
        print(f"Total Files Analyzed: {stats['total_files']}\n")
        
        print("By Directory:")
        for dir_name, count in sorted(stats['by_directory'].items(), key=lambda x: -x[1]):
            print(f"  {dir_name:30} {count:>6} files")
        
        print("\nBy Type:")
        for file_type, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
            print(f"  {file_type:30} {count:>6} files")
        
        print("\nBy Extension:")
        for ext, count in sorted(stats['by_extension'].items(), key=lambda x: -x[1])[:20]:
            print(f"  {ext:30} {count:>6} files")
        
        # Save report
        report_path = self.intelligence_dir / f"master_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.write_text(json.dumps(stats, indent=2))
        print(f"\n📄 Report saved: {report_path.name}")
    
    def list_directories(self):
        """List all configured directories"""
        print("📁 Configured Directories\n")
        print(f"{'Name':<30} {'Path':<40} {'Type':<15} {'Priority':<10} {'Status'}")
        print("=" * 100)
        
        for dir_config in self.config['directories']:
            status = "✅ Enabled" if dir_config.get('enabled', True) else "❌ Disabled"
            path = dir_config['path'].replace(str(self.home), '~')
            print(f"{dir_config['name']:<30} {path:<40} {dir_config.get('type', 'unknown'):<15} {dir_config.get('priority', 'low'):<10} {status}")


def main():
    parser = argparse.ArgumentParser(description='Master Content Analyzer')
    parser.add_argument('--all', action='store_true', help='Process all directories')
    parser.add_argument('--dir', type=str, help='Process specific directory by name')
    parser.add_argument('--limit', type=int, help='Limit files per directory')
    parser.add_argument('--report', action='store_true', help='Generate master report')
    parser.add_argument('--list', action='store_true', help='List all directories')
    parser.add_argument('--config', action='store_true', help='Show/edit configuration')
    
    args = parser.parse_args()
    
    analyzer = MasterContentAnalyzer()
    
    if args.list:
        analyzer.list_directories()
    elif args.config:
        print("📋 Configuration:")
        print(json.dumps(analyzer.config, indent=2))
        print(f"\n📄 Config file: {analyzer.config_path}")
    elif args.report:
        analyzer.generate_master_report()
    elif args.dir:
        analyzer.process_directory(args.dir, limit=args.limit)
    elif args.all:
        analyzer.process_all_directories(limit_per_dir=args.limit)
    else:
        print("🧠 Master Content Analyzer")
        print("\nUsage:")
        print("  --all           Process all directories")
        print("  --dir NAME      Process specific directory")
        print("  --limit N       Limit files per directory")
        print("  --report        Generate master report")
        print("  --list          List all directories")
        print("  --config        Show configuration")


if __name__ == '__main__':
    main()

