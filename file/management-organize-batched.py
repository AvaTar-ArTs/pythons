"""
File Management Organize Batched 3

This module provides functionality for file management organize batched 3.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200
CONSTANT_1024 = 1024
CONSTANT_10000 = 10000

#!/usr/bin/env python3
"""
Batched Content-Aware Chat Analysis Organizer
Processes files in batches to avoid massive file sizes
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib


class BatchedContentAnalyzer:
    def __init__(self, source_dir, target_dir, batch_size=10):
        """__init__ function."""

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.batch_size = batch_size
        self.all_files = []
        self.batch_results = []

    def analyze_chat_structure(self, content):
        """Analyze the structure of a chat analysis file"""
        patterns = {
            "chat_id": r"Chat ID.*?`([^`]+)`",
            "agent_id": r"Agent ID.*?`([^`]+)`",
            "created": r"Created.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
            "mode": r"Mode.*?(\w+)",
            "model": r"Model.*?(\w+)",
            "total_messages": r"Total Messages.*?(\d+)",
            "total_blobs": r"Total Blobs.*?(\d+)",
            "tool_calls": r"Tool Calls.*?(\d+)",
            "code_blocks": r"Code Blocks.*?(\d+)",
            "file_operations": r"File Operations.*?(\d+)",
            "terminal_commands": r"Terminal Commands.*?(\d+)",
        }

        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                extracted[key] = match.group(1)

        return extracted

    def extract_code_blocks(self, content, max_blocks=5):
        """Extract and categorize code blocks from content (limited)"""
        code_blocks = []

        # Find all code blocks
        code_pattern = r"```(\w+)?\n(.*?)\n```"
        matches = re.findall(code_pattern, content, re.DOTALL)

        # Limit to max_blocks to prevent huge files
        for i, (language, code) in enumerate(matches[:max_blocks]):
            if not language:
                language = "unknown"

            # Truncate very large code blocks
            if len(code) > CONSTANT_10000:
                code = code[:CONSTANT_10000] + "\n... [TRUNCATED]"

            code_info = {
                "index": i,
                "language": language,
                "code": code.strip(),
                "size": len(code),
                "lines": len(code.split("\n")),
                "type": self.classify_code_type(code, language),
            }
            code_blocks.append(code_info)

        return code_blocks

    def classify_code_type(self, code, language):
        """Classify the type of code based on content"""
        code_lower = code.lower()

        if "userscript" in code_lower or "tampermonkey" in code_lower:
            return "userscript"
        elif "function" in code_lower and "javascript" in language.lower():
            return "javascript_function"
        elif "class " in code_lower or "def " in code_lower:
            return "class_definition"
        elif "import " in code_lower or "from " in code_lower:
            return "imports"
        elif "html" in language.lower() or "<html" in code_lower:
            return "html_template"
        elif "css" in language.lower() or "style" in code_lower:
            return "styling"
        elif "json" in language.lower() or "{" in code and "}" in code:
            return "configuration"
        elif "bash" in language.lower() or "shell" in language.lower():
            return "shell_script"
        else:
            return "general_code"

    def extract_tool_calls(self, content, max_calls=10):
        """Extract tool call information (limited)"""
        tool_calls = []

        # Find tool call sections
        tool_pattern = r"### 🛠️ Message \d+ - TOOL.*?\n\n(.*?)(?=---|\n###|\Z)"
        tool_matches = re.findall(tool_pattern, content, re.DOTALL)

        # Limit to max_calls
        for tool_content in tool_matches[:max_calls]:
            # Extract tool type
            tool_type_match = re.search(r"Tool Result: (\w+)", tool_content)
            tool_type = tool_type_match.group(1) if tool_type_match else "unknown"

            # Extract tool ID
            id_match = re.search(r"ID: `([^`]+)`", tool_content)
            tool_id = id_match.group(1) if id_match else "unknown"

            # Extract size
            size_match = re.search(r"Size: (\d+) bytes", tool_content)
            size = int(size_match.group(1)) if size_match else 0

            tool_info = {
                "tool_type": tool_type,
                "tool_id": tool_id,
                "size": size,
                "content_preview": (
                    tool_content[:CONSTANT_200] + "..." if len(tool_content) > CONSTANT_200 else tool_content
                ),
            }
            tool_calls.append(tool_info)

        return tool_calls

    def identify_projects(self, content, filename):
        """Identify projects from content and filename"""
        projects = set()

        # Project patterns from content
        project_patterns = [
            r"Dr\.?\s*Adu.*?Project",
            r"Gainesville\s*Psychiatry.*?Project",
            r"SEO\s*Optimization.*?Project",
            r"(\w+)\s*SEO\s*Project",
            r"(\w+)\s*Website\s*Project",
            r"(\w+)\s*Analysis\s*Project",
            r"Project:\s*([^\n]+)",
            r"#\s*([^#\n]+)\s*Project",
            r"Digital Dive Framework",
            r"Chat Analysis",
            r"Script Optimizer",
            r"Analyze Sort",
            r"Universal Chat Exporter",
            r"Export Claude\.Ai",
            r"Chat Exporter",
            r"Content Analysis",
            r"File Organization",
            r"Data Processing",
        ]

        for pattern in project_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                clean_match = match.strip()[:50]
                if clean_match:
                    projects.add(clean_match)

        # Extract from filename patterns
        filename_lower = filename.lower()
        if "chat_" in filename_lower:
            # Extract chat ID and try to infer project
            chat_id = filename.split("_")[1] if "_" in filename else "unknown"
            projects.add(f"Chat_{chat_id}")

        return list(projects)

    def categorize_content(self, content, filename):
        """Categorize content based on analysis"""
        categories = set()

        # Content analysis patterns
        patterns = {
            "seo_optimization": [
                r"SEO",
                r"search engine optimization",
                r"meta tags",
                r"keywords",
                r"ranking",
                r"optimization",
                r"Dr\.?\s*Adu",
                r"Gainesville\s*Psychiatry",
            ],
            "web_development": [
                r"HTML",
                r"CSS",
                r"JavaScript",
                r"website",
                r"web development",
                r"frontend",
                r"backend",
                r"userscript",
                r"tampermonkey",
            ],
            "data_analysis": [
                r"analysis",
                r"statistics",
                r"data",
                r"metrics",
                r"performance",
                r"tracking",
                r"analytics",
                r"csv",
                r"json",
            ],
            "automation": [
                r"automation",
                r"script",
                r"tool",
                r"export",
                r"import",
                r"batch",
                r"processing",
                r"terminal",
            ],
            "content_creation": [
                r"content",
                r"writing",
                r"copy",
                r"text",
                r"article",
                r"blog",
                r"creative",
                r"narrative",
            ],
            "file_management": [r"file", r"directory", r"folder", r"organize", r"sort", r"structure", r"management"],
            "chat_analysis": [
                r"chat",
                r"conversation",
                r"message",
                r"discussion",
                r"analysis",
                r"export",
                r"conversation",
            ],
        }

        content_lower = content.lower()
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    categories.add(category)
                    break

        return list(categories)

    def analyze_single_file(self, file_path):
        """Perform deep analysis of a single file (with limits)"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Basic file info
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
            }

            # Deep analysis (with limits)
            file_info["chat_structure"] = self.analyze_chat_structure(content)
            file_info["code_blocks"] = self.extract_code_blocks(content, max_blocks=3)  # Limit code blocks
            file_info["tool_calls"] = self.extract_tool_calls(content, max_calls=5)  # Limit tool calls
            file_info["projects"] = self.identify_projects(content, file_path.name)
            file_info["categories"] = self.categorize_content(content, file_path.name)

            # Extract chat ID for relationships
            file_info["chat_id"] = file_info["chat_structure"].get("chat_id", "unknown")

            return file_info

        except Exception as e:
            logger.info(f"      ❌ Error analyzing {file_path.name}: {e}")
            return None

    def process_batch(self, file_batch, batch_number):
        """Process a batch of files"""
        logger.info(f"\n📦 Processing Batch {batch_number} ({len(file_batch)} files)...")

        batch_results = {
            "batch_number": batch_number,
            "files": [],
            "projects": set(),
            "categories": set(),
            "code_types": set(),
            "tool_types": set(),
            "statistics": {"total_files": len(file_batch), "total_size": 0, "total_words": 0},
        }

        for file_path in file_batch:
            logger.info(f"   📄 Analyzing: {file_path.relative_to(self.source_dir)}")
            file_analysis = self.analyze_single_file(file_path)
            if file_analysis:
                batch_results["files"].append(file_analysis)
                batch_results["projects"].update(file_analysis.get("projects", []))
                batch_results["categories"].update(file_analysis.get("categories", []))

                for code_block in file_analysis.get("code_blocks", []):
                    batch_results["code_types"].add(code_block.get("type", "unknown"))

                for tool_call in file_analysis.get("tool_calls", []):
                    batch_results["tool_types"].add(tool_call.get("tool_type", "unknown"))

                batch_results["statistics"]["total_size"] += file_analysis["size"]
                batch_results["statistics"]["total_words"] += file_analysis["word_count"]

        # Convert sets to lists for JSON serialization
        batch_results["projects"] = list(batch_results["projects"])
        batch_results["categories"] = list(batch_results["categories"])
        batch_results["code_types"] = list(batch_results["code_types"])
        batch_results["tool_types"] = list(batch_results["tool_types"])

        return batch_results

    def save_batch_results(self, batch_results):
        """Save batch results to individual files"""
        batch_dir = self.target_dir / "07_Exports" / "batches"
        batch_dir.mkdir(parents=True, exist_ok=True)

        # Save batch JSON
        batch_file = batch_dir / f"batch_{batch_results['batch_number']:03d}.json"
        with open(batch_file, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, indent=2, default=str)

        # Save batch summary
        summary_file = batch_dir / f"batch_{batch_results['batch_number']:03d}_summary.md"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"# Batch {batch_results['batch_number']} Analysis Summary\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Batch Overview\n")
            f.write(f"- **Files Processed:** {batch_results['statistics']['total_files']}\n")
            f.write(f"- **Total Size:** {batch_results['statistics']['total_size']:,} bytes\n")
            f.write(f"- **Total Words:** {batch_results['statistics']['total_words']:,}\n\n")

            f.write("## Projects Found\n")
            for project in batch_results["projects"]:
                f.write(f"- {project}\n")

            f.write("\n## Categories Found\n")
            for category in batch_results["categories"]:
                f.write(f"- {category}\n")

            f.write("\n## Code Types Found\n")
            for code_type in batch_results["code_types"]:
                f.write(f"- {code_type}\n")

            f.write("\n## Tool Types Found\n")
            for tool_type in batch_results["tool_types"]:
                f.write(f"- {tool_type}\n")

        logger.info(f"   ✅ Batch {batch_results['batch_number']} saved: {batch_file}")

    def scan_all_files_batched(self):
        """Scan and analyze all files in batches"""
        logger.info("🔍 Performing batched content-aware analysis...")

        if not self.source_dir.exists():
            logger.info(f"❌ Source directory not found: {self.source_dir}")
            return

        # Get all files first
        all_file_paths = []
        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [".md", ".html", ".txt", ".json", ".csv"]:
                all_file_paths.append(file_path)

        logger.info(f"📊 Total files to process: {len(all_file_paths)}")
        logger.info(f"📦 Processing in batches of {self.batch_size}")

        # Process in batches
        total_batches = (len(all_file_paths) + self.batch_size - 1) // self.batch_size

        for i in range(0, len(all_file_paths), self.batch_size):
            batch_number = (i // self.batch_size) + 1
            file_batch = all_file_paths[i : i + self.batch_size]

            logger.info(f"\n🔄 Processing batch {batch_number}/{total_batches}")
            batch_results = self.process_batch(file_batch, batch_number)
            self.batch_results.append(batch_results)
            self.save_batch_results(batch_results)

            # Add to all_files for summary
            self.all_files.extend(batch_results["files"])

        logger.info(f"\n📊 Total files analyzed: {len(self.all_files)}")
        logger.info(f"📦 Total batches processed: {len(self.batch_results)}")

    def generate_master_summary(self):
        """Generate master summary from all batches"""
        logger.info("\n📊 Generating master summary...")

        # Aggregate statistics from all batches
        master_stats = {
            "total_files": len(self.all_files),
            "total_size": sum(f["size"] for f in self.all_files),
            "total_words": sum(f["word_count"] for f in self.all_files),
            "total_batches": len(self.batch_results),
            "unique_projects": set(),
            "unique_categories": set(),
            "unique_code_types": set(),
            "unique_tool_types": set(),
        }

        for batch in self.batch_results:
            master_stats["unique_projects"].update(batch["projects"])
            master_stats["unique_categories"].update(batch["categories"])
            master_stats["unique_code_types"].update(batch["code_types"])
            master_stats["unique_tool_types"].update(batch["tool_types"])

        # Convert sets to lists
        master_stats["unique_projects"] = list(master_stats["unique_projects"])
        master_stats["unique_categories"] = list(master_stats["unique_categories"])
        master_stats["unique_code_types"] = list(master_stats["unique_code_types"])
        master_stats["unique_tool_types"] = list(master_stats["unique_tool_types"])

        # Save master summary
        master_file = self.target_dir / "MASTER_SUMMARY.json"
        with open(master_file, "w", encoding="utf-8") as f:
            json.dump(master_stats, f, indent=2, default=str)

        # Save master report
        report_file = self.target_dir / "MASTER_BATCHED_REPORT.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Batched Content-Aware Chat Analysis - Master Report\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Analysis Overview\n")
            f.write(f"- **Total Files:** {master_stats['total_files']}\n")
            f.write(
                f"- **Total Size:** {master_stats['total_size']:,} bytes ({master_stats['total_size']/CONSTANT_1024/CONSTANT_1024:.2f} MB)\n"
            )
            f.write(f"- **Total Words:** {master_stats['total_words']:,}\n")
            f.write(f"- **Total Batches:** {master_stats['total_batches']}\n")
            f.write(f"- **Unique Projects:** {len(master_stats['unique_projects'])}\n")
            f.write(f"- **Unique Categories:** {len(master_stats['unique_categories'])}\n")
            f.write(f"- **Unique Code Types:** {len(master_stats['unique_code_types'])}\n")
            f.write(f"- **Unique Tool Types:** {len(master_stats['unique_tool_types'])}\n\n")

            f.write("## All Projects Found\n")
            for project in sorted(master_stats["unique_projects"]):
                f.write(f"- {project}\n")

            f.write("\n## All Categories Found\n")
            for category in sorted(master_stats["unique_categories"]):
                f.write(f"- {category}\n")

            f.write("\n## All Code Types Found\n")
            for code_type in sorted(master_stats["unique_code_types"]):
                f.write(f"- {code_type}\n")

            f.write("\n## All Tool Types Found\n")
            for tool_type in sorted(master_stats["unique_tool_types"]):
                f.write(f"- {tool_type}\n")

            f.write("\n## Batch Files\n")
            f.write("Individual batch results are saved in `07_Exports/batches/` directory.\n")
            f.write("Each batch contains detailed analysis of a subset of files.\n")

        logger.info(f"   ✅ Master summary saved: {master_file}")
        logger.info(f"   ✅ Master report saved: {report_file}")

    def create_organized_structure(self):
        """Create organized directory structure"""
        logger.info("\n🏗️ Creating organized structure...")

        # Create main directories
        main_dirs = [
            "01_Projects",
            "02_Content_Categories",
            "03_Code_Extractions",
            "04_Tool_Analysis",
            "05_File_Relationships",
            "06_Statistics",
            "07_Exports",
        ]

        for dir_name in main_dirs:
            (self.target_dir / dir_name).mkdir(exist_ok=True)

        # Create batches subdirectory
        (self.target_dir / "07_Exports" / "batches").mkdir(exist_ok=True)

    def run_batched_analysis(self):
        """Run the complete batched analysis"""
        logger.info("🚀 Starting Batched Content-Aware Chat Analysis...")
        logger.info("📦 This will process files in small batches to avoid large file sizes")

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Run analysis steps
        self.create_organized_structure()
        self.scan_all_files_batched()
        self.generate_master_summary()

        logger.info(f"\n✅ Batched Analysis Complete!")
        logger.info(f"📁 Organized content saved to: {self.target_dir}")
        logger.info(f"📋 Check MASTER_BATCHED_REPORT.md for overview")
        logger.info(f"📦 Individual batch results in: 07_Exports/batches/")


def main():
    """Main execution function"""
    source_dir = "/Users/steven/Documents/cursor-agent/chat_analysis /markdown_reports"
    target_dir = Path("/Users/steven/Dr_Adu_GainesvillePFS_SEO_Project")

    # Process in small batches to avoid huge files
    analyzer = BatchedContentAnalyzer(source_dir, target_dir, batch_size=5)
    analyzer.run_batched_analysis()


if __name__ == "__main__":
    main()
