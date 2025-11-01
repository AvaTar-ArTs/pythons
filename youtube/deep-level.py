"""
Deep 6 Level Simplifier

This module provides functionality for deep 6 level simplifier.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Deep 6-Level Simplifier
Handles 6 levels deep and simplifies ALL the massive repetitive filenames
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class Deep6LevelSimplifier:
    """Simplifies filenames at 6 levels deep and organizes by type."""
    
    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path("/Users/steven/Documents/python")).expanduser()
        self.max_depth = 6
        
        # File type organization
        self.file_type_dirs = {
            '.html': Path(Path("/Users/steven/Documents/html")),
            '.md': Path(Path("/Users/steven/Documents/markdown")),
            '.csv': Path(Path("/Users/steven/Documents/csv")),
            '.pdf': Path(Path("/Users/steven/Documents/pdf")),
            '.json': Path(Path("/Users/steven/Documents/json")),
            '.txt': Path(Path("/Users/steven/Documents/text")),
            '.log': Path(Path("/Users/steven/Documents/logs")),
            '.png': Path(Path("/Users/steven/Documents/images")),
            '.jpg': Path(Path("/Users/steven/Documents/images")),
            '.jpeg': Path(Path("/Users/steven/Documents/images")),
            '.gif': Path(Path("/Users/steven/Documents/images")),
            '.svg': Path(Path("/Users/steven/Documents/images")),
            '.mp4': Path(Path("/Users/steven/Documents/videos")),
            '.mov': Path(Path("/Users/steven/Documents/videos")),
            '.avi': Path(Path("/Users/steven/Documents/videos")),
            '.zip': Path(Path("/Users/steven/Documents/archives")),
            '.tar': Path(Path("/Users/steven/Documents/archives")),
            '.gz': Path(Path("/Users/steven/Documents/archives")),
            '.exe': Path(Path("/Users/steven/Documents/executables")),
            '.dmg': Path(Path("/Users/steven/Documents/executables")),
            '.pkg': Path(Path("/Users/steven/Documents/executables")),
            '.py': Path(Path("/Users/steven/Documents/python")),  # Keep Python files in place
        }
        
        # Names to preserve (don't change these)
        self.preserve_patterns = [
            r'^\d+days?\.py$',  # 15days.py, 30days.py
            r'^[a-z]{2,4}\.py$',  # docx.py, csvp.py, bash.py
            r'^[A-Z][a-z]+[A-Z][a-z]+\.py$',  # TextToSpeech.py
            r'^[a-z]+[A-Z][a-z]+\.py$',  # botStories.py
            r'^[a-z]+_[a-z]+\.py$',  # file_utils.py
            r'^[A-Z][a-z]+\.py$',  # Calculator.py
            r'^[a-z]+\.py$',  # simple.py
        ]
    
    def analyze_deep_files(self):
        """Analyze all files at 6 levels deep."""
        logger.info("🔍 DEEP 6-LEVEL SIMPLIFIER")
        logger.info("=" * 80)
        logger.info("Handles 6 levels deep and simplifies ALL the massive repetitive filenames")
        logger.info("HTML → ~/Documents/html, MD → ~/Documents/markdown, etc.")
        print()
        
        # Find all files at all depths
        all_files = []
        depth_counts = defaultdict(int)
        
        for file_path in self.root_path.rglob('*'):
            try:
                depth = len(file_path.relative_to(self.root_path).parts)
                if depth > self.max_depth:
                    continue
            except ValueError:
                continue
            
            if file_path.is_file():
                file_info = {
                    'path': file_path,
                    'name': file_path.name,
                    'extension': file_path.suffix.lower(),
                    'size': file_path.stat().st_size,
                    'depth': depth,
                    'relative_path': str(file_path.relative_to(self.root_path))
                }
                all_files.append(file_info)
                depth_counts[depth] += 1
        
        logger.info(f"   Found {len(all_files)} files to analyze")
        logger.info(f"   Depth distribution:")
        for depth in sorted(depth_counts.keys()):
            logger.info(f"     Level {depth}: {depth_counts[depth]} files")
        
        # Categorize files
        python_files = []
        other_files = []
        
        for file_info in all_files:
            if file_info['extension'] == '.py':
                python_files.append(file_info)
            else:
                other_files.append(file_info)
        
        logger.info(f"   Python files: {len(python_files)}")
        logger.info(f"   Other files: {len(other_files)}")
        
        return python_files, other_files
    
    def simplify_filename(self, filename):
        """Simplify a filename by extracting only the meaningful core."""
        if self._should_preserve_name(filename):
            return filename
        
        # Remove extension temporarily
        name, ext = os.path.splitext(filename)
        
        # Extract meaningful core
        simplified = self._extract_meaningful_core(name)
        
        # If still too long, take first meaningful part
        if len(simplified) > 25:
            words = simplified.split('_')
            if len(words) > 1:
                simplified = '_'.join(words[:2])  # Take first 2 meaningful words
        
        return simplified + ext
    
    def _should_preserve_name(self, filename):
        """Check if filename should be preserved."""
        for pattern in self.preserve_patterns:
            if re.match(pattern, filename):
                return True
        return False
    
    def _extract_meaningful_core(self, name):
        """Extract the meaningful core from a filename."""
        # Remove all the junk patterns
        junk_patterns = [
            r'_\d+$',  # _1, _2, _3
            r'\(\d+\)$',  # (1), (2), (3)
            r'_\d+_\d+$',  # _1_2, _2_3
            r'_\d+_\d+_\d+$',  # _1_2_3
            r'_\d{8}_\d{6}',  # _20251028_021746
            r'_\d{8}',  # _20251028
            r'_\d{6}',  # _021746
            r'_\d{4}-\d{2}-\d{2}',  # _2025-10-28
            r'^documentation_documentation_documentation_',
            r'^documentation_documentation_',
            r'^documentation_',
            r'^web_resources_',
            r'^pydoc_html_',
            r'^html-generator_',
            r'^doc-generator_output_',
            r'_[a-f0-9]{8,}$',  # _a1a7b7066bc54
            r'_from_\w+$',  # _from_csv-processor
            r'_from_\w+_\d+$',  # _from_csv-processor_1
            r'_temp$', r'_tmp$', r'_backup$', r'_old$', r'_copy$',
            r'^legacy_categories_',
            r'^archived_',
            r'^backups_',
            r'^carbons_',
        ]
        
        # Apply junk removal
        for pattern in junk_patterns:
            name = re.sub(pattern, '', name)
        
        # Clean up spaces and special chars
        name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
        name = re.sub(r'_{2,}', '_', name)  # Multiple underscores
        name = name.strip('_')
        
        # Extract meaningful words
        words = re.split(r'[._-]', name.lower())
        
        # Filter out meaningless words
        meaningless = {
            'documentation', 'web', 'resources', 'package', 'data', 'html', 'generator',
            'output', 'docs', 'pydoc', 'blog', 'versions', 'config', 'custom', 'css',
            'temp', 'tmp', 'backup', 'old', 'copy', 'file', 'dir', 'folder', 'path',
            'name', 'title', 'content', 'text', 'version', 'v1', 'v2', 'v3', 'final',
            'draft', 'edit', 'update', 'new', 'test', 'script', 'app', 'main', 'util',
            'helper', 'tool', 'manager', 'handler', 'processor', 'converter', 'reader',
            'writer', 'analyzer', 'generator', 'creator', 'maker', 'builder', 'setup',
            'install', 'config', 'settings', 'options', 'preferences', 'default',
            'legacy', 'categories', 'archived', 'backups', 'carbons', 'requirements',
            'analysis', 'results', 'output', 'generated', 'created', 'modified'
        }
        
        meaningful_words = []
        for word in words:
            if word and word not in meaningless and len(word) > 2:
                meaningful_words.append(word)
        
        # Take first 2-3 meaningful words
        if meaningful_words:
            simplified = '_'.join(meaningful_words[:3])
        else:
            # If no meaningful words, try to extract from original
            simplified = self._extract_from_original(name)
        
        return simplified
    
    def _extract_from_original(self, name):
        """Extract meaningful parts from original name when no clear words found."""
        # Look for capitalized words (likely proper nouns)
        capitalized = re.findall(r'[A-Z][a-z]+', name)
        if capitalized:
            return '_'.join(capitalized[:2]).lower()
        
        # Look for common patterns
        if 'bot' in name.lower():
            return 'bot'
        elif 'analyze' in name.lower():
            return 'analyzer'
        elif 'convert' in name.lower():
            return 'converter'
        elif 'download' in name.lower():
            return 'downloader'
        elif 'upload' in name.lower():
            return 'uploader'
        elif 'generate' in name.lower():
            return 'generator'
        elif 'process' in name.lower():
            return 'processor'
        elif 'quiz' in name.lower():
            return 'quiz'
        elif 'image' in name.lower():
            return 'image'
        elif 'video' in name.lower():
            return 'video'
        else:
            return 'file'
    
    def create_deep_organization_plan(self, python_files, other_files):
        """Create organization plan for all files at all depths."""
        plan = {
            'python_renames': [],
            'file_moves': [],
            'directories_to_create': set()
        }
        
        # Handle Python files (simplify but keep in place)
        for file_info in python_files:
            simplified_name = self.simplify_filename(file_info['name'])
            if simplified_name != file_info['name']:
                plan['python_renames'].append({
                    'old_path': file_info['path'],
                    'old_name': file_info['name'],
                    'new_name': simplified_name,
                    'depth': file_info['depth'],
                    'relative_path': file_info['relative_path'],
                    'reason': self._get_simplification_reason(file_info['name'], simplified_name)
                })
        
        # Handle other files (move to appropriate directories)
        for file_info in other_files:
            ext = file_info['extension']
            if ext in self.file_type_dirs:
                target_dir = self.file_type_dirs[ext]
                plan['directories_to_create'].add(target_dir)
                
                simplified_name = self.simplify_filename(file_info['name'])
                target_path = target_dir / simplified_name
                
                plan['file_moves'].append({
                    'old_path': file_info['path'],
                    'old_name': file_info['name'],
                    'new_path': target_path,
                    'new_name': simplified_name,
                    'extension': ext,
                    'depth': file_info['depth'],
                    'relative_path': file_info['relative_path'],
                    'reason': f"Move {ext} file to {target_dir.name} directory"
                })
        
        return plan
    
    def _get_simplification_reason(self, old_name, new_name):
        """Get reason for filename simplification."""
        if old_name == new_name:
            return "No change needed"
        
        reasons = []
        
        if len(new_name) < len(old_name):
            reasons.append(f"Simplified from {len(old_name)} to {len(new_name)} chars")
        
        if re.search(r'_\d+$|\(\d+\)$', old_name):
            reasons.append("Removed duplicate numbers")
        
        if re.search(r'^documentation_documentation', old_name):
            reasons.append("Removed repetitive prefixes")
        
        if re.search(r'_[a-f0-9]{8,}$', old_name):
            reasons.append("Removed hash suffix")
        
        if re.search(r'_from_\w+', old_name):
            reasons.append("Removed 'from' suffix")
        
        if re.search(r'^legacy_categories_', old_name):
            reasons.append("Removed 'legacy_categories' prefix")
        
        return "; ".join(reasons) if reasons else "General simplification"
    
    def create_execution_script(self, plan, output_file):
        """Create execution script."""
        logger.info(f"\n🚀 Creating execution script: {output_file}")
        
        script_content = f'''#!/usr/bin/env python3
"""
Deep 6-Level Simplifier - Execution Script
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import shutil
from pathlib import Path

def execute_deep_organization():
    """Execute the deep simplification and organization plan."""
    logger.info("🔍 EXECUTING DEEP 6-LEVEL SIMPLIFICATION")
    logger.info("=" * 60)
    logger.info("Handles 6 levels deep and simplifies ALL the massive repetitive filenames")
    print()
    
    # Create backup directory
    backup_dir = Path(Path("/Users/steven/deep_6_level_backup"))
    backup_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Backup directory: {{backup_dir}}")
    
    # Create target directories
    target_dirs = {[str(d) for d in plan['directories_to_create']]}
    for target_dir in target_dirs:
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Created directory: {{target_dir}}")
    
    # Python file renames
    python_renames = {plan['python_renames']}
    logger.info(f"\\n🐍 Simplifying {{len(python_renames)}} Python files...")
    
    for i, rename in enumerate(python_renames, 1):
        old_path = rename['old_path']
        new_path = old_path.parent / rename['new_name']
        
        logger.info(f"   {{i}}/{{len(python_renames)}}: {{rename['old_name']}} → {{rename['new_name']}}")
        logger.info(f"     Depth: {{rename['depth']}} | Reason: {{rename['reason']}}")
        
        try:
            # Create backup
            backup_path = backup_dir / rename['old_name']
            shutil.copy2(old_path, backup_path)
            
            # Rename file
            old_path.rename(new_path)
            logger.info(f"     ✅ Success")
        except Exception as e:
            logger.info(f"     ❌ Error: {{e}}")
    
    # File moves
    file_moves = {plan['file_moves']}
    logger.info(f"\\n📁 Moving {{len(file_moves)}} files to organized directories...")
    
    for i, move in enumerate(file_moves, 1):
        old_path = move['old_path']
        new_path = move['new_path']
        
        logger.info(f"   {{i}}/{{len(file_moves)}}: {{move['old_name']}} → {{move['extension']}} directory")
        logger.info(f"     Depth: {{move['depth']}} | From: {{move['relative_path']}}")
        
        try:
            # Create backup
            backup_path = backup_dir / move['old_name']
            shutil.copy2(old_path, backup_path)
            
            # Move file
            shutil.move(str(old_path), str(new_path))
            logger.info(f"     ✅ Success")
        except Exception as e:
            logger.info(f"     ❌ Error: {{e}}")
    
    logger.info(f"\\n✅ Deep 6-level simplification complete!")
    logger.info(f"📁 All files backed up to: {{backup_dir}}")
    logger.info(f"🐍 Python files simplified and kept in place")
    logger.info(f"📁 Other files organized by type")
    logger.info(f"🔄 To rollback, use the backup directory")

if __name__ == "__main__":
    execute_deep_organization()
'''
        
        with open(output_file, 'w') as f:
            f.write(script_content)
        
        os.chmod(output_file, 0o755)
        logger.info(f"   Execution script created: {output_file}")
    
    def generate_deep_report(self, plan):
        """Generate deep organization report."""
        logger.info(f"\n📊 DEEP 6-LEVEL SIMPLIFICATION REPORT")
        logger.info("=" * 80)
        
        logger.info(f"🐍 PYTHON FILE SIMPLIFICATIONS")
        logger.info(f"   Files to simplify: {len(plan['python_renames'])}")
        logger.info(f"   (Kept in ~/Documents/python)")
        
        # Group by depth
        python_by_depth = defaultdict(list)
        for rename in plan['python_renames']:
            python_by_depth[rename['depth']].append(rename)
        
        logger.info(f"\n🐍 PYTHON SIMPLIFICATIONS BY DEPTH")
        for depth in sorted(python_by_depth.keys()):
            logger.info(f"   Level {depth}: {len(python_by_depth[depth])} files")
        
        logger.info(f"\n📁 FILE MOVES BY TYPE")
        file_moves = plan['file_moves']
        by_extension = defaultdict(list)
        for move in file_moves:
            by_extension[move['extension']].append(move)
        
        for ext, moves in by_extension.items():
            target_dir = self.file_type_dirs.get(ext, "Unknown")
            logger.info(f"   {ext}: {len(moves)} files → {target_dir}")
        
        # Group moves by depth
        moves_by_depth = defaultdict(list)
        for move in file_moves:
            moves_by_depth[move['depth']].append(move)
        
        logger.info(f"\n📁 FILE MOVES BY DEPTH")
        for depth in sorted(moves_by_depth.keys()):
            logger.info(f"   Level {depth}: {len(moves_by_depth[depth])} files")
        
        logger.info(f"\n📁 DIRECTORIES TO CREATE")
        for target_dir in plan['directories_to_create']:
            logger.info(f"   {target_dir}")
        
        logger.info(f"\n🎯 PYTHON SIMPLIFICATION EXAMPLES")
        for i, rename in enumerate(plan['python_renames'][:15], 1):
            logger.info(f"   {i}. {rename['old_name']} → {rename['new_name']}")
            logger.info(f"      Depth: {rename['depth']} | Reason: {rename['reason']}")
        
        logger.info(f"\n📁 FILE MOVE EXAMPLES")
        for i, move in enumerate(file_moves[:15], 1):
            logger.info(f"   {i}. {move['old_name']} → {move['extension']} directory")
            logger.info(f"      Depth: {move['depth']} | From: {move['relative_path']}")

def main():
    """Main execution function."""
    logger.info("🔍 DEEP 6-LEVEL SIMPLIFIER")
    logger.info("=" * 80)
    logger.info("Handles 6 levels deep and simplifies ALL the massive repetitive filenames")
    logger.info("HTML → ~/Documents/html, MD → ~/Documents/markdown, etc.")
    print()
    
    simplifier = Deep6LevelSimplifier()
    
    # Analyze deep files
    python_files, other_files = simplifier.analyze_deep_files()
    
    # Create deep organization plan
    plan = simplifier.create_deep_organization_plan(python_files, other_files)
    
    # Create execution script
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    execution_script = f"/Users/steven/deep_6_level_simplifier_{timestamp}.py"
    simplifier.create_execution_script(plan, execution_script)
    
    # Generate deep report
    simplifier.generate_deep_report(plan)
    
    logger.info(f"\n💾 BACKUP & SAFETY")
    logger.info(f"   Execution script: {execution_script}")
    logger.info(f"   🛡️  All changes will be backed up!")
    
    logger.info(f"\n🚀 NEXT STEPS")
    logger.info(f"   1. Review the deep simplification plan above")
    logger.info(f"   2. Run the execution script: python3 {execution_script}")
    logger.info(f"   3. Files will be simplified and organized at ALL depths!")
    
    logger.info(f"\n✅ DEEP 6-LEVEL SIMPLIFIER READY!")
    logger.info(f"   This will handle ALL the nested mess!")

if __name__ == "__main__":
    main()