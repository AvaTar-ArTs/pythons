#!/usr/bin/env python3
"""
Organize HTML Files Back to Site Folders
Moves HTML files from scattered locations back to their appropriate site directories
"""

import logging
import shutil
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class HTMLOrganizer:
    def __init__(self, documents_dir):
        self.documents_dir = Path(documents_dir)
        self.html_files = []
        self.site_folders = []
        self.moved_files = []
        self.created_dirs = []

    def find_html_files(self):
        """Find all HTML files in Documents directory"""
        logger.info("Finding HTML files...")

        for html_file in self.documents_dir.rglob("*.html"):
            # Skip files in system directories
            if any(
                skip in str(html_file)
                for skip in ["site-packages", ".venv", "__pycache__", ".git"]
            ):
                continue
            self.html_files.append(html_file)

        logger.info(f"Found {len(self.html_files)} HTML files")

    def find_site_folders(self):
        """Find existing site folders and project directories"""
        logger.info("Finding site folders...")

        # Look for common site folder patterns
        site_patterns = [
            "*site*",
            "*web*",
            "*html*",
            "*portfolio*",
            "*project*",
            "*demo*",
            "*showcase*",
        ]

        for pattern in site_patterns:
            for folder in self.documents_dir.rglob(pattern):
                if folder.is_dir() and not any(
                    skip in str(folder)
                    for skip in ["site-packages", ".venv", "__pycache__"]
                ):
                    self.site_folders.append(folder)

        # Also look for directories that already contain index.html
        for folder in self.documents_dir.rglob("*"):
            if folder.is_dir():
                if (folder / "index.html").exists():
                    self.site_folders.append(folder)

        # Remove duplicates
        self.site_folders = list(set(self.site_folders))
        logger.info(f"Found {len(self.site_folders)} potential site folders")

    def analyze_html_content(self, html_file):
        """Analyze HTML file content to determine its purpose"""
        try:
            with open(html_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read().lower()

            # Look for indicators of what type of site this is
            indicators = {
                "portfolio": [
                    "portfolio",
                    "about me",
                    "resume",
                    "cv",
                    "skills",
                    "experience",
                ],
                "gallery": ["gallery", "photos", "images", "album", "slideshow"],
                "blog": ["blog", "post", "article", "news", "journal"],
                "landing": ["landing", "home", "welcome", "hero", "cta"],
                "demo": ["demo", "example", "sample", "test", "preview"],
                "documentation": ["docs", "documentation", "guide", "tutorial", "help"],
                "ecommerce": ["shop", "store", "buy", "cart", "product", "price"],
                "game": ["game", "play", "score", "level", "player"],
                "tool": ["tool", "utility", "calculator", "converter", "generator"],
            }

            scores = {}
            for category, keywords in indicators.items():
                score = sum(1 for keyword in keywords if keyword in content)
                if score > 0:
                    scores[category] = score

            return max(scores.items(), key=lambda x: x[1]) if scores else ("misc", 0)
        except:
            return ("misc", 0)

    def suggest_site_folder(self, html_file):
        """Suggest the best site folder for an HTML file"""
        content_type, score = self.analyze_html_content(html_file)

        # Get the filename without extension
        filename = html_file.stem.lower()

        # Look for exact matches in site folder names
        for site_folder in self.site_folders:
            site_name = site_folder.name.lower()

            # Check for exact name matches
            if filename in site_name or site_name in filename:
                return site_folder

            # Check for content type matches
            if content_type in site_name:
                return site_folder

        # Look for directories that might be related
        for site_folder in self.site_folders:
            site_name = site_folder.name.lower()

            # Check for common patterns
            if any(
                pattern in site_name
                for pattern in ["html", "web", "site", "portfolio", "gallery"]
            ):
                if content_type in ["portfolio", "gallery", "landing"]:
                    return site_folder

        return None

    def create_site_structure(self):
        """Create organized site structure"""
        logger.info("Creating site structure...")

        # Create main site categories
        site_categories = {
            "portfolios": self.documents_dir / "HTML" / "portfolios",
            "galleries": self.documents_dir / "HTML" / "galleries",
            "demos": self.documents_dir / "HTML" / "demos",
            "tools": self.documents_dir / "HTML" / "tools",
            "misc": self.documents_dir / "HTML" / "misc",
        }

        for category, path in site_categories.items():
            path.mkdir(parents=True, exist_ok=True)
            self.created_dirs.append(path)

        return site_categories

    def organize_html_files(self):
        """Organize HTML files into appropriate folders"""
        logger.info("Organizing HTML files...")

        site_categories = self.create_site_structure()

        for html_file in self.html_files:
            try:
                # Skip if already in a good location
                if any(
                    site_folder in html_file.parents
                    for site_folder in self.site_folders
                ):
                    continue

                # Analyze the file
                content_type, score = self.analyze_html_content(html_file)

                # Try to find an existing site folder
                suggested_folder = self.suggest_site_folder(html_file)

                if suggested_folder:
                    # Move to existing site folder
                    dest_path = suggested_folder / html_file.name
                    if not dest_path.exists():
                        shutil.move(str(html_file), str(dest_path))
                        self.moved_files.append((html_file, dest_path))
                        logger.info(
                            f"Moved {html_file.name} to {suggested_folder.name}"
                        )
                else:
                    # Move to appropriate category folder
                    category = (
                        content_type if content_type in site_categories else "misc"
                    )
                    dest_path = site_categories[category] / html_file.name

                    if not dest_path.exists():
                        shutil.move(str(html_file), str(dest_path))
                        self.moved_files.append((html_file, dest_path))
                        logger.info(f"Moved {html_file.name} to {category}")

            except Exception as e:
                logger.error(f"Error moving {html_file}: {e}")

    def create_organization_report(self):
        """Create a report of the organization"""
        report_file = self.documents_dir / "HTML_ORGANIZATION_REPORT.txt"

        with open(report_file, "w") as f:
            f.write("=== HTML FILE ORGANIZATION REPORT ===\n\n")
            f.write(f"Total HTML files processed: {len(self.html_files)}\n")
            f.write(f"Files moved: {len(self.moved_files)}\n")
            f.write(f"Site folders found: {len(self.site_folders)}\n")
            f.write(f"New directories created: {len(self.created_dirs)}\n\n")

            f.write("=== FILES MOVED ===\n")
            for old_path, new_path in self.moved_files:
                f.write(f"{old_path} -> {new_path}\n")

            f.write("\n=== SITE FOLDERS IDENTIFIED ===\n")
            for folder in self.site_folders:
                f.write(f"{folder}\n")

            f.write("\n=== NEW DIRECTORIES CREATED ===\n")
            for dir_path in self.created_dirs:
                f.write(f"{dir_path}\n")

        logger.info(f"Organization report saved to {report_file}")

    def run_organization(self):
        """Run the complete organization process"""
        logger.info("Starting HTML file organization...")

        self.find_html_files()
        self.find_site_folders()
        self.organize_html_files()
        self.create_organization_report()

        logger.info("HTML file organization completed!")


if __name__ == "__main__":
    documents_dir = "/Users/steven/Documents"
    organizer = HTMLOrganizer(documents_dir)
    organizer.run_organization()
