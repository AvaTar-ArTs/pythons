#!/usr/bin/env python3
"""
Hidden Folders Scanner
Scans for hidden folders with scripts and generates actionable report
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any

class HiddenFolderScanner:
    """Scan hidden folders for scripts and tools"""
    
    def __init__(self, home_dir: Path = None):
        self.home = home_dir or Path.home()
        self.results_dir = self.home / 'intelligence' / 'scans'
        self.results_dir.mkdir(exist_ok=True)
        
        # Categories
        self.categories = {
            'user_scripts': [],
            'system_scripts': [],
            'config': [],
            'cache': [],
            'history': [],
            'package_managers': [],
        }
        
        # Known patterns
        self.system_patterns = [
            '.cursor', '.n8n', '.jupyter', '.oh-my-zsh', '.config',
            '.chatgpt', '.claude', '.grok', '.gemini'
        ]
        
        self.cache_patterns = [
            '.cache', '.pytest_cache', '.spicetify', '.local'
        ]
        
        self.package_patterns = [
            '.x-cmd.root', '.bun', '.apify', 'node_modules'
        ]
    
    def scan_folder(self, folder_path: Path) -> Dict[str, Any]:
        """Scan a single hidden folder"""
        if not folder_path.exists() or not folder_path.is_dir():
            return None
        
        folder_name = folder_path.name
        result = {
            'path': str(folder_path),
            'name': folder_name,
            'scripts': [],
            'config_files': [],
            'cache_files': [],
            'type': 'unknown',
            'script_count': 0,
        }
        
        # Find scripts
        for ext in ['.py', '.sh', '.js', '.ts']:
            scripts = list(folder_path.rglob(f'*{ext}'))
            result['scripts'].extend([str(s.relative_to(folder_path)) for s in scripts])
            result['script_count'] += len(scripts)
        
        # Categorize
        if any(pattern in folder_name for pattern in self.system_patterns):
            result['type'] = 'system'
        elif any(pattern in folder_name for pattern in self.cache_patterns):
            result['type'] = 'cache'
        elif any(pattern in folder_name for pattern in self.package_patterns):
            result['type'] = 'package_manager'
        elif 'history' in folder_name.lower():
            result['type'] = 'history'
        elif result['script_count'] > 0:
            result['type'] = 'user_scripts'
        else:
            result['type'] = 'config'
        
        return result
    
    def scan_all(self) -> Dict[str, Any]:
        """Scan all hidden folders"""
        print("🔍 Scanning hidden folders...\n")
        
        hidden_folders = []
        for item in self.home.iterdir():
            if item.name.startswith('.') and item.is_dir():
                # Skip known large folders
                if item.name in ['.x-cmd.root', '.cursor', '.git']:
                    continue
                
                result = self.scan_folder(item)
                if result:
                    hidden_folders.append(result)
        
        # Also check Documents/.intelligence
        docs_intel = self.home / 'Documents' / '.intelligence'
        if docs_intel.exists():
            result = self.scan_folder(docs_intel)
            if result:
                hidden_folders.append(result)
        
        # Categorize results
        categorized = defaultdict(list)
        for folder in hidden_folders:
            categorized[folder['type']].append(folder)
        
        return {
            'scan_date': datetime.now().isoformat(),
            'total_folders': len(hidden_folders),
            'categories': dict(categorized),
            'folders': hidden_folders
        }
    
    def generate_report(self, scan_results: Dict[str, Any]) -> str:
        """Generate human-readable report"""
        report = []
        report.append("# Hidden Folders Scan Report")
        report.append(f"**Generated:** {scan_results['scan_date']}\n")
        report.append(f"**Total Folders Scanned:** {scan_results['total_folders']}\n")
        
        # By category
        report.append("## By Category\n")
        for cat, folders in scan_results['categories'].items():
            report.append(f"### {cat.replace('_', ' ').title()}: {len(folders)}")
            for folder in folders[:5]:  # Show first 5
                report.append(f"- `{folder['name']}` - {folder['script_count']} scripts")
            if len(folders) > 5:
                report.append(f"  ... and {len(folders) - 5} more")
            report.append("")
        
        # Scripts found
        report.append("## Folders with Scripts\n")
        script_folders = [f for f in scan_results['folders'] if f['script_count'] > 0]
        script_folders.sort(key=lambda x: x['script_count'], reverse=True)
        
        for folder in script_folders[:10]:
            report.append(f"### {folder['name']}")
            report.append(f"- **Path:** `{folder['path']}`")
            report.append(f"- **Scripts:** {folder['script_count']}")
            report.append(f"- **Type:** {folder['type']}")
            if folder['scripts'][:3]:
                report.append(f"- **Sample:** {', '.join(folder['scripts'][:3])}")
            report.append("")
        
        return "\n".join(report)
    
    def save_results(self, scan_results: Dict[str, Any]):
        """Save scan results"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save JSON
        json_file = self.results_dir / f'scan_{timestamp}.json'
        json_file.write_text(json.dumps(scan_results, indent=2))
        
        # Save report
        report_file = self.results_dir / f'scan_{timestamp}.md'
        report = self.generate_report(scan_results)
        report_file.write_text(report)
        
        print(f"✅ Results saved:")
        print(f"   JSON: {json_file}")
        print(f"   Report: {report_file}")
        
        return json_file, report_file


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Scan hidden folders')
    parser.add_argument('--save', action='store_true', help='Save results to file')
    parser.add_argument('--report', action='store_true', help='Generate report')
    
    args = parser.parse_args()
    
    scanner = HiddenFolderScanner()
    results = scanner.scan_all()
    
    if args.save or args.report:
        scanner.save_results(results)
    else:
        # Quick summary
        print(f"📊 Found {results['total_folders']} hidden folders")
        for cat, folders in results['categories'].items():
            if folders:
                print(f"   {cat}: {len(folders)} folders")
        
        script_folders = [f for f in results['folders'] if f['script_count'] > 0]
        if script_folders:
            print(f"\n📜 Folders with scripts: {len(script_folders)}")
            for folder in sorted(script_folders, key=lambda x: x['script_count'], reverse=True)[:5]:
                print(f"   {folder['name']}: {folder['script_count']} scripts")


if __name__ == '__main__':
    main()

