"""
File Management Organize Save 3

This module provides functionality for file management organize save 3.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
AI Outputs Hub - Smart Auto-Save System
Automatically saves and organizes all AI assistant outputs with hub-based navigation
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import hashlib


class AIOutputsHub:
    def __init__(self, base_dir=Path("/Users/steven/AI_Outputs_Hub")):
        """__init__ function."""

        self.base_dir = Path(base_dir)
        self.setup_directories()
        self.metadata_file = self.base_dir / "hub_metadata.json"
        self.load_metadata()

    def setup_directories(self):
        """Create the hub directory structure"""
        directories = ["Projects", "Categories", "Timeline", "Quick_Access", "Exports", "Backups", "Templates"]

        for directory in directories:
            (self.base_dir / directory).mkdir(exist_ok=True)

        # Create category subdirectories
        categories = [
            "seo_analysis",
            "creative_automation",
            "brand_strategy",
            "technical_docs",
            "content_creation",
            "business_analysis",
            "conversations",
            "templates",
        ]

        for category in categories:
            (self.base_dir / "Categories" / category).mkdir(exist_ok=True)

    def load_metadata(self):
        """Load existing metadata or create new"""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
                # Convert keywords list back to set for operations
                if "keywords" in self.metadata and isinstance(self.metadata["keywords"], list):
                    self.metadata["keywords"] = set(self.metadata["keywords"])
        else:
            self.metadata = {
                "total_outputs": 0,
                "categories": {},
                "projects": {},
                "recent_outputs": [],
                "keywords": set(),
                "last_updated": None,
            }

    def save_metadata(self):
        """Save metadata to file"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        # Convert set to list for JSON serialization
        self.metadata["keywords"] = list(self.metadata["keywords"])

        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def auto_save_output(self, content, title, category="general", project=None, tags=None, content_type="markdown"):
        """Main auto-save function with smart organization"""
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y%m%d")
        time_str = timestamp.strftime("%H%M%S")

        # Generate unique filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).rstrip()
        safe_title = safe_title.replace(" ", "_")[:50]  # Limit length

        filename = f"{date_str}_{time_str}_{safe_title}.{content_type}"

        # Determine save location
        if project:
            save_dir = self.base_dir / "Projects" / project
        else:
            save_dir = self.base_dir / "Categories" / category

        save_dir.mkdir(exist_ok=True)
        filepath = save_dir / filename

        # Save content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        # Create timeline entry
        timeline_entry = {
            "filename": filename,
            "title": title,
            "category": category,
            "project": project,
            "tags": tags or [],
            "timestamp": timestamp.isoformat(),
            "filepath": str(filepath.relative_to(self.base_dir)),
            "size": len(content),
        }

        # Update metadata
        self.metadata["total_outputs"] += 1
        self.metadata["recent_outputs"].insert(0, timeline_entry)

        # Keep only last 50 recent outputs
        if len(self.metadata["recent_outputs"]) > 50:
            self.metadata["recent_outputs"] = self.metadata["recent_outputs"][:50]

        # Update category stats
        if category not in self.metadata["categories"]:
            self.metadata["categories"][category] = 0
        self.metadata["categories"][category] += 1

        # Update project stats
        if project:
            if project not in self.metadata["projects"]:
                self.metadata["projects"][project] = 0
            self.metadata["projects"][project] += 1

        # Add keywords
        if tags:
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(",")]
            self.metadata["keywords"].update(tags)

        # Create quick access copy for important files
        if category in ["seo_analysis", "creative_automation", "brand_strategy"]:
            quick_access_path = self.base_dir / "Quick_Access" / filename
            shutil.copy2(filepath, quick_access_path)

        # Create timeline copy
        timeline_path = self.base_dir / "Timeline" / filename
        shutil.copy2(filepath, timeline_path)

        # Save metadata
        self.save_metadata()

        return {
            "filepath": str(filepath),
            "filename": filename,
            "title": title,
            "category": category,
            "project": project,
            "timestamp": timestamp.isoformat(),
            "size": len(content),
        }

    def search_outputs(self, query, category=None, project=None):
        """Search through all outputs"""
        results = []
        query_lower = query.lower()

        for output in self.metadata["recent_outputs"]:
            if (
                query_lower in output["title"].lower()
                or query_lower in " ".join(output["tags"]).lower()
                or (category and output["category"] == category)
                or (project and output["project"] == project)
            ):
                results.append(output)

        return results

    def get_category_stats(self):
        """Get statistics for each category"""
        return self.metadata["categories"]

    def get_recent_outputs(self, limit=10):
        """Get recent outputs"""
        return self.metadata["recent_outputs"][:limit]

    def export_all(self, format="json"):
        """Export all outputs in specified format"""
        export_dir = self.base_dir / "Exports" / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        export_dir.mkdir(exist_ok=True)

        if format == "json":
            # Export metadata
            with open(export_dir / "metadata.json", "w") as f:
                json.dump(self.metadata, f, indent=2)

            # Export all outputs
            for output in self.metadata["recent_outputs"]:
                source_path = self.base_dir / output["filepath"]
                if source_path.exists():
                    dest_path = export_dir / output["filename"]
                    shutil.copy2(source_path, dest_path)

        return str(export_dir)

    def create_backup(self):
        """Create a backup of the entire hub"""
        backup_dir = self.base_dir / "Backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(self.base_dir, backup_dir, ignore=shutil.ignore_patterns("Backups"))
        return str(backup_dir)


# Usage example and helper functions
def quick_save(content, title, category="general", tags=None):
    """Quick save function for immediate use"""
    hub = AIOutputsHub()
    return hub.auto_save_output(content, title, category, tags=tags)


def save_seo_analysis(content, title, tags=None):
    """Save SEO analysis content"""
    return quick_save(content, title, "seo_analysis", tags)


def save_creative_automation(content, title, tags=None):
    """Save creative automation content"""
    return quick_save(content, title, "creative_automation", tags)


def save_brand_strategy(content, title, tags=None):
    """Save brand strategy content"""
    return quick_save(content, title, "brand_strategy", tags)


# Example usage
if __name__ == "__main__":
    # Test the system
    hub = AIOutputsHub()

    # Save a test output
    test_content = "# Test Output\nThis is a test of the auto-save system."
    result = hub.auto_save_output(
        content=test_content, title="Test Output", category="technical_docs", tags=["test", "automation", "python"]
    )

    logger.info(f"Saved: {result['filename']}")
    logger.info(f"Location: {result['filepath']}")
    logger.info(f"Hub Dashboard: {hub.base_dir}/Dashboard.html")
