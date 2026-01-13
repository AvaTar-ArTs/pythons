#!/usr/bin/env python3
"""
Smart Cleanup Script - Intelligent Content-Aware Organization
Uses intelligent analysis to organize and clean up files
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class SmartCleanup:
    """Intelligent file cleanup using content analysis"""

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path).expanduser()
        self.actions = []

    def analyze_directory(self) -> Dict:
        """Analyze all files in directory"""
        print(f"🔍 Analyzing {self.base_path}...")

        # Find all Python files
        py_files = list(self.base_path.glob('*.py'))
        print(f"Found {len(py_files)} Python files")

        # Categorize by intelligent rules
        categories = {
            'keep_main': [],
            'archive_old': [],
            'move_utilities': [],
            'move_experiments': [],
            'move_tests': []
        }

        for file in py_files:
            category = self._categorize_file(file)
            categories[category].append(file)

        return categories

    def _categorize_file(self, file: Path) -> str:
        """Intelligently categorize file"""
        filename = file.name.lower()

        # Keep the next-gen analyzer
        if filename == 'next_gen_content_analyzer.py':
            return 'keep_main'

        # Archive old analyzer versions
        if 'analyzer' in filename or 'analysis' in filename:
            if any(term in filename for term in ['advanced', 'enhanced', 'ultra', 'comprehensive', 'deep', 'intelligent']):
                return 'archive_old'

        # Utilities
        if any(term in filename for term in ['util', 'batch', 'zip', 'file_list']):
            return 'move_utilities'

        # Tests
        if filename.startswith('test_') or '_test' in filename:
            return 'move_tests'

        # Experiments and one-offs
        if any(term in filename for term in ['experiment', 'quick', 'simple', 'temp', 'try']):
            return 'move_experiments'

        # Generic analyzers go to archive
        if 'analyz' in filename:
            return 'archive_old'

        return 'keep_main'

    def analyze_docs(self) -> Dict:
        """Analyze documentation files"""
        print("\n📚 Analyzing documentation...")

        md_files = list(self.base_path.glob('*.md'))
        print(f"Found {len(md_files)} markdown files")

        categories = {
            'keep': [],
            'archive': [],
            'delete': []
        }

        for file in md_files:
            category = self._categorize_doc(file)
            categories[category].append(file)

        return categories

    def _categorize_doc(self, file: Path) -> str:
        """Categorize documentation file"""
        filename = file.name.lower()

        # Keep essential docs
        essential = [
            'readme.md',
            'next_gen_analyzer_readme.md',
            'transformation_summary.md',
            'quick_start.md',
            'vision.md'
        ]

        if filename in essential:
            return 'keep'

        # Archive potentially useful docs
        archive_patterns = [
            'comprehensive', 'final', 'content_based', 'documentation_summary',
            'code_browser', 'navigation', 'reorganization'
        ]

        if any(pattern in filename for pattern in archive_patterns):
            return 'archive'

        # Delete obsolete docs
        delete_patterns = [
            'analyze-1', 'duplicate-term', 'transcriber', 'yt-dlp',
            'v3.0-migration', 'readme.tr', '.seo_backup', 'old_readme',
            'issue_template', 'pull_request', 'privacy_policy',
            'sort-organize', 'python script for'
        ]

        if any(pattern in filename for pattern in delete_patterns):
            return 'delete'

        return 'archive'

    def generate_cleanup_plan(self, py_categories: Dict, doc_categories: Dict) -> List[Dict]:
        """Generate comprehensive cleanup plan"""
        plan = []
        timestamp = datetime.now().strftime('%Y%m%d')

        # Python files
        for file in py_categories['archive_old']:
            plan.append({
                'type': 'python',
                'action': 'archive',
                'file': file.name,
                'source': str(file),
                'destination': f'archive/code/{file.name}',
                'reason': 'Superseded by next-gen analyzer'
            })

        for file in py_categories['move_utilities']:
            plan.append({
                'type': 'python',
                'action': 'move',
                'file': file.name,
                'source': str(file),
                'destination': f'utilities/{file.name}',
                'reason': 'Standalone utility'
            })

        for file in py_categories['move_experiments']:
            plan.append({
                'type': 'python',
                'action': 'archive',
                'file': file.name,
                'source': str(file),
                'destination': f'archive/experiments/{file.name}',
                'reason': 'Experimental code'
            })

        # Documentation
        for file in doc_categories['archive']:
            plan.append({
                'type': 'documentation',
                'action': 'archive',
                'file': file.name,
                'source': str(file),
                'destination': f'archive/docs/{file.name}',
                'reason': 'Historical reference'
            })

        for file in doc_categories['delete']:
            plan.append({
                'type': 'documentation',
                'action': 'backup_delete',
                'file': file.name,
                'source': str(file),
                'destination': f'archive/backups/{timestamp}/{file.name}',
                'reason': 'Obsolete content'
            })

        return plan

    def execute_plan(self, plan: List[Dict], dry_run: bool = True):
        """Execute cleanup plan"""
        print(f"\n{'🔍 DRY RUN MODE' if dry_run else '✅ EXECUTING CLEANUP'}")
        print("=" * 70)

        # Group by action type
        actions_by_type = {}
        for action in plan:
            action_type = action['action']
            if action_type not in actions_by_type:
                actions_by_type[action_type] = []
            actions_by_type[action_type].append(action)

        # Summary
        print("\n📊 Summary:")
        for action_type, items in actions_by_type.items():
            print(f"  {action_type}: {len(items)} files")

        print("\n📋 Detailed Plan:\n")

        # Execute each action
        for i, action in enumerate(plan, 1):
            action_verb = action['action'].upper()
            file = action['file']
            dest = action['destination']
            reason = action['reason']

            print(f"{i}. {action_verb}: {file}")
            print(f"   → {dest}")
            print(f"   Reason: {reason}")

            if not dry_run:
                try:
                    # Create destination directory
                    dest_path = self.base_path / dest
                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    # Perform action
                    src = Path(action['source'])

                    if action['action'] in ['archive', 'move']:
                        shutil.move(str(src), str(dest_path))
                        print("   ✅ Moved successfully")
                    elif action['action'] == 'backup_delete':
                        shutil.copy2(str(src), str(dest_path))
                        src.unlink()
                        print("   ✅ Backed up and deleted")

                except Exception as e:
                    print(f"   ❌ Error: {e}")

            print()

        # Save plan
        plan_file = self.base_path / f'cleanup_plan_{datetime.now():%Y%m%d_%H%M%S}.json'
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2, default=str)
        print(f"📄 Plan saved to: {plan_file.name}\n")

    def run(self, dry_run: bool = True):
        """Run the complete cleanup process"""
        print("=" * 70)
        print("🧠 SMART CLEANUP - Intelligent Content-Aware Organization")
        print("=" * 70)
        print()

        # Analyze Python files
        py_categories = self.analyze_directory()

        # Show Python summary
        print("\n📊 Python Files Analysis:")
        for category, files in py_categories.items():
            if files:
                print(f"  {category}: {len(files)} files")
                for file in files[:3]:  # Show first 3
                    print(f"    - {file.name}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")

        # Analyze documentation
        doc_categories = self.analyze_docs()

        # Show docs summary
        print("\n📚 Documentation Analysis:")
        for category, files in doc_categories.items():
            if files:
                print(f"  {category}: {len(files)} files")
                for file in files[:3]:
                    print(f"    - {file.name}")
                if len(files) > 3:
                    print(f"    ... and {len(files) - 3} more")

        # Generate plan
        plan = self.generate_cleanup_plan(py_categories, doc_categories)

        # Execute
        self.execute_plan(plan, dry_run=dry_run)

        # Final message
        print("=" * 70)
        if dry_run:
            print("✅ Dry run complete!")
            print("\nReview the plan above. To execute:")
            print("  python3 smart_cleanup.py --execute")
        else:
            print("✅ Cleanup complete!")
            print("\nYour python directory is now organized!")
            print("\nNext steps:")
            print("  1. Review the changes: ls -la")
            print("  2. Update README.md with new structure")
            print("  3. Test the next-gen analyzer")
        print("=" * 70)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Smart cleanup using intelligent content analysis'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='~/Documents/python',
        help='Directory to clean up (default: ~/Documents/python)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Execute the plan (default is dry-run)'
    )

    args = parser.parse_args()

    # Create and run cleanup
    cleanup = SmartCleanup(args.directory)
    cleanup.run(dry_run=not args.execute)

if __name__ == '__main__':
    main()
