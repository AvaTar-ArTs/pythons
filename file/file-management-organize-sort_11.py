#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
- /Users/steven/Music/nocTurneMeLoDieS/python/FINAL_ORGANIZED/core_analysis/sort_python_files.py
- /Users/steven/Music/nocTurneMeLoDieS/python/CLEAN_ORGANIZED/core_analysis/sort_python_files.py

Combines the best features and functionality from multiple similar files.
"""

# Imports from all source files
from pathlib import Path
from typing import Dict, List, Tuple
import logging
import os
import re
import shutil

# Documentation from source files
        """Create the sorted directory structure."""
        """Analyze file content to determine its purpose."""
"""
    """Main function to run the sorter."""
        """Classify a file based on its name and content."""
        """Create detailed README files for each category."""
        """Main sorting function."""
        """Move files to their sorted directories."""
        """Get comprehensive file information."""
        """Generate a summary report of the sorting results."""

Python Files Sorter for Music Processing Directory

This script intelligently sorts Python files based on their functionality,
content, and purpose to create a well-organized directory structure.
"""

import os
import shutil
import re
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PythonFileSorter:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.archive_dir = self.base_dir / "Archive"
        self.sorted_dir = self.base_dir / "Sorted"
        
        # Create sorted directory structure
        self.categories = {
            "analysis": "Content Analysis Scripts",
            "transcription": "Transcription and Speech Processing",
            "generation": "Content Generation Scripts", 
            "processing": "File Processing and Conversion",
            "organization": "File Organization and Management",
            "web_scraping": "Web Scraping and Data Extraction",
            "utilities": "Utility and Helper Scripts",
            "experimental": "Experimental and Test Scripts",
            "deprecated": "Deprecated and Old Versions"
        }
        
        # File classification patterns
        self.classification_patterns = {
            "analysis": [
                r"analyze.*\.py$",
                r"analyzer.*\.py$",
                r".*analysis.*\.py$",
                r".*analytics.*\.py$"
            ],
            "transcription": [
                r"trans.*\.py$",
                r"transcript.*\.py$",
                r".*transcribe.*\.py$",
                r".*speech.*\.py$"
            ],
            "generation": [
                r"generate.*\.py$",
                r"gen.*\.py$",
                r".*create.*\.py$",
                r".*build.*\.py$"
            ],
            "processing": [
                r"mp3.*\.py$",
                r"mp4.*\.py$",
                r".*process.*\.py$",
                r".*convert.*\.py$",
                r".*transform.*\.py$"
            ],
            "organization": [
                r"organize.*\.py$",
                r"sort.*\.py$",
                r".*manage.*\.py$",
                r".*structure.*\.py$"
            ],
            "web_scraping": [
                r"suno.*\.py$",
                r".*scrape.*\.py$",
                r".*extract.*\.py$",
                r".*crawl.*\.py$"
            ],
            "utilities": [
                r"util.*\.py$",
                r"helper.*\.py$",
                r".*tool.*\.py$",
                r".*common.*\.py$"
            ]
        }
        
        # Keywords for content analysis
        self.content_keywords = {
            "analysis": ["analyze", "analysis", "analyzer", "analytics", "evaluate", "assess"],
            "transcription": ["transcript", "transcribe", "speech", "audio", "whisper", "openai"],
            "generation": ["generate", "create", "build", "make", "produce", "gen"],
            "processing": ["process", "convert", "transform", "mp3", "mp4", "audio", "video"],
            "organization": ["organize", "sort", "manage", "structure", "arrange"],
            "web_scraping": ["scrape", "extract", "crawl", "suno", "html", "beautifulsoup"],
            "utilities": ["util", "helper", "tool", "common", "shared", "base"]
        }

    def create_directory_structure(self):
        """Create the sorted directory structure."""
        logger.info("Creating directory structure...")
        
        # Create main sorted directory
        self.sorted_dir.mkdir(exist_ok=True)
        
        # Create category directories
        for category, description in self.categories.items():
            category_dir = self.sorted_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Create README for each category
            readme_path = category_dir / "README.md"
            with open(readme_path, 'w') as f:
                f.write(f"# {description}\n\n")
                f.write(f"This directory contains {description.lower()}.\n\n")
                f.write("## Files in this category:\n")
        
        logger.info("Directory structure created successfully")

    def analyze_file_content(self, file_path: Path) -> Dict[str, any]:
        """Analyze file content to determine its purpose."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
        except Exception as e:
            logger.warning(f"Could not read {file_path}: {e}")
            return {"category": "utilities", "confidence": 0.0, "keywords": []}
        
        # Count keyword matches for each category
        category_scores = {}
        found_keywords = []
        
        for category, keywords in self.content_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in content:
                    score += content.count(keyword)
                    found_keywords.append(keyword)
            
            category_scores[category] = score
        
        # Determine best category
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            confidence = category_scores[best_category] / sum(category_scores.values()) if sum(category_scores.values()) > 0 else 0
        else:
            best_category = "utilities"
            confidence = 0.0
        
        return {
            "category": best_category,
            "confidence": confidence,
            "keywords": list(set(found_keywords)),
            "scores": category_scores
        }

    def classify_file(self, file_path: Path) -> str:
        """Classify a file based on its name and content."""
        filename = file_path.name
        
        # First, try pattern matching on filename
        for category, patterns in self.classification_patterns.items():
            for pattern in patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    logger.info(f"Pattern match: {filename} -> {category}")
                    return category
        
        # If no pattern match, analyze content
        content_analysis = self.analyze_file_content(file_path)
        category = content_analysis["category"]
        confidence = content_analysis["confidence"]
        
        logger.info(f"Content analysis: {filename} -> {category} (confidence: {confidence:.2f})")
        
        # If confidence is low, put in experimental
        if confidence < 0.1:
            return "experimental"
        
        return category

    def get_file_info(self, file_path: Path) -> Dict[str, any]:
        """Get comprehensive file information."""
        stat = file_path.stat()
        
        return {
            "name": file_path.name,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "path": str(file_path),
            "extension": file_path.suffix,
            "stem": file_path.stem
        }

    def sort_files(self):
        """Main sorting function."""
        logger.info("Starting file sorting process...")
        
        # Create directory structure
        self.create_directory_structure()
        
        # Find all Python files
        python_files = list(self.archive_dir.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files to sort")
        
        # Process each file
        sorted_files = {}
        for file_path in python_files:
            try:
                # Skip if it's already in a subdirectory we want to preserve
                if any(part in str(file_path) for part in ["sora-video-generator", "suno-analytics"]):
                    continue
                
                # Classify the file
                category = self.classify_file(file_path)
                
                # Get file info
                file_info = self.get_file_info(file_path)
                file_info["category"] = category
                
                # Store for processing
                if category not in sorted_files:
                    sorted_files[category] = []
                sorted_files[category].append(file_info)
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue
        
        # Move files to appropriate directories
        self.move_files(sorted_files)
        
        # Generate summary report
        self.generate_summary_report(sorted_files)
        
        logger.info("File sorting completed successfully!")

    def move_files(self, sorted_files: Dict[str, List[Dict]]):
        """Move files to their sorted directories."""
        logger.info("Moving files to sorted directories...")
        
        for category, files in sorted_files.items():
            category_dir = self.sorted_dir / category
            
            for file_info in files:
                source_path = Path(file_info["path"])
                dest_path = category_dir / file_info["name"]
                
                try:
                    # Handle duplicate names
                    counter = 1
                    original_dest = dest_path
                    while dest_path.exists():
                        stem = original_dest.stem
                        suffix = original_dest.suffix
                        dest_path = category_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    # Move the file
                    shutil.move(str(source_path), str(dest_path))
                    logger.info(f"Moved: {file_info['name']} -> {category}/")
                    
                except Exception as e:
                    logger.error(f"Error moving {file_info['name']}: {e}")

    def generate_summary_report(self, sorted_files: Dict[str, List[Dict]]):
        """Generate a summary report of the sorting results."""
        report_path = self.sorted_dir / "SORTING_REPORT.md"
        
        with open(report_path, 'w') as f:
            f.write("# Python Files Sorting Report\n\n")
            f.write(f"Generated on: {os.popen('date').read().strip()}\n\n")
            
            f.write("## Summary\n\n")
            total_files = sum(len(files) for files in sorted_files.values())
            f.write(f"Total files sorted: {total_files}\n\n")
            
            f.write("## Categories\n\n")
            for category, files in sorted_files.items():
                f.write(f"### {self.categories[category]}\n")
                f.write(f"Files: {len(files)}\n\n")
                
                for file_info in files:
                    f.write(f"- `{file_info['name']}` ({file_info['size']} bytes)\n")
                
                f.write(Path("\n"))
            
            f.write("## Directory Structure\n\n")
            f.write("```\n")
            f.write("Sorted/\n")
            for category in sorted_files.keys():
                f.write(f"├── {category}/\n")
                f.write(f"│   ├── README.md\n")
                for file_info in sorted_files[category]:
                    f.write(f"│   ├── {file_info['name']}\n")
                f.write(f"│   └── ...\n")
            f.write("└── SORTING_REPORT.md\n")
            f.write("```\n")
        
        logger.info(f"Summary report generated: {report_path}")

    def create_category_readmes(self, sorted_files: Dict[str, List[Dict]]):
        """Create detailed README files for each category."""
        for category, files in sorted_files.items():
            readme_path = self.sorted_dir / category / "README.md"
            
            with open(readme_path, 'w') as f:
                f.write(f"# {self.categories[category]}\n\n")
                f.write(f"This directory contains {len(files)} Python files related to {self.categories[category].lower()}.\n\n")
                
                f.write("## Files\n\n")
                for file_info in sorted(files, key=lambda x: x['name']):
                    f.write(f"### {file_info['name']}\n")
                    f.write(f"- **Size:** {file_info['size']} bytes\n")
                    f.write(f"- **Modified:** {file_info['modified']}\n")
                    f.write(f"- **Original Path:** {file_info['path']}\n\n")

def main():
    """Main function to run the sorter."""
    base_dir = Path("/Users/steven/Music/nocTurneMeLoDieS/python")
    
    if not os.path.exists(base_dir):
        logger.error(f"Base directory not found: {base_dir}")
        return
    
    sorter = PythonFileSorter(base_dir)
    sorter.sort_files()
    
    logger.info("\n✅ Python files sorting completed!")
    logger.info(f"📁 Sorted files are in: {sorter.sorted_dir}")
    logger.info(f"📊 Check SORTING_REPORT.md for detailed information")

if __name__ == "__main__":
    main()