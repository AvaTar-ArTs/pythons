#!/usr/bin/env python3
"""Intelligent File Analysis with Content Awareness
==============================================
Analyzes out-of-place files using content awareness to provide
intelligent descriptions and organization recommendations.
"""

import os
import csv
import json
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict, Counter


class IntelligentFileAnalyzer:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.files_data = []
        self.analysis_results = {
            "project_categories": defaultdict(list),
            "content_patterns": defaultdict(list),
            "file_relationships": defaultdict(list),
            "organization_recommendations": [],
            "priority_files": [],
            "content_insights": {},
        }

    def load_csv_data(self):
        """Load the CSV data for analysis"""
        print("📊 Loading file data from CSV...")

        with open(self.csv_file_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.files_data.append(row)

        print(f"✅ Loaded {len(self.files_data)} files for analysis")

    def analyze_file_names(self):
        """Analyze file names for content patterns and project relationships"""
        print("🔍 Analyzing file names for content patterns...")

        # Common project patterns
        project_patterns = {
            "ai_content": [
                "ai",
                "content",
                "generation",
                "prompt",
                "gpt",
                "claude",
                "anthropic",
            ],
            "youtube": ["youtube", "yt", "video", "shorts", "channel", "upload"],
            "social_media": ["instagram", "tiktok", "twitter", "social", "media"],
            "web_development": ["html", "css", "js", "web", "website", "portfolio"],
            "data_analysis": ["data", "analysis", "csv", "json", "database", "stats"],
            "automation": ["automation", "bot", "script", "auto", "workflow"],
            "documentation": ["readme", "guide", "tutorial", "docs", "manual"],
            "as_man_thinketh": ["thinketh", "man", "think", "book", "audiobook"],
            "claude_projects": ["claude", "course", "tutorial", "prompt"],
            "notion_exports": ["notion", "export", "database", "page"],
            "obsidian": ["obsidian", "vault", "note", "mindmap"],
        }

        # Content type patterns
        content_patterns = {
            "templates": ["template", "example", "sample", "demo"],
            "configurations": ["config", "settings", "setup", "env"],
            "reports": ["report", "analysis", "summary", "results"],
            "backups": ["backup", "copy", "old", "archive"],
            "exports": ["export", "download", "extract"],
            "logs": ["log", "debug", "error", "trace"],
            "tests": ["test", "spec", "check", "verify"],
        }

        for file_info in self.files_data:
            file_name = file_info["file_name"].lower()
            current_location = file_info["current_location"]
            file_extension = file_info["file_extension"]

            # Analyze project context
            project_context = self._identify_project_context(
                file_name, current_location, project_patterns,
            )

            # Analyze content type
            content_type = self._identify_content_type(file_name, content_patterns)

            # Analyze file relationships
            relationships = self._identify_file_relationships(
                file_name, current_location,
            )

            # Enhanced file info
            enhanced_info = {
                **file_info,
                "project_context": project_context,
                "content_type": content_type,
                "relationships": relationships,
                "intelligent_description": self._generate_intelligent_description(
                    file_info, project_context, content_type,
                ),
                "organization_priority": self._calculate_organization_priority(
                    file_info, project_context, content_type,
                ),
            }

            # Categorize for analysis
            self.analysis_results["project_categories"][project_context].append(
                enhanced_info,
            )
            self.analysis_results["content_patterns"][content_type].append(
                enhanced_info,
            )

    def _identify_project_context(self, file_name, current_location, project_patterns):
        """Identify the project context of a file"""
        # Check current location first
        if "as-a-man-thinketh" in current_location.lower():
            return "as_man_thinketh_project"
        if "claude" in current_location.lower():
            return "claude_projects"
        if "obsidian" in current_location.lower():
            return "obsidian_vault"
        if "notion" in current_location.lower():
            return "notion_exports"
        if "portfolio" in current_location.lower():
            return "portfolio_work"
        if "python" in current_location.lower():
            return "python_projects"

        # Check file name patterns
        for project, keywords in project_patterns.items():
            if any(keyword in file_name for keyword in keywords):
                return project

        return "general_files"

    def _identify_content_type(self, file_name, content_patterns):
        """Identify the content type of a file"""
        for content_type, keywords in content_patterns.items():
            if any(keyword in file_name for keyword in keywords):
                return content_type

        return "regular_content"

    def _identify_file_relationships(self, file_name, current_location):
        """Identify relationships between files"""
        relationships = []

        # Check for numbered sequences
        if re.search(r"\(\d+\)", file_name):
            relationships.append("numbered_sequence")

        # Check for version patterns
        if re.search(r"v\d+", file_name) or re.search(r"version", file_name):
            relationships.append("versioned_file")

        # Check for date patterns
        if re.search(r"\d{4}-\d{2}-\d{2}", file_name):
            relationships.append("dated_file")

        # Check for backup patterns
        if any(word in file_name for word in ["backup", "copy", "old", "archive"]):
            relationships.append("backup_file")

        return relationships

    def _generate_intelligent_description(
        self, file_info, project_context, content_type,
    ):
        """Generate an intelligent description of what the file likely contains"""
        file_name = file_info["file_name"]
        file_extension = file_info["file_extension"]
        file_size_mb = float(file_info["file_size_mb"])

        descriptions = []

        # Size-based descriptions
        if file_size_mb > 100:
            descriptions.append(
                "Large file - likely contains substantial data or media",
            )
        elif file_size_mb > 10:
            descriptions.append(
                "Medium-sized file - probably contains structured data or documentation",
            )
        else:
            descriptions.append(
                "Small file - likely configuration, script, or simple data",
            )

        # Extension-based descriptions
        ext_descriptions = {
            ".py": "Python script or module",
            ".md": "Markdown documentation or notes",
            ".html": "Web page or HTML document",
            ".json": "Structured data in JSON format",
            ".csv": "Tabular data in CSV format",
            ".txt": "Plain text document",
            ".zip": "Compressed archive file",
        }

        if file_extension in ext_descriptions:
            descriptions.append(ext_descriptions[file_extension])

        # Project context descriptions
        context_descriptions = {
            "as_man_thinketh_project": "Part of the 'As a Man Thinketh' audiobook project",
            "claude_projects": "Claude AI course or tutorial material",
            "obsidian_vault": "Obsidian note-taking system file",
            "notion_exports": "Exported data from Notion workspace",
            "portfolio_work": "Portfolio or showcase material",
            "python_projects": "Python development project file",
            "ai_content": "AI-related content or automation",
            "youtube": "YouTube content or video-related material",
            "social_media": "Social media content or automation",
            "web_development": "Web development project file",
            "data_analysis": "Data analysis or processing file",
        }

        if project_context in context_descriptions:
            descriptions.append(context_descriptions[project_context])

        # Content type descriptions
        content_descriptions = {
            "templates": "Template or example file",
            "configurations": "Configuration or settings file",
            "reports": "Generated report or analysis",
            "backups": "Backup or archived file",
            "exports": "Exported data or content",
            "logs": "Log or debug information",
            "tests": "Test file or specification",
        }

        if content_type in content_descriptions:
            descriptions.append(content_descriptions[content_type])

        return " | ".join(descriptions)

    def _calculate_organization_priority(
        self, file_info, project_context, content_type,
    ):
        """Calculate the priority for organizing this file"""
        priority = 0

        # Size factor (larger files get higher priority)
        file_size_mb = float(file_info["file_size_mb"])
        if file_size_mb > 100:
            priority += 10
        elif file_size_mb > 10:
            priority += 5
        elif file_size_mb > 1:
            priority += 2

        # Project context factor
        high_priority_contexts = [
            "as_man_thinketh_project",
            "claude_projects",
            "portfolio_work",
        ]
        if project_context in high_priority_contexts:
            priority += 8

        # Content type factor
        high_priority_types = ["configurations", "templates", "reports"]
        if content_type in high_priority_types:
            priority += 5

        # File extension factor
        if file_info["file_extension"] in [".py", ".md", ".html"]:
            priority += 3

        return priority

    def generate_organization_recommendations(self):
        """Generate intelligent organization recommendations"""
        print("🎯 Generating organization recommendations...")

        recommendations = []

        # Analyze each project category
        for project, files in self.analysis_results["project_categories"].items():
            if not files:
                continue

            total_size = sum(float(f["file_size_mb"]) for f in files)
            file_count = len(files)

            recommendation = {
                "project_category": project,
                "file_count": file_count,
                "total_size_mb": round(total_size, 2),
                "priority": (
                    "high" if total_size > 100 or file_count > 100 else "medium"
                ),
                "recommended_actions": [],
                "sample_files": files[:5],  # First 5 files as examples
            }

            # Generate specific recommendations based on project type
            if project == "as_man_thinketh_project":
                recommendation["recommended_actions"] = [
                    "Create dedicated 'As-a-Man-Thinketh' project folder",
                    "Organize by content type: audio, scripts, documentation",
                    "Keep related files together for easy project management",
                ]
            elif project == "claude_projects":
                recommendation["recommended_actions"] = [
                    "Create 'Claude-Courses' folder structure",
                    "Separate course materials from general Claude content",
                    "Organize by course or tutorial topic",
                ]
            elif project == "notion_exports":
                recommendation["recommended_actions"] = [
                    "Create 'Notion-Exports' archive folder",
                    "Organize by export date or workspace",
                    "Consider cleaning up old exports",
                ]
            elif project == "portfolio_work":
                recommendation["recommended_actions"] = [
                    "Create 'Portfolio' folder with subcategories",
                    "Organize by project type or client",
                    "Keep showcase materials separate from work files",
                ]
            else:
                recommendation["recommended_actions"] = [
                    "Move to appropriate type-specific directory",
                    "Consider creating project-specific subfolders",
                    "Review for relevance and cleanup opportunities",
                ]

            recommendations.append(recommendation)

        self.analysis_results["organization_recommendations"] = recommendations

        # Identify priority files for immediate action
        all_files = []
        for files in self.analysis_results["project_categories"].values():
            all_files.extend(files)

        # Sort by organization priority
        priority_files = sorted(
            all_files, key=lambda x: x["organization_priority"], reverse=True,
        )[:20]
        self.analysis_results["priority_files"] = priority_files

    def generate_content_insights(self):
        """Generate insights about content patterns and relationships"""
        print("🧠 Generating content insights...")

        insights = {
            "total_files_analyzed": len(self.files_data),
            "total_size_gb": round(
                sum(float(f["file_size_mb"]) for f in self.files_data) / 1024, 2,
            ),
            "most_common_projects": [],
            "largest_file_categories": [],
            "organization_opportunities": [],
            "content_patterns": {},
        }

        # Most common project categories - use original data since enhanced data might not be available
        project_counts = Counter()
        for files in self.analysis_results["project_categories"].values():
            for f in files:
                if "project_context" in f:
                    project_counts[f["project_context"]] += 1
        insights["most_common_projects"] = project_counts.most_common(10)

        # Largest file categories by total size
        size_by_category = defaultdict(float)
        for f in self.files_data:
            size_by_category[f["file_extension"]] += float(f["file_size_mb"])
        insights["largest_file_categories"] = sorted(
            size_by_category.items(), key=lambda x: x[1], reverse=True,
        )

        # Organization opportunities
        opportunities = []

        # Large files that should be moved
        large_files = [f for f in self.files_data if float(f["file_size_mb"]) > 50]
        if large_files:
            opportunities.append(
                f"Move {len(large_files)} large files (>50MB) to free up space",
            )

        # Project-specific organization
        for project, files in self.analysis_results["project_categories"].items():
            if len(files) > 50:
                opportunities.append(
                    f"Organize {len(files)} files in '{project}' category",
                )

        insights["organization_opportunities"] = opportunities

        self.analysis_results["content_insights"] = insights

    def save_analysis_report(self):
        """Save the analysis report to files"""
        print("💾 Saving analysis report...")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save detailed analysis as JSON
        json_file = (
            f"/Users/steven/Documents/python/intelligent_file_analysis_{timestamp}.json"
        )
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(self.analysis_results, f, indent=2, default=str)

        # Save priority files as CSV
        priority_csv = f"/Users/steven/Documents/python/priority_files_{timestamp}.csv"
        with open(priority_csv, "w", newline="", encoding="utf-8") as csvfile:
            if self.analysis_results["priority_files"]:
                fieldnames = list(self.analysis_results["priority_files"][0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.analysis_results["priority_files"])

        # Save organization recommendations as CSV
        rec_csv = f"/Users/steven/Documents/python/organization_recommendations_{timestamp}.csv"
        with open(rec_csv, "w", newline="", encoding="utf-8") as csvfile:
            if self.analysis_results["organization_recommendations"]:
                fieldnames = [
                    "project_category",
                    "file_count",
                    "total_size_mb",
                    "priority",
                    "recommended_actions",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for rec in self.analysis_results["organization_recommendations"]:
                    writer.writerow(
                        {
                            "project_category": rec["project_category"],
                            "file_count": rec["file_count"],
                            "total_size_mb": rec["total_size_mb"],
                            "priority": rec["priority"],
                            "recommended_actions": "; ".join(
                                rec["recommended_actions"],
                            ),
                        },
                    )

        print("✅ Analysis saved to:")
        print(f"   📊 Detailed analysis: {json_file}")
        print(f"   🎯 Priority files: {priority_csv}")
        print(f"   📋 Recommendations: {rec_csv}")

        return json_file, priority_csv, rec_csv

    def print_summary(self):
        """Print a summary of the analysis"""
        print("\n" + "=" * 80)
        print("🧠 INTELLIGENT FILE ANALYSIS SUMMARY")
        print("=" * 80)

        insights = self.analysis_results["content_insights"]

        print("\n📊 OVERVIEW:")
        print(f"   Total files analyzed: {insights['total_files_analyzed']:,}")
        print(f"   Total size: {insights['total_size_gb']:.2f} GB")

        print("\n🏆 TOP PROJECT CATEGORIES:")
        for project, count in insights["most_common_projects"][:5]:
            print(f"   {project}: {count:,} files")

        print("\n💾 LARGEST FILE CATEGORIES BY SIZE:")
        for ext, size_mb in insights["largest_file_categories"][:5]:
            print(f"   {ext}: {size_mb:.1f} MB")

        print("\n🎯 TOP PRIORITY FILES TO ORGANIZE:")
        for i, file_info in enumerate(self.analysis_results["priority_files"][:5], 1):
            print(f"   {i}. {file_info['file_name']} ({file_info['file_size_mb']} MB)")
            print(f"      {file_info['intelligent_description']}")
            print(f"      Priority: {file_info['organization_priority']}")

        print("\n💡 ORGANIZATION OPPORTUNITIES:")
        for opportunity in insights["organization_opportunities"][:5]:
            print(f"   • {opportunity}")

        print("\n📋 PROJECT-SPECIFIC RECOMMENDATIONS:")
        for rec in self.analysis_results["organization_recommendations"][:5]:
            print(f"\n   🎯 {rec['project_category'].replace('_', ' ').title()}:")
            print(
                f"      Files: {rec['file_count']:,} | Size: {rec['total_size_mb']:.1f} MB | Priority: {rec['priority']}",
            )
            for action in rec["recommended_actions"]:
                print(f"      • {action}")


def main():
    """Main function"""
    print("🚀 Intelligent File Analysis with Content Awareness")
    print("=" * 60)

    # Find the most recent CSV file
    csv_files = list(
        Path("/Users/steven/Documents/python").glob("out_of_place_files_report_*.csv"),
    )
    if not csv_files:
        print(
            "❌ No CSV file found. Please run the out_of_place_files_analysis.py first.",
        )
        return

    latest_csv = max(csv_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 Using CSV file: {latest_csv}")

    # Initialize analyzer
    analyzer = IntelligentFileAnalyzer(str(latest_csv))

    # Run analysis
    analyzer.load_csv_data()
    analyzer.analyze_file_names()
    analyzer.generate_organization_recommendations()
    analyzer.generate_content_insights()

    # Save results
    json_file, priority_csv, rec_csv = analyzer.save_analysis_report()

    # Print summary
    analyzer.print_summary()

    print("\n✅ Analysis complete!")
    print("📊 Check the generated files for detailed insights and recommendations.")


if __name__ == "__main__":
    main()
