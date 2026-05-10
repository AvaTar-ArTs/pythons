import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Content-Aware File Organization Agent

This agent performs intelligent analysis of file systems with content-awareness
across multiple folder depths, creating systematic organization mappings and
providing improvement suggestions.

Based on analysis patterns from fancy-qwen.txt, this agent implements:
- Multi-depth folder structure analysis
- Content-aware categorization
- CSV mapping generation
- Organization improvement suggestions
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse


class ContentAwareOrganizer:
    """
    A content-aware file organization agent that analyzes folder structures
    and suggests improved organization systems.
    """
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.analysis_results = {}
        self.category_map = {
            'strategies': 'Planning',
            'guides': 'Documentation', 
            'reports': 'Analysis',
            'configs': 'Configuration',
            'transcripts': 'Documentation',
            'templates': 'Resources',
            'audio-analysis': 'Media',
            'temp-files': 'Temporary',
            'data': 'Data',
            'knowledge-base': 'Knowledge',
            'organized': 'Organized',
            'workspace': 'Active_Projects',
            'archives': 'Archives',
            'csv_explorer': 'Data_Analysis'
        }
        
    def analyze_folder_structure(self) -> Dict:
        """Analyze the folder structure with content awareness."""
        print(f"Analyzing folder structure: {self.root_path}")
        
        structure_analysis = {
            'root_items': [],
            'subdirectories': {},
            'file_types': {},
            'size_distribution': {},
            'depth_analysis': {}
        }
        
        # Count root level items
        for item in self.root_path.iterdir():
            if item.is_dir():
                structure_analysis['root_items'].append({
                    'name': item.name,
                    'type': 'directory',
                    'path': str(item),
                    'count': len(list(item.iterdir())) if item.is_dir() else 0
                })
                
                # Analyze subdirectories
                subdir_analysis = self._analyze_subdirectory(item)
                structure_analysis['subdirectories'][item.name] = subdir_analysis
            else:
                ext = item.suffix.lower()
                structure_analysis['file_types'][ext] = structure_analysis['file_types'].get(ext, 0) + 1
                structure_analysis['root_items'].append({
                    'name': item.name,
                    'type': 'file',
                    'path': str(item),
                    'size': item.stat().st_size
                })
        
        self.analysis_results['structure'] = structure_analysis
        return structure_analysis
    
    def _analyze_subdirectory(self, dir_path: Path) -> Dict:
        """Analyze a subdirectory for content patterns."""
        subdir_analysis = {
            'item_count': 0,
            'file_types': {},
            'subdirs': [],
            'estimated_category': self._infer_category(dir_path.name)
        }
        
        for item in dir_path.iterdir():
            subdir_analysis['item_count'] += 1
            if item.is_file():
                ext = item.suffix.lower()
                subdir_analysis['file_types'][ext] = subdir_analysis['file_types'].get(ext, 0) + 1
            elif item.is_dir():
                subdir_analysis['subdirs'].append(item.name)
        
        return subdir_analysis
    
    def _infer_category(self, dir_name: str) -> str:
        """Infer category based on directory name."""
        for key, category in self.category_map.items():
            if key.lower() in dir_name.lower():
                return category
        return 'Uncategorized'
    
    def create_organization_mapping(self) -> List[Dict]:
        """Create a mapping from current to suggested organization."""
        mappings = []
        
        for item in self.root_path.iterdir():
            old_path = str(item.relative_to(self.root_path))
            
            # Determine suggested new location based on content
            if item.is_dir():
                category = self._infer_category(item.name)
                new_path = f"{category}/{item.name}"
            else:
                ext = item.suffix.lower()
                if ext in ['.md', '.txt']:
                    new_path = f"Documentation/{item.name}"
                elif ext in ['.json', '.csv']:
                    new_path = f"Data/{item.name}"
                elif ext in ['.zip', '.rar']:
                    new_path = f"Archives/{item.name}"
                else:
                    new_path = f"Mixed_Content/{item.name}"
            
            mapping = {
                'old_path': old_path,
                'new_path': new_path,
                'category': self._infer_category(item.name) if item.is_dir() else 'File',
                'action': 'move',
                'reason': f"Organize {item.name} into appropriate category"
            }
            
            mappings.append(mapping)
        
        return mappings
    
    def generate_suggestions(self) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        # Check for duplicate content
        if self.analysis_results.get('structure'):
            file_types = self.analysis_results['structure']['file_types']
            if len(file_types) > 10:
                suggestions.append("Consider consolidating similar file types into fewer categories")
            
            # Check for deep nesting
            subdirs = self.analysis_results['structure']['subdirectories']
            for name, analysis in subdirs.items():
                if len(analysis.get('subdirs', [])) > 5:
                    suggestions.append(f"Directory '{name}' has many subdirectories - consider flattening structure")
        
        # General suggestions
        suggestions.extend([
            "Implement consistent naming conventions",
            "Regular maintenance to prevent further sprawl",
            "Backup strategy for important files",
            "Consider using tags instead of deep folder hierarchies"
        ])
        
        return suggestions
    
    def export_analysis_csv(self, filename: str = None) -> str:
        """Export the analysis to a CSV file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_aware_analysis_{timestamp}.csv"
        
        mappings = self.create_organization_mapping()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['old_path', 'new_path', 'category', 'action', 'reason']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for mapping in mappings:
                writer.writerow(mapping)
        
        print(f"Analysis exported to {filename}")
        return filename
    
    def run_complete_analysis(self) -> Dict:
        """Run a complete analysis and return results."""
        print("Starting content-aware analysis...")
        
        # Analyze structure
        structure = self.analyze_folder_structure()
        
        # Generate mappings
        mappings = self.create_organization_mapping()
        
        # Generate suggestions
        suggestions = self.generate_suggestions()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'root_path': str(self.root_path),
            'structure_analysis': structure,
            'organization_mappings': mappings,
            'improvement_suggestions': suggestions
        }
        
        self.analysis_results.update(results)
        
        print(f"Analysis complete. Found {len(mappings)} items to organize.")
        print(f"Suggestions: {len(suggestions)} improvement ideas generated.")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Content-Aware File Organization Agent")
    parser.add_argument("path", help="Path to analyze")
    parser.add_argument("--export-csv", action="store_true", help="Export analysis to CSV")
    parser.add_argument("--output", "-o", help="Output filename for CSV")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        return
    
    organizer = ContentAwareOrganizer(args.path)
    results = organizer.run_complete_analysis()
    
    if args.export_csv:
        csv_filename = args.output or None
        organizer.export_analysis_csv(csv_filename)
    
    # Print summary
    print("\n--- ANALYSIS SUMMARY ---")
    print(f"Root path: {results['root_path']}")
    print(f"Analysis time: {results['timestamp']}")
    print(f"Items to organize: {len(results['organization_mappings'])}")
    print(f"Suggestions: {len(results['improvement_suggestions'])}")
    
    print("\n--- SAMPLE MAPPINGS ---")
    for i, mapping in enumerate(results['organization_mappings'][:5]):
        print(f"{mapping['old_path']} -> {mapping['new_path']}")
    
    if len(results['organization_mappings']) > 5:
        print(f"... and {len(results['organization_mappings']) - 5} more")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)