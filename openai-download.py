#!/usr/bin/env python3
"""
Python Script Map Generator
Creates a comprehensive map of all Python scripts and their locations
"""

import os
import json
from pathlib import Path
from collections import defaultdict


class ScriptMapper:
    def __init__(self, base_path=Path(str(Path.home()) + "/Documents/python")):
        """__init__ function."""

        self.base_path = Path(base_path)
        self.script_map = {}
        self.category_map = {}
        self.functionality_map = {}

    def generate_complete_map(self):
        """Generate a complete map of all Python scripts."""
        logger.info("🗺️  Generating complete script map...")

        # Map by category
        for category_dir in self.base_path.glob("[0-9]*"):
            if category_dir.is_dir():
                category_name = category_dir.name
                self.category_map[category_name] = {
                    "description": self.get_category_description(category_name),
                    "subcategories": {},
                    "total_scripts": 0,
                }

                # Map subcategories
                for subdir in category_dir.iterdir():
                    if subdir.is_dir():
                        scripts = list(subdir.rglob("*.py"))
                        script_list = []

                        for script in scripts:
                            script_info = {
                                "name": script.name,
                                "path": str(script.relative_to(self.base_path)),
                                "full_path": str(script),
                                "size": script.stat().st_size,
                                "parent": str(
                                    script.parent.relative_to(self.base_path)
                                ),
                            }
                            script_list.append(script_info)
                            self.script_map[script.name] = script_info

                        self.category_map[category_name]["subcategories"][
                            subdir.name
                        ] = {
                            "description": self.get_subcategory_description(
                                subdir.name
                            ),
                            "scripts": script_list,
                            "count": len(script_list),
                        }
                        self.category_map[category_name]["total_scripts"] += len(
                            script_list
                        )

        # Map by functionality
        self.map_by_functionality()

        logger.info(
            f"✅ Mapped {len(self.script_map)} scripts across {len(self.category_map)} categories"
        )

    def get_category_description(self, category):
        """Get description for category."""
        descriptions = {
            "01_core_ai_analysis": "Core AI and analysis tools",
            "02_media_processing": "Media processing and conversion tools",
            "03_automation_platforms": "Platform automation and integration",
            "04_content_creation": "Content creation and generation",
            "05_data_management": "Data collection and management",
            "06_development_tools": "Development and testing utilities",
            "07_experimental": "Experimental and prototype projects",
            "08_archived": "Archived and deprecated projects",
        }
        return descriptions.get(category, "Unknown category")

    def get_subcategory_description(self, subcategory):
        """Get description for subcategory."""
        descriptions = {
            # Core AI Analysis
            "transcription": "Audio/video transcription tools",
            "content_analysis": "Text and content analysis",
            "data_processing": "Data analysis and processing",
            "ai_generation": "AI content generation tools",
            # Media Processing
            "image_tools": "Image processing and manipulation",
            "video_tools": "Video processing and editing",
            "audio_tools": "Audio processing and conversion",
            "format_conversion": "File format conversion",
            # Automation Platforms
            "youtube_automation": "YouTube content automation",
            "social_media_automation": "Social media platform automation",
            "web_automation": "Web scraping and automation",
            "api_integrations": "Third-party API integrations",
            # Content Creation
            "text_generation": "Text and content generation",
            "visual_content": "Visual content creation",
            "multimedia_creation": "Multimedia content creation",
            "creative_tools": "Creative and artistic tools",
            # Data Management
            "data_collection": "Data scraping and collection",
            "file_organization": "File management and organization",
            "database_tools": "Database and storage tools",
            "backup_utilities": "Backup and archival tools",
            # Development Tools
            "testing_framework": "Testing and debugging tools",
            "development_utilities": "Development helper tools",
            "code_analysis": "Code analysis and quality tools",
            "deployment_tools": "Deployment and distribution tools",
        }
        return descriptions.get(subcategory, "Unknown subcategory")

    def map_by_functionality(self):
        """Map scripts by functionality keywords."""
        functionality_keywords = {
            "transcription": ["transcrib", "whisper", "speech", "audio", "voice"],
            "analysis": ["analyz", "process", "extract", "parse", "examine"],
            "conversion": ["convert", "transform", "change", "export", "import"],
            "automation": ["automat", "bot", "schedul", "cron", "task"],
            "generation": ["generat", "creat", "produc", "build", "make"],
            "scraping": ["scrap", "extract", "crawl", "harvest", "collect"],
            "processing": ["process", "handl", "manipulat", "edit", "modify"],
            "organization": ["organiz", "sort", "categoriz", "classify", "arrang"],
            "visualization": ["plot", "chart", "graph", "visualiz", "display"],
            "testing": ["test", "debug", "validat", "check", "verify"],
        }

        for script_name, script_info in self.script_map.items():
            script_lower = script_name.lower()

            for functionality, keywords in functionality_keywords.items():
                if any(keyword in script_lower for keyword in keywords):
                    if functionality not in self.functionality_map:
                        self.functionality_map[functionality] = []
                    self.functionality_map[functionality].append(script_info)

    def save_map(self):
        """Save the complete map to files."""
        # Save complete map
        complete_map = {
            "script_map": self.script_map,
            "category_map": self.category_map,
            "functionality_map": self.functionality_map,
            "total_scripts": len(self.script_map),
            "total_categories": len(self.category_map),
        }

        with open(self.base_path / "complete_script_map.json", "w") as f:
            json.dump(complete_map, f, indent=2)

        # Save human-readable map
        self.save_human_readable_map()

        logger.info("💾 Script map saved to:")
        logger.info("  - complete_script_map.json")
        logger.info("  - script_map_readable.txt")

    def save_human_readable_map(self):
        """Save a human-readable map."""
        with open(self.base_path / "script_map_readable.txt", "w") as f:
            f.write("🐍 PYTHON SCRIPT MAP - COMPLETE DIRECTORY\n")
            f.write("=" * 60 + Path("\n\n"))

            # Overview
            f.write("📊 OVERVIEW:\n")
            f.write(f"Total Scripts: {len(self.script_map)}\n")
            f.write(f"Total Categories: {len(self.category_map)}\n\n")

            # Category breakdown
            f.write("📁 CATEGORY BREAKDOWN:\n")
            f.write("-" * 30 + Path("\n"))
            for category, info in self.category_map.items():
                f.write(f"\n{category}: {info['total_scripts']} scripts\n")
                f.write(f"  Description: {info['description']}\n")

                for subcat, subinfo in info["subcategories"].items():
                    f.write(f"  📂 {subcat}/ ({subinfo['count']} scripts)\n")
                    f.write(f"     Description: {subinfo['description']}\n")

                    # List first 10 scripts in each subcategory
                    for script in subinfo["scripts"][:10]:
                        f.write(f"     📄 {script['name']}\n")

                    if subinfo["count"] > 10:
                        f.write(f"     ... and {subinfo['count'] - 10} more scripts\n")

            # Functionality map
            f.write(f"\n\n🔍 SCRIPTS BY FUNCTIONALITY:\n")
            f.write("-" * 35 + Path("\n"))
            for functionality, scripts in self.functionality_map.items():
                f.write(f"\n{functionality.upper()}: {len(scripts)} scripts\n")
                for script in scripts[:10]:  # Show first 10
                    f.write(f"  📄 {script['name']} - {script['path']}\n")
                if len(scripts) > 10:
                    f.write(f"  ... and {len(scripts) - 10} more\n")

            # Quick reference
            f.write(f"\n\n🚀 QUICK REFERENCE:\n")
            f.write("-" * 20 + Path("\n"))
            f.write("To find a script:\n")
            f.write("1. Use find_script.py for interactive search\n")
            f.write("2. Check the category descriptions above\n")
            f.write("3. Look in the functionality sections\n")
            f.write("4. Use grep to search file contents\n\n")

            f.write("Common locations:\n")
            f.write("- Transcription tools: 01_core_ai_analysis/transcription/\n")
            f.write("- Image processing: 02_media_processing/image_tools/\n")
            f.write("- YouTube tools: 03_automation_platforms/youtube_automation/\n")
            f.write("- Data analysis: 01_core_ai_analysis/data_processing/\n")
            f.write("- File organization: 05_data_management/file_organization/\n")

    def print_quick_reference(self):
        """Print a quick reference guide."""
        logger.info("🚀 QUICK REFERENCE GUIDE")
        logger.info("=" * 40)
        print()

        logger.info("📁 MAIN CATEGORIES:")
        for category, info in self.category_map.items():
            logger.info(
                f"  {category}: {info['total_scripts']} scripts - {info['description']}"
            )

        logger.info(f"\n🔍 COMMON FUNCTIONALITIES:")
        for functionality, scripts in self.functionality_map.items():
            logger.info(f"  {functionality}: {len(scripts)} scripts")

        logger.info(f"\n💡 HOW TO FIND SCRIPTS:")
        logger.info("  1. Run: python find_script.py")
        logger.info("  2. Use: search <script_name>")
        logger.info("  3. Use: func <functionality>")
        logger.info("  4. Check: script_map_readable.txt")
        logger.info("  5. Use: grep -r 'keyword' .")


def main():
    """Main function."""
    mapper = ScriptMapper()
    mapper.generate_complete_map()
    mapper.save_map()
    mapper.print_quick_reference()


if __name__ == "__main__":
    main()
