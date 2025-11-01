"""
Excel Intelligent Organizer

This module provides functionality for excel intelligent organizer.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Intelligent Excel File Organizer
Advanced content-awareness system for organizing Excel files based on semantic analysis
"""

import os
import shutil
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import re


class ExcelIntelligentOrganizer:
    """Intelligent organizer for Excel files using advanced content analysis"""

    def __init__(self, source_dir: str, target_base: str = None):
        """__init__ function."""

        self.source_dir = Path(source_dir)
        self.target_base = (
            Path(target_base)
            if target_base
            else self.source_dir.parent / "organized_excel"
        )
        self.analysis_data = {}
        self.organization_plan = {}

        # Create target directory structure
        self._create_directory_structure()

    def _create_directory_structure(self):
        """Create organized directory structure"""
        directories = [
            "data/trivia",
            "data/entertainment",
            "data/educational",
            "data/templates",
            "data/analysis",
            "data/backups",
            "data/duplicates",
            "reports",
            "logs",
        ]

        for directory in directories:
            (self.target_base / directory).mkdir(parents=True, exist_ok=True)

    def analyze_excel_files(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of Excel files"""
        logger.info("🔍 Analyzing Excel files with advanced content-awareness...")

        excel_files = list(self.source_dir.glob("*.xlsx")) + list(
            self.source_dir.glob("*.xls")
        )

        analysis_results = {
            "total_files": len(excel_files),
            "files_analyzed": 0,
            "categories": {},
            "duplicates": [],
            "recommendations": [],
            "file_details": {},
        }

        for file_path in excel_files:
            logger.info(f"📊 Analyzing: {file_path.name}")

            try:
                # Read Excel file
                df = pd.read_excel(file_path)

                # Basic analysis
                file_info = {
                    "filepath": str(file_path),
                    "filename": file_path.name,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "file_size": file_path.stat().st_size,
                    "last_modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                    "content_analysis": self._analyze_content(df, file_path.name),
                    "category": self._categorize_file(df, file_path.name),
                    "quality_score": self._calculate_quality_score(df),
                    "duplicate_candidates": [],
                }

                # Check for duplicates
                duplicate_info = self._check_duplicates(
                    file_path, analysis_results["file_details"]
                )
                if duplicate_info:
                    file_info["duplicate_candidates"] = duplicate_info
                    analysis_results["duplicates"].append(
                        {"file": file_path.name, "duplicates": duplicate_info}
                    )

                # Categorize file
                category = file_info["category"]
                if category not in analysis_results["categories"]:
                    analysis_results["categories"][category] = []
                analysis_results["categories"][category].append(file_path.name)

                analysis_results["file_details"][file_path.name] = file_info
                analysis_results["files_analyzed"] += 1

            except Exception as e:
                logger.info(f"❌ Error analyzing {file_path.name}: {str(e)}")
                analysis_results["file_details"][file_path.name] = {
                    "filepath": str(file_path),
                    "filename": file_path.name,
                    "error": str(e),
                    "category": "error",
                    "quality_score": 0,
                }

        self.analysis_data = analysis_results
        return analysis_results

    def _analyze_content(self, df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Analyze content of Excel file"""
        analysis = {
            "data_types": {},
            "null_percentage": 0,
            "unique_values": {},
            "patterns": [],
            "content_summary": "",
        }

        # Analyze data types
        for col in df.columns:
            analysis["data_types"][col] = str(df[col].dtype)
            analysis["unique_values"][col] = df[col].nunique()

        # Calculate null percentage
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        analysis["null_percentage"] = (
            (null_cells / total_cells) * CONSTANT_100 if total_cells > 0 else 0
        )

        # Detect patterns
        patterns = []

        # Check for common patterns
        if any("trivia" in col.lower() for col in df.columns):
            patterns.append("trivia")
        if any("question" in col.lower() for col in df.columns):
            patterns.append("questions")
        if any("answer" in col.lower() for col in df.columns):
            patterns.append("answers")
        if any("score" in col.lower() for col in df.columns):
            patterns.append("scoring")
        if any("category" in col.lower() for col in df.columns):
            patterns.append("categorized")
        if any("date" in col.lower() for col in df.columns):
            patterns.append("temporal")
        if any("name" in col.lower() for col in df.columns):
            patterns.append("named_entities")

        # Check filename patterns
        filename_lower = filename.lower()
        if "trivia" in filename_lower:
            patterns.append("trivia_content")
        if "horror" in filename_lower:
            patterns.append("horror_theme")
        if "avatar" in filename_lower:
            patterns.append("avatar_content")
        if "discography" in filename_lower:
            patterns.append("music_content")
        if "flashcard" in filename_lower:
            patterns.append("educational")
        if "layout" in filename_lower:
            patterns.append("template")
        if "example" in filename_lower:
            patterns.append("template")

        analysis["patterns"] = patterns

        # Generate content summary
        if patterns:
            analysis["content_summary"] = (
                f"Content appears to be {', '.join(patterns[:3])}"
            )
        else:
            analysis["content_summary"] = "General data content"

        return analysis

    def _categorize_file(self, df: pd.DataFrame, filename: str) -> str:
        """Categorize file based on content and filename"""
        filename_lower = filename.lower()

        # Trivia and quiz content
        if any(
            keyword in filename_lower
            for keyword in ["trivia", "quiz", "question", "answer"]
        ):
            return "trivia"

        # Educational content
        if any(
            keyword in filename_lower
            for keyword in ["flashcard", "learn", "study", "education"]
        ):
            return "educational"

        # Entertainment content
        if any(
            keyword in filename_lower
            for keyword in ["horror", "movie", "film", "entertainment"]
        ):
            return "entertainment"

        # Music content
        if any(
            keyword in filename_lower
            for keyword in ["discography", "music", "song", "album"]
        ):
            return "music"

        # Avatar/character content
        if any(
            keyword in filename_lower for keyword in ["avatar", "character", "profile"]
        ):
            return "avatars"

        # Templates and layouts
        if any(
            keyword in filename_lower
            for keyword in ["template", "layout", "example", "format"]
        ):
            return "templates"

        # Analysis and data
        if any(
            keyword in filename_lower
            for keyword in ["analysis", "data", "report", "stats"]
        ):
            return "analysis"

        # Default to general data
        return "general"

    def _calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate quality score for the Excel file"""
        score = 0.0

        # Base score
        score += 0.3

        # Data completeness (lower null percentage = higher score)
        null_percentage = (
            df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        ) * CONSTANT_100
        score += max(0, (CONSTANT_100 - null_percentage) / CONSTANT_100) * 0.3

        # Data diversity (more unique values = higher score)
        avg_uniqueness = df.nunique().mean() / len(df)
        score += min(avg_uniqueness, 1.0) * 0.2

        # Structure (more columns = higher score, up to a point)
        column_score = min(len(df.columns) / 10, 1.0)
        score += column_score * 0.2

        return min(score, 1.0)

    def _check_duplicates(self, file_path: Path, existing_files: Dict) -> List[str]:
        """Check for potential duplicate files"""
        duplicates = []
        current_size = file_path.stat().st_size

        for filename, file_info in existing_files.items():
            if "file_size" in file_info and file_info["file_size"] == current_size:
                # Same size, check if names are similar
                if self._names_similar(file_path.name, filename):
                    duplicates.append(filename)

        return duplicates

    def _names_similar(self, name1: str, name2: str) -> bool:
        """Check if two filenames are similar (potential duplicates)"""
        # Remove common variations
        clean1 = re.sub(r"\s*[1-9]\s*$", "", name1.lower())
        clean2 = re.sub(r"\s*[1-9]\s*$", "", name2.lower())

        # Check if one is contained in the other
        return clean1 in clean2 or clean2 in clean1

    def generate_organization_plan(self) -> Dict[str, Any]:
        """Generate intelligent organization plan"""
        logger.info("📋 Generating intelligent organization plan...")

        plan = {
            "total_files": len(self.analysis_data["file_details"]),
            "categories": {},
            "duplicates_to_handle": [],
            "files_to_move": [],
            "recommendations": [],
        }

        # Organize by category
        for filename, file_info in self.analysis_data["file_details"].items():
            if "error" in file_info:
                continue

            category = file_info["category"]
            if category not in plan["categories"]:
                plan["categories"][category] = []

            # Determine target location
            target_location = self._get_target_location(category, file_info)

            plan["categories"][category].append(
                {
                    "filename": filename,
                    "source": file_info["filepath"],
                    "target": target_location,
                    "quality_score": file_info["quality_score"],
                    "duplicates": file_info.get("duplicate_candidates", []),
                }
            )

            plan["files_to_move"].append(
                {
                    "filename": filename,
                    "source": file_info["filepath"],
                    "target": target_location,
                    "category": category,
                }
            )

        # Handle duplicates
        for duplicate_info in self.analysis_data["duplicates"]:
            plan["duplicates_to_handle"].append(duplicate_info)

        # Generate recommendations
        plan["recommendations"] = self._generate_recommendations()

        self.organization_plan = plan
        return plan

    def _get_target_location(self, category: str, file_info: Dict) -> str:
        """Get target location for file based on category and analysis"""
        base_path = self.target_base

        if category == "trivia":
            return str(base_path / "data" / "trivia" / file_info["filename"])
        elif category == "educational":
            return str(base_path / "data" / "educational" / file_info["filename"])
        elif category == "entertainment":
            return str(base_path / "data" / "entertainment" / file_info["filename"])
        elif category == "music":
            return str(base_path / "data" / "entertainment" / file_info["filename"])
        elif category == "avatars":
            return str(base_path / "data" / "entertainment" / file_info["filename"])
        elif category == "templates":
            return str(base_path / "data" / "templates" / file_info["filename"])
        elif category == "analysis":
            return str(base_path / "data" / "analysis" / file_info["filename"])
        else:
            return str(base_path / "data" / "general" / file_info["filename"])

    def _generate_recommendations(self) -> List[str]:
        """Generate intelligent recommendations"""
        recommendations = []

        # Duplicate handling
        if self.analysis_data["duplicates"]:
            recommendations.append(
                f"Found {len(self.analysis_data['duplicates'])} potential duplicate files - consider consolidating"
            )

        # Quality improvements
        low_quality_files = [
            name
            for name, info in self.analysis_data["file_details"].items()
            if "quality_score" in info and info["quality_score"] < 0.5
        ]
        if low_quality_files:
            recommendations.append(
                f"Found {len(low_quality_files)} low-quality files - consider data cleaning"
            )

        # Category distribution
        category_counts = {
            cat: len(files) for cat, files in self.analysis_data["categories"].items()
        }
        if len(category_counts) > 1:
            recommendations.append(
                f"Files are distributed across {len(category_counts)} categories - good organization potential"
            )

        # File naming
        poorly_named = [
            name
            for name in self.analysis_data["file_details"].keys()
            if " " in name
            or not name.replace(".xlsx", "")
            .replace(".xls", "")
            .replace(" ", "")
            .isalnum()
        ]
        if poorly_named:
            recommendations.append(
                f"Consider renaming {len(poorly_named)} files for better organization"
            )

        return recommendations

    def execute_organization(self, dry_run: bool = True) -> Dict[str, Any]:
        """Execute the organization plan"""
        if dry_run:
            logger.info("🔍 DRY RUN - No files will be moved")
        else:
            logger.info("🚀 Executing organization plan...")

        results = {
            "files_moved": 0,
            "files_skipped": 0,
            "errors": [],
            "duplicates_handled": 0,
            "backups_created": 0,
        }

        # Create backups first
        if not dry_run:
            backup_dir = self.target_base / "data" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)

            for file_info in self.organization_plan["files_to_move"]:
                source = Path(file_info["source"])
                backup_path = backup_dir / source.name
                shutil.copy2(source, backup_path)
                results["backups_created"] += 1

        # Move files
        for file_info in self.organization_plan["files_to_move"]:
            try:
                source = Path(file_info["source"])
                target = Path(file_info["target"])

                # Create target directory if it doesn't exist
                target.parent.mkdir(parents=True, exist_ok=True)

                if dry_run:
                    logger.info(f"Would move: {source.name} -> {target}")
                else:
                    shutil.move(str(source), str(target))
                    logger.info(f"✅ Moved: {source.name} -> {target}")

                results["files_moved"] += 1

            except Exception as e:
                error_msg = f"Error moving {file_info['filename']}: {str(e)}"
                results["errors"].append(error_msg)
                logger.info(f"❌ {error_msg}")
                results["files_skipped"] += 1

        # Handle duplicates
        for duplicate_info in self.organization_plan["duplicates_to_handle"]:
            if not dry_run:
                # Move duplicates to duplicates folder
                dup_dir = self.target_base / "data" / "duplicates"
                dup_dir.mkdir(parents=True, exist_ok=True)

                for dup_file in duplicate_info["duplicates"]:
                    source_path = self.source_dir / dup_file
                    if source_path.exists():
                        target_path = dup_dir / dup_file
                        shutil.move(str(source_path), str(target_path))
                        results["duplicates_handled"] += 1

            results["duplicates_handled"] += len(duplicate_info["duplicates"])

        return results

    def generate_report(self) -> str:
        """Generate comprehensive organization report"""
        report_path = (
            self.target_base
            / "reports"
            / f"organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

        with open(report_path, "w") as f:
            f.write("# Excel File Organization Report\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # Summary
            f.write("## Summary\n\n")
            f.write(
                f"- **Total Files Analyzed:** {self.analysis_data['total_files']}\n"
            )
            f.write(
                f"- **Files Successfully Analyzed:** {self.analysis_data['files_analyzed']}\n"
            )
            f.write(
                f"- **Categories Found:** {len(self.analysis_data['categories'])}\n"
            )
            f.write(
                f"- **Potential Duplicates:** {len(self.analysis_data['duplicates'])}\n\n"
            )

            # Categories
            f.write("## File Categories\n\n")
            for category, files in self.analysis_data["categories"].items():
                f.write(f"### {category.title()} ({len(files)} files)\n")
                for file in files:
                    f.write(f"- {file}\n")
                f.write(Path("\n"))

            # Quality Analysis
            f.write("## Quality Analysis\n\n")
            quality_scores = [
                info.get("quality_score", 0)
                for info in self.analysis_data["file_details"].values()
                if "quality_score" in info
            ]
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                f.write(f"- **Average Quality Score:** {avg_quality:.2f}\n")
                f.write(
                    f"- **High Quality Files (>0.7):** {len([s for s in quality_scores if s > 0.7])}\n"
                )
                f.write(
                    f"- **Medium Quality Files (0.4-0.7):** {len([s for s in quality_scores if 0.4 <= s <= 0.7])}\n"
                )
                f.write(
                    f"- **Low Quality Files (<0.4):** {len([s for s in quality_scores if s < 0.4])}\n\n"
                )

            # Duplicates
            if self.analysis_data["duplicates"]:
                f.write("## Duplicate Files\n\n")
                for dup_info in self.analysis_data["duplicates"]:
                    f.write(
                        f"- **{dup_info['file']}** duplicates: {', '.join(dup_info['duplicates'])}\n"
                    )
                f.write(Path("\n"))

            # Recommendations
            f.write("## Recommendations\n\n")
            for i, rec in enumerate(
                self.organization_plan.get("recommendations", []), 1
            ):
                f.write(f"{i}. {rec}\n")
            f.write(Path("\n"))

            # Detailed File Analysis
            f.write("## Detailed File Analysis\n\n")
            for filename, info in self.analysis_data["file_details"].items():
                f.write(f"### {filename}\n")
                f.write(f"- **Category:** {info.get('category', 'unknown')}\n")
                f.write(f"- **Quality Score:** {info.get('quality_score', 0):.2f}\n")
                f.write(f"- **Rows:** {info.get('rows', 'N/A')}\n")
                f.write(f"- **Columns:** {info.get('columns', 'N/A')}\n")
                if "content_analysis" in info:
                    f.write(
                        f"- **Content Summary:** {info['content_analysis'].get('content_summary', 'N/A')}\n"
                    )
                    f.write(
                        f"- **Patterns:** {', '.join(info['content_analysis'].get('patterns', []))}\n"
                    )
                f.write(Path("\n"))

        logger.info(f"📄 Report generated: {report_path}")
        return str(report_path)


def main():
    """Main execution function"""
    logger.info("🚀 Excel Intelligent Organizer")
    logger.info("=" * 50)

    # Initialize organizer
    source_dir = Path(str(Path.home()) + "/Documents/CsV/xlsx")
    organizer = ExcelIntelligentOrganizer(source_dir)

    # Analyze files
    logger.info("Step 1: Analyzing Excel files...")
    analysis = organizer.analyze_excel_files()

    logger.info(f"\n📊 Analysis Complete:")
    logger.info(
        f"   Files analyzed: {analysis['files_analyzed']}/{analysis['total_files']}"
    )
    logger.info(f"   Categories found: {len(analysis['categories'])}")
    logger.info(f"   Potential duplicates: {len(analysis['duplicates'])}")

    # Generate organization plan
    logger.info("\nStep 2: Generating organization plan...")
    plan = organizer.generate_organization_plan()

    logger.info(f"\n📋 Organization Plan:")
    for category, files in plan["categories"].items():
        logger.info(f"   {category}: {len(files)} files")

    # Show recommendations
    logger.info(f"\n💡 Recommendations:")
    for i, rec in enumerate(plan["recommendations"], 1):
        logger.info(f"   {i}. {rec}")

    # Execute organization (dry run first)
    logger.info(f"\nStep 3: Executing organization (dry run)...")
    results = organizer.execute_organization(dry_run=True)

    logger.info(f"\n📈 Dry Run Results:")
    logger.info(f"   Files to move: {results['files_moved']}")
    logger.info(f"   Duplicates to handle: {results['duplicates_handled']}")
    logger.info(f"   Errors: {len(results['errors'])}")

    # Ask for confirmation
    logger.info(fPath("\n") + "=" * 50)
    response = input("Execute organization for real? (y/N): ").strip().lower()

    if response == "y":
        logger.info("\n🚀 Executing organization...")
        results = organizer.execute_organization(dry_run=False)

        logger.info(f"\n✅ Organization Complete:")
        logger.info(f"   Files moved: {results['files_moved']}")
        logger.info(f"   Duplicates handled: {results['duplicates_handled']}")
        logger.info(f"   Backups created: {results['backups_created']}")
        logger.info(f"   Errors: {len(results['errors'])}")

        if results["errors"]:
            logger.info(f"\n❌ Errors encountered:")
            for error in results["errors"]:
                logger.info(f"   - {error}")
    else:
        logger.info("\n⏭️  Organization cancelled.")

    # Generate report
    logger.info(f"\nStep 4: Generating report...")
    report_path = organizer.generate_report()
    logger.info(f"📄 Report saved to: {report_path}")


if __name__ == "__main__":
    main()
