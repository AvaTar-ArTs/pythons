#!/usr/bin/env python3
"""Adaptive Content-Aware Analyzer
Discovers categories dynamically from actual file content - no predefined categories
"""

import asyncio
import json
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent))
from next_gen_content_analyzer import NextGenContentAnalyzer, AnalysisConfig


class AdaptiveContentAnalyzer:
    """Discovers natural categories from content patterns"""

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path).expanduser()
        self.analyzer = NextGenContentAnalyzer(
            AnalysisConfig(
                enable_ml_analysis=True,
                enable_embeddings=False,
                enable_caching=True,
                max_file_size_mb=100,
            ),
        )
        self.analysis_results = []

    async def analyze_all_files(self, pattern: str = "*.py") -> list:
        """Analyze all files matching pattern"""
        print("🧠 ADAPTIVE CONTENT ANALYSIS")
        print("=" * 70)
        print(f"Analyzing: {self.base_path}")
        print(f"Pattern: {pattern}")
        print()

        # Find files
        files = list(self.base_path.rglob(pattern))
        files = [
            f
            for f in files
            if not any(
                part in f.parts
                for part in ["archive", "__pycache__", ".git", "_trash", ".history"]
            )
        ]

        print(f"Found {len(files)} files")
        print()

        # Analyze in batches
        batch_size = 50
        all_results = []

        for i in range(0, len(files), batch_size):
            batch = files[i : i + batch_size]
            print(
                f"📊 Batch {i // batch_size + 1}/{(len(files) - 1) // batch_size + 1}..."
            )

            try:
                results = await self.analyzer.analyze_batch(batch)
                all_results.extend(results)
            except Exception as e:
                print(f"   ⚠️  Error: {e}")

        self.analysis_results = all_results
        print(f"\n✅ Analyzed {len(all_results)} files\n")
        return all_results

    def extract_action_verbs(self, text: str) -> set[str]:
        """Extract action verbs from text"""
        # Common action verbs in code
        actions = {
            "download",
            "upload",
            "sync",
            "backup",
            "restore",
            "convert",
            "transform",
            "parse",
            "process",
            "analyze",
            "generate",
            "create",
            "build",
            "compile",
            "transcribe",
            "translate",
            "encode",
            "decode",
            "compress",
            "decompress",
            "resize",
            "scale",
            "crop",
            "rotate",
            "optimize",
            "enhance",
            "upscale",
            "scrape",
            "crawl",
            "fetch",
            "extract",
            "merge",
            "split",
            "combine",
            "sort",
            "filter",
            "search",
            "index",
            "classify",
            "categorize",
            "test",
            "validate",
            "verify",
            "check",
            "monitor",
            "track",
            "deploy",
            "publish",
            "release",
            "install",
            "setup",
            "configure",
            "organize",
            "clean",
            "rename",
            "move",
            "copy",
            "delete",
        }

        text_lower = text.lower()
        found = {action for action in actions if action in text_lower}
        return found

    def extract_domain_nouns(self, text: str) -> set[str]:
        """Extract domain-specific nouns"""
        domains = {
            "youtube",
            "video",
            "audio",
            "image",
            "photo",
            "picture",
            "database",
            "api",
            "web",
            "html",
            "css",
            "javascript",
            "pdf",
            "csv",
            "json",
            "xml",
            "markdown",
            "instagram",
            "twitter",
            "facebook",
            "social",
            "gallery",
            "album",
            "playlist",
            "collection",
            "file",
            "directory",
            "folder",
            "document",
            "text",
            "content",
            "data",
            "metadata",
            "model",
            "neural",
            "ai",
            "ml",
            "machine learning",
            "gui",
            "cli",
            "interface",
            "terminal",
            "test",
            "unit test",
            "integration",
            "git",
            "github",
            "repository",
            "commit",
        }

        text_lower = text.lower()
        found = {domain for domain in domains if domain in text_lower}
        return found

    def discover_natural_categories(self) -> dict[str, list]:
        """Discover categories from content patterns"""
        print("🔍 DISCOVERING NATURAL CATEGORIES FROM CONTENT")
        print("=" * 70)
        print()

        # Extract patterns from all files
        file_patterns = []
        for result in self.analysis_results:
            # Combine all text
            text = (
                result.intelligent_description
                + " "
                + " ".join(result.key_phrases)
                + " "
                + result.metadata.file_name
            )

            # Extract patterns
            actions = self.extract_action_verbs(text)
            domains = self.extract_domain_nouns(text)

            file_patterns.append(
                {
                    "result": result,
                    "actions": actions,
                    "domains": domains,
                    "text": text,
                },
            )

        # Discover common patterns
        action_counts = Counter()
        domain_counts = Counter()
        combo_counts = Counter()

        for fp in file_patterns:
            for action in fp["actions"]:
                action_counts[action] += 1
            for domain in fp["domains"]:
                domain_counts[domain] += 1
            # Track action+domain combinations
            for action in fp["actions"]:
                for domain in fp["domains"]:
                    combo_counts[(action, domain)] += 1

        # Generate categories based on patterns
        print("📊 Discovered Patterns:\n")
        print("Top Actions:")
        for action, count in action_counts.most_common(15):
            print(f"  {action:20s} ({count:3d} files)")

        print("\nTop Domains:")
        for domain, count in domain_counts.most_common(15):
            print(f"  {domain:20s} ({count:3d} files)")

        print("\nTop Action+Domain Combinations:")
        for (action, domain), count in combo_counts.most_common(15):
            if count >= 3:  # Only show combos that appear 3+ times
                print(f"  {action}-{domain:25s} ({count:3d} files)")

        print()

        # Create adaptive categories
        categories = defaultdict(list)

        for fp in file_patterns:
            result = fp["result"]
            actions = fp["actions"]
            domains = fp["domains"]

            # Determine best category using intelligent matching
            category = self._determine_adaptive_category(
                actions,
                domains,
                fp["text"],
                result.metadata.file_name,
                combo_counts,
                action_counts,
                domain_counts,
            )

            categories[category].append(result)

        # Sort by size
        sorted_cats = dict(
            sorted(categories.items(), key=lambda x: len(x[1]), reverse=True),
        )

        print("\n📁 DISCOVERED CATEGORIES:\n")
        for category, files in list(sorted_cats.items())[:20]:
            print(f"{category:40s} {len(files):4d} files")

        if len(sorted_cats) > 20:
            print(f"\n... and {len(sorted_cats) - 20} more categories")

        print()
        return sorted_cats

    def _determine_adaptive_category(:
        self,
        actions: set[str],
        domains: set[str],
        text: str,
        filename: str,
        combo_counts: Counter,
        action_counts: Counter,
        domain_counts: Counter,
    ) -> str:
        """Adaptively determine category based on content patterns"""
        # Find best action+domain combo
        best_combo = None
        best_score = 0

        for action in actions:
            for domain in domains:
                score = combo_counts.get((action, domain), 0)
                if score > best_score:
                    best_score = score
                    best_combo = (action, domain)

        # If strong combo exists, use it
        if best_combo and best_score >= 3:
            action, domain = best_combo
            return f"{action}-{domain}"

        # Otherwise use dominant action or domain
        if actions:
            # Get most common action
            best_action = max(actions, key=lambda a: action_counts.get(a, 0))
            if domains:
                best_domain = max(domains, key=lambda d: domain_counts.get(d, 0))
                return f"{best_action}-{best_domain}"
            return best_action

        if domains:
            best_domain = max(domains, key=lambda d: domain_counts.get(d, 0))
            return best_domain

        # Fallback: analyze filename
        filename_lower = filename.lower()

        if "test" in filename_lower:
            return "tests"
        if "config" in filename_lower or "settings" in filename_lower:
            return "configuration"
        if "util" in filename_lower or "helper" in filename_lower:
            return "utilities"
        if "gui" in filename_lower or "ui" in filename_lower:
            return "interface"

        return "general"

    def propose_structure(self, categories: dict[str, list]) -> dict[str, list[str]]:
        """Propose directory structure"""
        print("\n📂 PROPOSED ADAPTIVE STRUCTURE")
        print("=" * 70)

        structure = {}
        for category, files in categories.items():
            structure[category] = [f.metadata.file_path.name for f in files]

        print(f"\n{self.base_path}/")
        for category, files in list(categories.items())[:15]:
            print(f"├── {category:40s} ({len(files):3d} files)")

        if len(categories) > 15:
            print(f"└── ... and {len(categories) - 15} more categories")

        total = sum(len(files) for files in categories.values())
        print(f"\nTotal: {total} files in {len(categories)} adaptive categories")

        return structure

    def save_report(self, categories: dict, structure: dict):
        """Save analysis report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.base_path / f"adaptive_analysis_{timestamp}.json"

        report = {
            "timestamp": timestamp,
            "total_files": len(self.analysis_results),
            "categories_discovered": len(categories),
            "cluster_summary": {name: len(files) for name, files in categories.items()},
            "proposed_structure": structure,
            "statistics": self.analyzer.get_statistics(),
        }

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n📄 Report saved: {report_file.name}\n")
        return report_file

    async def run(self, pattern: str = "*.py"):
        """Run adaptive analysis"""
        print("=" * 70)
        print("🧠 ADAPTIVE CONTENT-AWARE ANALYZER")
        print("Categories discovered from actual content patterns")
        print("=" * 70)
        print()

        # Analyze files
        await self.analyze_all_files(pattern)

        # Discover natural categories
        categories = self.discover_natural_categories()

        # Propose structure
        structure = self.propose_structure(categories)

        # Save report
        report_file = self.save_report(categories, structure)

        print("=" * 70)
        print("✅ ADAPTIVE ANALYSIS COMPLETE")
        print("=" * 70)
        print()
        print("Categories are based on actual content patterns!")
        print(f"Review: cat {report_file.name}")
        print()


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Adaptive content-aware analyzer")
    parser.add_argument(
        "directory",
        nargs="?",
        default="~/Documents/python",
        help="Directory to analyze",
    )
    parser.add_argument(
        "--pattern",
        default="*.py",
        help="File pattern (default: *.py)",
    )

    args = parser.parse_args()

    analyzer = AdaptiveContentAnalyzer(args.directory)
    await analyzer.run(args.pattern)


if __name__ == "__main__":
    asyncio.run(main())
