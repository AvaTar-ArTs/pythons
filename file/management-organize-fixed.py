"""
File Management Organize Fixed 2

This module provides functionality for file management organize fixed 2.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_300 = 300
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Fixed Comprehensive Chat Analysis Organizer
Handles long filenames and organizes all chat analysis content
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib


class FixedChatOrganizer:
    def __init__(self, source_dir, target_dir):
        """__init__ function."""

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.all_files = []
        self.organized_content = {"projects": {}, "topics": {}, "file_types": {}, "timeline": [], "statistics": {}}

    def sanitize_filename(self, filename, max_length=CONSTANT_100):
        """Sanitize filename for filesystem with length limit"""
        # Remove or replace problematic characters
        sanitized = re.sub(r'[<>:"/\\\\|?*\\n\\r]', "_", filename)
        sanitized = re.sub(r"\\s+", "_", sanitized)  # Replace multiple spaces with underscore
        sanitized = sanitized.strip("._")  # Remove leading/trailing dots and underscores

        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[: max_length - 10] + "_truncated"

        return sanitized or "unnamed"

    def scan_all_files(self):
        """Scan all files in the chat analysis directory"""
        logger.info("🔍 Scanning all chat analysis files...")

        if not self.source_dir.exists():
            logger.info(f"❌ Source directory not found: {self.source_dir}")
            return

        # Scan all files recursively
        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".md", ".html", ".txt", ".json", ".csv"]:
                logger.info(f"   📄 Found: {file_path.relative_to(self.source_dir)}")

                try:
                    file_info = self.analyze_file(file_path)
                    if file_info:
                        self.all_files.append(file_info)
                except Exception as e:
                    logger.info(f"      ❌ Error analyzing {file_path.name}: {e}")

        logger.info(f"\\n📊 Total files found: {len(self.all_files)}")

    def analyze_file(self, file_path):
        """Analyze a single file and extract metadata"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            file_info = {
                "path": str(file_path),
                "relative_path": str(file_path.relative_to(self.source_dir)),
                "name": file_path.name,
                "extension": file_path.suffix,
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                "created": datetime.fromtimestamp(file_path.stat().st_ctime),
                "word_count": len(content.split()),
                "line_count": len(content.splitlines()),
                "content_hash": hashlib.md5(content.encode()).hexdigest(),
                "projects": self.extract_projects(content),
                "topics": self.extract_topics(content),
                "file_type": self.classify_file_type(file_path, content),
                "content_preview": content[:CONSTANT_300] + "..." if len(content) > CONSTANT_300 else content,
            }

            return file_info

        except Exception as e:
            logger.info(f"      ❌ Error reading {file_path.name}: {e}")
            return None

    def extract_projects(self, content):
        """Extract project names from content"""
        projects = set()

        # Common project patterns
        project_patterns = [
            r"Dr\\.?\\s*Adu.*?Project",
            r"Gainesville\\s*Psychiatry.*?Project",
            r"SEO\\s*Optimization.*?Project",
            r"(\\w+)\\s*SEO\\s*Project",
            r"(\\w+)\\s*Website\\s*Project",
            r"(\\w+)\\s*Analysis\\s*Project",
            r"Project:\\s*([^\\n]+)",
            r"#\\s*([^#\\n]+)\\s*Project",
            r"Digital Dive Framework",
            r"Chat Analysis",
            r"SEO Project",
            r"Website Optimization",
        ]

        for pattern in project_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                clean_match = match.strip()[:50]  # Limit length
                if clean_match:
                    projects.add(clean_match)

        return list(projects)

    def extract_topics(self, content):
        """Extract topics and keywords from content"""
        topics = set()

        # Topic patterns
        topic_patterns = {
            "seo": r"\\b(?:SEO|search engine optimization|meta tags|keywords|ranking)\\b",
            "psychiatry": r"\\b(?:psychiatry|psychiatrist|mental health|TMS therapy|forensic psychiatry)\\b",
            "web_development": r"\\b(?:HTML|CSS|JavaScript|website|web development|frontend|backend)\\b",
            "business": r"\\b(?:business|marketing|strategy|analysis|report)\\b",
            "technical": r"\\b(?:technical|implementation|code|programming|development)\\b",
            "design": r"\\b(?:design|UI|UX|visual|graphics|layout)\\b",
            "content": r"\\b(?:content|writing|copy|text|article|blog)\\b",
            "analytics": r"\\b(?:analytics|data|metrics|performance|tracking)\\b",
            "chat_analysis": r"\\b(?:chat|analysis|conversation|discussion)\\b",
            "digital_dive": r"\\b(?:digital dive|framework|narrative)\\b",
        }

        for topic, pattern in topic_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                topics.add(topic)

        return list(topics)

    def classify_file_type(self, file_path, content):
        """Classify the type of file based on content and name"""
        name_lower = file_path.name.lower()
        content_lower = content.lower()

        if "invoice" in name_lower or "pricing" in name_lower:
            return "invoice"
        elif "report" in name_lower or "analysis" in name_lower:
            return "report"
        elif "comparison" in name_lower or "before" in name_lower:
            return "comparison"
        elif "client" in name_lower or "non_technical" in name_lower:
            return "client_facing"
        elif "technical" in name_lower or "implementation" in name_lower:
            return "technical"
        elif "seo" in name_lower or "optimization" in name_lower:
            return "seo"
        elif "visual" in name_lower or "html" in name_lower:
            return "visual"
        elif file_path.suffix == ".html":
            return "html"
        elif file_path.suffix == ".md":
            return "markdown"
        elif file_path.suffix == ".json":
            return "json"
        elif file_path.suffix == ".csv":
            return "csv"
        else:
            return "other"

    def organize_content(self):
        """Organize content by projects, topics, and file types"""
        logger.info("\\n📁 Organizing content...")

        # Organize by projects
        for file_info in self.all_files:
            for project in file_info["projects"]:
                sanitized_project = self.sanitize_filename(project, 50)
                if sanitized_project not in self.organized_content["projects"]:
                    self.organized_content["projects"][sanitized_project] = []
                self.organized_content["projects"][sanitized_project].append(file_info)

        # Organize by topics
        for file_info in self.all_files:
            for topic in file_info["topics"]:
                if topic not in self.organized_content["topics"]:
                    self.organized_content["topics"][topic] = []
                self.organized_content["topics"][topic].append(file_info)

        # Organize by file types
        for file_info in self.all_files:
            file_type = file_info["file_type"]
            if file_type not in self.organized_content["file_types"]:
                self.organized_content["file_types"][file_type] = []
            self.organized_content["file_types"][file_type].append(file_info)

        # Create timeline
        self.organized_content["timeline"] = sorted(self.all_files, key=lambda x: x["modified"], reverse=True)

        # Generate statistics
        self.generate_statistics()

    def generate_statistics(self):
        """Generate comprehensive statistics"""
        stats = {
            "total_files": len(self.all_files),
            "total_size": sum(f["size"] for f in self.all_files),
            "total_words": sum(f["word_count"] for f in self.all_files),
            "file_types": {},
            "projects_count": len(self.organized_content["projects"]),
            "topics_count": len(self.organized_content["topics"]),
            "date_range": {
                "earliest": min(f["created"] for f in self.all_files).isoformat(),
                "latest": max(f["modified"] for f in self.all_files).isoformat(),
            },
        }

        # File type statistics
        for file_type, files in self.organized_content["file_types"].items():
            stats["file_types"][file_type] = {
                "count": len(files),
                "total_size": sum(f["size"] for f in files),
                "total_words": sum(f["word_count"] for f in files),
            }

        self.organized_content["statistics"] = stats

    def create_organized_structure(self):
        """Create organized directory structure"""
        logger.info("\\n🏗️ Creating organized directory structure...")

        # Create main directories
        main_dirs = ["01_Projects", "02_File_Types", "03_Topics", "04_Timeline", "05_Statistics", "06_Exports"]

        for dir_name in main_dirs:
            (self.target_dir / dir_name).mkdir(exist_ok=True)

        # Create project directories (with sanitized names)
        for project in self.organized_content["projects"].keys():
            project_dir = self.target_dir / "01_Projects" / project
            project_dir.mkdir(exist_ok=True)

        # Create file type directories
        for file_type in self.organized_content["file_types"].keys():
            type_dir = self.target_dir / "02_File_Types" / file_type
            type_dir.mkdir(exist_ok=True)

        # Create topic directories
        for topic in self.organized_content["topics"].keys():
            topic_dir = self.target_dir / "03_Topics" / topic
            topic_dir.mkdir(exist_ok=True)

    def copy_files_to_organized_structure(self):
        """Copy files to their organized locations"""
        logger.info("\\n📋 Copying files to organized structure...")

        # Copy to project directories
        for project, files in self.organized_content["projects"].items():
            project_dir = self.target_dir / "01_Projects" / project
            for file_info in files:
                self.copy_file_to_directory(file_info, project_dir)

        # Copy to file type directories
        for file_type, files in self.organized_content["file_types"].items():
            type_dir = self.target_dir / "02_File_Types" / file_type
            for file_info in files:
                self.copy_file_to_directory(file_info, type_dir)

        # Copy to topic directories
        for topic, files in self.organized_content["topics"].items():
            topic_dir = self.target_dir / "03_Topics" / topic
            for file_info in files:
                self.copy_file_to_directory(file_info, topic_dir)

    def copy_file_to_directory(self, file_info, target_dir):
        """Copy a file to a target directory with organized naming"""
        source_path = Path(file_info["path"])

        # Create organized filename
        timestamp = file_info["modified"].strftime("%Y%m%d_%H%M%S")
        safe_name = self.sanitize_filename(file_info["name"], 80)
        organized_name = f"{timestamp}_{safe_name}"
        target_path = target_dir / organized_name

        try:
            shutil.copy2(source_path, target_path)
            logger.info(f"   ✅ Copied: {file_info['name'][:50]}... -> {target_dir.name}")
        except Exception as e:
            logger.info(f"   ❌ Error copying {file_info['name']}: {e}")

    def generate_reports(self):
        """Generate comprehensive reports"""
        logger.info("\\n📊 Generating reports...")

        # Generate master index
        self.generate_master_index()

        # Generate project reports
        self.generate_project_reports()

        # Generate topic reports
        self.generate_topic_reports()

        # Generate file type reports
        self.generate_file_type_reports()

        # Generate timeline report
        self.generate_timeline_report()

        # Generate statistics report
        self.generate_statistics_report()

    def generate_master_index(self):
        """Generate master index file"""
        index_path = self.target_dir / "MASTER_INDEX.md"

        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# Comprehensive Chat Analysis - Master Index\\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

            f.write("## Overview\\n")
            f.write(f"- **Total Files:** {self.organized_content['statistics']['total_files']}\\n")
            f.write(f"- **Total Size:** {self.organized_content['statistics']['total_size']:,} bytes\\n")
            f.write(f"- **Total Words:** {self.organized_content['statistics']['total_words']:,}\\n")
            f.write(f"- **Projects:** {self.organized_content['statistics']['projects_count']}\\n")
            f.write(f"- **Topics:** {self.organized_content['statistics']['topics_count']}\\n\\n")

            f.write("## Directory Structure\\n")
            f.write("```\\n")
            f.write("01_Projects/          # Files organized by project\\n")
            f.write("02_File_Types/        # Files organized by type\\n")
            f.write("03_Topics/            # Files organized by topic\\n")
            f.write("04_Timeline/          # Files organized by date\\n")
            f.write("05_Statistics/        # Analysis reports\\n")
            f.write("06_Exports/           # Export files\\n")
            f.write("```\\n\\n")

            f.write("## Projects\\n")
            for project, files in self.organized_content["projects"].items():
                f.write(f"- **{project}:** {len(files)} files\\n")

            f.write("\\n## File Types\\n")
            for file_type, stats in self.organized_content["statistics"]["file_types"].items():
                f.write(f"- **{file_type}:** {stats['count']} files ({stats['total_size']:,} bytes)\\n")

    def generate_project_reports(self):
        """Generate individual project reports"""
        for project, files in self.organized_content["projects"].items():
            report_path = self.target_dir / "01_Projects" / project / f"{project}_REPORT.md"

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# {project} - Project Report\\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

                f.write(f"## Project Overview\\n")
                f.write(f"- **Total Files:** {len(files)}\\n")
                f.write(f"- **Total Size:** {sum(f['size'] for f in files):,} bytes\\n")
                f.write(f"- **Total Words:** {sum(f['word_count'] for f in files):,}\\n\\n")

                f.write("## Files in Project\\n")
                for file_info in sorted(files, key=lambda x: x["modified"], reverse=True):
                    f.write(f"### {file_info['name']}\\n")
                    f.write(f"- **Type:** {file_info['file_type']}\\n")
                    f.write(f"- **Size:** {file_info['size']:,} bytes\\n")
                    f.write(f"- **Words:** {file_info['word_count']:,}\\n")
                    f.write(f"- **Modified:** {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\\n")
                    f.write(f"- **Topics:** {', '.join(file_info['topics'])}\\n\\n")

    def generate_topic_reports(self):
        """Generate topic reports"""
        for topic, files in self.organized_content["topics"].items():
            report_path = self.target_dir / "03_Topics" / topic / f"{topic}_REPORT.md"

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# {topic.title()} - Topic Report\\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

                f.write(f"## Topic Overview\\n")
                f.write(f"- **Total Files:** {len(files)}\\n")
                f.write(f"- **Total Size:** {sum(f['size'] for f in files):,} bytes\\n")
                f.write(f"- **Total Words:** {sum(f['word_count'] for f in files):,}\\n\\n")

                f.write("## Files by Topic\\n")
                for file_info in sorted(files, key=lambda x: x["modified"], reverse=True):
                    f.write(f"### {file_info['name']}\\n")
                    f.write(f"- **Projects:** {', '.join(file_info['projects'])}\\n")
                    f.write(f"- **Type:** {file_info['file_type']}\\n")
                    f.write(f"- **Modified:** {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

    def generate_file_type_reports(self):
        """Generate file type reports"""
        for file_type, files in self.organized_content["file_types"].items():
            report_path = self.target_dir / "02_File_Types" / file_type / f"{file_type}_REPORT.md"

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# {file_type.title()} - File Type Report\\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

                f.write(f"## File Type Overview\\n")
                f.write(f"- **Total Files:** {len(files)}\\n")
                f.write(f"- **Total Size:** {sum(f['size'] for f in files):,} bytes\\n")
                f.write(f"- **Total Words:** {sum(f['word_count'] for f in files):,}\\n\\n")

                f.write("## Files by Type\\n")
                for file_info in sorted(files, key=lambda x: x["modified"], reverse=True):
                    f.write(f"### {file_info['name']}\\n")
                    f.write(f"- **Projects:** {', '.join(file_info['projects'])}\\n")
                    f.write(f"- **Topics:** {', '.join(file_info['topics'])}\\n")
                    f.write(f"- **Modified:** {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

    def generate_timeline_report(self):
        """Generate timeline report"""
        timeline_path = self.target_dir / "04_Timeline" / "TIMELINE_REPORT.md"

        with open(timeline_path, "w", encoding="utf-8") as f:
            f.write("# Timeline Report\\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

            f.write("## Files by Date (Most Recent First)\\n")
            for file_info in self.organized_content["timeline"]:
                f.write(f"### {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')} - {file_info['name']}\\n")
                f.write(f"- **Projects:** {', '.join(file_info['projects'])}\\n")
                f.write(f"- **Topics:** {', '.join(file_info['topics'])}\\n")
                f.write(f"- **Type:** {file_info['file_type']}\\n")
                f.write(f"- **Size:** {file_info['size']:,} bytes\\n\\n")

    def generate_statistics_report(self):
        """Generate comprehensive statistics report"""
        stats_path = self.target_dir / "05_Statistics" / "STATISTICS_REPORT.md"

        with open(stats_path, "w", encoding="utf-8") as f:
            f.write("# Comprehensive Statistics Report\\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

            stats = self.organized_content["statistics"]

            f.write("## Overall Statistics\\n")
            f.write(f"- **Total Files:** {stats['total_files']}\\n")
            f.write(
                f"- **Total Size:** {stats['total_size']:,} bytes ({stats['total_size']/CONSTANT_1024/CONSTANT_1024:.2f} MB)\\n"
            )
            f.write(f"- **Total Words:** {stats['total_words']:,}\\n")
            f.write(f"- **Projects:** {stats['projects_count']}\\n")
            f.write(f"- **Topics:** {stats['topics_count']}\\n")
            f.write(f"- **Date Range:** {stats['date_range']['earliest']} to {stats['date_range']['latest']}\\n\\n")

            f.write("## File Type Breakdown\\n")
            for file_type, type_stats in stats["file_types"].items():
                f.write(f"### {file_type.title()}\\n")
                f.write(f"- **Count:** {type_stats['count']}\\n")
                f.write(f"- **Total Size:** {type_stats['total_size']:,} bytes\\n")
                f.write(f"- **Total Words:** {type_stats['total_words']:,}\\n")
                f.write(f"- **Average Size:** {type_stats['total_size']//type_stats['count']:,} bytes\\n\\n")

    def export_to_json(self):
        """Export organized data to JSON"""
        json_path = self.target_dir / "06_Exports" / "organized_data.json"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.organized_content, f, indent=2, default=str)

        logger.info(f"   ✅ JSON export saved: {json_path}")

    def run_organization(self):
        """Run the complete organization process"""
        logger.info("🚀 Starting Fixed Comprehensive Chat Analysis Organization...")

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Run organization steps
        self.scan_all_files()
        self.organize_content()
        self.create_organized_structure()
        self.copy_files_to_organized_structure()
        self.generate_reports()
        self.export_to_json()

        logger.info(f"\\n✅ Organization Complete!")
        logger.info(f"📁 Organized content saved to: {self.target_dir}")
        logger.info(f"📋 Check MASTER_INDEX.md for navigation")


def main():
    """Main execution function"""
    source_dir = "/Users/steven/Documents/cursor-agent/chat_analysis "
    target_dir = Path("/Users/steven/COMPREHENSIVE_CHAT_ORGANIZATION")

    organizer = FixedChatOrganizer(source_dir, target_dir)
    organizer.run_organization()


if __name__ == "__main__":
    main()
