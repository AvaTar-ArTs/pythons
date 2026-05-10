#!/usr/bin/env python3
"""Deep Analysis and Intelligent Merge Tool

This script performs deep content analysis of Python files to identify:
1. Exact duplicates (same content)
2. Similar files (similar functionality with variations)
3. Merge opportunities (combining best features)
4. Content patterns and improvements

It creates intelligent merges that combine the best features from similar files.
"""

import os
import logging
import hashlib
import re
from pathlib import Path
from typing import Any
from collections import defaultdict
from datetime import datetime
import difflib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("deep_analysis_merge.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class DeepAnalysisMerger:
    """Deep analysis and intelligent merge tool for Python files."""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.final_dir = self.base_dir / "FINAL_ORGANIZED"
        self.duplicates_dir = self.base_dir / "DUPLICATES_ARCHIVE"
        self.clean_dir = self.base_dir / "CLEAN_ORGANIZED"
        self.merged_dir = self.base_dir / "DEEP_MERGED"

        # Analysis results
        self.file_hashes = {}
        self.content_analysis = {}
        self.similarity_groups = defaultdict(list)
        self.merge_opportunities = []
        self.quality_scores = {}

        # File patterns for analysis
        self.analysis_patterns = {
            "analyze": r"analyze|analysis|analyzer",
            "generate": r"generate|generation|generator",
            "transcribe": r"transcribe|transcript|transcription",
            "process": r"process|processing|processor",
            "organize": r"organize|organization|organizer",
            "scrape": r"scrape|scraping|scraper",
            "convert": r"convert|conversion|converter",
            "mp3": r"mp3|audio|sound",
            "mp4": r"mp4|video|visual",
            "csv": r"csv|data|spreadsheet",
            "html": r"html|web|page",
        }

    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception as e:
            logger.warning(f"Could not calculate hash for {file_path}: {e}")
            return ""

    def analyze_file_content(self, file_path: Path) -> dict[str, Any]:
        """Deep analysis of file content."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip()]

            # Basic metrics
            analysis = {
                "file_path": file_path,
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "lines": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "content": content,
                "imports": [],
                "functions": [],
                "classes": [],
                "docstrings": [],
                "openai_usage": False,
                "quality_indicators": {
                    "has_docstring": False,
                    "has_logging": False,
                    "has_error_handling": False,
                    "has_main_function": False,
                    "has_type_hints": False,
                    "has_comments": False,
                },
                "functionality_patterns": [],
                "dependencies": set(),
                "complexity_score": 0,
            }

            # Extract imports
            for line in lines:
                if line.strip().startswith("import ") or line.strip().startswith(
                    "from ",
                ):
                    analysis["imports"].append(line.strip())
                    # Extract module names
                    if "import " in line:
                        module = (
                            line.split("import ")[1]
                            .split(" as ")[0]
                            .split(".")[0]
                            .strip()
                        )
                        analysis["dependencies"].add(module)
                    elif "from " in line:
                        module = (
                            line.split("from ")[1]
                            .split(" import")[0]
                            .split(".")[0]
                            .strip()
                        )
                        analysis["dependencies"].add(module)

            # Extract functions and classes
            in_function = False
            in_class = False
            current_function = ""
            current_class = ""

            for i, line in enumerate(lines):
                stripped = line.strip()

                # Check for docstrings
                if '\"\'"' in line or "\'"'"" in line:
                    analysis["quality_indicators"]["has_docstring"] = True
                    if '\"\'"' in line:
                        analysis["docstrings"].append(line)

                # Check for logging
                if "logging" in line.lower() or "logger" in line.lower():
                    analysis["quality_indicators"]["has_logging"] = True

                # Check for error handling
                if "try:" in line or "except" in line or "finally:" in line:
                    analysis["quality_indicators"]["has_error_handling"] = True

                # Check for main function
                if 'if __name__ == "__main__":' in line:
                    analysis["quality_indicators"]["has_main_function"] = True

                # Check for type hints
                if "->" in line or (
                    ": " in line
                    and (
                        "str" in line
                        or "int" in line
                        or "List" in line
                        or "Dict" in line
                    )
                ):
                    analysis["quality_indicators"]["has_type_hints"] = True

                # Check for comments
                if line.strip().startswith("#") and len(line.strip()) > 3:
                    analysis["quality_indicators"]["has_comments"] = True

                # Extract functions
                if re.match(r"def\s+\w+", stripped):
                    func_name = re.match(r"def\s+(\w+)", stripped).group(1)
                    analysis["functions"].append(func_name)
                    in_function = True
                    current_function = func_name

                # Extract classes
                if re.match(r"class\s+\w+", stripped):
                    class_name = re.match(r"class\s+(\w+)", stripped).group(1)
                    analysis["classes"].append(class_name)
                    in_class = True
                    current_class = class_name

                # Check for OpenAI usage
                if (
                    "openai" in line.lower()
                    or "gpt" in line.lower()
                    or "whisper" in line.lower()
                ):
                    analysis["openai_usage"] = True

            # Identify functionality patterns
            content_lower = content.lower()
            for pattern_name, pattern in self.analysis_patterns.items():
                if re.search(pattern, content_lower):
                    analysis["functionality_patterns"].append(pattern_name)

            # Calculate quality score
            quality_score = 0
            for indicator, has_it in analysis["quality_indicators"].items():
                if has_it:
                    quality_score += 1

            # Add complexity score based on lines, functions, classes
            analysis["complexity_score"] = (
                len(analysis["functions"])
                + len(analysis["classes"])
                + (len(non_empty_lines) // 10)
            )
            analysis["quality_score"] = quality_score

            return analysis

        except Exception as e:
            logger.warning(f"Could not analyze {file_path}: {e}")
            return {
                "file_path": file_path,
                "filename": file_path.name,
                "size": 0,
                "lines": 0,
                "non_empty_lines": 0,
                "content": "",
                "imports": [],
                "functions": [],
                "classes": [],
                "docstrings": [],
                "openai_usage": False,
                "quality_indicators": {},
                "functionality_patterns": [],
                "dependencies": set(),
                "complexity_score": 0,
                "quality_score": 0,
            }

    def find_exact_duplicates(self) -> dict[str, list[Path]]:
        """Find exact duplicate files by content hash."""
        logger.info("Finding exact duplicates...")

        hash_to_files = defaultdict(list)

        # Scan all Python files
        for py_file in self.base_dir.rglob("*.py"):
            if py_file.exists():
                file_hash = self.calculate_file_hash(py_file)
                if file_hash:
                    hash_to_files[file_hash].append(py_file)

        # Filter out single files (no duplicates)
        duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

        logger.info(f"Found {len(duplicates)} groups of exact duplicates")
        return duplicates

    def find_similar_files(self) -> dict[str, list[Path]]:
        """Find similar files based on content analysis."""
        logger.info("Finding similar files...")

        # Analyze all Python files
        all_files = []
        for py_file in self.base_dir.rglob("*.py"):
            if py_file.exists():
                analysis = self.analyze_file_content(py_file)
                all_files.append(analysis)
                self.content_analysis[py_file] = analysis

        # Group by functionality patterns
        pattern_groups = defaultdict(list)
        for analysis in all_files:
            if analysis["functionality_patterns"]:
                # Create a signature based on functionality patterns
                signature = "_".join(sorted(analysis["functionality_patterns"]))
                pattern_groups[signature].append(analysis["file_path"])

        # Group by filename patterns
        filename_groups = defaultdict(list)
        for analysis in all_files:
            filename = analysis["filename"].lower()
            # Remove common suffixes and variations
            clean_name = re.sub(r"[_\-\s]*\d+[_\-\s]*$", "", filename)
            clean_name = re.sub(r"[_\-\s]*\([^)]*\)[_\-\s]*$", "", clean_name)
            clean_name = re.sub(r"[_\-\s]*copy[_\-\s]*$", "", clean_name)
            clean_name = re.sub(r"[_\-\s]*variants[_\-\s]*$", "", clean_name)
            clean_name = clean_name.strip("._-")

            if clean_name:
                filename_groups[clean_name].append(analysis["file_path"])

        # Combine similar groups
        similar_groups = {}
        group_id = 0

        # Process pattern groups
        for pattern, files in pattern_groups.items():
            if len(files) > 1:
                similar_groups[f"pattern_{group_id}"] = files
                group_id += 1

        # Process filename groups
        for name, files in filename_groups.items():
            if len(files) > 1:
                similar_groups[f"filename_{group_id}"] = files
                group_id += 1

        logger.info(f"Found {len(similar_groups)} groups of similar files")
        return similar_groups

    def calculate_similarity(self, file1: Path, file2: Path) -> float:
        """Calculate similarity between two files."""
        try:
            analysis1 = self.content_analysis.get(file1)
            analysis2 = self.content_analysis.get(file2)

            if not analysis1 or not analysis2:
                return 0.0

            # Compare functionality patterns
            patterns1 = set(analysis1["functionality_patterns"])
            patterns2 = set(analysis2["functionality_patterns"])
            pattern_similarity = len(patterns1.intersection(patterns2)) / max(
                len(patterns1.union(patterns2)),
                1,
            )

            # Compare imports
            imports1 = set(analysis1["imports"])
            imports2 = set(analysis2["imports"])
            import_similarity = len(imports1.intersection(imports2)) / max(
                len(imports1.union(imports2)),
                1,
            )

            # Compare functions
            funcs1 = set(analysis1["functions"])
            funcs2 = set(analysis2["functions"])
            func_similarity = len(funcs1.intersection(funcs2)) / max(
                len(funcs1.union(funcs2)),
                1,
            )

            # Compare content using difflib
            content1 = analysis1["content"]
            content2 = analysis2["content"]
            content_similarity = difflib.SequenceMatcher(
                None,
                content1,
                content2,
            ).ratio()

            # Weighted average
            total_similarity = (
                pattern_similarity * 0.3
                + import_similarity * 0.2
                + func_similarity * 0.2
                + content_similarity * 0.3
            )

            return total_similarity

        except Exception as e:
            logger.warning(
                f"Error calculating similarity between {file1} and {file2}: {e}",
            )
            return 0.0

    def select_best_file(self, files: list[Path]) -> Path:
        """Select the best file from a group based on quality metrics."""
        if not files:
            return None

        if len(files) == 1:
            return files[0]

        # Analyze all files if not already done
        for file_path in files:
            if file_path not in self.content_analysis:
                self.content_analysis[file_path] = self.analyze_file_content(file_path)

        # Score files based on quality metrics
        scored_files = []
        for file_path in files:
            analysis = self.content_analysis[file_path]

            # Calculate composite score
            score = (
                analysis["quality_score"] * 10  # Quality indicators
                + analysis["complexity_score"] * 2  # Complexity
                + len(analysis["functions"]) * 3  # Number of functions
                + len(analysis["classes"]) * 5  # Number of classes
                + (1 if analysis["openai_usage"] else 0) * 5  # OpenAI usage
                + (1 if analysis["quality_indicators"].get("has_docstring") else 0)
                * 3  # Docstrings
                + (1 if analysis["quality_indicators"].get("has_error_handling") else 0)
                * 2  # Error handling
                + analysis["size"] // 1000  # Size bonus
            )

            scored_files.append((file_path, score, analysis))

        # Sort by score (descending)
        scored_files.sort(key=lambda x: x[1], reverse=True)

        best_file = scored_files[0][0]
        logger.info(
            f"Selected best file: {best_file.name} (score: {scored_files[0][1]})",
        )

        return best_file

    def create_merged_file(self, files: list[Path], output_path: Path) -> bool:
        """Create a merged file combining the best features from multiple files."""
        try:
            if not files:
                return False

            # Select the best base file
            base_file = self.select_best_file(files)
            if not base_file:
                return False

            # Read base file content
            with open(base_file, encoding="utf-8") as f:
                base_content = f.read()

            # Analyze all files to extract unique features
            all_analyses = []
            for file_path in files:
                if file_path not in self.content_analysis:
                    self.content_analysis[file_path] = self.analyze_file_content(
                        file_path,
                    )
                all_analyses.append(self.content_analysis[file_path])

            # Extract unique functions, classes, and imports
            all_functions = set()
            all_classes = set()
            all_imports = set()
            all_docstrings = set()

            for analysis in all_analyses:
                all_functions.update(analysis["functions"])
                all_classes.update(analysis["classes"])
                all_imports.update(analysis["imports"])
                all_docstrings.update(analysis["docstrings"])

            # Create merged content
            merged_content = self._create_merged_content(
                base_content,
                all_functions,
                all_classes,
                all_imports,
                all_docstrings,
                files,
            )

            # Write merged file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(merged_content)

            logger.info(f"Created merged file: {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error creating merged file {output_path}: {e}")
            return False

    def _create_merged_content(:
        self,
        base_content: str,
        all_functions: set[str],
        all_classes: set[str],
        all_imports: set[str],
        all_docstrings: set[str],
        source_files: list[Path],
    ) -> str:
        """Create merged content combining features from multiple files."""
        # Start with enhanced header
        merged_content = f"\'"#!/usr/bin/env python3
"""
Merged Content Analysis Tool

This file was automatically merged from the following source files:
{chr(10).join(f"- {f}" for f in source_files)}

Combines the best features and functionality from multiple similar files.
"""

"\'"

        # Add all unique imports
        if all_imports:
            merged_content += "# Imports from all source files\n"
            for imp in sorted(all_imports):
                merged_content += f"{imp}\n"
            merged_content += "\n"

        # Add docstrings
        if all_docstrings:
            merged_content += "# Documentation from source files\n"
            for doc in all_docstrings:
                if doc.strip():
                    merged_content += f"{doc}\n"
            merged_content += "\n"

        # Add the main content (simplified version of base content)
        # Remove the original header and basic structure
        lines = base_content.split("\n")
        content_start = 0

        # Find where the actual code starts (after imports and docstrings)
        for i, line in enumerate(lines):
            if (
                line.strip()
                and not line.strip().startswith("#")
                and not line.strip().startswith('\"\'"')
                and not line.strip().startswith("\'"'"")
                and not line.strip().startswith("import ")
                and not line.strip().startswith("from ")
            ):
                content_start = i
                break

        # Add the main content
        main_content = "\n".join(lines[content_start:])
        merged_content += main_content

        return merged_content

    def run_deep_analysis_and_merge(self):
        """Run the complete deep analysis and merge process."""
        logger.info("Starting deep analysis and merge process...")

        try:
            # Step 1: Find exact duplicates
            exact_duplicates = self.find_exact_duplicates()

            # Step 2: Find similar files
            similar_groups = self.find_similar_files()

            # Step 3: Create merged directory
            self.merged_dir.mkdir(exist_ok=True)

            # Step 4: Process exact duplicates
            logger.info("Processing exact duplicates...")
            for hash_val, files in exact_duplicates.items():
                best_file = self.select_best_file(files)
                if best_file:
                    # Copy best file to merged directory
                    target_path = self.merged_dir / best_file.name
                    self._copy_file(best_file, target_path)
                    logger.info(f"Kept best duplicate: {best_file.name}")

            # Step 5: Process similar files
            logger.info("Processing similar files...")
            for group_name, files in similar_groups.items():
                if len(files) > 1:
                    # Create merged file
                    merged_filename = self._generate_merged_filename(files)
                    merged_path = self.merged_dir / merged_filename

                    if self.create_merged_file(files, merged_path):
                        logger.info(
                            f"Created merged file: {merged_filename} from {len(files)} files",
                        )
                    else:
                        # Fallback: just copy the best file
                        best_file = self.select_best_file(files)
                        if best_file:
                            target_path = self.merged_dir / best_file.name
                            self._copy_file(best_file, target_path)
                            logger.info(f"Kept best file: {best_file.name}")

            # Step 6: Generate analysis report
            self._generate_analysis_report(exact_duplicates, similar_groups)

            logger.info("Deep analysis and merge process completed!")

        except Exception as e:
            logger.error(f"Error during deep analysis and merge: {e}")
            raise

    def _copy_file(self, src: Path, dst: Path):
        """Copy file from source to destination."""
        try:
            import shutil

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        except Exception as e:
            logger.error(f"Error copying {src} to {dst}: {e}")

    def _generate_merged_filename(self, files: list[Path]) -> str:
        """Generate a filename for merged files."""
        # Get common base name
        base_names = [f.stem for f in files]
        common_prefix = os.path.commonprefix(base_names)

        if common_prefix:
            return f"{common_prefix}_merged.py"
        return f"merged_{len(files)}_files.py"

    def _generate_analysis_report(:
        self,
        exact_duplicates: dict[str, list[Path]],
        similar_groups: dict[str, list[Path]],
    ):
        """Generate comprehensive analysis report."""
        report_path = self.merged_dir / "DEEP_ANALYSIS_REPORT.md"

        with open(report_path, "w") as f:
            f.write("# Deep Analysis and Merge Report\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
            )

            f.write("## Overview\n\n")
            f.write(f"- **Exact duplicate groups:** {len(exact_duplicates)}\n")
            f.write(f"- **Similar file groups:** {len(similar_groups)}\n")
            f.write(f"- **Total files analyzed:** {len(self.content_analysis)}\n\n")

            f.write("## Exact Duplicates Found\n\n")
            for hash_val, files in exact_duplicates.items():
                f.write(f"### Group {hash_val[:8]}...\n")
                f.write(f"Files: {len(files)}\n")
                f.writelines(f"- {file_path}\n" for file_path in files)
                f.write("\n")

            f.write("## Similar File Groups\n\n")
            for group_name, files in similar_groups.items():
                f.write(f"### {group_name}\n")
                f.write(f"Files: {len(files)}\n")
                for file_path in files:
                    analysis = self.content_analysis.get(file_path, {})
                    f.write(
                        f"- {file_path} (Quality: {analysis.get('quality_score', 0)})\n",
                    )
                f.write("\n")

            f.write("## Quality Analysis Summary\n\n")
            quality_stats = defaultdict(int)
            for analysis in self.content_analysis.values():
                quality_stats[analysis.get("quality_score", 0)] += 1

            f.writelines(
                f"- Quality Score {score}: {count} files\n"
                for score, count in sorted(quality_stats.items())
            )

            f.write("\n## Functionality Patterns\n\n")
            pattern_stats = defaultdict(int)
            for analysis in self.content_analysis.values():
                for pattern in analysis.get("functionality_patterns", []):
                    pattern_stats[pattern] += 1

            for pattern, count in sorted(
                pattern_stats.items(),
                key=lambda x: x[1],
                reverse=True,
            ):
                f.write(f"- {pattern}: {count} files\n")


def main():
    """Main function."""
    base_dir = "/Users/steven/Music/nocTurneMeLoDieS/python"

    if not os.path.exists(base_dir):
        logger.error(f"Base directory not found: {base_dir}")
        return

    merger = DeepAnalysisMerger(base_dir)
    merger.run_deep_analysis_and_merge()


if __name__ == "__main__":
    main()
