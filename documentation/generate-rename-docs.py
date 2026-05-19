#!/usr/bin/env python3
"""from datetime import datetime
from pathlib import Path
import csv
import json
Script Rename Documentation Generator
Creates organized documentation of file renames with descriptions
Outputs: Markdown, CSV, and JSON formats
"""


class RenameDocGenerator:
    """Generate rename documentation in multiple formats"""

    def __init__(self):
        self.renames = []
        self.output_dir = Path.home() / "pythons" / "_docs"
        self.output_dir.mkdir(exist_ok=True)

    def add_rename(:
        self,
        current_name: str,
        description: str,
        new_name: str,
        action: str = "RENAME",
        category: str = "",
    ):
        """Add a rename entry"""
        self.renames.append(
            {
                "current_name": current_name,
                "description": description,
                "new_name": new_name,
                "action": action,
                "category": category,
            },
        )

    def generate_markdown(self, output_path: Path = None):
        """Generate Markdown documentation"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"rename_analysis_{timestamp}.md"

        with open(output_path, "w") as f:
            f.write("# 📝 Python Scripts Rename Analysis\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
            )
            f.write("---\n\n")

            # Group by action
            by_action = {}
            for item in self.renames:
                action = item["action"]
                by_action.setdefault(action, []).append(item)

            for action in ["RENAME", "DELETE", "KEEP", "MOVE"]:
                if action not in by_action:
                    continue

                items = by_action[action]

                if action == "RENAME":
                    icon = "🏷️"
                elif action == "DELETE":
                    icon = "🗑️"
                elif action == "KEEP":
                    icon = "✅"
                else:
                    icon = "📦"

                f.write(f"## {icon} {action} ({len(items)} files)\n\n")
                f.write("| Current Name | What It Does | New Name |\n")
                f.write("|--------------|--------------|----------|\n")

                for item in sorted(items, key=lambda x: x["current_name"]):
                    current = item["current_name"]
                    desc = item["description"]
                    new = (
                        item["new_name"]
                        if action == "RENAME"
                        else item.get("reason", "")
                    )
                    f.write(f"| `{current}` | {desc} | `{new}` |\n")

                f.write("\n")

            # Category breakdown if available
            by_category = {}
            for item in self.renames:
                if item.get("category"):
                    by_category.setdefault(item["category"], []).append(item)

            if by_category:
                f.write("---\n\n")
                f.write("## 📂 By Category\n\n")
                for category, items in sorted(by_category.items()):
                    f.write(f"### {category}\n\n")
                    for item in items:
                        f.write(
                            f"- **{item['current_name']}** → `{item['new_name']}`\n",
                        )
                        f.write(f"  - {item['description']}\n")
                    f.write("\n")

        return output_path

    def generate_csv(self, output_path: Path = None):
        """Generate CSV documentation"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"rename_analysis_{timestamp}.csv"

        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "current_name",
                    "description",
                    "new_name",
                    "action",
                    "category",
                ],
            )
            writer.writeheader()
            writer.writerows(self.renames)

        return output_path

    def generate_json(self, output_path: Path = None):
        """Generate JSON documentation"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"rename_analysis_{timestamp}.json"

        data = {
            "generated": datetime.now().isoformat(),
            "total_files": len(self.renames),
            "by_action": {},
            "by_category": {},
            "renames": self.renames,
        }

        # Group by action
        for item in self.renames:
            action = item["action"]
            data["by_action"].setdefault(action, []).append(item)

        # Group by category
        for item in self.renames:
            if item.get("category"):
                category = item["category"]
                data["by_category"].setdefault(category, []).append(item)

        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        return output_path

    def generate_all(self):
        """Generate all formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        md_path = self.generate_markdown()
        csv_path = self.generate_csv()
        json_path = self.generate_json()

        print("✅ Generated documentation:")
        print(f"   📄 Markdown: {md_path}")
        print(f"   📊 CSV:      {csv_path}")
        print(f"   🔧 JSON:     {json_path}")

        return md_path, csv_path, json_path


# Current batch data
def generate_current_batch():
    """Generate docs for current batch"""
    gen = RenameDocGenerator()

    # Batch 5 - Current analysis
    gen.add_rename(
        "analyze-metadata.py",
        "Generates cinematic image prompts FROM timestamped transcripts (text → image prompts)",
        "transcript-to-image-prompts.py",
        "RENAME",
        "Image Generation",
    )

    gen.add_rename(
        "analyze-prompt.py",
        "Enriches existing CSV with GPT Vision analysis (reads CSV, adds AI metadata)",
        "gpt-vision-csv-enricher.py",
        "RENAME",
        "Image Analysis",
    )

    gen.add_rename(
        "analyze-reader.py",
        "Analyzes images with GPT Vision for POD products (generates SEO, tags, product suggestions)",
        "gpt-vision-image-analyzer.py",
        "RENAME",
        "Image Analysis",
    )

    gen.add_rename(
        "alchemy-quiz.py",
        "CSV to audio quiz - Reads quiz CSV file and generates MP3s using OpenAI TTS",
        "csv-to-audio-quiz.py",
        "RENAME",
        "Audio Generation",
    )

    gen.add_rename(
        "ai-stability-code.py",
        "Intelligent code quality analyzer - Security, performance, style analysis with confidence scoring",
        "code-quality-analyzer.py",
        "RENAME",
        "Code Analysis",
    )

    gen.add_rename(
        "ADVANCED_SYSTEMS_CATALOG.py",
        "Project cataloger - Discovers all projects (pythons, workspace, GitHub) with tech stacks",
        "project-catalog-generator.py",
        "RENAME",
        "Documentation",
    )

    gen.add_rename(
        "AI_ORCHESTRATOR_ULTIMATE.py",
        "Multi-LLM orchestrator - Routes tasks to best AI model (12 APIs: GPT, Claude, Grok, Groq, etc.)",
        "multi-llm-orchestrator.py",
        "RENAME",
        "AI Tools",
    )

    gen.add_rename(
        "AI_SETUP_VERIFICATION.py",
        "AI SDK checker - Verifies installation of all AI service SDKs and API keys",
        "check-ai-sdks.py",
        "RENAME",
        "AI Tools",
    )

    gen.add_rename(
        "album-sorting.py",
        "Media album sorter - Sorts mp3/mp4/txt files by album name into organized folders",
        "sort-media-by-album.py",
        "RENAME",
        "Media Organization",
    )

    gen.add_rename(
        "analyze-code-complexity.py",
        "Python complexity analyzer - Uses Radon + Pylint for cyclomatic complexity, maintainability index",
        "python-complexity-analyzer.py",
        "RENAME",
        "Code Analysis",
    )

    gen.add_rename(
        "analyze-file-migration.py",
        "Migration planner - Shows what files will be migrated to which category folders",
        "migration-planner.py",
        "RENAME",
        "File Organization",
    )

    gen.add_rename(
        "analyze-file-versions.py",
        "Version detector - Finds all versioned scripts (script_v1, script_v2, etc.) and suggests which to keep",
        "find-script-versions.py",
        "RENAME",
        "File Organization",
    )

    gen.add_rename(
        "analyze-files-comprehensive.py",
        "Master analyzer - Runs ALL 14 production tools + 8 AI models for complete file analysis",
        "master-file-analyzer.py",
        "RENAME",
        "File Analysis",
    )

    gen.add_rename(
        "analyze-json-writer.py",
        "Image metadata helpers - Shared utilities for GPT-based image metadata enrichment",
        "image-metadata-helpers.py",
        "RENAME",
        "Image Analysis",
    )

    gen.add_rename(
        "_RefreshThread.py",
        "Rich library threading code - Not user code, part of Rich terminal library",
        "",
        "DELETE",
        "Cleanup",
    )

    gen.add_rename(
        "alchemyapi-audio-demo-generator.py",
        "Too project-specific - Creates emotional audio demos for AlchemyAPI project",
        "",
        "DELETE",
        "Cleanup",
    )

    gen.add_rename(
        "ai-deep-analyzer.py",
        "AI code analyzer with AST + semantic analysis - Already has good descriptive name",
        "ai-deep-analyzer.py",
        "KEEP",
        "Code Analysis",
    )

    gen.add_rename(
        "ai-docs-generator.py",
        "AI documentation generator - Uses GPT-4/Claude to analyze and document scripts",
        "ai-docs-generator.py",
        "KEEP",
        "Documentation",
    )

    return gen


if __name__ == "__main__":
    gen = generate_current_batch()
    gen.generate_all()
