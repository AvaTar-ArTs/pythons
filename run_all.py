#!/usr/bin/env python3
"""
Master Script Runner - Execute All Analysis and Organization Tasks

This script provides a unified interface to run all analysis, merge, and
organization scripts in the proper order. It supports:
- Running all analyses
- Running specific categories
- Exporting results
- Generating consolidated reports

Usage:
    python scripts/run_all.py                    # Run everything
    python scripts/run_all.py --category analysis
    python scripts/run_all.py --category merge
    python scripts/run_all.py --category organize
    python scripts/run_all.py --export            # Export all results
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import subprocess
import json

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

# Script categories and their execution order
SCRIPT_CATEGORIES = {
    'analysis': [
        {
            'name': 'Analysis Launcher',
            'script': 'analysis/analysis_launcher.sh',
            'description': 'Launch analysis scripts with options',
            'args': [],
        },
        {
            'name': 'Ultra Deep Analysis',
            'script': 'analysis/RUN_ULTRA_DEEP_ANALYSIS.sh',
            'description': 'Run ultra deep intelligence analysis',
            'args': [],
        },
        {
            'name': 'Local Dirs Analysis',
            'script': 'analysis/analyze_local_dirs.sh',
            'description': 'Analyze local directories',
            'args': [],
        },
    ],
    'merge': [
        {
            'name': 'Merge Diff',
            'script': 'merge/merge_diff.sh',
            'description': 'Merge differences between files',
            'args': [],
        },
        {
            'name': 'Merge Similar Markdown',
            'script': 'merge/merge_similar_markdown.sh',
            'description': 'Merge similar markdown files',
            'args': [],
        },
        {
            'name': 'Consolidate Images',
            'script': 'merge/consolidate_images.sh',
            'description': 'Consolidate image files',
            'args': [],
        },
    ],
    'organize': [
        {
            'name': 'Rename Files',
            'script': 'organize/rename_files.sh',
            'description': 'Rename files according to plan',
            'args': [],
        },
        {
            'name': 'Sort Files',
            'script': 'organize/sortD.sh',
            'description': 'Sort directory files',
            'args': [],
        },
        {
            'name': 'Content Separation',
            'script': 'organize/content_separation.py',
            'description': 'Proper content-aware file separation',
            'args': [],
        },
    ],
}


class ScriptRunner:
    """Manages execution of analysis and organization scripts."""
    
    def __init__(self, scripts_dir: Path):
        self.scripts_dir = scripts_dir
        self.results = []
        self.errors = []
    
    def run_script(self, script_info: Dict) -> Dict:
        """
        Run a single script and capture results.
        
        Args:
            script_info: Dictionary containing script information
            
        Returns:
            Dictionary with execution results
        """
        script_path = self.scripts_dir / script_info['script']
        
        if not script_path.exists():
            error_msg = f"Script not found: {script_path}"
            print(f"⚠️  {error_msg}")
            self.errors.append({
                'script': script_info['name'],
                'error': error_msg,
            })
            return {
                'script': script_info['name'],
                'status': 'not_found',
                'error': error_msg,
            }
        
        print(f"\n{'='*80}")
        print(f"▶️  Running: {script_info['name']}")
        print(f"   {script_info['description']}")
        print(f"{'='*80}\n")
        
        start_time = datetime.now()
        
        try:
            # Build command based on file extension
            if script_path.suffix == '.py':
                cmd = ['python3', str(script_path)] + script_info.get('args', [])
            elif script_path.suffix == '.sh':
                cmd = ['bash', str(script_path)] + script_info.get('args', [])
            else:
                cmd = [str(script_path)] + script_info.get('args', [])
            
            # Run script
            result = subprocess.run(
                cmd,
                cwd=self.scripts_dir.parent,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            
            status = 'success' if result.returncode == 0 else 'failed'
            
            result_info = {
                'script': script_info['name'],
                'status': status,
                'duration_seconds': duration,
                'returncode': result.returncode,
            }
            
            if status == 'success':
                print(f"✅ Completed: {script_info['name']} ({duration:.1f}s)")
            else:
                print(f"❌ Failed: {script_info['name']} (exit code: {result.returncode})")
                self.errors.append({
                    'script': script_info['name'],
                    'error': f"Exit code: {result.returncode}",
                })
            
            self.results.append(result_info)
            return result_info
            
        except subprocess.TimeoutExpired:
            error_msg = "Script execution timed out"
            print(f"⏱️  Timeout: {script_info['name']}")
            self.errors.append({
                'script': script_info['name'],
                'error': error_msg,
            })
            return {
                'script': script_info['name'],
                'status': 'timeout',
                'error': error_msg,
            }
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error running {script_info['name']}: {error_msg}")
            self.errors.append({
                'script': script_info['name'],
                'error': error_msg,
            })
            return {
                'script': script_info['name'],
                'status': 'error',
                'error': error_msg,
            }
    
    def run_category(self, category: str) -> Dict:
        """
        Run all scripts in a specific category.
        
        Args:
            category: Category name to run
            
        Returns:
            Summary dictionary
        """
        if category not in SCRIPT_CATEGORIES:
            print(f"❌ Unknown category: {category}")
            print(f"   Available categories: {', '.join(SCRIPT_CATEGORIES.keys())}")
            return {}
        
        scripts = SCRIPT_CATEGORIES[category]
        print(f"\n{'='*80}")
        print(f"🚀 Running {category.upper()} Category")
        print(f"   {len(scripts)} script(s) to execute")
        print(f"{'='*80}\n")
        
        for script_info in scripts:
            self.run_script(script_info)
        
        return self.generate_summary()
    
    def run_all(self) -> Dict:
        """
        Run all scripts in all categories.
        
        Returns:
            Summary dictionary
        """
        print(f"\n{'='*80}")
        print("🚀 RUNNING ALL ANALYSES AND ORGANIZATION TASKS")
        print(f"{'='*80}\n")
        
        # Run in order: analysis -> merge -> organize
        for category in ['analysis', 'merge', 'organize']:
            self.run_category(category)
        
        return self.generate_summary()
    
    def generate_summary(self) -> Dict:
        """
        Generate execution summary.
        
        Returns:
            Summary dictionary
        """
        total = len(self.results)
        successful = sum(1 for r in self.results if r['status'] == 'success')
        failed = total - successful
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_scripts': total,
            'successful': successful,
            'failed': failed,
            'errors': self.errors,
            'results': self.results,
        }
        
        return summary
    
    def print_summary(self, summary: Dict):
        """Print execution summary to console."""
        print(f"\n{'='*80}")
        print("📊 EXECUTION SUMMARY")
        print(f"{'='*80}\n")
        
        print(f"Total scripts: {summary['total_scripts']}")
        print(f"✅ Successful: {summary['successful']}")
        print(f"❌ Failed: {summary['failed']}")
        
        if summary['errors']:
            print(f"\n⚠️  Errors encountered:")
            for error in summary['errors']:
                print(f"   • {error['script']}: {error['error']}")
        
        if summary['results']:
            print(f"\n⏱️  Execution times:")
            for result in summary['results']:
                if 'duration_seconds' in result:
                    print(f"   • {result['script']}: {result['duration_seconds']:.1f}s")
        
        print(f"\n{'='*80}\n")
    
    def export_summary(self, summary: Dict, output_path: Optional[Path] = None):
        """
        Export summary to JSON file.
        
        Args:
            summary: Summary dictionary
            output_path: Optional output file path
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = Path.home() / f'scripts_execution_summary_{timestamp}.json'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Summary exported to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run all analysis and organization scripts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_all.py                    # Run everything
  python scripts/run_all.py --category analysis
  python scripts/run_all.py --category merge --export
  python scripts/run_all.py --list            # List all available scripts
        """
    )
    
    parser.add_argument(
        '--category',
        choices=['analysis', 'merge', 'organize'],
        help='Run scripts from specific category only'
    )
    
    parser.add_argument(
        '--export',
        action='store_true',
        help='Export execution summary to JSON'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available scripts and exit'
    )
    
    args = parser.parse_args()
    
    scripts_dir = Path(__file__).parent
    
    if args.list:
        print("\n📋 Available Scripts:\n")
        for category, scripts in SCRIPT_CATEGORIES.items():
            print(f"  {category.upper()}:")
            for script in scripts:
                print(f"    • {script['name']}")
                print(f"      {script['description']}")
            print()
        return
    
    runner = ScriptRunner(scripts_dir)
    
    if args.category:
        summary = runner.run_category(args.category)
    else:
        summary = runner.run_all()
    
    runner.print_summary(summary)
    
    if args.export:
        runner.export_summary(summary)


if __name__ == '__main__':
    main()
