#!/usr/bin/env python3
"""
Specialized Content Organizer Agent

Implements content-aware file organization approaches based on the methodologies
demonstrated in fancy-qwen.txt, including multi-depth analysis, semantic
categorization, content analysis, and organizational mapping capabilities.
"""

import os
import json
import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import mimetypes
from collections import defaultdict
import hashlib


@dataclass
class FileMetadata:
    """Represents metadata for a file including semantic categorization."""
    path: str
    name: str
    size: int
    extension: str
    mime_type: str
    modification_time: float
    content_preview: str = ""
    semantic_category: str = ""
    content_tags: List[str] = None
    business_value: float = 0.0
    depth_level: int = 0
    
    def __post_init__(self):
        if self.content_tags is None:
            self.content_tags = []


class ContentAnalyzer:
    """Analyzes content to determine semantic categories and tags."""
    
    def __init__(self):
        # Define semantic categories with keywords
        self.semantic_categories = {
            'AI/ML': ['ai', 'ml', 'neural', 'network', 'deep learning', 'machine learning', 'artificial intelligence'],
            'Web Development': ['web', 'html', 'css', 'javascript', 'react', 'vue', 'angular', 'frontend', 'backend'],
            'Automation': ['automation', 'script', 'bot', 'automate', 'workflow', 'process'],
            'Data Science': ['data', 'analysis', 'analytics', 'dataset', 'statistic', 'visualization'],
            'Business Strategy': ['strategy', 'plan', 'business', 'marketing', 'executive', 'roadmap'],
            'Documentation': ['doc', 'documentation', 'guide', 'manual', 'tutorial', 'readme'],
            'Configuration': ['config', 'settings', 'setup', 'environment', 'deployment'],
            'Research': ['research', 'study', 'paper', 'academic', 'thesis', 'investigation'],
            'Finance': ['finance', 'budget', 'accounting', 'investment', 'financial'],
            'Legal': ['legal', 'contract', 'agreement', 'policy', 'terms', 'license'],
            'Healthcare': ['health', 'medical', 'patient', 'clinical', 'pharma'],
            'Education': ['education', 'course', 'learning', 'teaching', 'student', 'curriculum'],
            'Security': ['security', 'privacy', 'encryption', 'authentication', 'authorization'],
            'Testing': ['test', 'testing', 'unit', 'integration', 'qa', 'quality'],
            'Media': ['image', 'video', 'audio', 'photo', 'graphic', 'design'],
            'Communication': ['email', 'message', 'chat', 'meeting', 'presentation'],
            'Project Management': ['project', 'task', 'schedule', 'timeline', 'milestone', 'gantt'],
            'Development': ['code', 'programming', 'software', 'development', 'developer'],
            'System Administration': ['server', 'infrastructure', 'devops', 'cloud', 'database'],
            'Creative': ['creative', 'design', 'art', 'writing', 'content', 'copywriting']
        }
        
        # Define strategic importance keywords
        self.strategic_keywords = {
            'strategy': 2.0, 'plan': 1.8, 'implementation': 1.5, 'roadmap': 1.7,
            'vision': 1.6, 'mission': 1.6, 'goal': 1.4, 'objective': 1.4,
            'initiative': 1.5, 'project': 1.3, 'program': 1.4, 'portfolio': 1.5,
            'executive': 1.8, 'board': 1.7, 'stakeholder': 1.5, 'governance': 1.6,
            'innovation': 1.7, 'transformation': 1.8, 'change': 1.4, 'restructuring': 1.6
        }
    
    def analyze_content(self, file_path: str, preview_size: int = 500) -> str:
        """Analyze file content to extract preview text."""
        try:
            if file_path.endswith(('.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.csv')):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(preview_size)
                    return content.strip()
            else:
                # For binary files, return file signature info
                return f"Binary file of type: {mimetypes.guess_type(file_path)[0]}"
        except Exception:
            return "Could not read file content"
    
    def categorize_semantically(self, file_path: str, content_preview: str = "") -> Tuple[str, List[str]]:
        """Categorize file based on semantic analysis of name and content."""
        file_name = os.path.basename(file_path).lower()
        combined_text = f"{file_name} {content_preview}".lower()
        
        category_scores = defaultdict(float)
        all_tags = set()
        
        # Score categories based on keywords
        for category, keywords in self.semantic_categories.items():
            for keyword in keywords:
                if keyword in combined_text:
                    category_scores[category] += 1.0
        
        # Calculate business value based on strategic keywords
        business_value = 0.0
        for keyword, weight in self.strategic_keywords.items():
            if keyword in combined_text:
                business_value += weight
        
        # Determine primary category
        primary_category = max(category_scores, key=category_scores.get) if category_scores else "Uncategorized"
        
        # Extract additional tags
        for category, keywords in self.semantic_categories.items():
            for keyword in keywords:
                if keyword in combined_text:
                    all_tags.add(keyword)
        
        return primary_category, list(all_tags), business_value


class MultiDepthAnalyzer:
    """Analyzes folder structures with multi-depth awareness."""
    
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
    
    def analyze_folder_structure(self, root_path: str, max_depth: int = 5) -> List[FileMetadata]:
        """Analyze folder structure with multi-depth awareness."""
        all_files = []
        
        def walk_with_depth(path, current_depth):
            if current_depth > max_depth:
                return
            
            try:
                for entry in os.scandir(path):
                    if entry.is_file():
                        # Get file metadata
                        stat = entry.stat()
                        mime_type, _ = mimetypes.guess_type(entry.path)
                        
                        # Analyze content
                        content_preview = self.content_analyzer.analyze_content(entry.path)
                        semantic_category, tags, business_value = self.content_analyzer.categorize_semantically(
                            entry.path, content_preview
                        )
                        
                        file_meta = FileMetadata(
                            path=entry.path,
                            name=entry.name,
                            size=stat.st_size,
                            extension=os.path.splitext(entry.name)[1],
                            mime_type=mime_type or "unknown",
                            modification_time=stat.st_mtime,
                            content_preview=content_preview[:200],  # Truncate preview
                            semantic_category=semantic_category,
                            content_tags=tags,
                            business_value=business_value,
                            depth_level=current_depth
                        )
                        all_files.append(file_meta)
                    
                    elif entry.is_dir():
                        walk_with_depth(entry.path, current_depth + 1)
            except PermissionError:
                # Skip directories we don't have permission to access
                pass
        
        walk_with_depth(root_path, 0)
        return all_files


class OrganizationalMapper:
    """Creates organizational mappings and suggests improvements."""
    
    def __init__(self):
        self.multi_depth_analyzer = MultiDepthAnalyzer()
    
    def create_csv_mapping(self, root_path: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Create CSV mapping of original to new file organization."""
        files = self.multi_depth_analyzer.analyze_folder_structure(root_path, max_depth)
        mappings = []
        
        for file_meta in files:
            # Generate suggested new path based on semantic category
            category_dir = file_meta.semantic_category.replace('/', '_').replace(' ', '_').lower()
            if category_dir == "uncategorized":
                category_dir = "miscellaneous"
            
            # Create new path suggestion
            original_dir = os.path.dirname(file_meta.path)
            file_extension = os.path.splitext(file_meta.name)[1]
            new_filename = f"{file_meta.name}"
            new_path = os.path.join(original_dir, "..", "_organized_by_category", category_dir, new_filename)
            
            # Clean up the path
            new_path = os.path.normpath(new_path)
            
            mapping = {
                "original_path": file_meta.path,
                "original_name": file_meta.name,
                "new_path_suggestion": new_path,
                "semantic_category": file_meta.semantic_category,
                "content_tags": ", ".join(file_meta.content_tags),
                "business_value": file_meta.business_value,
                "depth_level": file_meta.depth_level,
                "file_size": file_meta.size,
                "mime_type": file_meta.mime_type,
                "modification_time": datetime.fromtimestamp(file_meta.modification_time).isoformat(),
                "content_preview": file_meta.content_preview
            }
            mappings.append(mapping)
        
        return mappings
    
    def suggest_improvements(self, root_path: str, max_depth: int = 5) -> Dict[str, Any]:
        """Provide improvement suggestions for the folder structure."""
        files = self.multi_depth_analyzer.analyze_folder_structure(root_path, max_depth)
        
        # Analyze current organization
        extensions = defaultdict(int)
        categories = defaultdict(int)
        depths = defaultdict(int)
        sizes = [f.size for f in files]
        
        for file_meta in files:
            extensions[file_meta.extension] += 1
            categories[file_meta.semantic_category] += 1
            depths[file_meta.depth_level] += 1
        
        # Calculate statistics
        total_files = len(files)
        total_size = sum(sizes)
        avg_size = total_size / total_files if total_files > 0 else 0
        
        # Identify potential improvements
        improvements = []
        
        # Suggest consolidation for uncategorized files
        uncategorized_count = categories.get("Uncategorized", 0)
        if uncategorized_count > 0:
            improvements.append(f"Consolidate {uncategorized_count} uncategorized files into appropriate semantic categories")
        
        # Suggest flattening if too deep
        deepest_level = max(depths.keys()) if depths else 0
        if deepest_level > 4:
            improvements.append(f"Consider flattening folder structure - current max depth is {deepest_level}")
        
        # Suggest cleanup for temporary files
        temp_extensions = ['.tmp', '.temp', '.bak', '.old']
        temp_files = sum(extensions[ext] for ext in temp_extensions if ext in extensions)
        if temp_files > 0:
            improvements.append(f"Clean up {temp_files} temporary files ({', '.join([ext for ext in temp_extensions if extensions.get(ext, 0) > 0])})")
        
        # Suggest archival for old files
        old_files = [f for f in files if (datetime.now().timestamp() - f.modification_time) > 365 * 24 * 3600]  # Older than 1 year
        if len(old_files) > 0:
            improvements.append(f"Archive {len(old_files)} files older than 1 year")
        
        return {
            "total_files": total_files,
            "total_size_bytes": total_size,
            "average_file_size_bytes": avg_size,
            "extension_distribution": dict(extensions),
            "category_distribution": dict(categories),
            "depth_distribution": dict(depths),
            "improvement_suggestions": improvements,
            "top_extensions": sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10],
            "top_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]
        }


class ContentOrganizerAgent:
    """Main agent class that orchestrates content organization."""
    
    def __init__(self):
        self.organizational_mapper = OrganizationalMapper()
    
    def analyze_directory(self, directory_path: str, max_depth: int = 5) -> Dict[str, Any]:
        """Analyze a directory with content-awareness in multi-folder depths."""
        print(f"Analyzing directory: {directory_path} with max depth: {max_depth}")
        
        # Validate directory exists
        if not os.path.isdir(directory_path):
            raise ValueError(f"Directory does not exist: {directory_path}")
        
        # Create organizational mapping
        csv_mappings = self.organizational_mapper.create_csv_mapping(directory_path, max_depth)
        
        # Get improvement suggestions
        improvements = self.organizational_mapper.suggest_improvements(directory_path, max_depth)
        
        return {
            "directory_path": directory_path,
            "csv_mappings": csv_mappings,
            "improvements": improvements,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def export_csv_mapping(self, csv_mappings: List[Dict[str, Any]], output_path: str):
        """Export the CSV mapping to a file."""
        if not csv_mappings:
            print("No mappings to export")
            return
        
        fieldnames = csv_mappings[0].keys()
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for mapping in csv_mappings:
                # Handle any values that might cause CSV issues
                safe_mapping = {}
                for key, value in mapping.items():
                    if isinstance(value, (list, dict)):
                        safe_mapping[key] = json.dumps(value)
                    else:
                        safe_mapping[key] = value
                writer.writerow(safe_mapping)
        
        print(f"CSV mapping exported to: {output_path}")
    
    def generate_summary_report(self, analysis_result: Dict[str, Any]) -> str:
        """Generate a summary report of the analysis."""
        improvements = analysis_result['improvements']
        
        report = f"""
Content Organization Analysis Report
====================================

Analysis Performed On: {analysis_result['analysis_timestamp']}
Target Directory: {analysis_result['directory_path']}

Statistics:
-----------
- Total Files Analyzed: {improvements['total_files']}
- Total Size: {improvements['total_size_bytes']:,} bytes ({improvements['total_size_bytes']/1024/1024:.2f} MB)
- Average File Size: {improvements['average_file_size_bytes']:.2f} bytes
- Max Directory Depth Analyzed: {max(improvements['depth_distribution'].keys()) if improvements['depth_distribution'] else 0}

Top 10 File Extensions:
-----------------------
"""
        
        for ext, count in improvements['top_extensions']:
            report += f"- {ext or 'no extension'}: {count} files\n"
        
        report += "\nTop 10 Semantic Categories:\n"
        report += "-" * 30 + "\n"
        
        for cat, count in improvements['top_categories']:
            report += f"- {cat}: {count} files\n"
        
        report += "\nImprovement Suggestions:\n"
        report += "-" * 25 + "\n"
        
        if improvements['improvement_suggestions']:
            for i, suggestion in enumerate(improvements['improvement_suggestions'], 1):
                report += f"{i}. {suggestion}\n"
        else:
            report += "No specific improvements suggested. Folder structure appears well-organized.\n"
        
        return report


def main():
    """Example usage of the Content Organizer Agent."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python content_organizer_agent.py <directory_path> [max_depth]")
        print("Example: python content_organizer_agent.py /Users/steven/Documents 5")
        return
    
    directory_path = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # Initialize the agent
    agent = ContentOrganizerAgent()
    
    try:
        # Perform analysis
        print(f"Starting content-aware analysis of: {directory_path}")
        result = agent.analyze_directory(directory_path, max_depth)
        
        # Generate and print summary report
        report = agent.generate_summary_report(result)
        print(report)
        
        # Export CSV mapping
        csv_output_path = f"organizational_mapping_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        agent.export_csv_mapping(result['csv_mappings'], csv_output_path)
        
        print(f"\nCSV mapping saved to: {csv_output_path}")
        print(f"Total mappings created: {len(result['csv_mappings'])}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()