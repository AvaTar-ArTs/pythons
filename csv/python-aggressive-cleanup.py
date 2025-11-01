"""
Python Aggressive Cleanup

This module provides functionality for python aggressive cleanup.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
Python Aggressive Cleanup System
Handles massive repetitive filenames and complex cleanup patterns
Fixes files like documentation_documentation_documentation_web_resources_...
"""

import os
import re
import json
import csv
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

class AggressiveCleanupSystem:
    """Handles massive repetitive filenames and complex cleanup patterns."""
    
    def __init__(self):
        """__init__ function."""

        self.root_path = Path(Path("/Users/steven/Documents/python")).expanduser()
        self.max_depth = 6
        self.backup_data = []
        
        # Aggressive cleanup patterns
        self.cleanup_patterns = {
            'repetitive_prefixes': [
                r'^documentation_documentation_documentation_',
                r'^documentation_documentation_',
                r'^documentation_',
                r'^web_resources_',
                r'^package_data_',
                r'^pydoc_html_',
                r'^html-generator_',
                r'^doc-generator_output_',
                r'^docs_html_',
                r'^documentation_web_resources_',
            ],
            'repetitive_suffixes': [
                r'_\d+$',  # _1, _2, _3
                r'\(\d+\)$',  # (1), (2), (3)
                r'_\d+_\d+$',  # _1_2, _2_3
                r'_\d+_\d+_\d+$',  # _1_2_3
                r'_\d{8}_\d{6}$',  # _20251027_145831
                r'_\d{8}$',  # _20251027
                r'_\d{6}$',  # _145831
            ],
            'hash_suffixes': [
                r'_[a-f0-9]{8,}$',  # _a1a7b7066bc54, _2f5816cd27
                r'_[a-f0-9]{6,8}$',  # _a1a7b70, _2f5816c
            ],
            'temp_suffixes': [
                r'_temp$', r'_tmp$', r'_backup$', r'_old$', r'_copy$',
                r'_bak$', r'_orig$', r'_new$', r'_test$'
            ],
            'from_suffixes': [
                r'_from_\w+$',  # _from_csv-processor
                r'_from_\w+_\d+$',  # _from_csv-processor_1
            ],
            'spaces_and_special': [
                r'[^a-zA-Z0-9._-]',  # Replace with underscore
            ],
            'multiple_underscores': [
                r'_{2,}',  # Replace multiple underscores with single
            ]
        }
        
        # Patterns to preserve (don't rename these)
        self.preserve_patterns = [
            r'^\d+days?\.py$',  # 15days.py, 30days.py
            r'^[a-z]{2,4}\.py$',  # docx.py, csvp.py, bash.py
            r'^[A-Z][a-z]+[A-Z][a-z]+\.py$',  # TextToSpeech.py
            r'^[a-z]+[A-Z][a-z]+\.py$',  # botStories.py
            r'^[a-z]+_[a-z]+\.py$',  # file_utils.py
            r'^[A-Z][a-z]+\.py$',  # Calculator.py
            r'^[a-z]+\.py$',  # simple.py
            r'^[A-Z][a-z]+_[A-Z][a-z]+\.py$',  # YouTube_Bot.py
        ]
    
    def analyze_and_cleanup(self):
        """Analyze all files and create aggressive cleanup plan."""
        logger.info("🔥 AGGRESSIVE CLEANUP SYSTEM")
        logger.info("=" * 80)
        logger.info("Handles massive repetitive filenames and complex cleanup patterns")
        logger.info("Fixes files like documentation_documentation_documentation_web_resources_...")
        print()
        
        # Find all files (not just Python)
        all_files = []
        for file_path in self.root_path.rglob('*'):
            try:
                depth = len(file_path.relative_to(self.root_path).parts)
                if depth > self.max_depth:
                    continue
            except ValueError:
                continue
            
            if file_path.is_file():
                file_info = {
                    'original_path': str(file_path),
                    'original_name': file_path.name,
                    'relative_path': str(file_path.relative_to(self.root_path)),
                    'size': file_path.stat().st_size,
                    'extension': file_path.suffix,
                    'depth': depth
                }
                
                all_files.append(file_info)
        
        logger.info(f"   Found {len(all_files)} total files")
        
        # Categorize files
        preserve_files = []
        cleanup_files = []
        
        for file_info in all_files:
            original_name = file_info['original_name']
            
            # Check if this is a good name to preserve
            should_preserve = self._should_preserve_name(original_name)
            
            if should_preserve:
                preserve_files.append(file_info)
                logger.info(f"   ✅ PRESERVE: {original_name}")
            else:
                # Check if it needs cleanup
                suggested_name = self._generate_clean_name(file_info)
                if suggested_name != original_name:
                    cleanup_files.append({
                        'file_info': file_info,
                        'suggested_name': suggested_name,
                        'reason': self._get_cleanup_reason(original_name, suggested_name)
                    })
                    logger.info(f"   🔧 CLEANUP: {original_name} → {suggested_name}")
                else:
                    preserve_files.append(file_info)
                    logger.info(f"   ✅ KEEP: {original_name}")
        
        logger.info(f"\n📊 CLEANUP STATISTICS")
        logger.info(f"   Files to preserve: {len(preserve_files)}")
        logger.info(f"   Files to cleanup: {len(cleanup_files)}")
        logger.info(f"   Cleanup rate: {len(cleanup_files)/len(all_files):.1%}")
        
        # Create cleanup plan
        cleanup_plan = []
        for cleanup_item in cleanup_files:
            file_info = cleanup_item['file_info']
            suggested_name = cleanup_item['suggested_name']
            reason = cleanup_item['reason']
            
            cleanup_plan.append({
                'original_path': file_info['original_path'],
                'original_name': file_info['original_name'],
                'suggested_name': suggested_name,
                'depth': file_info['depth'],
                'extension': file_info['extension'],
                'reason': reason
            })
            
            # Add to backup data
            self.backup_data.append({
                'original_path': file_info['original_path'],
                'original_name': file_info['original_name'],
                'suggested_name': suggested_name,
                'depth': file_info['depth'],
                'extension': file_info['extension'],
                'size': file_info['size'],
                'reason': reason
            })
        
        # Resolve naming conflicts
        self._resolve_conflicts(cleanup_plan)
        
        return cleanup_plan
    
    def _should_preserve_name(self, filename):
        """Check if a filename should be preserved."""
        # Check against preserve patterns
        for pattern in self.preserve_patterns:
            if re.match(pattern, filename):
                return True
        
        # Check if it's a meaningful name (not generic)
        if filename.lower() in ['test.py', 'main.py', 'app.py', 'script.py', 'file.py', 'data.py', 'temp.py', 'tmp.py']:
            return False
        
        # Check if it has problematic patterns
        for pattern_type, patterns in self.cleanup_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename):
                    return False
        
        # If it's reasonably short and meaningful, preserve it
        if len(filename) <= 30 and not re.search(r'[^a-zA-Z0-9._-]', filename):
            return True
        
        return False
    
    def _generate_clean_name(self, file_info):
        """Generate a clean name for problematic files."""
        original_name = file_info['original_name']
        extension = file_info['extension']
        base_name = original_name.replace(extension, '')
        
        # Start with original name
        suggested_name = base_name
        
        # Apply cleanup patterns
        for pattern_type, patterns in self.cleanup_patterns.items():
            for pattern in patterns:
                if pattern_type == 'spaces_and_special':
                    # Replace spaces and special chars with underscores
                    suggested_name = re.sub(r'[^a-zA-Z0-9._-]', '_', suggested_name)
                elif pattern_type == 'multiple_underscores':
                    # Replace multiple underscores with single
                    suggested_name = re.sub(r'_{2,}', '_', suggested_name)
                else:
                    # Remove the pattern
                    suggested_name = re.sub(pattern, '', suggested_name)
        
        # Clean up the name
        suggested_name = suggested_name.strip('_')
        suggested_name = re.sub(r'_{2,}', '_', suggested_name)
        
        # If name is too short or empty, try to extract meaningful parts
        if len(suggested_name) < 3:
            meaningful_parts = self._extract_meaningful_parts(original_name)
            if meaningful_parts:
                suggested_name = '_'.join(meaningful_parts)
            else:
                suggested_name = 'file'
        
        # Add extension back
        suggested_name = suggested_name + extension
        
        # Final cleanup
        suggested_name = re.sub(r'[^a-zA-Z0-9._-]', '', suggested_name)
        suggested_name = suggested_name.lower()
        
        return suggested_name
    
    def _extract_meaningful_parts(self, filename):
        """Extract meaningful parts from filename for naming."""
        parts = []
        
        # Split by common separators
        words = re.split(r'[._-]', filename.lower())
        
        # Filter out common meaningless words
        meaningless_words = {
            'documentation', 'web', 'resources', 'package', 'data', 'html', 'generator',
            'output', 'docs', 'pydoc', 'blog', 'versions', 'config', 'custom', 'css',
            'js', 'mjs', 'toml', 'ts', 'yml', 'yaml', 'json', 'md', 'txt', 'log',
            'temp', 'tmp', 'backup', 'old', 'copy', 'bak', 'orig', 'new', 'test',
            'file', 'dir', 'folder', 'path', 'name', 'title', 'content', 'text',
            'version', 'v1', 'v2', 'v3', 'final', 'draft', 'edit', 'update'
        }
        
        for word in words:
            if word and word not in meaningless_words and len(word) > 2:
                parts.append(word)
        
        return parts[:5]  # Limit to 5 parts
    
    def _get_cleanup_reason(self, original_name, suggested_name):
        """Get reason for cleanup."""
        if original_name == suggested_name:
            return "No change needed"
        
        reasons = []
        
        # Check what was cleaned up
        if re.search(r'^documentation_documentation_documentation_', original_name):
            reasons.append("Removed repetitive 'documentation' prefixes")
        elif re.search(r'^documentation_documentation_', original_name):
            reasons.append("Removed duplicate 'documentation' prefix")
        elif re.search(r'^web_resources_', original_name):
            reasons.append("Removed 'web_resources' prefix")
        
        if re.search(r'_\d+$|\(\d+\)$', original_name):
            reasons.append("Removed duplicate numbers")
        
        if re.search(r'_\d{8}_\d{6}|_\d{8}', original_name):
            reasons.append("Removed timestamp")
        
        if re.search(r'_[a-f0-9]{8,}$', original_name):
            reasons.append("Removed hash suffix")
        
        if re.search(r'[^a-zA-Z0-9._-]', original_name):
            reasons.append("Cleaned special characters")
        
        if re.search(r'_{2,}', original_name):
            reasons.append("Fixed multiple underscores")
        
        if len(suggested_name) < len(original_name):
            reasons.append("Shortened filename")
        
        if reasons:
            return "; ".join(reasons)
        else:
            return "General cleanup"
    
    def _resolve_conflicts(self, cleanup_plan):
        """Resolve naming conflicts."""
        name_counts = defaultdict(int)
        name_to_files = defaultdict(list)
        
        # Group by suggested name
        for op in cleanup_plan:
            suggested_name = op['suggested_name']
            name_counts[suggested_name] += 1
            name_to_files[suggested_name].append(op)
        
        # Resolve conflicts
        for suggested_name, files in name_to_files.items():
            if len(files) > 1:
                # Sort by depth (shallower files get priority)
                files.sort(key=lambda x: x['depth'])
                
                for i, op in enumerate(files):
                    if i == 0:
                        continue  # Keep first file with original name
                    else:
                        # Add number suffix
                        base_name = op['suggested_name'].replace(op['extension'], '')
                        op['suggested_name'] = f"{base_name}_{i}{op['extension']}"
    
    def create_csv_backup(self, output_file):
        """Create CSV backup."""
        logger.info(f"\n💾 Creating CSV backup: {output_file}")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'original_path', 'original_name', 'suggested_name',
                'depth', 'extension', 'size', 'reason'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in self.backup_data:
                writer.writerow(row)
        
        logger.info(f"   CSV backup created with {len(self.backup_data)} entries")
    
    def generate_execution_script(self, cleanup_plan, output_file):
        """Generate execution script."""
        logger.info(f"\n🚀 Generating execution script: {output_file}")
        
        script_content = f'''#!/usr/bin/env python3
"""
Python Aggressive Cleanup - Execution Script
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import shutil
from pathlib import Path

def execute_cleanup():
    """Execute the aggressive cleanup plan."""
    logger.info("🔥 EXECUTING AGGRESSIVE CLEANUP")
    logger.info("=" * 60)
    logger.info("Handles massive repetitive filenames and complex cleanup patterns")
    print()
    
    # Create backup directory
    backup_dir = Path(Path("/Users/steven/python_aggressive_cleanup_backup"))
    backup_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Backup directory: {{backup_dir}}")
    
    # Cleanup operations
    cleanup_operations = {cleanup_plan}
    
    logger.info(f"\\n📦 Executing {{len(cleanup_operations)}} cleanups...")
    logger.info("   (Only problematic files will be cleaned up)")
    logger.info("   (Good names will be preserved)")
    print()
    
    for i, op in enumerate(cleanup_operations, 1):
        old_path = Path(op['original_path'])
        new_path = old_path.parent / op['suggested_name']
        
        logger.info(f"   {{i}}/{{len(cleanup_operations)}}: {{op['original_name']}} → {{op['suggested_name']}}")
        logger.info(f"     Extension: {{op['extension']}}")
        logger.info(f"     Depth: {{op['depth']}}")
        logger.info(f"     Reason: {{op['reason']}}")
        
        try:
            # Create backup
            backup_path = backup_dir / op['original_name']
            shutil.copy2(old_path, backup_path)
            
            # Rename file
            old_path.rename(new_path)
            
        except Exception as e:
            logger.info(f"     ❌ Error: {{e}}")
        else:
            logger.info(f"     ✅ Success")
    
    logger.info(f"\\n✅ Aggressive cleanup complete!")
    logger.info(f"📁 All files backed up to: {{backup_dir}}")
    logger.info(f"🔥 Massive repetitive filenames cleaned up!")
    logger.info(f"🔄 To rollback, use the CSV file to restore original names")

if __name__ == "__main__":
    execute_cleanup()
'''
        
        with open(output_file, 'w') as f:
            f.write(script_content)
        
        os.chmod(output_file, 0o755)
        logger.info(f"   Execution script created and made executable")
    
    def generate_report(self, cleanup_plan):
        """Generate comprehensive report."""
        logger.info(f"\n📊 GENERATING AGGRESSIVE CLEANUP REPORT")
        logger.info("=" * 80)
        
        logger.info(f"📈 CLEANUP STATISTICS")
        logger.info(f"   Total files to cleanup: {len(cleanup_plan)}")
        logger.info(f"   (Only problematic files will be cleaned up)")
        logger.info(f"   (Good names will be preserved)")
        
        # Group by reason
        reason_counts = Counter(op['reason'] for op in cleanup_plan)
        logger.info(f"\n🔧 CLEANUP REASONS")
        for reason, count in reason_counts.most_common():
            logger.info(f"   {reason}: {count} files")
        
        # Group by extension
        extension_counts = Counter(op['extension'] for op in cleanup_plan)
        logger.info(f"\n📁 CLEANUP BY EXTENSION")
        for ext, count in extension_counts.most_common():
            logger.info(f"   {ext}: {count} files")
        
        # Group by depth
        depth_counts = Counter(op['depth'] for op in cleanup_plan)
        logger.info(f"\n📁 CLEANUP BY DEPTH")
        for depth in sorted(depth_counts.keys()):
            logger.info(f"   Depth {depth}: {depth_counts[depth]} files")
        
        logger.info(f"\n📝 CLEANUP EXAMPLES")
        for i, op in enumerate(cleanup_plan[:15], 1):
            logger.info(f"   {i}. {op['original_name']}")
            logger.info(f"      → {op['suggested_name']}")
            logger.info(f"      Reason: {op['reason']}")
            logger.info(f"      Extension: {op['extension']}")
            logger.info(f"      Depth: {op['depth']}")
            print()
        
        logger.info(f"\n🛡️  PRESERVED NAMES (examples)")
        logger.info(f"   ✅ 15days.py - preserved")
        logger.info(f"   ✅ docx.py - preserved")
        logger.info(f"   ✅ csvp.py - preserved")
        logger.info(f"   ✅ TextToSpeech.py - preserved")
        logger.info(f"   ✅ botStories.py - preserved")

def main():
    """Main execution function."""
    logger.info("🔥 PYTHON AGGRESSIVE CLEANUP SYSTEM")
    logger.info("=" * 80)
    logger.info("Handles massive repetitive filenames and complex cleanup patterns")
    logger.info("Fixes files like documentation_documentation_documentation_web_resources_...")
    print()
    
    cleanup_system = AggressiveCleanupSystem()
    
    # Analyze and create cleanup plan
    cleanup_plan = cleanup_system.analyze_and_cleanup()
    
    # Create CSV backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_backup_file = f"/Users/steven/python_aggressive_cleanup_backup_{timestamp}.csv"
    cleanup_system.create_csv_backup(csv_backup_file)
    
    # Generate execution script
    execution_script = f"/Users/steven/python_aggressive_cleanup_execute_{timestamp}.py"
    cleanup_system.generate_execution_script(cleanup_plan, execution_script)
    
    # Generate report
    cleanup_system.generate_report(cleanup_plan)
    
    logger.info(f"\n💾 BACKUP & SAFETY")
    logger.info(f"   CSV backup: {csv_backup_file}")
    logger.info(f"   Execution script: {execution_script}")
    logger.info(f"   🛡️  All changes can be rolled back using the CSV file!")
    
    logger.info(f"\n🚀 NEXT STEPS")
    logger.info(f"   1. Review the cleanup examples above")
    logger.info(f"   2. Check the CSV backup file")
    logger.info(f"   3. Run the execution script when ready: python3 {execution_script}")
    logger.info(f"   4. Use CSV file to rollback if needed")
    
    logger.info(f"\n✅ AGGRESSIVE CLEANUP SYSTEM READY!")
    logger.info(f"   This will clean up those massive repetitive filenames!")

if __name__ == "__main__":
    main()