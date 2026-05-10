import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Rename-Only Analyzer
Focuses ONLY on renaming files to better names
NO deletions - all files stay, just get better names
"""

import csv
from pathlib import Path
from datetime import datetime


class RenameOnlyAnalyzer:
    """Rename files accurately - no deletions"""

    def __init__(self, original_csv):
        self.csv_path = Path(original_csv)
        self.pythons_dir = Path.home() / "pythons"
        self.scripts = []
        self.renames = []

    def load_csv(self):
        """Load original analysis CSV"""
        with open(self.csv_path, "r") as f:
            reader = csv.DictReader(f)
            self.scripts = list(reader)
        print(f"✅ Loaded {len(self.scripts)} scripts")

    def create_rename_mappings(self):
        """Manual mappings for accurate renames"""

        # Based on your handoff doc style - ACCURATE functional names
        mappings = {
            # Already completed
            "catalog-to-csv.py": (
                "etsy-listing-generator.py",
                "Generates Etsy listing metadata from images",
            ),
            # Your approved renames from handoff
            "sufflecsv.py": (
                "shuffle-csv-from-url.py",
                "Downloads CSV from URL and shuffles rows",
            ),
            "categorizer.py": (
                "gpt-script-categorizer.py",
                "Categorizes Python scripts using GPT",
            ),
            "documents.py": (
                "backup-documents-to-csv.py",
                "Backs up ~/documents directory to CSV",
            ),
            "reddit.py": (
                "reddit-to-html-formatter.py",
                "Formats Reddit comments as HTML",
            ),
            "instagram.py": ("instagram-bot-module.py", "Instagram bot utility module"),
            "askredditbot.py": (
                "reddit-auto-poster.py",
                "Automatically posts to r/AskReddit",
            ),
            # Snake_case to kebab-case conversions
            "advanced_script_finder.py": (
                "advanced-script-finder.py",
                "snake_case → kebab-case",
            ),
            "deep_folder_analyzer.py": (
                "deep-folder-analyzer.py",
                "snake_case → kebab-case",
            ),
            "scan_volumes.py": ("scan-volumes.py", "snake_case → kebab-case"),
            "workspace_optimizer.py": (
                "workspace-optimizer.py",
                "snake_case → kebab-case",
            ),
            "project_consolidator.py": (
                "project-consolidator.py",
                "snake_case → kebab-case",
            ),
            "video_compressor.py": ("video-compressor.py", "snake_case → kebab-case"),
            "create_sphinx_docs.py": (
                "create-sphinx-docs.py",
                "snake_case → kebab-case",
            ),
            "ts_python_bridge.py": (
                "typescript-python-bridge.py",
                "snake_case → kebab-case + clarity",
            ),
            # ALL_CAPS to proper-case
            "AI_SETUP_VERIFICATION.py": (
                "check-ai-sdks.py",
                "Checks AI SDK installation",
            ),
            "AI_ORCHESTRATOR_ULTIMATE.py": (
                "multi-llm-orchestrator.py",
                "Orchestrates multiple LLMs",
            ),
            "ADVANCED_SYSTEMS_CATALOG.py": (
                "project-catalog-generator.py",
                "Generates project catalog",
            ),
            "DEEP_CONTENT_ANALYZER_ULTIMATE.py": (
                "deep-content-analyzer.py",
                "Deep content analysis",
            ),
            "COMPLETE_MEDIA_PROMPT_ANALYZER.py": (
                "media-prompt-analyzer.py",
                "Analyzes media prompts",
            ),
            "INTELLIGENT_WORKFLOW_BUILDER.py": (
                "intelligent-workflow-builder.py",
                "Builds intelligent workflows",
            ),
            "PROMPT_HUNTER_ULTIMATE.py": ("prompt-hunter.py", "Hunts for prompts"),
            "PROMPT_CSV_ANALYZER_ULTIMATE.py": (
                "csv-prompt-analyzer.py",
                "Analyzes CSV prompts",
            ),
            "UNIFIED_CONTENT_ORCHESTRATOR.py": (
                "content-orchestrator.py",
                "Orchestrates content creation",
            ),
            "PROCESS_BATCH_RENAMES.py": (
                "batch-rename-executor.py",
                "Executes batch renames",
            ),
            "SMART_AUTOMATION_DISCOVERY.py": (
                "automation-discovery-engine.py",
                "Discovers automation opportunities",
            ),
            # Generic analyze- prefix fixes
            "analyze-file-migration.py": (
                "plan-file-migration.py",
                "Plans file migration strategy",
            ),
            "analyze-file-versions.py": (
                "find-duplicate-versions.py",
                "Finds duplicate script versions",
            ),
            "analyze-files-comprehensive.py": (
                "comprehensive-file-analyzer.py",
                "Comprehensive file analysis",
            ),
            "analyze-code-complexity.py": (
                "python-complexity-analyzer.py",
                "Analyzes Python code complexity",
            ),
            "analyze-metadata.py": (
                "extract-image-metadata.py",
                "Extracts image metadata",
            ),
            "analyze-prompt.py": (
                "transcript-to-prompts.py",
                "Converts transcripts to image prompts",
            ),
            "analyze-reader.py": (
                "gpt-vision-image-analyzer.py",
                "Analyzes images with GPT Vision",
            ),
            "analyze-json-writer.py": (
                "image-metadata-helpers.py",
                "Helper functions for image metadata",
            ),
            "analyze-writer.py": ("code-quality-monitor.py", "Monitors code quality"),
            # Single-word ambiguous names
            "compile.py": (
                "compile-image-catalog.py",
                "Compiles image info to master CSV",
            ),
            "converts.py": (
                "batch-convert-upscale.py",
                "Batch converts and upscales images",
            ),
            "convertupscale.py": (
                "convert-upscale-single.py",
                "Converts and upscales single image",
            ),
            "createimages.py": (
                "dalle-batch-generator.py",
                "Batch generates images with DALL-E",
            ),
            "csvsort.py": (
                "download-images-from-csv.py",
                "Downloads and sorts images from CSV",
            ),
            "denoiser.py": ("ffdnet-denoiser.py", "Denoises images with FFDNet"),
            "lexica.py": (
                "lexica-art-search-downloader.py",
                "Searches and downloads from Lexica.art",
            ),
            "mydesigner.py": ("batch-image-processor.py", "Batch processes images"),
            "nativetypes.py": (
                "jinja2-native-converter.py",
                "Jinja2 native type conversion",
            ),
            "organizer.py": ("sort-images-by-type.py", "Sorts images by format type"),
            "parse.py": ("parse-onedrive-photo-urls.py", "Parses OneDrive photo URLs"),
            "setuptools.py": ("setuptools-bootstrap.py", "Bootstrap for setuptools"),
            "upscalecreateimages.py": (
                "generate-and-upscale-images.py",
                "Generates and upscales images",
            ),
            "cover.py": (
                "generate-typography-covers.py",
                "Generates typography cover images",
            ),
            "vision.py": (
                "gpt-vision-image-describer.py",
                "Describes images with GPT Vision",
            ),
            "textgenerator.py": (
                "openai-text-generator.py",
                "Generates text with OpenAI",
            ),
            "smart.py": (
                "smart-organization-planner.py",
                "Generates organization plans",
            ),
            "sorts.py": (
                "image-sorter-with-exclusions.py",
                "Sorts images with exclusion patterns",
            ),
            "rename.py": ("batch-image-renamer.py", "Batch renames image files"),
            "renamer.py": ("python-script-renamer.py", "Renames Python scripts"),
            "scrape.py": ("reddit-content-scraper.py", "Scrapes Reddit content"),
            "organize.py": ("organize-ai-outputs.py", "Organizes AI output files"),
            "implement.py": (
                "execute-smart-organization.py",
                "Executes smart organization",
            ),
            "pyorganize.py": (
                "extract-python-structure.py",
                "Extracts functions and classes",
            ),
            "pytables.py": ("test-pandas-hdf5.py", "Tests Pandas HDF5 functionality"),
            "translation.py": ("telegram-file-bot.py", "Telegram file downloader bot"),
            "backupcsv.py": ("backup-to-csv.py", "Backs up data to CSV"),
            "brand.py": ("load-brand-json.py", "Loads brand configuration from JSON"),
        }

        return mappings

    def apply_renames(self):
        """Apply rename mappings"""
        mappings = self.create_rename_mappings()

        for script in self.scripts:
            current = script["current_name"]

            if current in mappings:
                new_name, reason = mappings[current]
                action = "RENAME"
            else:
                new_name = current
                action = "KEEP"
                reason = "Name is already clear and descriptive"

            self.renames.append(
                {
                    "action": action,
                    "current_name": current,
                    "suggested_name": new_name,
                    "reason": reason,
                    "category": script.get("category", "Uncategorized"),
                    "description": script.get("description", "")[:150],
                    "apis_used": script.get("apis_used", ""),
                    "lines": script.get("lines", ""),
                    "size_kb": script.get("size_kb", ""),
                }
            )

    def save_clean_csv(self):
        """Save clean rename CSV"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.pythons_dir / f"FINAL_RENAME_PLAN_{timestamp}.csv"

        fieldnames = [
            "action",
            "current_name",
            "suggested_name",
            "reason",
            "category",
            "description",
            "apis_used",
            "lines",
            "size_kb",
        ]

        # Sort: RENAME with actual changes first
        def sort_key(x):
            if x["action"] == "RENAME" and x["current_name"] != x["suggested_name"]:
                return (0, x["category"], x["current_name"])
            else:
                return (1, x["category"], x["current_name"])

        sorted_renames = sorted(self.renames, key=sort_key)

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_renames)

        return output_path

    def print_summary(self):
        """Print summary"""
        actual_renames = [
            r
            for r in self.renames
            if r["action"] == "RENAME" and r["current_name"] != r["suggested_name"]
        ]

        print("\n" + "=" * 80)
        print("📊 FINAL SUMMARY")
        print("=" * 80)

        print("\n✨ Results:")
        print(f"   🏷️ {len(actual_renames)} files will be renamed")
        print(
            f"   ✅ {len(self.renames) - len(actual_renames)} files keep current names"
        )

        print("\n🏷️ Top 30 Renames:")
        for i, item in enumerate(actual_renames[:30], 1):
            print(f"\n{i}. {item['current_name']}")
            print(f"   → {item['suggested_name']}")
            print(f"   Reason: {item['reason']}")


def main():
    original_csv = Path.home() / "pythons" / "_all_scripts_analysis_20251106_132427.csv"

    analyzer = RenameOnlyAnalyzer(original_csv)
    analyzer.load_csv()
    analyzer.apply_renames()

    output_csv = analyzer.save_clean_csv()
    analyzer.print_summary()

    print(f"\n{'=' * 80}")
    print("💾 FINAL RENAME PLAN saved to:")
    print(f"   {output_csv}")
    print("\n🎯 Review the CSV and execute renames!")


try:
        main()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)