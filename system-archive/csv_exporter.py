#!/usr/bin/env python3
"""
CSV Exporter - Export analysis results to CSV format
"""

import csv
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class CSVExporter:
    """Exports analysis results to CSV format."""
    
    def export(self, result: Any, output_dir: Path):
        """Export analysis results to CSV files."""
        print("   📊 Exporting CSV files...")
        
        # Export file analysis
        self._export_file_analysis(result, output_dir)
        
        # Export category analysis
        self._export_category_analysis(result, output_dir)
        
        # Export duplicate analysis
        self._export_duplicate_analysis(result, output_dir)
        
        # Export depth analysis
        self._export_depth_analysis(result, output_dir)
        
        # Export GitHub analysis (if available)
        if hasattr(result, 'github_structure') and result.github_structure:
            self._export_github_analysis(result, output_dir)
        
        # Export codex analysis (if available)
        if hasattr(result, 'codex_configs') and result.codex_configs:
            self._export_codex_analysis(result, output_dir)
        
        print("   ✅ CSV export complete")
    
    def _export_file_analysis(self, result: Any, output_dir: Path):
        """Export detailed file analysis to CSV."""
        csv_path = output_dir / "file_analysis.csv"
        
        # Prepare data for CSV
        file_data = []
        
        # If we have file details from the analyzer
        if hasattr(result, 'files') and result.files:
            for file_info in result.files:
                file_data.append({
                    'path': file_info.path,
                    'name': file_info.name,
                    'extension': file_info.extension,
                    'size_bytes': file_info.size,
                    'size_mb': round(file_info.size / (1024 * 1024), 2),
                    'modified_time': file_info.modified_time.isoformat(),
                    'mime_type': file_info.mime_type,
                    'category': file_info.category,
                    'depth': file_info.depth,
                    'priority': file_info.priority,
                    'is_duplicate': file_info.is_duplicate,
                    'duplicate_group': file_info.duplicate_group or ''
                })
        else:
            # Fallback: create summary data
            file_data.append({
                'path': result.root_path,
                'name': 'ROOT',
                'extension': '',
                'size_bytes': 0,
                'size_mb': 0,
                'modified_time': result.analysis_timestamp.isoformat(),
                'mime_type': 'directory',
                'category': 'root',
                'depth': 0,
                'priority': 10,
                'is_duplicate': False,
                'duplicate_group': ''
            })
        
        # Write CSV
        if file_data:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = file_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(file_data)
        
        print(f"     📄 File analysis: {csv_path}")
    
    def _export_category_analysis(self, result: Any, output_dir: Path):
        """Export category analysis to CSV."""
        csv_path = output_dir / "category_analysis.csv"
        
        category_data = []
        for category, count in result.categories.items():
            size_bytes = result.size_by_category.get(category, 0)
            size_mb = round(size_bytes / (1024 * 1024), 2)
            
            category_data.append({
                'category': category,
                'file_count': count,
                'size_bytes': size_bytes,
                'size_mb': size_mb,
                'percentage_of_files': round((count / result.total_files) * 100, 2) if result.total_files > 0 else 0,
                'percentage_of_size': round((size_bytes / sum(result.size_by_category.values())) * 100, 2) if sum(result.size_by_category.values()) > 0 else 0
            })
        
        # Sort by file count
        category_data.sort(key=lambda x: x['file_count'], reverse=True)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = category_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(category_data)
        
        print(f"     📄 Category analysis: {csv_path}")
    
    def _export_duplicate_analysis(self, result: Any, output_dir: Path):
        """Export duplicate analysis to CSV."""
        csv_path = output_dir / "duplicate_analysis.csv"
        
        duplicate_data = []
        for i, (content_hash, file_paths) in enumerate(result.duplicate_groups.items()):
            for j, file_path in enumerate(file_paths):
                duplicate_data.append({
                    'duplicate_group_id': i,
                    'content_hash': content_hash,
                    'file_path': file_path,
                    'is_representative': j == 0,  # First file is representative
                    'group_size': len(file_paths)
                })
        
        if duplicate_data:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = duplicate_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(duplicate_data)
        
        print(f"     📄 Duplicate analysis: {csv_path}")
    
    def _export_depth_analysis(self, result: Any, output_dir: Path):
        """Export depth distribution analysis to CSV."""
        csv_path = output_dir / "depth_analysis.csv"
        
        depth_data = []
        for depth, count in result.depth_distribution.items():
            depth_data.append({
                'depth': depth,
                'file_count': count,
                'percentage': round((count / result.total_files) * 100, 2) if result.total_files > 0 else 0
            })
        
        # Sort by depth
        depth_data.sort(key=lambda x: x['depth'])
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = depth_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(depth_data)
        
        print(f"     📄 Depth analysis: {csv_path}")
    
    def _export_github_analysis(self, result: Any, output_dir: Path):
        """Export GitHub analysis to CSV."""
        csv_path = output_dir / "github_analysis.csv"
        
        github_data = []
        github_structure = result.github_structure
        
        # Repository health metrics
        github_data.append({
            'metric': 'health_score',
            'value': github_structure.get('repository_health_score', 0),
            'description': 'Overall repository health score (0-100)'
        })
        
        github_data.append({
            'metric': 'has_readme',
            'value': 1 if github_structure.get('has_readme', False) else 0,
            'description': 'Has README.md file'
        })
        
        github_data.append({
            'metric': 'has_license',
            'value': 1 if github_structure.get('has_license', False) else 0,
            'description': 'Has LICENSE file'
        })
        
        github_data.append({
            'metric': 'has_contributing',
            'value': 1 if github_structure.get('has_contributing', False) else 0,
            'description': 'Has CONTRIBUTING.md file'
        })
        
        github_data.append({
            'metric': 'has_gitignore',
            'value': 1 if github_structure.get('has_gitignore', False) else 0,
            'description': 'Has .gitignore file'
        })
        
        github_data.append({
            'metric': 'has_github_workflows',
            'value': 1 if github_structure.get('has_github_workflows', False) else 0,
            'description': 'Has GitHub Actions workflows'
        })
        
        # Code file counts
        github_data.append({
            'metric': 'code_files_count',
            'value': len(github_structure.get('code_files', [])),
            'description': 'Number of code files'
        })
        
        github_data.append({
            'metric': 'test_files_count',
            'value': len(github_structure.get('test_files', [])),
            'description': 'Number of test files'
        })
        
        github_data.append({
            'metric': 'config_files_count',
            'value': len(github_structure.get('config_files', [])),
            'description': 'Number of configuration files'
        })
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = github_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(github_data)
        
        print(f"     📄 GitHub analysis: {csv_path}")
    
    def _export_codex_analysis(self, result: Any, output_dir: Path):
        """Export codex analysis to CSV."""
        csv_path = output_dir / "codex_analysis.csv"
        
        codex_data = []
        codex_configs = result.codex_configs
        
        # AI tool configurations
        for tool, config in codex_configs.items():
            if isinstance(config, dict):
                for key, value in config.items():
                    codex_data.append({
                        'ai_tool': tool,
                        'config_key': key,
                        'config_value': str(value),
                        'config_type': type(value).__name__
                    })
            else:
                codex_data.append({
                    'ai_tool': tool,
                    'config_key': 'config',
                    'config_value': str(config),
                    'config_type': type(config).__name__
                })
        
        if codex_data:
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = codex_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(codex_data)
        
        print(f"     📄 Codex analysis: {csv_path}")
    
    def _export_file_type_analysis(self, result: Any, output_dir: Path):
        """Export file type analysis to CSV."""
        csv_path = output_dir / "file_type_analysis.csv"
        
        file_type_data = []
        for ext, count in result.file_types.items():
            file_type_data.append({
                'extension': ext,
                'file_count': count,
                'percentage': round((count / result.total_files) * 100, 2) if result.total_files > 0 else 0
            })
        
        # Sort by file count
        file_type_data.sort(key=lambda x: x['file_count'], reverse=True)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = file_type_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(file_type_data)
        
        print(f"     📄 File type analysis: {csv_path}")
    
    def _export_summary_report(self, result: Any, output_dir: Path):
        """Export summary report to CSV."""
        csv_path = output_dir / "summary_report.csv"
        
        summary_data = [
            {
                'metric': 'total_files',
                'value': result.total_files,
                'description': 'Total number of files analyzed'
            },
            {
                'metric': 'total_directories',
                'value': result.total_directories,
                'description': 'Total number of directories analyzed'
            },
            {
                'metric': 'max_depth',
                'value': result.max_depth,
                'description': 'Maximum depth reached during analysis'
            },
            {
                'metric': 'duplicate_groups',
                'value': len(result.duplicate_groups),
                'description': 'Number of duplicate file groups found'
            },
            {
                'metric': 'unique_categories',
                'value': len(result.categories),
                'description': 'Number of unique file categories'
            },
            {
                'metric': 'unique_file_types',
                'value': len(result.file_types),
                'description': 'Number of unique file extensions'
            },
            {
                'metric': 'analysis_timestamp',
                'value': result.analysis_timestamp.isoformat(),
                'description': 'When the analysis was performed'
            },
            {
                'metric': 'root_path',
                'value': result.root_path,
                'description': 'Root path that was analyzed'
            }
        ]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = summary_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(summary_data)
        
        print(f"     📄 Summary report: {csv_path}")