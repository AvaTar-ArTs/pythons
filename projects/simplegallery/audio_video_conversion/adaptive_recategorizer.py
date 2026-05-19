#!/usr/bin/env python3
"""Adaptive Re-categorizer - Intelligently improve categorization results

Takes the context-fluid analysis and applies intelligent improvements:
1. Consolidates fragmented categories
2. Fixes malformed category names
3. Groups by actual functional purpose
4. Identifies patterns (tests, utilities, scrapers, etc.)
"""

import json
from pathlib import Path
from collections import defaultdict


class AdaptiveRecategorizer:
    """Intelligently improve categorization results"""

    def __init__(self, analysis_file: Path):
        self.analysis_file = Path(analysis_file)
        with open(self.analysis_file) as f:
            self.analysis = json.load(f)

        self.improved_categories = {}
        self.file_purposes = {}

    def analyze_and_improve(self):
        """Main improvement process"""
        print("🔄 ADAPTIVE RE-CATEGORIZATION")
        print("=" * 70)
        print()

        # Step 1: Identify file purposes from content and names
        print("📊 Step 1: Identifying file purposes...")
        self._identify_file_purposes()
        print(f"   ✅ Identified purposes for {len(self.file_purposes)} files")
        print()

        # Step 2: Group by functional purpose
        print("🎯 Step 2: Grouping by functional purpose...")
        self._group_by_purpose()
        print(f"   ✅ Created {len(self.improved_categories)} functional categories")
        print()

        # Step 3: Show improvements
        print("📈 Step 3: Improvement summary...")
        self._show_improvements()
        print()

        # Step 4: Save improved analysis
        print("💾 Step 4: Saving improved analysis...")
        self._save_improved_analysis()
        print()

        return self.improved_categories

    def _identify_file_purposes(self):
        """Identify what each file actually does"""
        # Functional patterns to identify
        purpose_patterns = {
            # Testing
            "test": ["test_", "_test.py", "unittest", "pytest", "test.py"],
            # Web scraping
            "web-scraping": [
                "scraper",
                "scrape",
                "selenium",
                "beautifulsoup",
                "requests",
            ],
            # Image processing
            "image-processing": [
                "image",
                "img",
                "photo",
                "pillow",
                "opencv",
                "resize",
                "upscale",
            ],
            # Video processing
            "video-processing": ["video", "mp4", "ffmpeg", "moviepy", "transcod"],
            # Audio processing
            "audio-processing": [
                "audio",
                "mp3",
                "wav",
                "sound",
                "whisper",
                "transcrib",
            ],
            # YouTube automation
            "youtube-automation": ["youtube", "yt-dlp", "ytdl", "yt_", "thumbnail"],
            # Instagram/Social media bots
            "social-media-automation": [
                "instagram",
                "instapy",
                "bot",
                "follow",
                "like",
                "comment",
            ],
            # Data analysis
            "data-analysis": [
                "pandas",
                "numpy",
                "analysis",
                "analyze",
                "stats",
                "dataframe",
            ],
            # Machine Learning
            "machine-learning": [
                "model",
                "train",
                "predict",
                "sklearn",
                "tensorflow",
                "keras",
                "ml_",
            ],
            # API clients/servers
            "api-development": [
                "api",
                "endpoint",
                "flask",
                "fastapi",
                "django",
                "router",
            ],
            # File utilities
            "file-utilities": [
                "organize",
                "cleanup",
                "rename",
                "move",
                "file_tool",
                "dedupe",
            ],
            # Configuration
            "configuration": ["config", "settings", "setup.py", "__init__"],
            # Database
            "database": ["database", "db", "sql", "mongo", "postgres", "orm"],
            # Web development
            "web-development": ["html", "css", "gallery", "website", "webpage"],
            # Automation scripts
            "automation": ["automat", "batch", "process_", "runner", "scheduler"],
            # Content generation
            "content-generation": ["generat", "prompt", "gpt", "openai", "llm", "ai_"],
            # Data extraction/ETL
            "data-extraction": ["extract", "parse", "crawler", "fetch", "download"],
            # Utilities/Helpers
            "utilities": ["util", "helper", "tool", "common", "shared"],
        }

        # Analyze each file
        for file_path, file_info in self._get_all_files().items():
            filename = Path(file_path).name.lower()

            # Check against patterns
            matched_purposes = []
            for purpose, patterns in purpose_patterns.items():
                if any(pattern in filename for pattern in patterns):
                    matched_purposes.append(purpose)

            # Check file content (from analysis)
            if file_info.get("content_summary"):
                content = file_info["content_summary"].lower()
                for purpose, patterns in purpose_patterns.items():
                    if any(pattern in content for pattern in patterns):
                        if purpose not in matched_purposes:
                            matched_purposes.append(purpose)

            # Assign primary purpose
            if matched_purposes:
                # Prioritize specific purposes over generic
                priority_order = [
                    "test",
                    "youtube-automation",
                    "social-media-automation",
                    "image-processing",
                    "video-processing",
                    "audio-processing",
                    "web-scraping",
                    "machine-learning",
                    "api-development",
                    "database",
                    "web-development",
                    "content-generation",
                    "data-extraction",
                    "file-utilities",
                    "automation",
                    "data-analysis",
                    "configuration",
                    "utilities",
                ]

                for priority_purpose in priority_order:
                    if priority_purpose in matched_purposes:
                        self.file_purposes[file_path] = priority_purpose
                        break
                else:
                    self.file_purposes[file_path] = matched_purposes[0]
            else:
                # Default to general
                self.file_purposes[file_path] = "general-scripts"

    def _get_all_files(self) -> dict:
        """Get all files from analysis"""
        files = {}
        for category_name, category_info in self.analysis["context_categories"].items():
            for file_path in category_info["files"]:
                files[file_path] = {
                    "original_category": category_name,
                    "content_summary": category_info.get("description", ""),
                }
        return files

    def _group_by_purpose(self):
        """Group files by their identified purpose"""
        purpose_groups = defaultdict(list)

        for file_path, purpose in self.file_purposes.items():
            purpose_groups[purpose].append(file_path)

        # Create improved categories
        for purpose, files in purpose_groups.items():
            # Further split large categories
            if len(files) > 100 and purpose in ["test", "data-analysis", "utilities"]:
                # Split tests by what they test
                if purpose == "test":
                    self._split_tests(files)
                # Split utilities by type
                elif purpose == "utilities":
                    self._split_utilities(files)
                else:
                    self.improved_categories[purpose] = {
                        "files": files,
                        "count": len(files),
                        "description": self._get_purpose_description(purpose),
                    }
            else:
                self.improved_categories[purpose] = {
                    "files": files,
                    "count": len(files),
                    "description": self._get_purpose_description(purpose),
                }

    def _split_tests(self, test_files: list[str]):
        """Split test files into subcategories"""
        test_groups = defaultdict(list)

        for file_path in test_files:
            filename = Path(file_path).name.lower()

            # Identify test type
            if "unit" in filename or "test_unit" in filename:
                test_groups["unit-tests"].append(file_path)
            elif "integration" in filename or "test_integration" in filename:
                test_groups["integration-tests"].append(file_path)
            elif "api" in filename or "test_api" in filename:
                test_groups["api-tests"].append(file_path)
            else:
                # Group by parent directory or module
                parent = Path(file_path).parent.name
                if parent != "python":
                    test_groups[f"{parent}-tests"].append(file_path)
                else:
                    test_groups["general-tests"].append(file_path)

        # Add to improved categories
        for group_name, files in test_groups.items():
            if len(files) >= 3:  # Only create group if 3+ files
                self.improved_categories[group_name] = {
                    "files": files,
                    "count": len(files),
                    "description": f"Test files for {group_name.replace('-tests', '')}",
                }
            else:
                # Merge small groups into general-tests
                if "general-tests" not in self.improved_categories:
                    self.improved_categories["general-tests"] = {
                        "files": [],
                        "count": 0,
                        "description": "General test files",
                    }
                self.improved_categories["general-tests"]["files"].extend(files)
                self.improved_categories["general-tests"]["count"] += len(files)

    def _split_utilities(self, utility_files: list[str]):
        """Split utility files into subcategories"""
        utility_groups = defaultdict(list)

        for file_path in utility_files:
            filename = Path(file_path).name.lower()

            if "file" in filename or "path" in filename:
                utility_groups["file-utilities"].append(file_path)
            elif "string" in filename or "text" in filename:
                utility_groups["text-utilities"].append(file_path)
            elif "date" in filename or "time" in filename:
                utility_groups["datetime-utilities"].append(file_path)
            elif "log" in filename:
                utility_groups["logging-utilities"].append(file_path)
            else:
                utility_groups["general-utilities"].append(file_path)

        # Add to improved categories
        for group_name, files in utility_groups.items():
            self.improved_categories[group_name] = {
                "files": files,
                "count": len(files),
                "description": f"{group_name.replace('-', ' ').title()}",
            }

    def _get_purpose_description(self, purpose: str) -> str:
        """Get human-readable description for purpose"""
        descriptions = {
            "test": "Test files (unit, integration, etc.)",
            "web-scraping": "Web scraping and data extraction scripts",
            "image-processing": "Image manipulation and processing tools",
            "video-processing": "Video editing and conversion scripts",
            "audio-processing": "Audio processing and transcription",
            "youtube-automation": "YouTube download and automation",
            "social-media-automation": "Social media bots and automation",
            "data-analysis": "Data analysis and visualization scripts",
            "machine-learning": "ML models and training scripts",
            "api-development": "API endpoints and web services",
            "file-utilities": "File organization and management tools",
            "configuration": "Configuration and setup files",
            "database": "Database connections and queries",
            "web-development": "Web page generation and galleries",
            "automation": "General automation and batch processing",
            "content-generation": "AI content and prompt generation",
            "data-extraction": "Data extraction and ETL pipelines",
            "utilities": "Helper functions and utilities",
            "general-scripts": "General-purpose Python scripts",
        }
        return descriptions.get(purpose, purpose.replace("-", " ").title())

    def _show_improvements(self):
        """Show before/after comparison"""
        original_cats = len(self.analysis["context_categories"])
        improved_cats = len(self.improved_categories)

        print(f"   Original categories: {original_cats}")
        print(f"   Improved categories: {improved_cats}")
        print(
            f"   Reduction: {original_cats - improved_cats} ({100 * (original_cats - improved_cats) / original_cats:.1f}%)",
        )
        print()

        # Show top categories
        sorted_cats = sorted(
            self.improved_categories.items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        )

        print("   Top 15 improved categories:")
        for i, (name, info) in enumerate(sorted_cats[:15], 1):
            print(f"      {i:2}. {name:30} ({info['count']:4} files)")

    def _save_improved_analysis(self):
        """Save improved analysis to new JSON"""
        improved_analysis = {
            "timestamp": self.analysis["timestamp"],
            "directory": self.analysis["directory"],
            "total_files": self.analysis["total_files"],
            "original_categories": len(self.analysis["context_categories"]),
            "improved_categories": len(self.improved_categories),
            "categories": self.improved_categories,
            "improvement_stats": {
                "category_reduction": len(self.analysis["context_categories"])
                - len(self.improved_categories),
                "single_file_categories_removed": sum(
                    1
                    for c in self.analysis["context_categories"].values()
                    if c["file_count"] == 1
                ),
                "meaningful_groupings_created": len(self.improved_categories),
            },
        }

        output_file = (
            self.analysis_file.parent
            / f"improved_analysis_{self.analysis['timestamp']}.json"
        )
        with open(output_file, "w") as f:
            json.dump(improved_analysis, f, indent=2)

        print(f"   ✅ Saved: {output_file.name}")


def main():
    import sys

    if len(sys.argv) > 1:
        analysis_file = Path(sys.argv[1])
    else:
        # Find most recent analysis
        import glob

        analyses = glob.glob(str(Path.cwd() / "context_fluid_analysis_*.json"))
        if not analyses:
            print("❌ No analysis file found")
            sys.exit(1)
        analysis_file = Path(max(analyses, key=lambda p: Path(p).stat().st_mtime))
        print(f"📄 Using: {analysis_file.name}")
        print()

    recategorizer = AdaptiveRecategorizer(analysis_file)
    recategorizer.analyze_and_improve()

    print("=" * 70)
    print("✅ Adaptive re-categorization complete!")
    print()


if __name__ == "__main__":
    main()
