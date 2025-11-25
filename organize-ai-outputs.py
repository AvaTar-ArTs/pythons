#!/usr/bin/env python3
"""
AI Outputs Hub - Auto-Organize Dry Run
Shows what auto-organize would do without making changes
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class AutoOrganizeDryRun:
    def __init__(self, base_dir=Path(str(Path.home()) + "/AI_Outputs_Hub")):
        """__init__ function."""

        self.base_dir = Path(base_dir)
        self.analysis_results = {
            "files_analyzed": 0,
            "suggested_moves": [],
            "category_suggestions": {},
            "duplicate_files": [],
            "missing_metadata": [],
            "organization_opportunities": [],
        }

    def analyze_file_content(self, file_path):
        """Analyze file content to suggest categories and organization"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract title from filename
            filename = file_path.name
            title = (
                filename.replace(".html", "")
                .replace(".markdown", "")
                .replace(".md", "")
            )

            # Analyze content for category suggestions
            content_lower = content.lower()

            # Category detection keywords
            category_keywords = {
                "seo_analysis": [
                    "seo",
                    "keyword",
                    "trending",
                    "optimization",
                    "ranking",
                    "search",
                    "google",
                ],
                "creative_automation": [
                    "creative",
                    "automation",
                    "ai",
                    "generation",
                    "art",
                    "design",
                    "content",
                ],
                "brand_strategy": [
                    "brand",
                    "strategy",
                    "marketing",
                    "positioning",
                    "identity",
                    "logo",
                ],
                "technical_docs": [
                    "technical",
                    "documentation",
                    "api",
                    "code",
                    "development",
                    "programming",
                ],
                "content_creation": [
                    "content",
                    "writing",
                    "blog",
                    "article",
                    "copy",
                    "text",
                ],
                "business_analysis": [
                    "business",
                    "analysis",
                    "strategy",
                    "plan",
                    "report",
                    "metrics",
                ],
                "conversations": [
                    "conversation",
                    "chat",
                    "discussion",
                    "analysis",
                    "cursor-agent",
                ],
            }

            # Score each category
            category_scores = {}
            for category, keywords in category_keywords.items():
                score = sum(1 for keyword in keywords if keyword in content_lower)
                if score > 0:
                    category_scores[category] = score

            # Get top category
            suggested_category = (
                max(category_scores.items(), key=lambda x: x[1])[0]
                if category_scores
                else "general"
            )

            # Extract potential tags
            tags = []
            if "cursor-agent" in content_lower or "cursor agent" in content_lower:
                tags.append("cursor-agent")
            if "analysis" in content_lower:
                tags.append("analysis")
            if "comprehensive" in content_lower:
                tags.append("comprehensive")
            if "comparative" in content_lower:
                tags.append("comparative")
            if "html" in filename.lower():
                tags.append("html")
            if "markdown" in filename.lower() or "md" in filename.lower():
                tags.append("markdown")

            return {
                "filename": filename,
                "title": title,
                "suggested_category": suggested_category,
                "category_score": category_scores.get(suggested_category, 0),
                "suggested_tags": tags,
                "file_size": len(content),
                "content_preview": (
                    content[:CONSTANT_200] + "..."
                    if len(content) > CONSTANT_200
                    else content
                ),
            }

        except Exception as e:
            return {
                "filename": file_path.name,
                "error": str(e),
                "suggested_category": "general",
                "suggested_tags": [],
            }

    def find_duplicates(self):
        """Find potential duplicate files"""
        file_hashes = {}
        duplicates = []

        for file_path in self.base_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        file_hash = hash(content)

                        if file_hash in file_hashes:
                            duplicates.append(
                                {
                                    "original": str(file_hashes[file_hash]),
                                    "duplicate": str(file_path),
                                    "size": len(content),
                                }
                            )
                        else:
                            file_hashes[file_hash] = file_path
                except (OSError, IOError, FileNotFoundError):
                    continue

        return duplicates

    def analyze_directory_structure(self):
        """Analyze current directory structure and suggest improvements"""
        structure_analysis = {"current_structure": {}, "suggestions": []}

        # Analyze current structure
        for category_dir in (self.base_dir / "Categories").iterdir():
            if category_dir.is_dir():
                file_count = len([f for f in category_dir.iterdir() if f.is_file()])
                structure_analysis["current_structure"][category_dir.name] = file_count

        # Analyze Projects directory
        for project_dir in (self.base_dir / "Projects").iterdir():
            if project_dir.is_dir():
                file_count = len([f for f in project_dir.iterdir() if f.is_file()])
                structure_analysis["current_structure"][
                    f"Projects/{project_dir.name}"
                ] = file_count

        # Generate suggestions
        if structure_analysis["current_structure"].get("technical_docs", 0) > 10:
            structure_analysis["suggestions"].append(
                {
                    "type": "subcategory",
                    "category": "technical_docs",
                    "suggestion": 'Consider creating subcategories like "api-docs", "tutorials", "reference"',
                }
            )

        if (
            structure_analysis["current_structure"].get(
                "Projects/cursor-agent-analysis", 0
            )
            > 5
        ):
            structure_analysis["suggestions"].append(
                {
                    "type": "project_organization",
                    "project": "cursor-agent-analysis",
                    "suggestion": "Consider organizing by date or analysis type within the project",
                }
            )

        return structure_analysis

    def run_dry_run(self):
        """Run the complete dry-run analysis"""
        logger.info("🔍 AI Outputs Hub - Auto-Organize Dry Run")
        logger.info("=" * 60)
        logger.info(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"📁 Hub Directory: {self.base_dir}")
        print()

        # Analyze all files
        logger.info("📊 FILE ANALYSIS")
        logger.info("-" * 30)

        all_files = []
        for file_path in self.base_dir.rglob("*"):
            if (
                file_path.is_file()
                and not file_path.name.startswith(".")
                and file_path.suffix in [".html", ".md", ".markdown"]
            ):
                analysis = self.analyze_file_content(file_path)
                all_files.append(analysis)
                self.analysis_results["files_analyzed"] += 1

        # Show file analysis results
        for file_analysis in all_files:
            if "error" not in file_analysis:
                logger.info(f"📄 {file_analysis['filename']}")
                logger.info(
                    f"   📂 Suggested Category: {file_analysis['suggested_category']}"
                )
                logger.info(
                    f"   🏷️  Suggested Tags: {', '.join(file_analysis['suggested_tags'])}"
                )
                logger.info(
                    f"   📏 File Size: {file_analysis['file_size']:,} characters"
                )
                logger.info(f"   📝 Preview: {file_analysis['content_preview']}")
                print()

        # Find duplicates
        logger.info("🔍 DUPLICATE FILE DETECTION")
        logger.info("-" * 30)
        duplicates = self.find_duplicates()
        if duplicates:
            for dup in duplicates:
                logger.info(f"⚠️  Duplicate found:")
                logger.info(f"   Original: {dup['original']}")
                logger.info(f"   Duplicate: {dup['duplicate']}")
                logger.info(f"   Size: {dup['size']:,} bytes")
                print()
        else:
            logger.info("✅ No duplicate files found")
            print()

        # Analyze directory structure
        logger.info("📁 DIRECTORY STRUCTURE ANALYSIS")
        logger.info("-" * 30)
        structure = self.analyze_directory_structure()

        logger.info("Current Structure:")
        for location, count in structure["current_structure"].items():
            logger.info(f"   📂 {location}: {count} files")
        print()

        if structure["suggestions"]:
            logger.info("💡 Organization Suggestions:")
            for suggestion in structure["suggestions"]:
                logger.info(f"   • {suggestion['suggestion']}")
            print()

        # Generate organization recommendations
        logger.info("🎯 ORGANIZATION RECOMMENDATIONS")
        logger.info("-" * 30)

        # Group files by suggested category
        category_groups = defaultdict(list)
        for file_analysis in all_files:
            if "error" not in file_analysis:
                category_groups[file_analysis["suggested_category"]].append(
                    file_analysis
                )

        for category, files in category_groups.items():
            if len(files) > 0:
                logger.info(f"📂 {category.upper()}:")
                for file_analysis in files:
                    current_location = "Unknown"
                    # Try to determine current location
                    for file_path in self.base_dir.rglob(file_analysis["filename"]):
                        if file_path.exists():
                            current_location = str(file_path.relative_to(self.base_dir))
                            break

                    logger.info(f"   📄 {file_analysis['filename']}")
                    logger.info(f"      Current: {current_location}")
                    logger.info(f"      Suggested: Categories/{category}/")
                    if file_analysis["suggested_tags"]:
                        logger.info(
                            f"      Tags: {', '.join(file_analysis['suggested_tags'])}"
                        )
                    print()

        # Summary
        logger.info("📋 DRY RUN SUMMARY")
        logger.info("-" * 30)
        logger.info(f"📊 Files Analyzed: {self.analysis_results['files_analyzed']}")
        logger.info(f"🔍 Duplicates Found: {len(duplicates)}")
        logger.info(f"📂 Categories Identified: {len(category_groups)}")
        logger.info(f"💡 Suggestions Generated: {len(structure['suggestions'])}")
        print()

        logger.info("⚠️  This was a DRY RUN - no files were moved or modified")
        logger.info("✅ To apply these changes, run the actual auto-organize function")

        return self.analysis_results


if __name__ == "__main__":
    organizer = AutoOrganizeDryRun()
    organizer.run_dry_run()
