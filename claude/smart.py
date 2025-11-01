"""
Ai Tools Claude Smart 3

This module provides functionality for ai tools claude smart 3.

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
Smart Organization Plan Generator
================================
Creates a comprehensive CSV with organization suggestions including
original locations for easy restoration if needed.
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict


class SmartOrganizationPlanner:
    def __init__(self, csv_file_path):
        """__init__ function."""

        self.csv_file_path = csv_file_path
        self.files_data = []
        self.organization_plan = []

    def load_csv_data(self):
        """Load the CSV data for analysis"""
        logger.info("📊 Loading file data from CSV...")

        with open(self.csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.files_data.append(row)

        logger.info(f"✅ Loaded {len(self.files_data)} files for analysis")

    def analyze_file_for_organization(self, file_info):
        """Analyze a file and determine the best organization strategy"""

        file_name = file_info["file_name"]
        file_extension = file_info["file_extension"]
        current_location = file_info["current_location"]
        file_size_mb = float(file_info["file_size_mb"])
        relative_path = file_info["relative_path"]
        full_path = file_info["full_path"]

        # Determine project context
        project_context = self._identify_project_context(
            file_name, current_location, relative_path
        )

        # Determine content type
        content_type = self._identify_content_type(file_name)

        # Generate organization suggestions
        suggestions = self._generate_organization_suggestions(
            file_name, file_extension, project_context, content_type, file_size_mb
        )

        # Calculate priority
        priority = self._calculate_priority(file_info, project_context, content_type)

        # Generate restore information
        restore_info = self._generate_restore_info(
            full_path, relative_path, current_location
        )

        return {
            "file_name": file_name,
            "file_extension": file_extension,
            "current_location": current_location,
            "relative_path": relative_path,
            "full_path": full_path,
            "file_size_mb": file_size_mb,
            "modified_date": file_info["modified_date"],
            "project_context": project_context,
            "content_type": content_type,
            "priority": priority,
            "suggested_destination": suggestions["destination"],
            "suggested_folder_structure": suggestions["folder_structure"],
            "organization_reason": suggestions["reason"],
            "restore_path": restore_info["restore_path"],
            "restore_instructions": restore_info["instructions"],
            "backup_recommended": file_size_mb > 10,  # Backup files larger than 10MB
            "immediate_action": priority >= 15,  # High priority files
            "estimated_impact": self._calculate_impact(file_size_mb, file_extension),
        }

    def _identify_project_context(self, file_name, current_location, relative_path):
        """Identify the project context of a file"""

        # Check current location patterns
        location_lower = current_location.lower()
        path_lower = relative_path.lower()

        if "as-a-man-thinketh" in path_lower or "as_a_man_thinketh" in path_lower:
            return "as_man_thinketh_project"
        elif "claude" in path_lower or "claude" in location_lower:
            return "claude_projects"
        elif "obsidian" in path_lower or "obsidian" in location_lower:
            return "obsidian_vault"
        elif "notion" in path_lower or "notion" in location_lower:
            return "notion_exports"
        elif "portfolio" in path_lower or "portfolio" in location_lower:
            return "portfolio_work"
        elif "python" in path_lower and "python" not in location_lower:
            return "python_projects"
        elif "docs" in path_lower:
            return "documentation"
        elif "data" in path_lower:
            return "data_analysis"

        # Check file name patterns
        file_lower = file_name.lower()

        if any(word in file_lower for word in ["youtube", "yt", "video", "shorts"]):
            return "youtube_content"
        elif any(
            word in file_lower for word in ["instagram", "tiktok", "social", "media"]
        ):
            return "social_media"
        elif any(
            word in file_lower for word in ["ai", "gpt", "claude", "automation", "bot"]
        ):
            return "ai_content"
        elif any(
            word in file_lower for word in ["html", "css", "js", "web", "website"]
        ):
            return "web_development"
        elif any(
            word in file_lower for word in ["csv", "json", "data", "analysis", "stats"]
        ):
            return "data_analysis"

        return "general_files"

    def _identify_content_type(self, file_name):
        """Identify the content type of a file"""

        file_lower = file_name.lower()

        if any(
            word in file_lower for word in ["template", "example", "sample", "demo"]
        ):
            return "template"
        elif any(word in file_lower for word in ["config", "settings", "setup", "env"]):
            return "configuration"
        elif any(
            word in file_lower for word in ["report", "analysis", "summary", "results"]
        ):
            return "report"
        elif any(word in file_lower for word in ["backup", "copy", "old", "archive"]):
            return "backup"
        elif any(word in file_lower for word in ["export", "download", "extract"]):
            return "export"
        elif any(word in file_lower for word in ["log", "debug", "error", "trace"]):
            return "log"
        elif any(word in file_lower for word in ["test", "spec", "check", "verify"]):
            return "test"

        return "regular_content"

    def _generate_organization_suggestions(
        self, file_name, file_extension, project_context, content_type, file_size_mb
    ):
        """Generate specific organization suggestions for a file"""

        # Base destination by file type
        base_destinations = {
            ".py": "~/Documents/python/",
            ".md": "~/Documents/markD/",
            ".html": "~/Documents/HTML/",
            ".json": "~/Documents/json/",
            ".csv": "~/Documents/CsV/",
            ".txt": "~/Documents/txt/",
            ".zip": "~/Documents/Archives/",
        }

        base_destination = base_destinations.get(file_extension, "~/Documents/Other/")

        # Project-specific folder structures
        project_folders = {
            "as_man_thinketh_project": "As-a-Man-Thinketh/",
            "claude_projects": "Claude-Courses/",
            "obsidian_vault": "Obsidian-Vault/",
            "notion_exports": "Notion-Exports/",
            "portfolio_work": "Portfolio/",
            "youtube_content": "YouTube-Content/",
            "social_media": "Social-Media/",
            "ai_content": "AI-Content/",
            "web_development": "Web-Development/",
            "data_analysis": "Data-Analysis/",
            "documentation": "Documentation/",
        }

        # Content type subfolders
        content_subfolders = {
            "template": "Templates/",
            "configuration": "Config/",
            "report": "Reports/",
            "backup": "Backups/",
            "export": "Exports/",
            "log": "Logs/",
            "test": "Tests/",
        }

        # Build suggested folder structure
        suggested_folder = base_destination.rstrip("/")

        if project_context in project_folders:
            suggested_folder += f"/{project_folders[project_context]}"

        if content_type in content_subfolders:
            suggested_folder += f"/{content_subfolders[content_type]}"

        # Special cases for large files
        if file_size_mb > CONSTANT_100:
            suggested_folder += Path("/Large-Files")
        elif file_size_mb > 10:
            suggested_folder += Path("/Medium-Files")

        # Generate reason
        reasons = []
        if file_size_mb > 50:
            reasons.append(
                f"Large file ({file_size_mb:.1f}MB) - high priority for organization"
            )
        if project_context != "general_files":
            reasons.append(
                f"Project-specific file - belongs in {project_context.replace('_', ' ').title()}"
            )
        if content_type != "regular_content":
            reasons.append(f"Special content type - {content_type}")

        if not reasons:
            reasons.append("Standard file type organization")

        return {
            "destination": suggested_folder,
            "folder_structure": suggested_folder.replace("~/Documents/", ""),
            "reason": " | ".join(reasons),
        }

    def _calculate_priority(self, file_info, project_context, content_type):
        """Calculate organization priority"""
        priority = 0

        file_size_mb = float(file_info["file_size_mb"])

        # Size factor
        if file_size_mb > CONSTANT_100:
            priority += 20
        elif file_size_mb > 50:
            priority += 15
        elif file_size_mb > 10:
            priority += 10
        elif file_size_mb > 1:
            priority += 5

        # Project context factor
        high_priority_contexts = [
            "portfolio_work",
            "claude_projects",
            "as_man_thinketh_project",
        ]
        if project_context in high_priority_contexts:
            priority += 10

        # Content type factor
        high_priority_types = ["configuration", "template", "report"]
        if content_type in high_priority_types:
            priority += 8

        # File extension factor
        if file_info["file_extension"] in [".html", ".py", ".md"]:
            priority += 5

        return priority

    def _generate_restore_info(self, full_path, relative_path, current_location):
        """Generate information needed to restore files"""

        # Create a restore path that preserves the original structure
        restore_path = f"RESTORE_TO: {relative_path}"

        # Generate restore instructions
        instructions = []

        if (
            "python" in current_location.lower()
            and "python" not in relative_path.lower()
        ):
            instructions.append(
                "Originally in Python directory - may be part of a Python project"
            )

        if "portfolio" in current_location.lower():
            instructions.append("Portfolio material - keep with related showcase files")

        if "claude" in current_location.lower():
            instructions.append(
                "Claude course material - belongs with educational content"
            )

        if "notion" in current_location.lower():
            instructions.append(
                "Notion export - may be part of a larger workspace export"
            )

        if not instructions:
            instructions.append(
                "Standard file - can be restored to any appropriate location"
            )

        return {"restore_path": restore_path, "instructions": " | ".join(instructions)}

    def _calculate_impact(self, file_size_mb, file_extension):
        """Calculate the impact of organizing this file"""

        if file_size_mb > CONSTANT_100:
            return "High - Large file, significant space savings"
        elif file_size_mb > 10:
            return "Medium - Moderate file, some space savings"
        elif file_extension in [".py", ".md", ".html"]:
            return "High - Important file type for organization"
        else:
            return "Low - Small file, minimal impact"

    def generate_organization_plan(self):
        """Generate the complete organization plan"""
        logger.info("🎯 Generating smart organization plan...")

        for file_info in self.files_data:
            try:
                plan_entry = self.analyze_file_for_organization(file_info)
                self.organization_plan.append(plan_entry)
            except Exception as e:
                logger.info(
                    f"⚠️  Error processing {file_info.get('file_name', 'unknown')}: {e}"
                )
                continue

        # Sort by priority (highest first)
        self.organization_plan.sort(key=lambda x: x["priority"], reverse=True)

        logger.info(
            f"✅ Generated organization plan for {len(self.organization_plan)} files"
        )

    def save_organization_plan(self):
        """Save the organization plan to CSV"""
        logger.info("💾 Saving organization plan...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = (
            f"/Users/steven/Documents/python/smart_organization_plan_{timestamp}.csv"
        )

        fieldnames = [
            "file_name",
            "file_extension",
            "file_size_mb",
            "modified_date",
            "current_location",
            "relative_path",
            "full_path",
            "project_context",
            "content_type",
            "priority",
            "suggested_destination",
            "suggested_folder_structure",
            "organization_reason",
            "restore_path",
            "restore_instructions",
            "backup_recommended",
            "immediate_action",
            "estimated_impact",
        ]

        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.organization_plan)

        logger.info(f"✅ Organization plan saved to: {csv_filename}")
        return csv_filename

    def generate_summary_report(self):
        """Generate a summary report"""
        logger.info("📊 Generating summary report...")

        # Count by priority
        priority_counts = defaultdict(int)
        size_by_priority = defaultdict(float)

        for entry in self.organization_plan:
            priority_level = (
                "High"
                if entry["priority"] >= 15
                else "Medium" if entry["priority"] >= 10 else "Low"
            )
            priority_counts[priority_level] += 1
            size_by_priority[priority_level] += entry["file_size_mb"]

        # Count by project context
        project_counts = defaultdict(int)
        for entry in self.organization_plan:
            project_counts[entry["project_context"]] += 1

        # Count immediate actions
        immediate_actions = sum(
            1 for entry in self.organization_plan if entry["immediate_action"]
        )
        backup_recommended = sum(
            1 for entry in self.organization_plan if entry["backup_recommended"]
        )

        total_size = sum(entry["file_size_mb"] for entry in self.organization_plan)

        summary = {
            "total_files": len(self.organization_plan),
            "total_size_gb": round(total_size / CONSTANT_1024, 2),
            "immediate_actions": immediate_actions,
            "backup_recommended": backup_recommended,
            "priority_breakdown": dict(priority_counts),
            "size_by_priority": {k: round(v, 2) for k, v in size_by_priority.items()},
            "top_projects": dict(
                sorted(project_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ),
        }

        return summary

    def print_summary(self):
        """Print a summary of the organization plan"""
        summary = self.generate_summary_report()

        logger.info(Path("\n") + "=" * 80)
        logger.info("🎯 SMART ORGANIZATION PLAN SUMMARY")
        logger.info("=" * 80)

        logger.info(f"\n📊 OVERVIEW:")
        logger.info(f"   Total files to organize: {summary['total_files']:,}")
        logger.info(f"   Total size: {summary['total_size_gb']:.2f} GB")
        logger.info(f"   Immediate actions needed: {summary['immediate_actions']:,}")
        logger.info(f"   Files requiring backup: {summary['backup_recommended']:,}")

        logger.info(f"\n🎯 PRIORITY BREAKDOWN:")
        for priority, count in summary["priority_breakdown"].items():
            size = summary["size_by_priority"][priority]
            logger.info(f"   {priority}: {count:,} files ({size:.1f} MB)")

        logger.info(f"\n🏆 TOP PROJECT CATEGORIES:")
        for project, count in list(summary["top_projects"].items())[:5]:
            logger.info(f"   {project.replace('_', ' ').title()}: {count:,} files")

        logger.info(f"\n🚀 TOP 10 FILES FOR IMMEDIATE ACTION:")
        for i, entry in enumerate(self.organization_plan[:10], 1):
            logger.info(
                f"   {i:2d}. {entry['file_name']} ({entry['file_size_mb']:.1f} MB)"
            )
            logger.info(f"       → {entry['suggested_destination']}")
            logger.info(f"       Reason: {entry['organization_reason']}")
            if entry["backup_recommended"]:
                logger.info(f"       ⚠️  BACKUP RECOMMENDED")


def main():
    """Main function"""
    logger.info("🚀 Smart Organization Plan Generator")
    logger.info("=" * 50)

    # Find the most recent CSV file
    csv_files = list(
        Path("/Users/steven/Documents/python").glob("out_of_place_files_report_*.csv")
    )
    if not csv_files:
        logger.info(
            "❌ No CSV file found. Please run the out_of_place_files_analysis.py first."
        )
        return

    latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
    logger.info(f"📁 Using CSV file: {latest_csv}")

    # Initialize planner
    planner = SmartOrganizationPlanner(str(latest_csv))

    # Generate plan
    planner.load_csv_data()
    planner.generate_organization_plan()

    # Save plan
    csv_filename = planner.save_organization_plan()

    # Print summary
    planner.print_summary()

    logger.info(f"\n✅ Smart organization plan complete!")
    logger.info(f"📋 CSV saved to: {csv_filename}")
    logger.info(f"\n💡 Next steps:")
    logger.info(f"   1. Review the CSV file")
    logger.info(f"   2. Start with 'immediate_action' = True files")
    logger.info(f"   3. Use 'restore_path' column to restore if needed")
    logger.info(f"   4. Follow 'suggested_destination' for organization")


if __name__ == "__main__":
    main()
