"""
Html Keep Or Remove Audit

This module provides functionality for html keep or remove audit.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
HTML Content Analyzer
Uses deep analysis and fluid awareness to determine what's worth keeping vs removable
"""

import os
import re
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import hashlib


class HTMLContentAnalyzer:
    """Analyzes HTML content to determine value and ownership."""

    def __init__(self):
        """__init__ function."""

        self.html_path = Path(Path(str(Path.home()) + "/Documents/HTML"))
        self.max_depth = 6

        # Analysis results
        self.analysis_results = {
            "worth_keeping": [],
            "removable": [],
            "duplicates": [],
            "generated_content": [],
            "personal_content": [],
            "documentation": [],
            "templates": [],
            "unknown": [],
        }

        # Patterns for different content types
        self.patterns = {
            "personal_content": [
                r"steven",
                r"chaplinski",
                r"personal",
                r"bio",
                r"profile",
                r"portfolio",
                r"resume",
                r"cv",
                r"about",
                r"contact",
            ],
            "generated_content": [
                r"generated",
                r"auto",
                r"bot",
                r"output",
                r"created",
                r"documentation_",
                r"pydoc_",
                r"html-generator_",
                r"legacy_categories_",
                r"archived_",
                r"backups_",
            ],
            "documentation": [
                r"readme",
                r"docs",
                r"guide",
                r"tutorial",
                r"manual",
                r"api",
                r"reference",
                r"help",
                r"instructions",
            ],
            "templates": [
                r"template",
                r"example",
                r"sample",
                r"demo",
                r"test",
                r"placeholder",
                r"boilerplate",
                r"starter",
            ],
            "duplicate_indicators": [
                r"\(\d+\)",
                r"_\d+$",
                r"copy",
                r"duplicate",
                r"backup",
                r"old",
                r"version",
                r"v\d+",
                r"_\d{8}",
            ],
        }

    def analyze_html_content(self, file_path):
        """Analyze HTML file content for value assessment."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Basic file info
            file_info = {
                "path": str(file_path),
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "modified": file_path.stat().st_mtime,
                "depth": len(file_path.relative_to(self.html_path).parts),
                "content_hash": hashlib.md5(content.encode()).hexdigest(),
                "content_length": len(content),
                "analysis": {},
            }

            # Content analysis
            file_info["analysis"] = {
                "title": self._extract_title(content),
                "has_scripts": bool(re.search(r"<script", content, re.IGNORECASE)),
                "has_styles": bool(re.search(r"<style", content, re.IGNORECASE)),
                "has_forms": bool(re.search(r"<form", content, re.IGNORECASE)),
                "has_images": bool(re.search(r"<img", content, re.IGNORECASE)),
                "has_links": bool(re.search(r"<a\s+href", content, re.IGNORECASE)),
                "word_count": len(re.findall(r"\b\w+\b", content)),
                "personal_indicators": self._count_patterns(
                    content, self.patterns["personal_content"]
                ),
                "generated_indicators": self._count_patterns(
                    content, self.patterns["generated_content"]
                ),
                "documentation_indicators": self._count_patterns(
                    content, self.patterns["documentation"]
                ),
                "template_indicators": self._count_patterns(
                    content, self.patterns["templates"]
                ),
                "duplicate_indicators": self._count_patterns(
                    content, self.patterns["duplicate_indicators"]
                ),
                "is_minimal": len(content.strip()) < CONSTANT_1000,
                "is_boilerplate": self._is_boilerplate(content),
                "has_meaningful_content": self._has_meaningful_content(content),
            }

            return file_info

        except Exception as e:
            logger.info(f"❌ Error analyzing {file_path}: {e}")
            return None

    def _extract_title(self, content):
        """Extract title from HTML content."""
        title_match = re.search(
            r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL
        )
        if title_match:
            return title_match.group(1).strip()
        return "No title"

    def _count_patterns(self, content, patterns):
        """Count occurrences of patterns in content."""
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, content, re.IGNORECASE))
        return count

    def _is_boilerplate(self, content):
        """Check if content is boilerplate/template."""
        boilerplate_indicators = [
            r"<!DOCTYPE html>",
            r"<html",
            r"<head>",
            r"<body>",
            r"<title>",
            r"<meta",
            r"<link",
            r"<script",
            r"<style",
        ]

        # Count HTML structure elements
        structure_count = sum(
            len(re.findall(pattern, content, re.IGNORECASE))
            for pattern in boilerplate_indicators
        )

        # If it has HTML structure but little content, it's likely boilerplate
        content_ratio = len(content.strip()) / max(structure_count, 1)
        return content_ratio < 50  # Less than 50 chars per HTML element

    def _has_meaningful_content(self, content):
        """Check if content has meaningful, non-boilerplate text."""
        # Remove HTML tags
        text_content = re.sub(r"<[^>]+>", " ", content)
        # Remove extra whitespace
        text_content = re.sub(r"\s+", " ", text_content).strip()

        # Check for meaningful words (not just HTML structure)
        meaningful_words = re.findall(r"\b[a-zA-Z]{4,}\b", text_content)
        return len(meaningful_words) > 20  # At least 20 meaningful words

    def classify_file(self, file_info):
        """Classify file based on analysis."""
        analysis = file_info["analysis"]

        # Check for duplicates first
        if analysis["duplicate_indicators"] > 0:
            return "duplicates"

        # Check for generated content
        if (
            analysis["generated_indicators"] > 2
            or "documentation_" in file_info["name"].lower()
        ):
            return "generated_content"

        # Check for personal content
        if analysis["personal_indicators"] > 0:
            return "personal_content"

        # Check for documentation
        if analysis["documentation_indicators"] > 1:
            return "documentation"

        # Check for templates
        if analysis["template_indicators"] > 0 or analysis["is_boilerplate"]:
            return "templates"

        # Check if minimal/empty
        if analysis["is_minimal"] or not analysis["has_meaningful_content"]:
            return "removable"

        # If it has meaningful content and no red flags, it's worth keeping
        if analysis["has_meaningful_content"] and analysis["word_count"] > 50:
            return "worth_keeping"

        return "unknown"

    def find_duplicates(self, file_analyses):
        """Find duplicate files based on content hash."""
        hash_groups = defaultdict(list)

        for file_info in file_analyses:
            if file_info and file_info.get("content_hash"):
                hash_groups[file_info["content_hash"]].append(file_info)

        duplicates = []
        for hash_val, files in hash_groups.items():
            if len(files) > 1:
                # Keep the most recent one, mark others as duplicates
                files.sort(key=lambda x: x["modified"], reverse=True)
                duplicates.extend(files[1:])  # All but the first (most recent)

        return duplicates

    def generate_removal_plan(self):
        """Generate a plan for what can be safely removed."""
        logger.info("🔍 ANALYZING HTML CONTENT WITH FLUID AWARENESS")
        logger.info("=" * 80)
        logger.info("Determining what's worth keeping vs removable")
        print()

        # Find all HTML files
        html_files = []
        for file_path in self.html_path.rglob("*.html"):
            try:
                depth = len(file_path.relative_to(self.html_path).parts)
                if depth <= self.max_depth:
                    html_files.append(file_path)
            except ValueError:
                continue

        logger.info(f"📊 Found {len(html_files)} HTML files to analyze")

        # Analyze each file
        file_analyses = []
        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                logger.info(f"   Analyzing {i}/{len(html_files)} files...")

            analysis = self.analyze_html_content(file_path)
            if analysis:
                file_analyses.append(analysis)

        logger.info(f"✅ Analysis complete: {len(file_analyses)} files analyzed")

        # Find duplicates
        logger.info("\n🔍 Finding duplicates...")
        duplicates = self.find_duplicates(file_analyses)
        logger.info(f"   Found {len(duplicates)} duplicate files")

        # Classify each file
        logger.info("\n🧠 Classifying files with fluid awareness...")
        for file_info in file_analyses:
            classification = self.classify_file(file_info)
            file_info["classification"] = classification
            self.analysis_results[classification].append(file_info)

        # Generate summary
        self._generate_summary()

        # Create detailed reports
        self._create_detailed_reports()

        return self.analysis_results

    def _generate_summary(self):
        """Generate analysis summary."""
        logger.info(f"\n📊 ANALYSIS SUMMARY")
        logger.info("=" * 50)

        total_files = sum(len(files) for files in self.analysis_results.values())

        for category, files in self.analysis_results.items():
            if files:
                logger.info(f"{category.replace('_', ' ').title()}: {len(files)} files")

                # Show some examples
                if len(files) <= 5:
                    for file_info in files[:3]:
                        logger.info(f"   • {file_info['name']}")
                else:
                    for file_info in files[:3]:
                        logger.info(f"   • {file_info['name']}")
                    logger.info(f"   ... and {len(files) - 3} more")
                print()

        # Calculate space savings
        removable_files = (
            self.analysis_results["removable"]
            + self.analysis_results["duplicates"]
            + self.analysis_results["generated_content"]
            + self.analysis_results["templates"]
        )

        total_removable_size = sum(f["size"] for f in removable_files)
        total_size = sum(
            f["size"]
            for f in [f for files in self.analysis_results.values() for f in files]
        )

        logger.info(f"💾 SPACE ANALYSIS")
        logger.info(f"   Total files: {total_files}")
        logger.info(f"   Removable files: {len(removable_files)}")
        logger.info(
            f"   Space that can be freed: {total_removable_size / (CONSTANT_1024*CONSTANT_1024):.1f} MB"
        )
        logger.info(
            f"   Percentage removable: {(len(removable_files)/total_files)*CONSTANT_100:.1f}%"
        )

    def _create_detailed_reports(self):
        """Create detailed CSV reports."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create comprehensive report
        csv_file = fstr(Path.home()) + "/Documents/python/html_analysis_{timestamp}.csv"
        logger.info(f"\n📊 Creating detailed analysis report: {csv_file}")

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "classification",
                "file_name",
                "file_path",
                "file_size",
                "depth_level",
                "title",
                "word_count",
                "has_scripts",
                "has_styles",
                "has_forms",
                "personal_indicators",
                "generated_indicators",
                "documentation_indicators",
                "template_indicators",
                "duplicate_indicators",
                "is_minimal",
                "is_boilerplate",
                "has_meaningful_content",
                "modified_date",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for category, files in self.analysis_results.items():
                for file_info in files:
                    row = {
                        "classification": category,
                        "file_name": file_info["name"],
                        "file_path": file_info["path"],
                        "file_size": file_info["size"],
                        "depth_level": file_info["depth"],
                        "title": file_info["analysis"]["title"],
                        "word_count": file_info["analysis"]["word_count"],
                        "has_scripts": file_info["analysis"]["has_scripts"],
                        "has_styles": file_info["analysis"]["has_styles"],
                        "has_forms": file_info["analysis"]["has_forms"],
                        "personal_indicators": file_info["analysis"][
                            "personal_indicators"
                        ],
                        "generated_indicators": file_info["analysis"][
                            "generated_indicators"
                        ],
                        "documentation_indicators": file_info["analysis"][
                            "documentation_indicators"
                        ],
                        "template_indicators": file_info["analysis"][
                            "template_indicators"
                        ],
                        "duplicate_indicators": file_info["analysis"][
                            "duplicate_indicators"
                        ],
                        "is_minimal": file_info["analysis"]["is_minimal"],
                        "is_boilerplate": file_info["analysis"]["is_boilerplate"],
                        "has_meaningful_content": file_info["analysis"][
                            "has_meaningful_content"
                        ],
                        "modified_date": datetime.fromtimestamp(
                            file_info["modified"]
                        ).isoformat(),
                    }
                    writer.writerow(row)

        logger.info(
            f"   ✅ Detailed report created with {sum(len(files) for files in self.analysis_results.values())} files"
        )

        # Create removal recommendations
        self._create_removal_recommendations(timestamp)

    def _create_removal_recommendations(self, timestamp):
        """Create specific removal recommendations."""
        rec_file = fstr(Path.home()) + "/Documents/python/html_removal_recommendations_{timestamp}.md"
        logger.info(f"📋 Creating removal recommendations: {rec_file}")

        with open(rec_file, "w") as f:
            f.write("# HTML Content Removal Recommendations\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Safe to remove
            f.write("## 🗑️ SAFE TO REMOVE\n\n")
            removable_categories = [
                "removable",
                "duplicates",
                "generated_content",
                "templates",
            ]

            for category in removable_categories:
                files = self.analysis_results[category]
                if files:
                    f.write(
                        f"### {category.replace('_', ' ').title()} ({len(files)} files)\n\n"
                    )
                    for file_info in files[:10]:  # Show first 10
                        f.write(
                            f"- `{file_info['name']}` ({file_info['size']} bytes)\n"
                        )
                    if len(files) > 10:
                        f.write(f"- ... and {len(files) - 10} more files\n")
                    f.write(Path("\n"))

            # Worth keeping
            f.write("## ✅ WORTH KEEPING\n\n")
            keep_categories = ["worth_keeping", "personal_content", "documentation"]

            for category in keep_categories:
                files = self.analysis_results[category]
                if files:
                    f.write(
                        f"### {category.replace('_', ' ').title()} ({len(files)} files)\n\n"
                    )
                    for file_info in files[:10]:  # Show first 10
                        f.write(
                            f"- `{file_info['name']}` ({file_info['size']} bytes)\n"
                        )
                    if len(files) > 10:
                        f.write(f"- ... and {len(files) - 10} more files\n")
                    f.write(Path("\n"))

            # Summary
            total_files = sum(len(files) for files in self.analysis_results.values())
            removable_files = sum(
                len(self.analysis_results[cat]) for cat in removable_categories
            )
            keep_files = sum(len(self.analysis_results[cat]) for cat in keep_categories)

            f.write("## 📊 SUMMARY\n\n")
            f.write(f"- **Total files analyzed**: {total_files}\n")
            f.write(f"- **Safe to remove**: {removable_files} files\n")
            f.write(f"- **Worth keeping**: {keep_files} files\n")
            f.write(
                f"- **Removal percentage**: {(removable_files/total_files)*CONSTANT_100:.1f}%\n\n"
            )

            f.write("## 🚀 NEXT STEPS\n\n")
            f.write("1. Review the detailed CSV report for specific file analysis\n")
            f.write("2. Manually verify a few files from each category\n")
            f.write("3. Create a backup before removing files\n")
            f.write("4. Use the removal script to safely delete recommended files\n")

        logger.info(f"   ✅ Removal recommendations created")


def main():
    """Main execution function."""
    analyzer = HTMLContentAnalyzer()
    results = analyzer.generate_removal_plan()

    logger.info(f"\n🎯 ANALYSIS COMPLETE!")
    logger.info(
        f"Use the generated reports to make informed decisions about what to keep vs remove."
    )


if __name__ == "__main__":
    main()
