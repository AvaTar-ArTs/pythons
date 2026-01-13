#!/usr/bin/env python3
"""
Content-Aware Chat Analysis Organizer
Deep analyzes chat files to understand patterns and organize intelligently
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib


class ContentAwareAnalyzer:
    def __init__(self, source_dir, target_dir):
        """__init__ function."""

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.all_files = []
        self.analysis_results = {
            "chat_patterns": {},
            "code_extractions": {},
            "project_identifications": {},
            "content_categories": {},
            "file_relationships": {},
            "statistics": {},
        }

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

    def extract_code_blocks(self, content):
        """Extract and categorize code blocks from content"""
        code_blocks = []

        # Find all code blocks
        code_pattern = r"```(\w+)?\n(.*?)\n```"
        matches = re.findall(code_pattern, content, re.DOTALL)

        for i, (language, code) in enumerate(matches):
            if not language:
                language = "unknown"

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

    def extract_tool_calls(self, content):
        """Extract tool call information"""
        tool_calls = []

        # Find tool call sections
        tool_pattern = r"### 🛠️ Message \d+ - TOOL.*?\n\n(.*?)(?=---|\n###|\Z)"
        tool_matches = re.findall(tool_pattern, content, re.DOTALL)

        for tool_content in tool_matches:
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
                    tool_content[:CONSTANT_200] + "..."
                    if len(tool_content) > CONSTANT_200
                    else tool_content
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
            "file_management": [
                r"file",
                r"directory",
                r"folder",
                r"organize",
                r"sort",
                r"structure",
                r"management",
            ],
        }

        content_lower = content.lower()
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    categories.add(category)
                    break

        return list(categories)

    def analyze_file_relationships(self, files):
        """Analyze relationships between files"""
        relationships = {}

        for file_info in files:
            file_id = file_info.get("chat_id", "unknown")
            relationships[file_id] = {
                "related_files": [],
                "shared_projects": [],
                "shared_topics": [],
                "code_similarities": [],
            }

            # Find related files by shared projects/topics
            for other_file in files:
                if other_file.get("chat_id") == file_id:
                    continue

                shared_projects = set(file_info.get("projects", [])) & set(
                    other_file.get("projects", [])
                )
                shared_topics = set(file_info.get("categories", [])) & set(
                    other_file.get("categories", [])
                )

                if shared_projects or shared_topics:
                    relationships[file_id]["related_files"].append(
                        {
                            "file_id": other_file.get("chat_id", "unknown"),
                            "shared_projects": list(shared_projects),
                            "shared_topics": list(shared_topics),
                        }
                    )

        return relationships

    def analyze_single_file(self, file_path):
        """Perform deep analysis of a single file"""
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

            # Deep analysis
            file_info["chat_structure"] = self.analyze_chat_structure(content)
            file_info["code_blocks"] = self.extract_code_blocks(content)
            file_info["tool_calls"] = self.extract_tool_calls(content)
            file_info["projects"] = self.identify_projects(content, file_path.name)
            file_info["categories"] = self.categorize_content(content, file_path.name)

            # Extract chat ID for relationships
            file_info["chat_id"] = file_info["chat_structure"].get("chat_id", "unknown")

            return file_info

        except Exception as e:
            logger.info(f"      ❌ Error analyzing {file_path.name}: {e}")
            return None

    def scan_all_files(self):
        """Scan and analyze all files"""
        logger.info("🔍 Performing content-aware analysis of all files...")

        if not self.source_dir.exists():
            logger.info(f"❌ Source directory not found: {self.source_dir}")
            return

        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in [
                ".md",
                ".html",
                ".txt",
                ".json",
                ".csv",
            ]:
                logger.info(
                    f"   📄 Analyzing: {file_path.relative_to(self.source_dir)}"
                )
                file_analysis = self.analyze_single_file(file_path)
                if file_analysis:
                    self.all_files.append(file_analysis)

        logger.info(f"\\n📊 Total files analyzed: {len(self.all_files)}")

    def generate_analysis_summary(self):
        """Generate comprehensive analysis summary"""
        logger.info("\\n📊 Generating analysis summary...")

        # Analyze patterns across all files
        all_projects = set()
        all_categories = set()
        all_code_types = set()
        all_tool_types = set()

        for file_info in self.all_files:
            all_projects.update(file_info.get("projects", []))
            all_categories.update(file_info.get("categories", []))

            for code_block in file_info.get("code_blocks", []):
                all_code_types.add(code_block.get("type", "unknown"))

            for tool_call in file_info.get("tool_calls", []):
                all_tool_types.add(tool_call.get("tool_type", "unknown"))

        # Generate statistics
        self.analysis_results["statistics"] = {
            "total_files": len(self.all_files),
            "total_size": sum(f["size"] for f in self.all_files),
            "total_words": sum(f["word_count"] for f in self.all_files),
            "unique_projects": len(all_projects),
            "unique_categories": len(all_categories),
            "unique_code_types": len(all_code_types),
            "unique_tool_types": len(all_tool_types),
            "date_range": {
                "earliest": min(f["created"] for f in self.all_files).isoformat(),
                "latest": max(f["modified"] for f in self.all_files).isoformat(),
            },
        }

        # Analyze file relationships
        self.analysis_results["file_relationships"] = self.analyze_file_relationships(
            self.all_files
        )

        # Group by projects
        project_groups = {}
        for file_info in self.all_files:
            for project in file_info.get("projects", []):
                if project not in project_groups:
                    project_groups[project] = []
                project_groups[project].append(file_info)

        self.analysis_results["project_identifications"] = project_groups

        # Group by categories
        category_groups = {}
        for file_info in self.all_files:
            for category in file_info.get("categories", []):
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(file_info)

        self.analysis_results["content_categories"] = category_groups

    def create_organized_structure(self):
        """Create organized directory structure based on analysis"""
        logger.info("\\n🏗️ Creating content-aware organized structure...")

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

        # Create project directories
        for project in self.analysis_results["project_identifications"].keys():
            project_dir = (
                self.target_dir / "01_Projects" / self.sanitize_filename(project, 50)
            )
            project_dir.mkdir(exist_ok=True)

        # Create category directories
        for category in self.analysis_results["content_categories"].keys():
            category_dir = self.target_dir / "02_Content_Categories" / category
            category_dir.mkdir(exist_ok=True)

        # Create code type directories
        all_code_types = set()
        for file_info in self.all_files:
            for code_block in file_info.get("code_blocks", []):
                all_code_types.add(code_block.get("type", "unknown"))

        for code_type in all_code_types:
            code_dir = self.target_dir / "03_Code_Extractions" / code_type
            code_dir.mkdir(exist_ok=True)

    def extract_and_organize_code(self):
        """Extract and organize code blocks by type"""
        logger.info("\\n💻 Extracting and organizing code blocks...")

        for file_info in self.all_files:
            for code_block in file_info.get("code_blocks", []):
                code_type = code_block.get("type", "unknown")
                language = code_block.get("language", "unknown")

                # Create filename for code block
                timestamp = file_info["modified"].strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{file_info['chat_id']}_{code_type}_{language}.{language}"

                # Save code block
                code_dir = self.target_dir / "03_Code_Extractions" / code_type
                code_path = code_dir / filename

                try:
                    with open(code_path, "w", encoding="utf-8") as f:
                        f.write(f"# {code_type.title()} - {language.upper()}\n")
                        f.write(f"**Source:** {file_info['name']}\\n")
                        f.write(f"**Chat ID:** {file_info['chat_id']}\\n")
                        f.write(
                            f"**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                        )
                        f.write("```" + language + Path("\\n"))
                        f.write(code_block["code"])
                        f.write("\\n```\\n")

                    logger.info(f"   ✅ Extracted: {code_type}/{filename}")
                except Exception as e:
                    logger.info(f"   ❌ Error extracting code: {e}")

    def generate_comprehensive_reports(self):
        """Generate comprehensive analysis reports"""
        logger.info("\\n📊 Generating comprehensive reports...")

        # Master analysis report
        self.generate_master_analysis_report()

        # Project reports
        self.generate_project_reports()

        # Category reports
        self.generate_category_reports()

        # Code analysis reports
        self.generate_code_analysis_reports()

        # Tool analysis reports
        self.generate_tool_analysis_reports()

        # Relationship reports
        self.generate_relationship_reports()

    def generate_master_analysis_report(self):
        """Generate master analysis report"""
        report_path = self.target_dir / "MASTER_ANALYSIS_REPORT.md"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Content-Aware Chat Analysis - Master Report\\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
            )

            stats = self.analysis_results["statistics"]
            f.write("## Analysis Overview\\n")
            f.write(f"- **Total Files:** {stats['total_files']}\\n")
            f.write(
                f"- **Total Size:** {stats['total_size']:,} bytes ({stats['total_size']/CONSTANT_1024/CONSTANT_1024:.2f} MB)\\n"
            )
            f.write(f"- **Total Words:** {stats['total_words']:,}\\n")
            f.write(f"- **Unique Projects:** {stats['unique_projects']}\\n")
            f.write(f"- **Content Categories:** {stats['unique_categories']}\\n")
            f.write(f"- **Code Types:** {stats['unique_code_types']}\\n")
            f.write(f"- **Tool Types:** {stats['unique_tool_types']}\\n\\n")

            f.write("## Project Breakdown\\n")
            for project, files in self.analysis_results[
                "project_identifications"
            ].items():
                f.write(f"- **{project}:** {len(files)} files\\n")

            f.write("\\n## Content Categories\\n")
            for category, files in self.analysis_results["content_categories"].items():
                f.write(f"- **{category}:** {len(files)} files\\n")

    def generate_project_reports(self):
        """Generate individual project reports"""
        for project, files in self.analysis_results["project_identifications"].items():
            report_path = (
                self.target_dir
                / "01_Projects"
                / self.sanitize_filename(project, 50)
                / f"{self.sanitize_filename(project, 30)}_ANALYSIS.md"
            )

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# {project} - Project Analysis\\n")
                f.write(
                    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                )

                f.write(f"## Project Overview\\n")
                f.write(f"- **Files:** {len(files)}\\n")
                f.write(f"- **Total Size:** {sum(f['size'] for f in files):,} bytes\\n")
                f.write(
                    f"- **Total Words:** {sum(f['word_count'] for f in files):,}\\n\\n"
                )

                f.write("## Files in Project\\n")
                for file_info in sorted(
                    files, key=lambda x: x["modified"], reverse=True
                ):
                    f.write(f"### {file_info['name']}\\n")
                    f.write(f"- **Chat ID:** {file_info.get('chat_id', 'unknown')}\\n")
                    f.write(
                        f"- **Categories:** {', '.join(file_info.get('categories', []))}\\n"
                    )
                    f.write(
                        f"- **Code Blocks:** {len(file_info.get('code_blocks', []))}\\n"
                    )
                    f.write(
                        f"- **Tool Calls:** {len(file_info.get('tool_calls', []))}\\n"
                    )
                    f.write(
                        f"- **Modified:** {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                    )

    def generate_category_reports(self):
        """Generate category reports"""
        for category, files in self.analysis_results["content_categories"].items():
            report_path = (
                self.target_dir
                / "02_Content_Categories"
                / category
                / f"{category}_ANALYSIS.md"
            )

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# {category.title()} - Category Analysis\\n")
                f.write(
                    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                )

                f.write(f"## Category Overview\\n")
                f.write(f"- **Files:** {len(files)}\\n")
                f.write(f"- **Total Size:** {sum(f['size'] for f in files):,} bytes\\n")
                f.write(
                    f"- **Total Words:** {sum(f['word_count'] for f in files):,}\\n\\n"
                )

                f.write("## Files by Category\\n")
                for file_info in sorted(
                    files, key=lambda x: x["modified"], reverse=True
                ):
                    f.write(f"### {file_info['name']}\\n")
                    f.write(
                        f"- **Projects:** {', '.join(file_info.get('projects', []))}\\n"
                    )
                    f.write(f"- **Chat ID:** {file_info.get('chat_id', 'unknown')}\\n")
                    f.write(
                        f"- **Modified:** {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                    )

    def generate_code_analysis_reports(self):
        """Generate code analysis reports"""
        code_stats = {}

        for file_info in self.all_files:
            for code_block in file_info.get("code_blocks", []):
                code_type = code_block.get("type", "unknown")
                if code_type not in code_stats:
                    code_stats[code_type] = {
                        "count": 0,
                        "total_size": 0,
                        "languages": set(),
                        "files": set(),
                    }

                code_stats[code_type]["count"] += 1
                code_stats[code_type]["total_size"] += code_block.get("size", 0)
                code_stats[code_type]["languages"].add(
                    code_block.get("language", "unknown")
                )
                code_stats[code_type]["files"].add(file_info["name"])

        for code_type, stats in code_stats.items():
            report_path = (
                self.target_dir
                / "03_Code_Extractions"
                / code_type
                / f"{code_type}_ANALYSIS.md"
            )

            with open(report_path, "w", encoding="utf-8") as f:
                f.write(f"# {code_type.title()} - Code Analysis\\n")
                f.write(
                    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
                )

                f.write(f"## Code Type Overview\\n")
                f.write(f"- **Total Blocks:** {stats['count']}\\n")
                f.write(f"- **Total Size:** {stats['total_size']:,} bytes\\n")
                f.write(f"- **Languages:** {', '.join(stats['languages'])}\\n")
                f.write(f"- **Files:** {len(stats['files'])}\\n\\n")

                f.write("## Source Files\\n")
                for filename in sorted(stats["files"]):
                    f.write(f"- {filename}\\n")

    def generate_tool_analysis_reports(self):
        """Generate tool analysis reports"""
        tool_stats = {}

        for file_info in self.all_files:
            for tool_call in file_info.get("tool_calls", []):
                tool_type = tool_call.get("tool_type", "unknown")
                if tool_type not in tool_stats:
                    tool_stats[tool_type] = {
                        "count": 0,
                        "total_size": 0,
                        "files": set(),
                    }

                tool_stats[tool_type]["count"] += 1
                tool_stats[tool_type]["total_size"] += tool_call.get("size", 0)
                tool_stats[tool_type]["files"].add(file_info["name"])

        tool_report_path = self.target_dir / "04_Tool_Analysis" / "TOOL_ANALYSIS.md"

        with open(tool_report_path, "w", encoding="utf-8") as f:
            f.write("# Tool Call Analysis\\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
            )

            f.write("## Tool Usage Overview\\n")
            for tool_type, stats in tool_stats.items():
                f.write(f"### {tool_type.title()}\\n")
                f.write(f"- **Count:** {stats['count']}\\n")
                f.write(f"- **Total Size:** {stats['total_size']:,} bytes\\n")
                f.write(f"- **Files:** {len(stats['files'])}\\n\\n")

    def generate_relationship_reports(self):
        """Generate file relationship reports"""
        relationship_report_path = (
            self.target_dir / "05_File_Relationships" / "RELATIONSHIPS.md"
        )

        with open(relationship_report_path, "w", encoding="utf-8") as f:
            f.write("# File Relationship Analysis\\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n"
            )

            f.write("## File Relationships\\n")
            for file_id, relationships in self.analysis_results[
                "file_relationships"
            ].items():
                f.write(f"### {file_id}\\n")
                f.write(
                    f"- **Related Files:** {len(relationships['related_files'])}\\n"
                )
                for rel in relationships["related_files"]:
                    f.write(
                        f"  - {rel['file_id']} (Projects: {', '.join(rel['shared_projects'])}, Topics: {', '.join(rel['shared_topics'])})\\n"
                    )
                f.write(Path("\\n"))

    def sanitize_filename(self, filename, max_length=CONSTANT_100):
        """Sanitize filename for filesystem"""
        sanitized = re.sub(r'[<>:"/\\\\|?*\\n\\r]', "_", filename)
        sanitized = re.sub(r"\\s+", "_", sanitized)
        sanitized = sanitized.strip("._")

        if len(sanitized) > max_length:
            sanitized = sanitized[: max_length - 10] + "_truncated"

        return sanitized or "unnamed"

    def export_analysis_data(self):
        """Export analysis data to JSON"""
        json_path = self.target_dir / "07_Exports" / "analysis_data.json"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.analysis_results, f, indent=2, default=str)

        logger.info(f"   ✅ Analysis data exported: {json_path}")

    def run_complete_analysis(self):
        """Run the complete content-aware analysis"""
        logger.info("🚀 Starting Content-Aware Chat Analysis...")

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Run analysis steps
        self.scan_all_files()
        self.generate_analysis_summary()
        self.create_organized_structure()
        self.extract_and_organize_code()
        self.generate_comprehensive_reports()
        self.export_analysis_data()

        logger.info(f"\\n✅ Content-Aware Analysis Complete!")
        logger.info(f"📁 Organized content saved to: {self.target_dir}")
        logger.info(f"📋 Check MASTER_ANALYSIS_REPORT.md for overview")


def main():
    """Main execution function"""
    source_dir = str(Path.home()) + "/Documents/cursor-agent/chat_analysis "
    target_dir = Path(str(Path.home()) + "/CONTENT_AWARE_CHAT_ANALYSIS")

    analyzer = ContentAwareAnalyzer(source_dir, target_dir)
    analyzer.run_complete_analysis()


if __name__ == "__main__":
    main()
