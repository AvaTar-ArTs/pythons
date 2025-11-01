"""
Dr Adu Seo Content Organizer

This module provides functionality for dr adu seo content organizer.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_500 = 500

#!/usr/bin/env python3
"""
Deep Read and Organizer for Dr. Adu SEO Project
Searches through chat analysis and markdown reports to find and organize Dr. Adu content
"""

import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path
import markdown
from bs4 import BeautifulSoup


class DrAduDeepReader:
    def __init__(self, source_dir, target_dir):
        """__init__ function."""

        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.found_files = []
        self.dr_adu_content = []
        self.analysis_results = {
            "search_terms": [
                "Dr. Adu",
                "Dr Lawrence Adu",
                "Lawrence Adu",
                "Gainesville Psychiatry",
                "gainesvillepfs.com",
                "Gainesville Psychiatry and Forensic Services",
                "TMS therapy",
                "forensic psychiatry",
                "SEO optimization",
                "psychiatrist Gainesville",
            ],
            "file_types": [".md", ".html", ".txt", ".json"],
            "found_content": [],
            "organized_files": [],
        }

    def search_for_dr_adu_content(self):
        """Search through all files for Dr. Adu related content"""
        logger.info("🔍 Deep searching for Dr. Adu SEO content...")

        if not self.source_dir.exists():
            logger.info(f"❌ Source directory not found: {self.source_dir}")
            return

        # Search through all subdirectories
        for file_path in self.source_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in self.analysis_results["file_types"]:
                logger.info(f"   📄 Scanning: {file_path.relative_to(self.source_dir)}")

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Check if file contains Dr. Adu related content
                    relevance_score = self.calculate_relevance_score(content)

                    if relevance_score > 0:
                        file_info = {
                            "file_path": str(file_path),
                            "relative_path": str(file_path.relative_to(self.source_dir)),
                            "relevance_score": relevance_score,
                            "content_preview": (
                                content[:CONSTANT_500] + "..." if len(content) > CONSTANT_500 else content
                            ),
                            "matched_terms": self.find_matched_terms(content),
                            "file_size": file_path.stat().st_size,
                            "word_count": len(content.split()),
                            "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        }

                        self.found_files.append(file_info)
                        logger.info(f"      ✅ Found relevant content (score: {relevance_score})")

                except Exception as e:
                    logger.info(f"      ❌ Error reading {file_path.name}: {e}")

        # Sort by relevance score
        self.found_files.sort(key=lambda x: x["relevance_score"], reverse=True)
        logger.info(f"\n📊 Found {len(self.found_files)} relevant files")

    def calculate_relevance_score(self, content):
        """Calculate relevance score based on Dr. Adu related terms"""
        score = 0
        content_lower = content.lower()

        # High priority terms
        high_priority = [
            "dr. adu",
            "dr lawrence adu",
            "lawrence adu",
            "gainesville psychiatry and forensic services",
            "gainesvillepfs.com",
        ]

        # Medium priority terms
        medium_priority = [
            "gainesville psychiatry",
            "tms therapy",
            "forensic psychiatry",
            "psychiatrist gainesville",
            "seo optimization",
            "mental health services",
        ]

        # Low priority terms
        low_priority = ["psychiatry", "gainesville", "seo", "optimization", "mental health", "therapy", "psychiatrist"]

        # Calculate scores
        for term in high_priority:
            score += content_lower.count(term.lower()) * 10

        for term in medium_priority:
            score += content_lower.count(term.lower()) * 5

        for term in low_priority:
            score += content_lower.count(term.lower()) * 1

        return score

    def find_matched_terms(self, content):
        """Find which specific terms were matched"""
        matched = []
        content_lower = content.lower()

        for term in self.analysis_results["search_terms"]:
            if term.lower() in content_lower:
                matched.append(term)

        return matched

    def extract_dr_adu_content(self):
        """Extract and organize Dr. Adu specific content"""
        logger.info("\n📝 Extracting Dr. Adu content...")

        for file_info in self.found_files:
            try:
                with open(file_info["file_path"], "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Extract relevant sections
                sections = self.extract_relevant_sections(content)

                if sections:
                    content_info = {
                        "source_file": file_info["relative_path"],
                        "relevance_score": file_info["relevance_score"],
                        "sections": sections,
                        "file_metadata": file_info,
                    }
                    self.dr_adu_content.append(content_info)

            except Exception as e:
                logger.info(f"   ❌ Error extracting from {file_info['file_path']}: {e}")

    def extract_relevant_sections(self, content):
        """Extract sections that contain Dr. Adu related information"""
        sections = []

        # Split content into paragraphs
        paragraphs = content.split("\n\n")

        for i, paragraph in enumerate(paragraphs):
            if self.calculate_relevance_score(paragraph) > 5:  # Threshold for relevance
                sections.append(
                    {
                        "paragraph_number": i,
                        "content": paragraph.strip(),
                        "relevance_score": self.calculate_relevance_score(paragraph),
                        "matched_terms": self.find_matched_terms(paragraph),
                    }
                )

        return sections

    def organize_content(self):
        """Organize the found content into structured files"""
        logger.info("\n📁 Organizing Dr. Adu content...")

        # Create organized directory structure
        organized_dirs = {
            "invoices": self.target_dir / "01_Invoices",
            "technical_reports": self.target_dir / "02_Technical_Reports",
            "client_reports": self.target_dir / "03_Client_Reports",
            "seo_analysis": self.target_dir / "04_SEO_Analysis",
            "content_extracts": self.target_dir / "05_Content_Extracts",
            "visual_comparisons": self.target_dir / "06_Visual_Comparisons",
        }

        for dir_path in organized_dirs.values():
            dir_path.mkdir(exist_ok=True)

        # Organize content by type
        self.organize_by_content_type()

        # Copy relevant files
        self.copy_relevant_files()

        # Create master index
        self.create_master_index()

    def organize_by_content_type(self):
        """Organize content by type and create structured files"""

        # Group content by type
        content_groups = {
            "invoices": [],
            "technical": [],
            "client_facing": [],
            "seo_analysis": [],
            "visual": [],
            "general": [],
        }

        for content_info in self.dr_adu_content:
            source_file = content_info["source_file"].lower()

            if any(term in source_file for term in ["invoice", "pricing", "cost", "value"]):
                content_groups["invoices"].append(content_info)
            elif any(term in source_file for term in ["technical", "implementation", "code", "html"]):
                content_groups["technical"].append(content_info)
            elif any(term in source_file for term in ["client", "non_technical", "business"]):
                content_groups["client_facing"].append(content_info)
            elif any(term in source_file for term in ["seo", "analysis", "audit", "optimization"]):
                content_groups["seo_analysis"].append(content_info)
            elif any(term in source_file for term in ["comparison", "visual", "before_after"]):
                content_groups["visual"].append(content_info)
            else:
                content_groups["general"].append(content_info)

        # Create organized files
        self.create_organized_files(content_groups)

    def create_organized_files(self, content_groups):
        """Create organized files from content groups"""

        for group_name, content_list in content_groups.items():
            if not content_list:
                continue

            # Sort by relevance score
            content_list.sort(key=lambda x: x["relevance_score"], reverse=True)

            # Create comprehensive file for this group
            filename = f"DR_ADU_{group_name.upper()}_COMPREHENSIVE.md"
            file_path = self.target_dir / filename

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Dr. Adu SEO Project - {group_name.title()} Content\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Source Files:** {len(content_list)}\n\n")

                for i, content_info in enumerate(content_list, 1):
                    f.write(f"## Source {i}: {content_info['source_file']}\n")
                    f.write(f"**Relevance Score:** {content_info['relevance_score']}\n")
                    f.write(f"**Matched Terms:** {', '.join(content_info['file_metadata']['matched_terms'])}\n\n")

                    for j, section in enumerate(content_info["sections"], 1):
                        f.write(f"### Section {j} (Score: {section['relevance_score']})\n")
                        f.write(f"**Terms:** {', '.join(section['matched_terms'])}\n\n")
                        f.write(f"{section['content']}\n\n")
                        f.write("---\n\n")

    def copy_relevant_files(self):
        """Copy the most relevant files to the organized directory"""
        logger.info("📋 Copying most relevant files...")

        # Copy top 5 most relevant files
        top_files = self.found_files[:5]

        for i, file_info in enumerate(top_files, 1):
            source_path = Path(file_info["file_path"])
            target_path = self.target_dir / f"ORIGINAL_{i:02d}_{source_path.name}"

            try:
                shutil.copy2(source_path, target_path)
                logger.info(f"   ✅ Copied: {source_path.name}")
            except Exception as e:
                logger.info(f"   ❌ Error copying {source_path.name}: {e}")

    def create_master_index(self):
        """Create a master index of all Dr. Adu content"""
        index_path = self.target_dir / "MASTER_INDEX.md"

        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# Dr. Adu SEO Project - Master Index\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Project Overview\n")
            f.write(f"- **Total Files Found:** {len(self.found_files)}\n")
            f.write(f"- **Content Extracts:** {len(self.dr_adu_content)}\n")
            f.write(f"- **Source Directory:** {self.source_dir}\n")
            f.write(f"- **Target Directory:** {self.target_dir}\n\n")

            f.write("## Most Relevant Files (Top 10)\n")
            for i, file_info in enumerate(self.found_files[:10], 1):
                f.write(f"{i}. **{file_info['relative_path']}** (Score: {file_info['relevance_score']})\n")
                f.write(f"   - Matched Terms: {', '.join(file_info['matched_terms'])}\n")
                f.write(f"   - Size: {file_info['file_size']:,} bytes\n")
                f.write(f"   - Words: {file_info['word_count']:,}\n\n")

            f.write("## Content Categories\n")
            f.write("- **Invoices & Pricing:** DR_ADU_INVOICES_COMPREHENSIVE.md\n")
            f.write("- **Technical Reports:** DR_ADU_TECHNICAL_COMPREHENSIVE.md\n")
            f.write("- **Client Reports:** DR_ADU_CLIENT_FACING_COMPREHENSIVE.md\n")
            f.write("- **SEO Analysis:** DR_ADU_SEO_ANALYSIS_COMPREHENSIVE.md\n")
            f.write("- **Visual Comparisons:** DR_ADU_VISUAL_COMPREHENSIVE.md\n")
            f.write("- **General Content:** DR_ADU_GENERAL_COMPREHENSIVE.md\n\n")

            f.write("## Search Terms Used\n")
            for term in self.analysis_results["search_terms"]:
                f.write(f"- {term}\n")

    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        report_path = self.target_dir / "DEEP_ANALYSIS_REPORT.md"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Dr. Adu SEO Project - Deep Analysis Report\n")
            f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## Search Results Summary\n")
            f.write(f"- **Source Directory:** `{self.source_dir}`\n")
            f.write(f"- **Files Scanned:** {len(self.found_files)}\n")
            f.write(f"- **Relevant Files Found:** {len([f for f in self.found_files if f['relevance_score'] > 0])}\n")
            f.write(f"- **Content Extracts:** {len(self.dr_adu_content)}\n\n")

            f.write("## Top Matched Terms\n")
            all_terms = {}
            for file_info in self.found_files:
                for term in file_info["matched_terms"]:
                    all_terms[term] = all_terms.get(term, 0) + 1

            sorted_terms = sorted(all_terms.items(), key=lambda x: x[1], reverse=True)
            for term, count in sorted_terms[:15]:
                f.write(f"- **{term}:** {count} files\n")

            f.write("\n## File Analysis Details\n")
            for file_info in self.found_files[:20]:  # Top 20 files
                f.write(f"### {file_info['relative_path']}\n")
                f.write(f"- **Relevance Score:** {file_info['relevance_score']}\n")
                f.write(f"- **File Size:** {file_info['file_size']:,} bytes\n")
                f.write(f"- **Word Count:** {file_info['word_count']:,}\n")
                f.write(f"- **Matched Terms:** {', '.join(file_info['matched_terms'])}\n")
                f.write(f"- **Last Modified:** {file_info['last_modified']}\n\n")

    def run_analysis(self):
        """Run the complete analysis"""
        logger.info("🚀 Starting Deep Read and Organization for Dr. Adu SEO Project...")

        # Ensure target directory exists
        self.target_dir.mkdir(parents=True, exist_ok=True)

        # Run analysis steps
        self.search_for_dr_adu_content()
        self.extract_dr_adu_content()
        self.organize_content()
        self.generate_analysis_report()

        logger.info(f"\n✅ Analysis Complete!")
        logger.info(f"📁 Organized content saved to: {self.target_dir}")
        logger.info(f"📋 Check MASTER_INDEX.md for navigation")


def main():
    """Main execution function"""
    source_dir = Path("/Users/steven/Documents/cursor-agent/chat_analysis/markdown_reports")
    target_dir = Path("/Users/steven/Dr_Adu_GainesvillePFS_SEO_Project/ORGANIZED_CONTENT")

    analyzer = DrAduDeepReader(source_dir, target_dir)
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
