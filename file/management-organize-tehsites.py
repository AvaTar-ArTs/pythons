"""
File Management Organize Tehsites 8

This module provides functionality for file management organize tehsites 8.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100
CONSTANT_1024 = 1024
CONSTANT_4096 = 4096
CONSTANT_10000 = 10000

#!/usr/bin/env python3
"""
TehSiTes Deep Content-Aware Analysis Script
Finds and organizes content at 15+ levels deep with intelligent content analysis
"""

import os
import shutil
import hashlib
from pathlib import Path
import logging
from collections import defaultdict
import json
import time
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DeepContentAwareTehSiTes:
    def __init__(self, tehSiTes_dir):
        """__init__ function."""

        self.tehSiTes_dir = Path(tehSiTes_dir)
        self.deep_analysis = {}
        self.deep_paths = []
        self.content_groups = defaultdict(list)
        self.duplicates_found = 0
        self.files_removed = 0
        self.space_saved = 0
        self.cleanup_log = []
        self.start_time = time.time()
        self.max_depth = 0

    def analyze_deep_content(self, min_depth=15):
        """Analyze content at 15+ levels deep with content awareness"""
        logger.info(f"Analyzing content at {min_depth}+ levels deep...")

        total_files = 0
        deep_files = 0
        deep_dirs = 0

        for root, dirs, files in os.walk(self.tehSiTes_dir):
            current_depth = len(Path(root).parts) - len(self.tehSiTes_dir.parts)
            self.max_depth = max(self.max_depth, current_depth)

            # Skip certain directories
            if any(skip in root for skip in ["node_modules", ".git", "__pycache__", ".venv"]):
                continue

            # Track deep paths
            if current_depth >= min_depth:
                deep_dirs += 1
                if deep_dirs % CONSTANT_100 == 0:
                    logger.info(f"Found {deep_dirs} directories at depth {current_depth}+")

                # Analyze deep directory content
                deep_analysis = self.analyze_directory_content_deep(Path(root), current_depth)
                if deep_analysis:
                    self.deep_paths.append(deep_analysis)

            for file in files:
                file_path = Path(root) / file
                if file_path.is_file():
                    total_files += 1
                    if total_files % CONSTANT_10000 == 0:
                        logger.info(f"Processed {total_files} files (max depth: {self.max_depth})...")

                    if current_depth >= min_depth:
                        deep_files += 1

        logger.info(f"Analysis complete:")
        logger.info(f"  Total files: {total_files}")
        logger.info(f"  Files at depth {min_depth}+: {deep_files}")
        logger.info(f"  Directories at depth {min_depth}+: {deep_dirs}")
        logger.info(f"  Maximum depth reached: {self.max_depth}")

        return deep_files, deep_dirs

    def analyze_directory_content_deep(self, dir_path, depth):
        """Deep content analysis for directories at 15+ levels"""
        if not dir_path.exists():
            return None

        analysis = {
            "path": str(dir_path),
            "name": dir_path.name,
            "depth": depth,
            "file_types": defaultdict(int),
            "file_count": 0,
            "total_size": 0,
            "has_package_json": False,
            "has_requirements_txt": False,
            "has_readme": False,
            "has_index_html": False,
            "has_avatararts": False,
            "has_quantumforgelabs": False,
            "has_dr_adu": False,
            "has_seo": False,
            "has_portfolio": False,
            "has_gallery": False,
            "has_tools": False,
            "has_org": False,
            "has_hub": False,
            "has_react": False,
            "has_nextjs": False,
            "has_python": False,
            "has_node": False,
            "keywords": set(),
            "deep_files": [],
            "content_category": "unknown",
        }

        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.is_file():
                        analysis["file_count"] += 1
                        analysis["total_size"] += file_path.stat().st_size

                        # Track deep files
                        file_depth = len(file_path.parts) - len(self.tehSiTes_dir.parts)
                        if file_depth >= 15:
                            analysis["deep_files"].append(
                                {
                                    "path": str(file_path),
                                    "name": file.name,
                                    "depth": file_depth,
                                    "size": file_path.stat().st_size,
                                }
                            )

                        # Analyze file extension
                        ext = file_path.suffix.lower()
                        analysis["file_types"][ext] += 1

                        # Check for specific files
                        if file.name.lower() == "package.json":
                            analysis["has_package_json"] = True
                        elif file.name.lower() == "requirements.txt":
                            analysis["has_requirements_txt"] = True
                        elif file.name.lower() in ["readme.md", "readme.txt", "readme"]:
                            analysis["has_readme"] = True
                        elif file.name.lower() == "index.html":
                            analysis["has_index_html"] = True

                        # Analyze file content for keywords
                        try:
                            if file_path.suffix.lower() in [
                                ".md",
                                ".txt",
                                ".html",
                                ".js",
                                ".py",
                                ".json",
                                ".jsx",
                                ".tsx",
                                ".ts",
                            ]:
                                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                                    content = f.read().lower()

                                    if "avatararts" in content:
                                        analysis["has_avatararts"] = True
                                        analysis["keywords"].add("avatararts")
                                    if "quantumforgelabs" in content:
                                        analysis["has_quantumforgelabs"] = True
                                        analysis["keywords"].add("quantumforgelabs")
                                    if "dr.adu" in content or "dr adu" in content or "gainesville" in content:
                                        analysis["has_dr_adu"] = True
                                        analysis["keywords"].add("dr_adu")
                                    if "seo" in content or "search engine" in content:
                                        analysis["has_seo"] = True
                                        analysis["keywords"].add("seo")
                                    if "portfolio" in content:
                                        analysis["has_portfolio"] = True
                                        analysis["keywords"].add("portfolio")
                                    if "gallery" in content:
                                        analysis["has_gallery"] = True
                                        analysis["keywords"].add("gallery")
                                    if "tools" in content or "utilities" in content:
                                        analysis["has_tools"] = True
                                        analysis["keywords"].add("tools")
                                    if "react" in content or "jsx" in content:
                                        analysis["has_react"] = True
                                        analysis["keywords"].add("react")
                                    if "next" in content or "nextjs" in content:
                                        analysis["has_nextjs"] = True
                                        analysis["keywords"].add("nextjs")
                                    if "python" in content or "import " in content:
                                        analysis["has_python"] = True
                                        analysis["keywords"].add("python")
                                    if "node" in content or "npm" in content:
                                        analysis["has_node"] = True
                                        analysis["keywords"].add("node")
                        except (IndexError, KeyError):
                            pass

                # Analyze directory name for keywords
                dir_name_lower = dir_path.name.lower()
                if "avatararts" in dir_name_lower:
                    analysis["has_avatararts"] = True
                    analysis["keywords"].add("avatararts")
                if "quantumforgelabs" in dir_name_lower:
                    analysis["has_quantumforgelabs"] = True
                    analysis["keywords"].add("quantumforgelabs")
                if "dr" in dir_name_lower and "adu" in dir_name_lower:
                    analysis["has_dr_adu"] = True
                    analysis["keywords"].add("dr_adu")
                if "seo" in dir_name_lower:
                    analysis["has_seo"] = True
                    analysis["keywords"].add("seo")
                if "portfolio" in dir_name_lower:
                    analysis["has_portfolio"] = True
                    analysis["keywords"].add("portfolio")
                if "gallery" in dir_name_lower:
                    analysis["has_gallery"] = True
                    analysis["keywords"].add("gallery")
                if "tools" in dir_name_lower:
                    analysis["has_tools"] = True
                    analysis["keywords"].add("tools")
                if "org" in dir_name_lower:
                    analysis["has_org"] = True
                    analysis["keywords"].add("org")
                if "hub" in dir_name_lower:
                    analysis["has_hub"] = True
                    analysis["keywords"].add("hub")

            # Determine content category
            analysis["content_category"] = self.determine_content_category(analysis)

        except Exception as e:
            logger.error(f"Error analyzing deep directory {dir_path}: {e}")

        return analysis

    def determine_content_category(self, analysis):
        """Determine the content category based on analysis"""
        if analysis["has_avatararts"]:
            if analysis["has_gallery"]:
                return "avatararts_gallery"
            elif analysis["has_portfolio"]:
                return "avatararts_portfolio"
            elif analysis["has_tools"]:
                return "avatararts_tools"
            elif analysis["has_org"]:
                return "avatararts_org"
            elif analysis["has_hub"]:
                return "avatararts_hub"
            else:
                return "avatararts_general"
        elif analysis["has_quantumforgelabs"]:
            return "quantumforgelabs"
        elif analysis["has_dr_adu"]:
            return "dr_adu"
        elif analysis["has_seo"]:
            return "seo"
        elif analysis["has_react"] or analysis["has_nextjs"]:
            return "web_development"
        elif analysis["has_python"]:
            return "python_development"
        elif analysis["has_node"]:
            return "node_development"
        elif analysis["has_package_json"]:
            return "javascript_project"
        elif analysis["has_requirements_txt"]:
            return "python_project"
        else:
            return "general"

    def group_deep_content(self):
        """Group deep content by category and similarity"""
        logger.info("Grouping deep content by category...")

        for analysis in self.deep_paths:
            category = analysis["content_category"]
            self.content_groups[category].append(analysis)

        # Log grouping results
        for category, analyses in self.content_groups.items():
            logger.info(f"{category}: {len(analyses)} deep directories")
            for analysis in analyses[:3]:  # Show first 3 examples
                logger.info(f"  - {analysis['name']} (depth {analysis['depth']}, {analysis['file_count']} files)")

    def find_deep_duplicates(self):
        """Find duplicate files in deep structures"""
        logger.info("Finding duplicate files in deep structures...")

        file_hashes = defaultdict(list)

        for analysis in self.deep_paths:
            for deep_file in analysis["deep_files"]:
                file_path = Path(deep_file["path"])
                if file_path.exists():
                    file_hash = self.calculate_file_hash(file_path)
                    if file_hash:
                        file_hashes[file_hash].append(file_path)

        # Count duplicates
        for file_hash, file_list in file_hashes.items():
            if len(file_list) > 1:
                self.duplicates_found += len(file_list) - 1

                # Remove duplicates, keeping the shallowest
                file_list.sort(key=lambda x: len(x.parts))
                keep_file = file_list[0]
                remove_files = file_list[1:]

                for file_to_remove in remove_files:
                    try:
                        file_size = file_to_remove.stat().st_size
                        file_to_remove.unlink()
                        self.files_removed += 1
                        self.space_saved += file_size
                        self.cleanup_log.append(
                            {
                                "action": "REMOVED_DEEP_DUPLICATE",
                                "file": str(file_to_remove),
                                "kept": str(keep_file),
                                "size": file_size,
                                "depth": len(file_to_remove.parts) - len(self.tehSiTes_dir.parts),
                            }
                        )
                    except Exception as e:
                        logger.error(f"Error removing deep duplicate {file_to_remove}: {e}")

        logger.info(f"Found and removed {self.duplicates_found} duplicate files in deep structures")

    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(CONSTANT_4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return None

    def flatten_deep_structures(self):
        """Flatten overly deep directory structures"""
        logger.info("Flattening deep directory structures...")

        # Find directories that are too deep (20+ levels)
        deep_dirs = [analysis for analysis in self.deep_paths if analysis["depth"] >= 20]

        flattened_count = 0
        for analysis in deep_dirs:
            try:
                dir_path = Path(analysis["path"])
                if not dir_path.exists():
                    continue

                # Find a suitable parent directory to move files to
                target_depth = 10  # Target depth
                current_path = dir_path
                target_path = None

                # Walk up the directory tree to find a suitable parent
                for _ in range(analysis["depth"] - target_depth):
                    current_path = current_path.parent
                    if len(current_path.parts) - len(self.tehSiTes_dir.parts) <= target_depth:
                        target_path = current_path
                        break

                if target_path and target_path != dir_path:
                    # Move files from deep directory to shallower location
                    for item in dir_path.iterdir():
                        if item.is_file():
                            dest_path = target_path / item.name
                            if not dest_path.exists():
                                shutil.move(str(item), str(dest_path))
                                flattened_count += 1
                                self.cleanup_log.append(
                                    {
                                        "action": "FLATTENED_DEEP_FILE",
                                        "file": str(item),
                                        "destination": str(dest_path),
                                        "original_depth": analysis["depth"],
                                    }
                                )

                # Remove empty deep directory
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    self.cleanup_log.append(
                        {"action": "REMOVED_EMPTY_DEEP_DIR", "directory": str(dir_path), "depth": analysis["depth"]}
                    )

            except Exception as e:
                logger.error(f"Error flattening {analysis['path']}: {e}")

        logger.info(f"Flattened {flattened_count} files from deep structures")

    def organize_deep_content(self):
        """Organize deep content into appropriate locations"""
        logger.info("Organizing deep content into appropriate locations...")

        # Create organized directories for each category
        organized_base = self.tehSiTes_dir / "DEEP_ORGANIZED"
        organized_base.mkdir(exist_ok=True)

        for category, analyses in self.content_groups.items():
            category_dir = organized_base / category
            category_dir.mkdir(exist_ok=True)

            for analysis in analyses:
                try:
                    source_dir = Path(analysis["path"])
                    if not source_dir.exists():
                        continue

                    # Create a meaningful name for the deep directory
                    depth_suffix = f"_depth_{analysis['depth']}"
                    target_name = f"{analysis['name']}{depth_suffix}"
                    target_dir = category_dir / target_name

                    # Move the directory
                    if not target_dir.exists():
                        shutil.move(str(source_dir), str(target_dir))
                        self.cleanup_log.append(
                            {
                                "action": "ORGANIZED_DEEP_DIRECTORY",
                                "source": str(source_dir),
                                "destination": str(target_dir),
                                "category": category,
                                "depth": analysis["depth"],
                            }
                        )
                        logger.info(f"Organized {source_dir.name} to {category}/{target_name}")

                except Exception as e:
                    logger.error(f"Error organizing {analysis['path']}: {e}")

    def create_deep_analysis_report(self):
        """Create comprehensive deep analysis report"""
        report_file = self.tehSiTes_dir / "DEEP_CONTENT_ANALYSIS_REPORT.txt"

        with open(report_file, "w") as f:
            f.write("=== TEHSITES DEEP CONTENT-AWARE ANALYSIS REPORT ===\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Time: {time.time() - self.start_time:.2f} seconds\n\n")

            f.write("=== DEPTH ANALYSIS ===\n")
            f.write(f"Maximum Depth Reached: {self.max_depth}\n")
            f.write(f"Deep Directories Found: {len(self.deep_paths)}\n")
            f.write(f"Deep Files Found: {sum(len(analysis['deep_files']) for analysis in self.deep_paths)}\n\n")

            f.write("=== CONTENT CATEGORIES ===\n")
            for category, analyses in self.content_groups.items():
                f.write(f"\n{category.upper()}:\n")
                f.write(f"  Directories: {len(analyses)}\n")
                f.write(f"  Total Files: {sum(analysis['file_count'] for analysis in analyses)}\n")
                f.write(
                    f"  Total Size: {sum(analysis['total_size'] for analysis in analyses) / (CONSTANT_1024*CONSTANT_1024):.2f} MB\n"
                )
                f.write(f"  Examples:\n")
                for analysis in analyses[:5]:  # Show first 5 examples
                    f.write(f"    - {analysis['name']} (depth {analysis['depth']}, {analysis['file_count']} files)\n")
            f.write(Path("\n"))

            f.write("=== DEEPEST PATHS ===\n")
            sorted_paths = sorted(self.deep_paths, key=lambda x: x["depth"], reverse=True)
            for analysis in sorted_paths[:20]:  # Show top 20 deepest
                f.write(f"Depth {analysis['depth']}: {analysis['path']}\n")
            f.write(Path("\n"))

            f.write("=== CLEANUP SUMMARY ===\n")
            f.write(f"Duplicate Files Found: {self.duplicates_found}\n")
            f.write(f"Files Removed: {self.files_removed}\n")
            f.write(f"Space Saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB\n")
            f.write(f"Cleanup Actions: {len(self.cleanup_log)}\n\n")

            f.write("=== CLEANUP ACTIONS ===\n")
            for log_entry in self.cleanup_log:
                f.write(
                    f"{log_entry['action']}: {log_entry.get('file', log_entry.get('directory', log_entry.get('source', 'N/A')))}\n"
                )
                if "destination" in log_entry:
                    f.write(f"  Destination: {log_entry['destination']}\n")
                if "kept" in log_entry:
                    f.write(f"  Kept: {log_entry['kept']}\n")
                if "size" in log_entry:
                    f.write(f"  Size: {log_entry['size']} bytes\n")
                if "depth" in log_entry:
                    f.write(f"  Depth: {log_entry['depth']}\n")
                if "category" in log_entry:
                    f.write(f"  Category: {log_entry['category']}\n")
                f.write(Path("\n"))

            f.write("=== RECOMMENDATIONS ===\n")
            f.write("1. Review the DEEP_ORGANIZED directory structure\n")
            f.write("2. Consider archiving very deep content\n")
            f.write("3. Implement depth limits for new projects\n")
            f.write("4. Use symbolic links for deep structures when needed\n")
            f.write("5. Regular deep cleanup to prevent excessive nesting\n")

        logger.info(f"Deep content analysis report saved to {report_file}")

    def run_deep_content_analysis(self):
        """Run the complete deep content analysis"""
        logger.info("Starting deep content-aware analysis (15+ levels)...")

        # Analyze deep content
        deep_files, deep_dirs = self.analyze_deep_content(min_depth=15)

        if deep_dirs == 0:
            logger.info("No directories found at 15+ levels deep. Checking 10+ levels...")
            deep_files, deep_dirs = self.analyze_deep_content(min_depth=10)

        if deep_dirs == 0:
            logger.info("No directories found at 10+ levels deep. Checking 8+ levels...")
            deep_files, deep_dirs = self.analyze_deep_content(min_depth=8)

        if deep_dirs > 0:
            # Group and organize deep content
            self.group_deep_content()
            self.find_deep_duplicates()
            self.flatten_deep_structures()
            self.organize_deep_content()
        else:
            logger.info("No deep directories found to organize")

        self.create_deep_analysis_report()

        logger.info("Deep content analysis completed!")
        logger.info(f"Total files removed: {self.files_removed}")
        logger.info(f"Total space saved: {self.space_saved / (CONSTANT_1024*CONSTANT_1024):.2f} MB")
        logger.info(f"Maximum depth reached: {self.max_depth}")


if __name__ == "__main__":
    tehSiTes_dir = Path("/Users/steven/tehSiTes")
    analyzer = DeepContentAwareTehSiTes(tehSiTes_dir)
    analyzer.run_deep_content_analysis()
