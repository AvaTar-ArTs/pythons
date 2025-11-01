
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_001 = 001
CONSTANT_100 = 100
CONSTANT_200 = 200
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096

#!/usr/bin/env python3
"""
Etsy Collection Cleanup and Optimizer
Identifies and handles duplicates, creates optimization recommendations.
"""

import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict
import shutil

class CleanupOptimizer:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.organization_path = self.root_path / "00_Organization"
        self.duplicates = defaultdict(list)
        self.optimization_reports = {}
        
    def find_duplicates(self):
        """Find duplicate files using content hashing"""
        logger.info("Scanning for duplicate files...")
        
        file_hashes = {}
        total_files = 0
        
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and not str(file_path).startswith(str(self.organization_path)):
                total_files += 1
                if total_files % CONSTANT_1000 == 0:
                    logger.info(f"Processed {total_files} files...")
                
                try:
                    file_hash = self.get_file_hash(file_path)
                    if file_hash:
                        if file_hash in file_hashes:
                            self.duplicates[file_hash].append({
                                'path': str(file_path),
                                'size': file_path.stat().st_size,
                                'modified': file_path.stat().st_mtime
                            })
                        else:
                            file_hashes[file_hash] = {
                                'path': str(file_path),
                                'size': file_path.stat().st_size,
                                'modified': file_path.stat().st_mtime
                            }
                except Exception as e:
                    continue
        
        logger.info(f"Found {len(self.duplicates)} duplicate groups affecting {sum(len(group) for group in self.duplicates.values())} files")
        return self.duplicates
    
    def get_file_hash(self, filepath):
        """Get MD5 hash of file"""
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except (OSError, IOError, FileNotFoundError):
            return None
    
    def analyze_duplicate_patterns(self):
        """Analyze patterns in duplicate files"""
        patterns = {
            'css_files': 0,
            'js_files': 0,
            'image_files': 0,
            'system_files': 0,
            'gallery_duplicates': 0
        }
        
        for hash_val, files in self.duplicates.items():
            for file_info in files:
                file_path = Path(file_info['path'])
                file_ext = file_path.suffix.lower()
                file_name = file_path.name.lower()
                
                if file_ext == '.css':
                    patterns['css_files'] += 1
                elif file_ext == '.js':
                    patterns['js_files'] += 1
                elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    patterns['image_files'] += 1
                elif any(word in file_name for word in ['preloader', 'default-skin', 'photoswipe']):
                    patterns['system_files'] += 1
                elif 'gallery' in str(file_path) or 'public' in str(file_path):
                    patterns['gallery_duplicates'] += 1
        
        return patterns
    
    def create_cleanup_recommendations(self):
        """Create recommendations for cleanup"""
        recommendations = []
        
        patterns = self.analyze_duplicate_patterns()
        
        if patterns['css_files'] > 50:
            recommendations.append({
                'type': 'system_cleanup',
                'priority': 'high',
                'title': 'Consolidate CSS Files',
                'description': f'Found {patterns["css_files"]} duplicate CSS files across projects',
                'action': 'Create shared CSS library and use symbolic links',
                'potential_savings': f'~{patterns["css_files"] * 0.01:.1f} MB'
            })
        
        if patterns['js_files'] > 50:
            recommendations.append({
                'type': 'system_cleanup',
                'priority': 'high',
                'title': 'Consolidate JavaScript Files',
                'description': f'Found {patterns["js_files"]} duplicate JS files across projects',
                'action': 'Create shared JS library and use symbolic links',
                'potential_savings': f'~{patterns["js_files"] * 0.02:.1f} MB'
            })
        
        if patterns['system_files'] > CONSTANT_100:
            recommendations.append({
                'type': 'system_cleanup',
                'priority': 'medium',
                'title': 'Remove Duplicate System Files',
                'description': f'Found {patterns["system_files"]} duplicate system files (preloader, etc.)',
                'action': 'Keep one copy and create symbolic links in other locations',
                'potential_savings': f'~{patterns["system_files"] * 0.CONSTANT_001:.1f} MB'
            })
        
        if patterns['gallery_duplicates'] > CONSTANT_200:
            recommendations.append({
                'type': 'content_cleanup',
                'priority': 'medium',
                'title': 'Review Gallery Duplicates',
                'description': f'Found {patterns["gallery_duplicates"]} duplicate files in gallery projects',
                'action': 'Review if these are intentional duplicates or can be consolidated',
                'potential_savings': 'Variable - needs manual review'
            })
        
        return recommendations
    
    def create_optimization_plan(self):
        """Create optimization plan for the collection"""
        
        # Calculate total potential savings
        total_duplicate_size = 0
        for hash_val, files in self.duplicates.items():
            if len(files) > 1:
                # Keep the newest file, calculate savings from others
                files_sorted = sorted(files, key=lambda x: x['modified'], reverse=True)
                for file_info in files_sorted[1:]:  # Skip the newest (keep this one)
                    total_duplicate_size += file_info['size']
        
        optimization_plan = {
            'summary': {
                'total_duplicates': len(self.duplicates),
                'total_duplicate_files': sum(len(files) for files in self.duplicates.values()),
                'potential_savings_mb': total_duplicate_size / (CONSTANT_1024 * CONSTANT_1024),
                'potential_savings_gb': total_duplicate_size / (CONSTANT_1024 * CONSTANT_1024 * CONSTANT_1024)
            },
            'recommendations': self.create_cleanup_recommendations(),
            'duplicate_analysis': self.analyze_duplicate_patterns(),
            'action_plan': self.create_action_plan()
        }
        
        return optimization_plan
    
    def create_action_plan(self):
        """Create step-by-step action plan"""
        actions = [
            {
                'step': 1,
                'title': 'Backup Collection',
                'description': 'Create a backup before making any changes',
                'command': 'cp -r /Users/steven/Pictures/etsy /Users/steven/Pictures/etsy_backup_$(date +%Y%m%d)',
                'risk': 'low'
            },
            {
                'step': 2,
                'title': 'Create Shared Libraries',
                'description': 'Create shared CSS and JS libraries',
                'command': 'mkdir -p /Users/steven/Pictures/etsy/00_Organization/shared_libraries/{css,js,images}',
                'risk': 'low'
            },
            {
                'step': 3,
                'title': 'Consolidate System Files',
                'description': 'Move duplicate system files to shared libraries',
                'command': 'Move duplicate CSS/JS files to shared libraries and create symlinks',
                'risk': 'medium'
            },
            {
                'step': 4,
                'title': 'Review Content Duplicates',
                'description': 'Manually review and consolidate content duplicates',
                'command': 'Review duplicate content files and decide which to keep',
                'risk': 'high'
            },
            {
                'step': 5,
                'title': 'Update Project References',
                'description': 'Update project files to use shared libraries',
                'command': 'Update HTML files to reference shared CSS/JS files',
                'risk': 'medium'
            }
        ]
        
        return actions
    
    def generate_cleanup_reports(self):
        """Generate comprehensive cleanup reports"""
        
        # Find duplicates
        self.find_duplicates()
        
        # Create optimization plan
        optimization_plan = self.create_optimization_plan()
        
        # Save detailed duplicate report
        duplicate_report = {
            'summary': optimization_plan['summary'],
            'duplicates': dict(self.duplicates),
            'patterns': optimization_plan['duplicate_analysis'],
            'recommendations': optimization_plan['recommendations']
        }
        
        with open(self.organization_path / 'duplicate_analysis.json', 'w') as f:
            json.dump(duplicate_report, f, indent=2)
        
        # Create human-readable report
        report_content = f"""# Etsy Collection Cleanup Report

## Summary
- **Total Duplicate Groups:** {optimization_plan['summary']['total_duplicates']:,}
- **Total Duplicate Files:** {optimization_plan['summary']['total_duplicate_files']:,}
- **Potential Space Savings:** {optimization_plan['summary']['potential_savings_gb']:.2f} GB

## Duplicate Patterns
"""
        
        for pattern, count in optimization_plan['duplicate_analysis'].items():
            report_content += f"- **{pattern.replace('_', ' ').title()}:** {count:,} files\n"
        
        report_content += "\n## Recommendations\n\n"
        
        for i, rec in enumerate(optimization_plan['recommendations'], 1):
            report_content += f"### {i}. {rec['title']} ({rec['priority'].upper()} PRIORITY)\n"
            report_content += f"**Description:** {rec['description']}\n\n"
            report_content += f"**Action:** {rec['action']}\n\n"
            if 'potential_savings' in rec:
                report_content += f"**Potential Savings:** {rec['potential_savings']}\n\n"
        
        report_content += "\n## Action Plan\n\n"
        
        for action in optimization_plan['action_plan']:
            report_content += f"### Step {action['step']}: {action['title']}\n"
            report_content += f"**Description:** {action['description']}\n\n"
            report_content += f"**Command:** `{action['command']}`\n\n"
            report_content += f"**Risk Level:** {action['risk'].upper()}\n\n"
        
        with open(self.organization_path / 'cleanup_report.md', 'w') as f:
            f.write(report_content)
        
        return optimization_plan

def main():
    optimizer = CleanupOptimizer(Path("/Users/steven/Pictures/etsy"))
    
    logger.info("Starting cleanup and optimization analysis...")
    
    optimization_plan = optimizer.generate_cleanup_reports()
    
    logger.info("✓ Duplicate analysis complete")
    logger.info("✓ Cleanup recommendations generated")
    logger.info("✓ Action plan created")
    
    logger.info(f"\nCleanup Analysis Complete!")
    logger.info(f"Found {optimization_plan['summary']['total_duplicates']:,} duplicate groups")
    logger.info(f"Potential savings: {optimization_plan['summary']['potential_savings_gb']:.2f} GB")
    logger.info(f"Generated {len(optimization_plan['recommendations'])} optimization recommendations")
    
    logger.info(f"\nReports saved to: /Users/steven/Pictures/etsy/00_Organization/")
    logger.info("- cleanup_report.md (Human-readable report)")
    logger.info("- duplicate_analysis.json (Detailed data)")

if __name__ == "__main__":
    main()