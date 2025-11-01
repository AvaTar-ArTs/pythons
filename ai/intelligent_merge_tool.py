
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_033 = 033
CONSTANT_256 = 256
CONSTANT_65536 = 65536

#!/usr/bin/env python3
"""
🔀 INTELLIGENT MERGE TOOL
=========================
AI-Powered Deep Analysis and Smart Merging System

Features:
✨ Deep file analysis and comparison
✨ Intelligent diff generation
✨ Conflict detection and resolution
✨ Smart merge decisions with AI reasoning
✨ Safe backup before merge
✨ Detailed merge report
"""

import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Color codes
class Colors:
    HEADER = '\CONSTANT_033[95m'
    BLUE = '\CONSTANT_033[94m'
    CYAN = '\CONSTANT_033[96m'
    GREEN = '\CONSTANT_033[92m'
    YELLOW = '\CONSTANT_033[93m'
    RED = '\CONSTANT_033[91m'
    MAGENTA = '\CONSTANT_033[35m'
    END = '\CONSTANT_033[0m'
    BOLD = '\CONSTANT_033[1m'

# Emojis
class Emojis:
    MERGE = "🔀"
    BRAIN = "🧠"
    DIFF = "📊"
    CHECK = "✅"
    WARNING = "⚠️"
    FIRE = "🔥"
    FOLDER = "📁"
    FILE = "📄"
    ROCKET = "🚀"
    SPARKLES = "✨"
    SHIELD = "🛡️"
    MICROSCOPE = "🔬"
    CHART = "📈"


class IntelligentMergeTool:
    """AI-Powered Intelligent Merge System"""

    def __init__(self, target_dir: str, source_dirs: List[str],
                 dry_run: bool = True, interactive: bool = True):
        self.target_dir = Path(target_dir)
        self.source_dirs = [Path(d) for d in source_dirs]
        self.dry_run = dry_run
        self.interactive = interactive

        # Create backup directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.target_dir / f"merge_backup_{timestamp}"
        self.merge_report_dir = self.target_dir / f"merge_analysis_{timestamp}"

        self.stats = {
            'files_analyzed': 0,
            'conflicts_found': 0,
            'files_merged': 0,
            'files_skipped': 0,
            'identical_files': 0,
            'new_files': 0,
            'updated_files': 0
        }

        self.merge_log = []
        self.conflict_log = []

    def print_header(self, text: str, color=Colors.CYAN, emoji=""):
        """Print fancy headers"""
        logger.info(f"\n{color}{Colors.BOLD}{'='*80}")
        logger.info(f"{emoji} {text}")
        logger.info(f"{'='*80}{Colors.END}\n")

    def calculate_hash(self, filepath: Path) -> str:
        """Calculate SHA-CONSTANT_256 hash"""
        try:
            hasher = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(CONSTANT_65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def analyze_python_file(self, filepath: Path) -> Dict[str, Any]:
        """Deep analyze Python file"""
        import ast

        analysis = {
            'path': str(filepath),
            'size': 0,
            'lines': 0,
            'functions': [],
            'classes': [],
            'imports': [],
            'docstring': None,
            'has_main': False,
            'is_valid_python': False,
            'last_modified': None
        }

        try:
            analysis['size'] = filepath.stat().st_size
            analysis['last_modified'] = filepath.stat().st_mtime

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                analysis['lines'] = len(content.splitlines())

            # AST Analysis
            tree = ast.parse(content)
            analysis['is_valid_python'] = True
            analysis['docstring'] = ast.get_docstring(tree)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['functions'].append(node.name)
                    if node.name == 'main':
                        analysis['has_main'] = True
                elif isinstance(node, ast.ClassDef):
                    analysis['classes'].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis['imports'].append(node.module)

        except Exception as e:
            analysis['error'] = str(e)

        return analysis

    def generate_detailed_diff(self, file1: Path, file2: Path) -> Tuple[List[str], Dict[str, int]]:
        """Generate detailed diff with statistics"""
        try:
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f:
                lines1 = f.readlines()
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f:
                lines2 = f.readlines()

            # Generate unified diff
            diff = list(difflib.unified_diff(
                lines1, lines2,
                fromfile=str(file1),
                tofile=str(file2),
                lineterm=''
            ))

            # Calculate diff statistics
            stats = {
                'additions': sum(1 for line in diff if line.startswith('+')),
                'deletions': sum(1 for line in diff if line.startswith('-')),
                'total_changes': len([l for l in diff if l.startswith(('+', '-'))]),
                'diff_lines': len(diff)
            }

            return diff, stats

        except Exception as e:
            return [f"ERROR: {e}"], {'error': str(e)}

    def compare_files(self, source_file: Path, target_file: Path) -> Dict[str, Any]:
        """Deep comparison of two files"""

        comparison = {
            'source': str(source_file),
            'target': str(target_file),
            'identical': False,
            'conflict': False,
            'recommendation': 'unknown',
            'reason': '',
            'source_analysis': {},
            'target_analysis': {},
            'diff_stats': {},
            'diff_preview': []
        }

        # Check if files are identical
        source_hash = self.calculate_hash(source_file)
        target_hash = self.calculate_hash(target_file)

        if source_hash == target_hash:
            comparison['identical'] = True
            comparison['recommendation'] = 'skip'
            comparison['reason'] = 'Files are identical - no merge needed'
            self.stats['identical_files'] += 1
            return comparison

        # Analyze both files
        if source_file.suffix == '.py':
            comparison['source_analysis'] = self.analyze_python_file(source_file)
            comparison['target_analysis'] = self.analyze_python_file(target_file)

        # Generate diff
        diff, diff_stats = self.generate_detailed_diff(target_file, source_file)
        comparison['diff_stats'] = diff_stats
        comparison['diff_preview'] = diff[:50]  # First 50 lines

        # Intelligent decision making
        source_newer = source_file.stat().st_mtime > target_file.stat().st_mtime
        source_larger = source_file.stat().st_size > target_file.stat().st_size

        # Check if it's a conflict (both modified significantly)
        if diff_stats.get('total_changes', 0) > 10:
            comparison['conflict'] = True
            self.stats['conflicts_found'] += 1

            # Make recommendation based on analysis
            if source_newer and source_larger:
                comparison['recommendation'] = 'replace'
                comparison['reason'] = 'Source is newer and larger - likely more complete'
            elif source_newer:
                comparison['recommendation'] = 'replace'
                comparison['reason'] = 'Source is newer'
            elif comparison.get('source_analysis', {}).get('functions', []) > \
                 comparison.get('target_analysis', {}).get('functions', []):
                comparison['recommendation'] = 'replace'
                comparison['reason'] = 'Source has more functionality'
            else:
                comparison['recommendation'] = 'manual'
                comparison['reason'] = 'Significant differences - manual review recommended'
        else:
            # Minor differences
            if source_newer:
                comparison['recommendation'] = 'replace'
                comparison['reason'] = 'Source is newer with minor changes'
            else:
                comparison['recommendation'] = 'keep'
                comparison['reason'] = 'Target is newer'

        return comparison

    def scan_and_compare(self) -> Dict[str, Any]:
        """Scan source directories and compare with target - PARENT FOLDER AWARE"""

        self.print_header("SCANNING AND ANALYZING FILES (PARENT-FOLDER AWARE)", Colors.CYAN, Emojis.MICROSCOPE)

        file_map = {}  # relative_path -> {source_files: [], target_file: path, parent_dirs: set}

        # Scan target directory
        logger.info(f"{Colors.CYAN}{Emojis.FOLDER} Scanning target: {self.target_dir}{Colors.END}")
        target_files = {}
        target_dirs = set()

        for root, dirs, files in os.walk(self.target_dir):
            # Skip backup and analysis directories
            dirs[:] = [d for d in dirs if not d.startswith(('merge_backup_', 'merge_analysis_',
                                                           'dedup_backup', 'ai_diff_reports_',
                                                           '.git', '.', '__pycache__', 'node_modules'))]

            # Track parent directories
            if root != str(self.target_dir):
                rel_dir = Path(root).relative_to(self.target_dir)
                target_dirs.add(str(rel_dir))
                # Add all parent dirs
                for parent in rel_dir.parents:
                    if parent != Path('.'):
                        target_dirs.add(str(parent))

            for filename in files:
                if filename.startswith('.') or filename.endswith(('.pyc', '.pyo')):
                    continue

                filepath = Path(root) / filename
                rel_path = filepath.relative_to(self.target_dir)
                target_files[str(rel_path)] = {
                    'path': filepath,
                    'parent_dir': str(rel_path.parent) if rel_path.parent != Path('.') else '',
                    'depth': len(rel_path.parts) - 1
                }

        logger.info(f"{Colors.GREEN}  Found {len(target_files)} files in target{Colors.END}")
        logger.info(f"{Colors.GREEN}  Found {len(target_dirs)} directories in target{Colors.END}")

        # Scan source directories with parent awareness
        for source_idx, source_dir in enumerate(self.source_dirs, 1):
            source_name = source_dir.name
            logger.info(f"\n{Colors.CYAN}{Emojis.FOLDER} Scanning source [{source_idx}/{len(self.source_dirs)}]: {source_dir}{Colors.END}")
            logger.info(f"{Colors.YELLOW}  Source parent: {source_name}{Colors.END}")

            source_count = 0
            source_dirs_found = set()

            for root, dirs, files in os.walk(source_dir):
                dirs[:] = [d for d in dirs if not d.startswith(('.git', '.', '__pycache__', 'node_modules'))]

                # Track parent directories in source
                if root != str(source_dir):
                    rel_dir = Path(root).relative_to(source_dir)
                    source_dirs_found.add(str(rel_dir))

                for filename in files:
                    if filename.startswith('.') or filename.endswith(('.pyc', '.pyo')):
                        continue

                    filepath = Path(root) / filename
                    rel_path = filepath.relative_to(source_dir)
                    rel_path_str = str(rel_path)

                    # Get parent directory info
                    parent_dir = str(rel_path.parent) if rel_path.parent != Path('.') else ''
                    depth = len(rel_path.parts) - 1

                    if rel_path_str not in file_map:
                        file_map[rel_path_str] = {
                            'source_files': [],
                            'target_file': target_files.get(rel_path_str),
                            'parent_dirs': set(),
                            'relative_path': rel_path_str,
                            'filename': filename,
                            'parent_dir': parent_dir,
                            'depth': depth
                        }

                    file_map[rel_path_str]['source_files'].append({
                        'path': filepath,
                        'source_dir': source_dir,
                        'source_name': source_name,
                        'parent_dir': parent_dir,
                        'depth': depth,
                        'abs_path': str(filepath.absolute())
                    })

                    # Track which parent directories this file comes from
                    file_map[rel_path_str]['parent_dirs'].add(source_name)

                    source_count += 1

            logger.info(f"{Colors.GREEN}  Found {source_count} files in {source_name}{Colors.END}")
            logger.info(f"{Colors.GREEN}  Found {len(source_dirs_found)} subdirectories{Colors.END}")

        # Display parent folder summary
        logger.info(f"\n{Colors.BOLD}{Colors.MAGENTA}PARENT FOLDER SUMMARY:{Colors.END}")
        parent_sources = defaultdict(int)
        for info in file_map.values():
            for source in info['parent_dirs']:
                parent_sources[source] += 1

        for source, count in parent_sources.items():
            logger.info(f"  {Colors.CYAN}{source}:{Colors.END} {count} files")

        return file_map

    def analyze_and_merge(self, file_map: Dict) -> None:
        """Analyze files and perform intelligent merge - PARENT FOLDER AWARE"""

        self.print_header("DEEP ANALYSIS AND COMPARISON (PARENT-AWARE)", Colors.YELLOW, Emojis.BRAIN)

        # Create directories
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.merge_report_dir.mkdir(parents=True, exist_ok=True)

        merge_plan = []

        # Sort by depth (shallow files first, then deeper nested files)
        sorted_files = sorted(file_map.items(), key=lambda x: x[1]['depth'])

        for rel_path, info in sorted_files:
            source_files = info['source_files']
            target_file_info = info['target_file']
            parent_dir = info['parent_dir']

            # Skip if no source files
            if not source_files:
                continue

            self.stats['files_analyzed'] += 1

            # Choose best source file (from highest priority directory)
            best_source_info = None
            for source_dir in self.source_dirs:
                for sf in source_files:
                    if sf['source_dir'] == source_dir:
                        best_source_info = sf
                        break
                if best_source_info:
                    break

            if not best_source_info:
                best_source_info = source_files[0]

            best_source = best_source_info['path']
            source_parent = best_source_info['source_name']

            # Build target path with parent awareness
            target_path = self.target_dir / rel_path

            # Case 1: New file (doesn't exist in target)
            if not target_file_info:
                merge_plan.append({
                    'action': 'add',
                    'source': best_source,
                    'target': target_path,
                    'rel_path': rel_path,
                    'parent_dir': parent_dir,
                    'source_parent': source_parent,
                    'reason': f'New file from {source_parent}',
                    'conflict': False,
                    'depth': info['depth']
                })
                self.stats['new_files'] += 1
                continue

            # Case 2: File exists - compare
            target_file = target_file_info['path']
            comparison = self.compare_files(best_source, target_file)

            if comparison['identical']:
                # Skip identical files
                continue

            # Save diff report for conflicts
            if comparison['conflict']:
                diff_file = self.merge_report_dir / f"{rel_path.replace('/', '_')}_diff.txt"
                diff_file.parent.mkdir(parents=True, exist_ok=True)

                with open(diff_file, 'w', encoding='utf-8') as f:
                    f.write(f"DIFF ANALYSIS: {rel_path}\n")
                    f.write(f"="*80 + Path("\n\n"))
                    f.write(f"Source: {best_source}\n")
                    f.write(f"Target: {target_file}\n\n")
                    f.write(f"Recommendation: {comparison['recommendation']}\n")
                    f.write(f"Reason: {comparison['reason']}\n\n")
                    f.write(f"Diff Stats:\n")
                    for key, val in comparison['diff_stats'].items():
                        f.write(f"  {key}: {val}\n")
                    f.write(f"\n{'='*80}\n\n")
                    f.write('\n'.join(comparison['diff_preview']))

                comparison['diff_file'] = str(diff_file)

            merge_plan.append({
                'action': comparison['recommendation'],
                'source': best_source,
                'target': target_file,
                'rel_path': rel_path,
                'parent_dir': parent_dir,
                'source_parent': source_parent,
                'target_parent': target_file_info.get('parent_dir', ''),
                'reason': comparison['reason'],
                'conflict': comparison['conflict'],
                'diff_file': comparison.get('diff_file'),
                'comparison': comparison,
                'depth': info['depth']
            })

            if comparison['recommendation'] in ['replace', 'add']:
                self.stats['updated_files'] += 1

        # Execute merge plan (sorted by depth to ensure parent dirs exist)
        self.execute_merge_plan(merge_plan)

    def execute_merge_plan(self, merge_plan: List[Dict]) -> None:
        """Execute the merge plan - PARENT FOLDER AWARE"""

        self.print_header("EXECUTING MERGE PLAN (PRESERVING DIRECTORY STRUCTURE)", Colors.GREEN, Emojis.MERGE)

        logger.info(f"{Colors.YELLOW}Total actions: {len(merge_plan)}{Colors.END}")
        logger.info(f"{Colors.CYAN}Mode: {'DRY RUN' if self.dry_run else 'LIVE MERGE'}{Colors.END}\n")

        # Sort by depth to ensure parent directories are created first
        merge_plan.sort(key=lambda x: x.get('depth', 0))

        for idx, action in enumerate(merge_plan, 1):
            action_type = action['action']
            rel_path = action['rel_path']
            parent_dir = action.get('parent_dir', '')
            source_parent = action.get('source_parent', 'unknown')

            # Show action with parent info
            logger.info(f"\n{Colors.BOLD}[{idx}/{len(merge_plan)}] {rel_path}{Colors.END}")
            if parent_dir:
                logger.info(f"Parent: {Colors.CYAN}{parent_dir}/{Colors.END}")
            logger.info(f"Source: {Colors.MAGENTA}{source_parent}{Colors.END}")
            logger.info(f"Action: {Colors.YELLOW}{action_type.upper()}{Colors.END}")
            logger.info(f"Reason: {action['reason']}")

            if action['conflict']:
                logger.info(f"{Colors.RED}{Emojis.WARNING} CONFLICT DETECTED{Colors.END}")
                if action.get('diff_file'):
                    logger.info(f"Diff: {Colors.BLUE}{action['diff_file']}{Colors.END}")

            # Interactive mode - ask for confirmation
            if self.interactive and action['conflict']:
                logger.info(f"\n{Colors.CYAN}Options:{Colors.END}")
                logger.info("  [y] Yes, proceed with recommended action")
                logger.info("  [n] No, skip this file")
                logger.info("  [v] View diff")
                logger.info("  [k] Keep target (don't merge)")
                logger.info("  [q] Quit")

                choice = input(f"\n{Colors.BOLD}Choice: {Colors.END}").lower().strip()

                if choice == 'q':
                    logger.info(f"{Colors.YELLOW}Merge aborted by user{Colors.END}")
                    return
                elif choice == 'n' or choice == 'k':
                    logger.info(f"{Colors.YELLOW}Skipped{Colors.END}")
                    self.stats['files_skipped'] += 1
                    continue
                elif choice == 'v':
                    if action.get('diff_file'):
                        subprocess.run(['cat', action['diff_file']])
                    logger.info(f"\n{Colors.CYAN}Proceed? [y/n]{Colors.END}")
                    if input().lower() != 'y':
                        self.stats['files_skipped'] += 1
                        continue

            # Perform action
            if action_type == 'skip':
                continue
            elif action_type == 'manual':
                logger.info(f"{Colors.YELLOW}⚠️  Marked for manual review{Colors.END}")
                self.conflict_log.append(action)
                continue

            # Execute merge with parent directory preservation
            try:
                source = action['source']
                target = action['target']

                # Ensure parent directory structure exists
                if not self.dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    logger.info(f"{Colors.CYAN}  → Ensuring parent dir: {target.parent.relative_to(self.target_dir)}{Colors.END}")

                # Backup existing file
                if target.exists() and not self.dry_run:
                    backup_path = self.backup_dir / action['rel_path']
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, backup_path)
                    logger.info(f"{Colors.BLUE}  → Backed up to: {backup_path.relative_to(self.backup_dir)}{Colors.END}")

                # Copy/Update file
                if not self.dry_run:
                    shutil.copy2(source, target)
                    # Preserve parent directory metadata
                    logger.info(f"{Colors.GREEN}{Emojis.CHECK} Merged successfully → {target.relative_to(self.target_dir)}{Colors.END}")
                else:
                    logger.info(f"{Colors.YELLOW}[DRY RUN] Would create: {target.relative_to(self.target_dir)}{Colors.END}")
                    if action.get('parent_dir'):
                        logger.info(f"{Colors.YELLOW}[DRY RUN] Parent structure: {action['parent_dir']}/{Colors.END}")

                self.stats['files_merged'] += 1
                self.merge_log.append(action)

            except Exception as e:
                logger.info(f"{Colors.RED}{Emojis.WARNING} Error: {e}{Colors.END}")
                logger.info(f"{Colors.RED}  Source: {source}{Colors.END}")
                logger.info(f"{Colors.RED}  Target: {target}{Colors.END}")

    def generate_report(self) -> str:
        """Generate comprehensive merge report"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.target_dir / f"MERGE_REPORT_{timestamp}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🔀 INTELLIGENT MERGE REPORT\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE MERGE'}\n\n")
            f.write("---\n\n")

            # Statistics
            f.write("## 📊 MERGE STATISTICS\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| **Files Analyzed** | {self.stats['files_analyzed']:,} |\n")
            f.write(f"| **Files Merged** | {self.stats['files_merged']:,} |\n")
            f.write(f"| **New Files Added** | {self.stats['new_files']:,} |\n")
            f.write(f"| **Files Updated** | {self.stats['updated_files']:,} |\n")
            f.write(f"| **Identical Files Skipped** | {self.stats['identical_files']:,} |\n")
            f.write(f"| **Conflicts Detected** | {self.stats['conflicts_found']:,} |\n")
            f.write(f"| **Files Skipped** | {self.stats['files_skipped']:,} |\n")
            f.write(f"| **Backup Location** | `{self.backup_dir}` |\n")
            f.write(f"| **Diff Reports** | `{self.merge_report_dir}` |\n\n")

            # Merged files (grouped by parent directory)
            f.write("## ✅ MERGED FILES (Organized by Parent Directory)\n\n")

            # Group by parent directory
            by_parent = defaultdict(list)
            for action in self.merge_log:
                parent = action.get('parent_dir', '') or '(root)'
                by_parent[parent].append(action)

            for parent in sorted(by_parent.keys()):
                actions = by_parent[parent]
                f.write(f"### 📁 {parent}\n\n")
                f.write(f"**Files:** {len(actions)}\n\n")

                for action in actions:
                    f.write(f"#### {Path(action['rel_path']).name}\n")
                    f.write(f"- **Full Path:** `{action['rel_path']}`\n")
                    f.write(f"- **Action:** {action['action']}\n")
                    f.write(f"- **Source Parent:** `{action.get('source_parent', 'unknown')}`\n")
                    f.write(f"- **Source:** `{action['source']}`\n")
                    f.write(f"- **Reason:** {action['reason']}\n")
                    if action.get('diff_file'):
                        f.write(f"- **Diff Report:** `{action['diff_file']}`\n")
                    f.write(Path("\n"))

            # Conflicts requiring manual review
            if self.conflict_log:
                f.write("## ⚠️ CONFLICTS REQUIRING MANUAL REVIEW\n\n")
                for action in self.conflict_log:
                    f.write(f"### {action['rel_path']}\n")
                    f.write(f"- **Source:** `{action['source']}`\n")
                    f.write(f"- **Target:** `{action['target']}`\n")
                    f.write(f"- **Reason:** {action['reason']}\n")
                    if action.get('diff_file'):
                        f.write(f"- **Diff Report:** `{action['diff_file']}`\n")
                    f.write(Path("\n"))

            # Rollback instructions
            f.write("## 🔄 ROLLBACK INSTRUCTIONS\n\n")
            f.write("If you need to undo the merge:\n\n")
            f.write("```bash\n")
            f.write(f"# Restore from backup:\n")
            f.write(f"cp -R {self.backup_dir}/* {self.target_dir}/\n")
            f.write("```\n\n")

        return str(report_file)

    def run(self) -> None:
        """Run the intelligent merge process"""

        # Banner
        logger.info(f"{Colors.BOLD}{Colors.MAGENTA}")
        logger.info("╔═══════════════════════════════════════════════════════════════════════════════╗")
        logger.info("║                                                                               ║")
        logger.info("║                    🔀 INTELLIGENT MERGE TOOL 🧠                               ║")
        logger.info("║                                                                               ║")
        logger.info("║              AI-Powered Deep Analysis and Smart Merging                      ║")
        logger.info("║                                                                               ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}\n")

        logger.info(f"{Colors.CYAN}{Emojis.FOLDER} Target: {self.target_dir}{Colors.END}")
        logger.info(f"{Colors.CYAN}{Emojis.FOLDER} Sources:{Colors.END}")
        for src in self.source_dirs:
            logger.info(f"  • {src}")
        print()

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}{Emojis.SHIELD} MODE: DRY RUN (no files will be modified){Colors.END}")
        else:
            logger.info(f"{Colors.RED}{Emojis.WARNING} MODE: LIVE MERGE (files will be modified!){Colors.END}")

        logger.info(f"{Colors.CYAN}Interactive: {'Yes' if self.interactive else 'No'}{Colors.END}\n")

        # Scan and compare
        file_map = self.scan_and_compare()

        # Analyze and merge
        self.analyze_and_merge(file_map)

        # Generate report
        self.print_header("GENERATING REPORT", Colors.BLUE, Emojis.CHART)
        report_file = self.generate_report()

        # Final summary
        self.print_header("MERGE COMPLETE!", Colors.GREEN, Emojis.ROCKET)

        logger.info(f"{Colors.BOLD}📊 FINAL STATISTICS:{Colors.END}\n")
        logger.info(f"  {Emojis.MICROSCOPE} Analyzed: {Colors.CYAN}{self.stats['files_analyzed']:,}{Colors.END}")
        logger.info(f"  {Emojis.MERGE} Merged: {Colors.CYAN}{self.stats['files_merged']:,}{Colors.END}")
        logger.info(f"  {Emojis.SPARKLES} New Files: {Colors.CYAN}{self.stats['new_files']:,}{Colors.END}")
        logger.info(f"  {Emojis.CHECK} Updated: {Colors.CYAN}{self.stats['updated_files']:,}{Colors.END}")
        logger.info(f"  {Emojis.WARNING} Conflicts: {Colors.CYAN}{self.stats['conflicts_found']:,}{Colors.END}")
        logger.info(f"  ⏭️  Skipped: {Colors.CYAN}{self.stats['files_skipped']:,}{Colors.END}\n")

        logger.info(f"{Colors.BOLD}📝 OUTPUTS:{Colors.END}\n")
        logger.info(f"  {Emojis.FILE} Report: {Colors.BLUE}{report_file}{Colors.END}")
        logger.info(f"  {Emojis.FOLDER} Backups: {Colors.BLUE}{self.backup_dir}{Colors.END}")
        logger.info(f"  {Emojis.DIFF} Diffs: {Colors.BLUE}{self.merge_report_dir}{Colors.END}\n")

        if self.dry_run:
            logger.info(f"{Colors.YELLOW}{Emojis.WARNING} This was a DRY RUN. Use --live to actually merge files.{Colors.END}\n")
        else:
            logger.info(f"{Colors.GREEN}{Emojis.CHECK} Merge complete! Review the report and diffs.{Colors.END}\n")


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(
        description="🔀 Intelligent Merge Tool - AI-Powered Smart Merging",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--target', type=str, default=Path("/Users/steven/Documents/python"),
                       help='Target directory (default: ~/Documents/python)')
    parser.add_argument('--sources', nargs='+',
                       default=[Path("/Users/steven/Documents/python-repo"),
                               Path("/Users/steven/Documents/python_backup")],
                       help='Source directories to merge from')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Dry run mode (default, safe)')
    parser.add_argument('--live', action='store_true',
                       help='Live mode (actually merges files)')
    parser.add_argument('--interactive', action='store_true', default=True,
                       help='Interactive mode (asks for confirmation on conflicts)')
    parser.add_argument('--batch', action='store_true',
                       help='Batch mode (no confirmation)')

    args = parser.parse_args()

    dry_run = not args.live
    interactive = not args.batch

    merger = IntelligentMergeTool(
        target_dir=args.target,
        source_dirs=args.sources,
        dry_run=dry_run,
        interactive=interactive
    )

    merger.run()


if __name__ == "__main__":
    main()
