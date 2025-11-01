"""
Python Intelligent Renamer Flat

This module provides functionality for python intelligent renamer flat.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Python Intelligent Renamer - Flat Structure
Intelligent renaming of Python files while keeping them in the root directory
with CSV backup for safe rollback capability.
"""

import os
import re
import ast
import json
import csv
import hashlib
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import difflib


class FlatIntelligentRenamer:
    """Intelligent renamer that keeps files in the root directory."""

    def __init__(self):
        """__init__ function."""

        self.project_patterns = {
            "YouTube_Automation": [
                "youtube",
                "upload",
                "bot",
                "subscriber",
                "viewer",
                "shorts",
                "playlist",
                "ytdl",
            ],
            "Instagram_Automation": [
                "instagram",
                "bot",
                "follow",
                "story",
                "post",
                "comment",
                "insta",
            ],
            "Content_Generation": [
                "content",
                "generator",
                "creator",
                "maker",
                "suno",
                "sora",
                "gpt",
                "text",
            ],
            "Media_Processing": [
                "video",
                "audio",
                "image",
                "photo",
                "mp3",
                "mp4",
                "transcribe",
                "ffmpeg",
            ],
            "Data_Analysis": [
                "analyze",
                "csv",
                "json",
                "data",
                "report",
                "analytics",
                "statistics",
            ],
            "Web_Scraping": [
                "scrape",
                "crawl",
                "beautifulsoup",
                "selenium",
                "requests",
                "spider",
            ],
            "AI_ML": ["ai", "ml", "gpt", "openai", "ollama", "llm", "neural", "claude"],
            "Automation": [
                "automation",
                "bot",
                "auto",
                "scheduler",
                "cron",
                "workflow",
            ],
            "File_Management": [
                "file",
                "organize",
                "clean",
                "duplicate",
                "merge",
                "rename",
                "organizer",
            ],
            "Utilities": ["util", "helper", "tool", "config", "env", "setup", "common"],
        }

        self.functionality_patterns = {
            "transcription": [
                "transcribe",
                "whisper",
                "speech",
                "audio",
                "text",
                "voice",
            ],
            "image_processing": [
                "image",
                "photo",
                "resize",
                "crop",
                "ocr",
                "pil",
                "opencv",
            ],
            "video_processing": [
                "video",
                "ffmpeg",
                "frame",
                "extract",
                "convert",
                "mp4",
            ],
            "data_processing": ["csv", "json", "excel", "database", "sql", "pandas"],
            "api_integration": [
                "api",
                "rest",
                "http",
                "oauth",
                "authentication",
                "requests",
            ],
            "web_automation": [
                "selenium",
                "beautifulsoup",
                "requests",
                "scrape",
                "crawl",
            ],
            "social_media": [
                "instagram",
                "youtube",
                "twitter",
                "tiktok",
                "social",
                "follow",
            ],
            "content_creation": [
                "generate",
                "create",
                "content",
                "text",
                "image",
                "video",
            ],
            "file_operations": [
                "file",
                "directory",
                "organize",
                "clean",
                "duplicate",
                "merge",
            ],
            "ai_services": ["openai", "gpt", "claude", "ollama", "llm", "ai"],
        }

        self.backup_data = []
        self.renaming_plan = []
        self.conflict_resolver = {}

    def analyze_and_rename(self, root_path, max_depth=6):
        """Analyze all Python files and create intelligent renaming plan."""
        root_path = Path(root_path).expanduser()

        logger.info(f"🐍 PYTHON INTELLIGENT RENAMER - FLAT STRUCTURE")
        logger.info("=" * 80)
        logger.info(f"Root: {root_path}")
        logger.info(f"Max depth: {max_depth}")
        logger.info("Keeping all files in the root directory with intelligent names")
        print()

        # Find all Python files
        logger.info("🔍 Discovering Python files...")
        python_files = []

        for file_path in root_path.rglob("*.py"):
            try:
                depth = len(file_path.relative_to(root_path).parts)
                if depth > max_depth:
                    continue
            except ValueError:
                continue

            if (
                file_path.is_file()
                and file_path.stat().st_size < 10 * CONSTANT_1024 * CONSTANT_1024
            ):  # < 10MB
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    file_info = {
                        "original_path": str(file_path),
                        "original_name": file_path.name,
                        "relative_path": str(file_path.relative_to(root_path)),
                        "content": content,
                        "size": file_path.stat().st_size,
                        "lines": len(content.splitlines()),
                        "depth": depth,
                        "project_category": "Unknown",
                        "functionality": "Unknown",
                        "complexity_score": 0,
                        "suggested_name": None,
                        "confidence": 0.0,
                        "dependencies": [],
                        "functions": [],
                        "classes": [],
                    }

                    python_files.append(file_info)

                except (IOError, OSError, UnicodeDecodeError):
                    continue

        logger.info(f"   Found {len(python_files)} Python files")

        # Analyze each file
        logger.info("\n🔍 Analyzing file content...")
        for i, file_info in enumerate(python_files):
            if i % 20 == 0:
                logger.info(f"   Progress: {i}/{len(python_files)} files analyzed")

            self._analyze_file_content(file_info)

        logger.info("   Content analysis complete!")

        # Generate intelligent names
        logger.info("\n🧠 Generating intelligent names...")
        self._generate_intelligent_names(python_files)

        # Resolve naming conflicts
        logger.info("\n🔧 Resolving naming conflicts...")
        self._resolve_naming_conflicts(python_files)

        # Create renaming plan
        logger.info("\n📋 Creating renaming plan...")
        self._create_renaming_plan(python_files)

        return python_files

    def _analyze_file_content(self, file_info):
        """Deep analysis of file content."""
        content = file_info["content"]
        content_lower = content.lower()

        try:
            # Parse AST for better understanding
            tree = ast.parse(content)

            # Extract imports and dependencies
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            file_info["dependencies"] = imports

            # Extract function and class definitions
            functions = []
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

            file_info["functions"] = functions
            file_info["classes"] = classes

        except SyntaxError:
            # Fallback to text analysis
            imports = re.findall(
                r"^(?:from\s+(\S+)\s+)?import\s+(\S+)", content, re.MULTILINE
            )
            file_info["dependencies"] = [imp[0] or imp[1] for imp in imports]
            functions = re.findall(r"^def\s+(\w+)\s*\(", content, re.MULTILINE)
            file_info["functions"] = functions
            file_info["classes"] = []

        # Categorize by path
        relative_path_lower = file_info["relative_path"].lower()
        for category, patterns in self.project_patterns.items():
            for pattern in patterns:
                if pattern in relative_path_lower:
                    file_info["project_category"] = category
                    break

        # Analyze functionality patterns
        functionality_scores = {}
        for functionality, patterns in self.functionality_patterns.items():
            score = 0
            for pattern in patterns:
                if pattern in content_lower:
                    score += content_lower.count(pattern)
            functionality_scores[functionality] = score

        if functionality_scores:
            file_info["functionality"] = max(
                functionality_scores, key=functionality_scores.get
            )
            file_info["confidence"] = min(
                functionality_scores[file_info["functionality"]] / 20, 1.0
            )

        # Calculate complexity score
        file_info["complexity_score"] = self._calculate_complexity(content, file_info)

    def _calculate_complexity(self, content, file_info):
        """Calculate code complexity score."""
        lines = content.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]

        complexity = 0
        complexity += len(file_info.get("functions", [])) * 2
        complexity += len(file_info.get("classes", [])) * 3
        complexity += len(file_info.get("dependencies", [])) * 1
        complexity += len(non_empty_lines) * 0.1

        # Add complexity for nested structures
        for line in lines:
            if line.strip().startswith(
                ("if ", "for ", "while ", "try:", "except", "with ")
            ):
                complexity += 1
            if line.strip().startswith(("class ", "def ")):
                complexity += 2

        return min(complexity / CONSTANT_100, 1.0)

    def _generate_intelligent_names(self, python_files):
        """Generate intelligent names for all files."""
        for file_info in python_files:
            if file_info["confidence"] < 0.2:
                file_info["suggested_name"] = file_info["original_name"]
                continue

            name_parts = []

            # Add project category prefix
            if file_info["project_category"] != "Unknown":
                category_name = file_info["project_category"].replace("_", " ").title()
                name_parts.append(category_name)

            # Add primary functionality
            if file_info["functionality"] != "Unknown":
                func_name = file_info["functionality"].replace("_", " ").title()
                name_parts.append(func_name)

            # Add specific action if available
            if file_info.get("functions"):
                action_funcs = [
                    f
                    for f in file_info["functions"]
                    if any(
                        word in f.lower()
                        for word in [
                            "analyze",
                            "process",
                            "generate",
                            "create",
                            "clean",
                            "organize",
                            "merge",
                            "extract",
                            "convert",
                        ]
                    )
                ]
                if action_funcs:
                    action_name = action_funcs[0].replace("_", " ").title()
                    name_parts.append(action_name)

            # Add domain-specific terms
            content_lower = file_info["content"].lower()
            if "youtube" in content_lower:
                name_parts.append("YouTube")
            elif "instagram" in content_lower:
                name_parts.append("Instagram")
            elif "audio" in content_lower or "transcribe" in content_lower:
                name_parts.append("Audio")
            elif "video" in content_lower or "mp4" in content_lower:
                name_parts.append("Video")
            elif "image" in content_lower or "photo" in content_lower:
                name_parts.append("Image")
            elif "csv" in content_lower or "data" in content_lower:
                name_parts.append("Data")
            elif "ai" in content_lower or "gpt" in content_lower:
                name_parts.append("AI")

            # Generate final name
            if name_parts:
                suggested_name = "".join(name_parts) + ".py"
                suggested_name = re.sub(r"[^a-zA-Z0-9._-]", "", suggested_name)
            else:
                suggested_name = file_info["original_name"]

            file_info["suggested_name"] = suggested_name

    def _resolve_naming_conflicts(self, python_files):
        """Resolve naming conflicts by adding numbers."""
        name_counts = defaultdict(int)
        name_to_files = defaultdict(list)

        # Group files by suggested name
        for file_info in python_files:
            suggested_name = file_info["suggested_name"]
            name_counts[suggested_name] += 1
            name_to_files[suggested_name].append(file_info)

        # Resolve conflicts
        for suggested_name, files in name_to_files.items():
            if len(files) > 1:
                # Sort by confidence and complexity
                files.sort(
                    key=lambda x: (x["confidence"], x["complexity_score"]), reverse=True
                )

                for i, file_info in enumerate(files):
                    if i == 0:
                        # Keep the best file with original name
                        file_info["final_name"] = suggested_name
                    else:
                        # Add number suffix
                        base_name = suggested_name.replace(".py", "")
                        file_info["final_name"] = f"{base_name}_{i}.py"
            else:
                files[0]["final_name"] = suggested_name

    def _create_renaming_plan(self, python_files):
        """Create the final renaming plan."""
        for file_info in python_files:
            if file_info["final_name"] != file_info["original_name"]:
                self.renaming_plan.append(
                    {
                        "original_path": file_info["original_path"],
                        "original_name": file_info["original_name"],
                        "new_name": file_info["final_name"],
                        "project_category": file_info["project_category"],
                        "functionality": file_info["functionality"],
                        "confidence": file_info["confidence"],
                        "reason": f"Intelligent naming based on {file_info['functionality']} functionality",
                    }
                )

                # Add to backup data
                self.backup_data.append(
                    {
                        "original_path": file_info["original_path"],
                        "original_name": file_info["original_name"],
                        "new_name": file_info["final_name"],
                        "project_category": file_info["project_category"],
                        "functionality": file_info["functionality"],
                        "confidence": file_info["confidence"],
                        "complexity_score": file_info["complexity_score"],
                        "size": file_info["size"],
                        "lines": file_info["lines"],
                        "reason": f"Intelligent naming based on {file_info['functionality']} functionality",
                    }
                )

    def create_csv_backup(self, output_file):
        """Create CSV backup with old and new names."""
        logger.info(f"\n💾 Creating CSV backup: {output_file}")

        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "original_path",
                "original_name",
                "new_name",
                "project_category",
                "functionality",
                "confidence",
                "complexity_score",
                "size",
                "lines",
                "reason",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.backup_data:
                writer.writerow(row)

        logger.info(f"   CSV backup created with {len(self.backup_data)} entries")
        logger.info(f"   This is your safety net for rollback!")

    def generate_execution_script(self, output_file):
        """Generate execution script for the renaming."""
        logger.info(f"\n🚀 Generating execution script: {output_file}")

        script_content = f'''#!/usr/bin/env python3
"""
Python Intelligent Renamer - Execution Script
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

import os
import shutil
from pathlib import Path

def execute_renaming():
    """Execute the intelligent renaming plan."""
    logger.info("🔄 EXECUTING PYTHON INTELLIGENT RENAMING")
    logger.info("=" * 60)
    
    # Create backup directory
    backup_dir = Path(Path("/Users/steven/python_renaming_backup"))
    backup_dir.mkdir(exist_ok=True)
    logger.info(f"📁 Backup directory: {{backup_dir}}")
    
    # Renaming operations
    renaming_operations = {self.renaming_plan}
    
    logger.info(f"\\n📦 Executing {{len(renaming_operations)}} renames...")
    
    for i, op in enumerate(renaming_operations, 1):
        old_path = Path(op['original_path'])
        new_path = old_path.parent / op['new_name']
        
        logger.info(f"   {{i}}/{{len(renaming_operations)}}: {{op['original_name']}} → {{op['new_name']}}")
        logger.info(f"     Category: {{op['project_category']}}")
        logger.info(f"     Functionality: {{op['functionality']}}")
        logger.info(f"     Confidence: {{op['confidence']:.1%}}")
        
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
    
    logger.info(f"\\n✅ Renaming complete!")
    logger.info(f"📁 All files backed up to: {{backup_dir}}")
    logger.info(f"🔄 To rollback, use the CSV file to restore original names")

if __name__ == "__main__":
    execute_renaming()
'''

        with open(output_file, "w") as f:
            f.write(script_content)

        # Make executable
        os.chmod(output_file, 0o755)

        logger.info(f"   Execution script created and made executable")

    def generate_report(self, python_files):
        """Generate comprehensive renaming report."""
        logger.info(f"\n📊 INTELLIGENT RENAMING REPORT")
        logger.info("=" * 80)

        # Statistics
        total_files = len(python_files)
        files_to_rename = len(self.renaming_plan)
        files_keeping_name = total_files - files_to_rename

        logger.info(f"📈 RENAMING STATISTICS")
        logger.info(f"   Total Python files: {total_files}")
        logger.info(f"   Files to rename: {files_to_rename}")
        logger.info(f"   Files keeping original name: {files_keeping_name}")
        logger.info(f"   Renaming rate: {files_to_rename/total_files:.1%}")

        # Project category breakdown
        category_counts = Counter(op["project_category"] for op in self.renaming_plan)
        logger.info(f"\n📁 RENAMING BY PROJECT CATEGORY")
        for category, count in category_counts.most_common():
            logger.info(f"   {category.replace('_', ' ').title()}: {count} files")

        # Functionality breakdown
        functionality_counts = Counter(op["functionality"] for op in self.renaming_plan)
        logger.info(f"\n⚙️  RENAMING BY FUNCTIONALITY")
        for functionality, count in functionality_counts.most_common():
            logger.info(f"   {functionality.replace('_', ' ').title()}: {count} files")

        # Confidence analysis
        high_confidence = [op for op in self.renaming_plan if op["confidence"] > 0.7]
        medium_confidence = [
            op for op in self.renaming_plan if 0.3 <= op["confidence"] <= 0.7
        ]
        low_confidence = [op for op in self.renaming_plan if op["confidence"] < 0.3]

        logger.info(f"\n🎯 CONFIDENCE ANALYSIS")
        logger.info(f"   High confidence (>0.7): {len(high_confidence)} files")
        logger.info(f"   Medium confidence (0.3-0.7): {len(medium_confidence)} files")
        logger.info(f"   Low confidence (<0.3): {len(low_confidence)} files")

        # Show some examples
        logger.info(f"\n📝 RENAMING EXAMPLES")
        for i, op in enumerate(self.renaming_plan[:10], 1):
            logger.info(f"   {i}. {op['original_name']}")
            logger.info(f"      → {op['new_name']}")
            logger.info(f"      Category: {op['project_category']}")
            logger.info(f"      Functionality: {op['functionality']}")
            logger.info(f"      Confidence: {op['confidence']:.1%}")
            print()


def main():
    """Main execution function."""
    logger.info("🐍 PYTHON INTELLIGENT RENAMER - FLAT STRUCTURE")
    logger.info("=" * 80)
    logger.info("Intelligent renaming while keeping all files in the root directory")
    logger.info("with CSV backup for safe rollback capability")
    print()

    renamer = FlatIntelligentRenamer()

    # Analyze and create renaming plan
    python_files = renamer.analyze_and_rename("~/Documents/python", max_depth=6)

    # Create CSV backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_backup_file = f"/Users/steven/python_renaming_backup_{timestamp}.csv"
    renamer.create_csv_backup(csv_backup_file)

    # Generate execution script
    execution_script = f"/Users/steven/python_intelligent_rename_execute_{timestamp}.py"
    renamer.generate_execution_script(execution_script)

    # Generate report
    renamer.generate_report(python_files)

    logger.info(f"\n💾 BACKUP & SAFETY")
    logger.info(f"   CSV backup: {csv_backup_file}")
    logger.info(f"   Execution script: {execution_script}")
    logger.info(f"   🛡️  All changes can be rolled back using the CSV file!")

    logger.info(f"\n🚀 NEXT STEPS")
    logger.info(f"   1. Review the CSV backup file")
    logger.info(f"   2. Check the renaming examples above")
    logger.info(
        f"   3. Run the execution script when ready: python3 {execution_script}"
    )
    logger.info(f"   4. Use CSV file to rollback if needed")

    logger.info(f"\n✅ INTELLIGENT RENAMING PLAN COMPLETE!")
    logger.info(f"   All files will stay in ~/Documents/python with intelligent names!")


if __name__ == "__main__":
    main()
