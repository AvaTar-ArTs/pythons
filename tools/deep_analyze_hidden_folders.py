#!/usr/bin/env python3
"""
Deep Intelligent Content-Aware Analysis of Hidden Folders
Analyzes all specified hidden folders with semantic understanding
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any, Optional
import hashlib

class DeepHiddenFolderAnalyzer:
    """Deep content-aware analysis of hidden folders"""
    
    def __init__(self, home_dir: Path = None):
        self.home = home_dir or Path.home()
        self.results_dir = self.home / 'intelligence' / 'deep_analysis'
        self.results_dir.mkdir(exist_ok=True)
        
        # Target folders
        self.target_folders = [
            '.aider', '.apify', '.aspnet', '.bun', '.bundle', '.cache',
            '.cfg', '.chatgpt', '.claude', '.claude-server-commander', '.codex',
            '.composer', '.config', '.cups', '.cursor', '.dotfiles', '.dotnet',
            '.EasyOCR', '.env.d', '.gem', '.gemini', '.github', '.gnupg',
            '.grok', '.history', '.hyper_plugins', '.idlerc', '.intelligence',
            '.ipython', '.iterm2', '.jupyter', '.keras', '.lh', '.local',
            '.m2', '.mamba', '.matplotlib', '.mplayer', '.n8n', '.npm',
            '.nuget', '.oh-my-zsh', '.ollama', '.package_manager_backup_20251106_070741',
            '.pdf-filler-profiles', '.postman', '.putty', '.pytest_cache',
            '.qodo', '.raycast', '.rustup', '.secrets', '.ServiceHub',
            '.sonarlint', '.spicetify', '.spotdl', '.ssh', '.streamlit',
            '.u2net', '.update_logs', '.x-cmd.root', '.zsh_sessions'
        ]
        
        # Content type patterns
        self.content_patterns = {
            'scripts': ['.py', '.sh', '.js', '.ts', '.rb', '.go', '.rs'],
            'config': ['.json', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg'],
            'docs': ['.md', '.txt', '.rst', '.adoc'],
            'data': ['.db', '.sqlite', '.csv', '.log'],
            'cache': ['.cache', '.tmp', '.lock'],
        }
        
        # Category definitions
        self.categories = {
            'development_tools': ['.aider', '.cursor', '.vscode', '.idea'],
            'package_managers': ['.npm', '.bun', '.gem', '.m2', '.nuget', '.composer', '.rustup'],
            'ai_tools': ['.chatgpt', '.claude', '.grok', '.gemini', '.codex'],
            'automation': ['.n8n', '.apify', '.raycast'],
            'config': ['.config', '.cfg', '.dotfiles'],
            'cache': ['.cache', '.pytest_cache', '.spicetify', '.local'],
            'history': ['.history', '.zsh_sessions', '.update_logs'],
            'security': ['.ssh', '.gnupg', '.secrets'],
            'frameworks': ['.oh-my-zsh', '.ipython', '.jupyter', '.idlerc'],
            'cloud_services': ['.postman', '.qodo', '.ServiceHub'],
            'media_tools': ['.mplayer', '.spotdl', '.EasyOCR', '.u2net'],
            'system': ['.cups', '.iterm2', '.hyper_plugins'],
        }
    
    def categorize_folder(self, folder_name: str) -> str:
        """Intelligently categorize a folder"""
        folder_lower = folder_name.lower()
        
        for category, patterns in self.categories.items():
            if any(pattern in folder_lower for pattern in patterns):
                return category
        
        # Fallback categorization
        if 'cache' in folder_lower or 'tmp' in folder_lower:
            return 'cache'
        elif 'history' in folder_lower or 'log' in folder_lower:
            return 'history'
        elif 'backup' in folder_lower:
            return 'backup'
        elif 'config' in folder_lower or 'cfg' in folder_lower:
            return 'config'
        else:
            return 'other'
    
    def analyze_content(self, folder_path: Path) -> Dict[str, Any]:
        """Deep content analysis of a folder"""
        if not folder_path.exists():
            return {'exists': False}
        
        analysis = {
            'exists': True,
            'path': str(folder_path),
            'name': folder_path.name,
            'category': self.categorize_folder(folder_path.name),
            'size_mb': 0,
            'file_count': 0,
            'dir_count': 0,
            'content_types': defaultdict(int),
            'scripts': [],
            'configs': [],
            'docs': [],
            'largest_files': [],
            'recent_files': [],
            'has_user_scripts': False,
            'has_system_scripts': False,
            'has_config': False,
            'has_cache': False,
            'recommendation': 'keep_hidden',
        }
        
        try:
            # Get folder size
            total_size = 0
            file_count = 0
            dir_count = 0
            
            # Analyze files
            for item in folder_path.rglob('*'):
                try:
                    if item.is_file():
                        file_count += 1
                        size = item.stat().st_size
                        total_size += size
                        
                        ext = item.suffix.lower()
                        
                        # Categorize by extension
                        if ext in self.content_patterns['scripts']:
                            analysis['scripts'].append({
                                'path': str(item.relative_to(folder_path)),
                                'size': size,
                                'ext': ext
                            })
                            if folder_path.name in ['.env.d', '.intelligence']:
                                analysis['has_user_scripts'] = True
                            else:
                                analysis['has_system_scripts'] = True
                        elif ext in self.content_patterns['config']:
                            analysis['configs'].append(str(item.relative_to(folder_path)))
                            analysis['has_config'] = True
                        elif ext in self.content_patterns['docs']:
                            analysis['docs'].append(str(item.relative_to(folder_path)))
                        
                        analysis['content_types'][ext or 'no_ext'] += 1
                        
                        # Track largest files
                        if len(analysis['largest_files']) < 10:
                            analysis['largest_files'].append({
                                'path': str(item.relative_to(folder_path)),
                                'size_mb': round(size / 1024 / 1024, 2)
                            })
                            analysis['largest_files'].sort(key=lambda x: x['size_mb'], reverse=True)
                        
                    elif item.is_dir():
                        dir_count += 1
                except (PermissionError, OSError):
                    continue
            
            analysis['size_mb'] = round(total_size / 1024 / 1024, 2)
            analysis['file_count'] = file_count
            analysis['dir_count'] = dir_count
            
            # Determine if cache
            if analysis['category'] == 'cache' or 'cache' in folder_path.name.lower():
                analysis['has_cache'] = True
            
            # Generate recommendation
            if analysis['has_user_scripts']:
                analysis['recommendation'] = 'review_visibility'
            elif analysis['has_system_scripts'] and analysis['category'] in ['development_tools', 'automation']:
                analysis['recommendation'] = 'document'
            elif analysis['has_cache'] and analysis['size_mb'] > 100:
                analysis['recommendation'] = 'cleanup_candidate'
            elif analysis['category'] == 'security':
                analysis['recommendation'] = 'keep_hidden_secure'
            else:
                analysis['recommendation'] = 'keep_hidden'
        
        except Exception as e:
            analysis['error'] = str(e)
        
        return analysis
    
    def analyze_all(self) -> Dict[str, Any]:
        """Analyze all target folders"""
        print("🔍 Deep Content-Aware Analysis of Hidden Folders")
        print("=" * 70)
        print(f"📁 Analyzing {len(self.target_folders)} folders...\n")
        
        results = {
            'analysis_date': datetime.now().isoformat(),
            'total_folders': len(self.target_folders),
            'folders_analyzed': 0,
            'folders_not_found': 0,
            'categories': defaultdict(list),
            'recommendations': defaultdict(list),
            'statistics': {
                'total_size_mb': 0,
                'total_files': 0,
                'total_scripts': 0,
                'folders_with_scripts': 0,
                'folders_with_user_scripts': 0,
            },
            'folders': {}
        }
        
        for folder_name in self.target_folders:
            folder_path = self.home / folder_name
            print(f"  Analyzing: {folder_name}...", end=' ')
            
            analysis = self.analyze_content(folder_path)
            results['folders'][folder_name] = analysis
            
            if analysis.get('exists'):
                results['folders_analyzed'] += 1
                category = analysis['category']
                results['categories'][category].append(folder_name)
                
                recommendation = analysis['recommendation']
                results['recommendations'][recommendation].append(folder_name)
                
                # Update statistics
                results['statistics']['total_size_mb'] += analysis.get('size_mb', 0)
                results['statistics']['total_files'] += analysis.get('file_count', 0)
                script_count = len(analysis.get('scripts', []))
                results['statistics']['total_scripts'] += script_count
                
                if script_count > 0:
                    results['statistics']['folders_with_scripts'] += 1
                if analysis.get('has_user_scripts'):
                    results['statistics']['folders_with_user_scripts'] += 1
                
                print(f"✅ ({analysis['size_mb']} MB, {analysis['file_count']} files)")
            else:
                results['folders_not_found'] += 1
                print("❌ Not found")
        
        print(f"\n✅ Analysis complete!")
        print(f"   Folders analyzed: {results['folders_analyzed']}")
        print(f"   Total size: {results['statistics']['total_size_mb']:.2f} MB")
        print(f"   Total files: {results['statistics']['total_files']:,}")
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive report"""
        report = []
        report.append("# Deep Content-Aware Analysis of Hidden Folders")
        report.append(f"**Generated:** {results['analysis_date']}\n")
        
        # Executive Summary
        report.append("## 📊 Executive Summary\n")
        stats = results['statistics']
        report.append(f"- **Folders Analyzed:** {results['folders_analyzed']}/{results['total_folders']}")
        report.append(f"- **Total Size:** {stats['total_size_mb']:.2f} MB")
        report.append(f"- **Total Files:** {stats['total_files']:,}")
        report.append(f"- **Total Scripts:** {stats['total_scripts']}")
        report.append(f"- **Folders with Scripts:** {stats['folders_with_scripts']}")
        report.append(f"- **Folders with User Scripts:** {stats['folders_with_user_scripts']}\n")
        
        # By Category
        report.append("## 📁 By Category\n")
        for category, folders in sorted(results['categories'].items()):
            report.append(f"### {category.replace('_', ' ').title()} ({len(folders)})")
            for folder in sorted(folders):
                folder_data = results['folders'][folder]
                if folder_data.get('exists'):
                    size = folder_data.get('size_mb', 0)
                    files = folder_data.get('file_count', 0)
                    scripts = len(folder_data.get('scripts', []))
                    report.append(f"- **`{folder}`** - {size:.1f} MB, {files:,} files, {scripts} scripts")
            report.append("")
        
        # Recommendations
        report.append("## 🎯 Recommendations\n")
        for rec_type, folders in sorted(results['recommendations'].items()):
            if folders:
                report.append(f"### {rec_type.replace('_', ' ').title()}")
                for folder in sorted(folders):
                    folder_data = results['folders'][folder]
                    if folder_data.get('exists'):
                        reason = self._get_recommendation_reason(folder_data)
                        report.append(f"- **`{folder}`** - {reason}")
                report.append("")
        
        # Detailed Analysis
        report.append("## 🔍 Detailed Analysis\n")
        
        # Folders with scripts
        script_folders = [
            (name, data) for name, data in results['folders'].items()
            if data.get('exists') and data.get('scripts')
        ]
        script_folders.sort(key=lambda x: len(x[1].get('scripts', [])), reverse=True)
        
        if script_folders:
            report.append("### Folders with Scripts\n")
            for folder_name, folder_data in script_folders[:15]:
                report.append(f"#### `{folder_name}`")
                report.append(f"- **Category:** {folder_data['category']}")
                report.append(f"- **Size:** {folder_data['size_mb']:.1f} MB")
                report.append(f"- **Scripts:** {len(folder_data['scripts'])}")
                report.append(f"- **Type:** {'User scripts' if folder_data.get('has_user_scripts') else 'System scripts'}")
                if folder_data['scripts'][:5]:
                    report.append("- **Sample scripts:**")
                    for script in folder_data['scripts'][:5]:
                        report.append(f"  - `{script['path']}` ({script['size']/1024:.1f} KB)")
                report.append("")
        
        # Large folders
        large_folders = [
            (name, data) for name, data in results['folders'].items()
            if data.get('exists') and data.get('size_mb', 0) > 50
        ]
        large_folders.sort(key=lambda x: x[1].get('size_mb', 0), reverse=True)
        
        if large_folders:
            report.append("### Large Folders (>50 MB)\n")
            for folder_name, folder_data in large_folders:
                report.append(f"- **`{folder_name}`** - {folder_data['size_mb']:.1f} MB ({folder_data['file_count']:,} files)")
            report.append("")
        
        return "\n".join(report)
    
    def _get_recommendation_reason(self, folder_data: Dict) -> str:
        """Get reason for recommendation"""
        if folder_data.get('has_user_scripts'):
            return "Contains user scripts - consider visibility"
        elif folder_data.get('has_system_scripts'):
            return "Contains system scripts - document if needed"
        elif folder_data.get('has_cache') and folder_data.get('size_mb', 0) > 100:
            return f"Large cache ({folder_data['size_mb']:.1f} MB) - cleanup candidate"
        elif folder_data['category'] == 'security':
            return "Security-sensitive - must stay hidden"
        else:
            return "Standard config/cache - correctly hidden"
    
    def save_results(self, results: Dict[str, Any]):
        """Save analysis results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = self.results_dir / f'deep_analysis_{timestamp}.json'
        json_file.write_text(json.dumps(results, indent=2))
        
        # Save report
        report_file = self.results_dir / f'deep_analysis_{timestamp}.md'
        report = self.generate_report(results)
        report_file.write_text(report)
        
        print(f"\n📄 Results saved:")
        print(f"   JSON: {json_file}")
        print(f"   Report: {report_file}")
        
        return json_file, report_file


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Deep analyze hidden folders')
    parser.add_argument('--save', action='store_true', help='Save results')
    parser.add_argument('--quick', action='store_true', help='Quick scan (skip large folders)')
    
    args = parser.parse_args()
    
    analyzer = DeepHiddenFolderAnalyzer()
    results = analyzer.analyze_all()
    
    if args.save:
        analyzer.save_results(results)
    else:
        # Quick summary
        print("\n📊 Quick Summary:")
        print(f"   Categories: {len(results['categories'])}")
        print(f"   Total size: {results['statistics']['total_size_mb']:.1f} MB")
        print(f"   Scripts found: {results['statistics']['total_scripts']}")
        print("\n   Run with --save to generate full report")


if __name__ == '__main__':
    main()

