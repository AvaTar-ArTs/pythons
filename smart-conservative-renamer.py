import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_33 = 33

#!/usr/bin/env python3
"""
🎯 SMART CONSERVATIVE RENAMER
==============================
Based on your actual preferences - keeps good names, fixes bad ones

Your Rules (learned from examples):
✅ YouTubeBot.py → YouTubeBot.py (keep if already good!)
✅ enhanced_content_analyzer_v2.py → content_analyzer_v2.py (remove redundant words)
✅ comprehensive_chat_organizer.py → chat_organizer.py (simplify)
✅ vidgenUI.py → VidGen.py (clean up, ProperCase)
✅ whisper-combiner_1.py → Whisper_combiner.py (capitalize, clean version)
"""

import ast
import csv
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"
    END = "\033[0m"


class SmartConservativeRenamer:
    """Conservative renamer that respects already-good names - CONTENT & PARENT AWARE"""

    # Words to remove (redundant/verbose)
    REDUNDANT_WORDS = [
        "enhanced_",
        "comprehensive_",
        "advanced_",
        "simple_",
        "basic_",
        "fixed_",
        "new_",
        "updated_",
        "improved_",
        "better_",
        "direct_",
        "quick_",
        "fast_",
        "easy_",
        "_read_",
    ]

    # Patterns that indicate a GOOD name (keep it!)
    GOOD_NAME_PATTERNS = [
        r"^[A-Z][a-zA-Z]+Bot\.py$",  # YouTubeBot, InstagramBot
        r"^[A-Z][a-z]+[A-Z][a-z]+\.py$",  # WhisperTranscriber, VideoGenerator
        r"^\w+_\w+_\w+\.py$",  # openai_file_categorizer (3+ words)
        r"^\w+-\w+-\w+\.py$",  # political-analysist-prompter
        r"^\w+_\w+\.py$",  # deep_organizer (2 words, descriptive)
    ]

    # BAD name patterns (definitely rename)
    BAD_NAME_PATTERNS = [
        r"^[a-z]{1,4}\.py$",  # api.py, gpt.py, leo.py, vid.py
        r".*copy.*\.py$",  # ythumb copy.py
        r"^[a-z]+\d+\.py$",  # yt_6.py, voices_4.py
        r"^[a-z]--\.py$",  # y--.py
        r".*\.\.py$",  # 2..py
        r".*-\.py$",  # quiz-.py
        r"^y-.*\.py$",  # y--.py
    ]

    # Parent folder context (adds context to generic names)
    FOLDER_CONTEXT = {
        "youtube": ["youtube", "yt", "video"],
        "instagram": ["instagram", "insta", "ig"],
        "reddit": ["reddit"],
        "leonardo": ["leonardo", "ai"],
        "dalle": ["dalle", "ai"],
        "whisper": ["whisper", "audio", "transcribe"],
        "quiz": ["quiz", "trivia"],
        "bot": ["bot", "automation"],
    }

    def __init__(self, target_dir: str, dry_run: bool = True, csv_output: Optional[str] = None):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.rename_plan = []
        self.csv_output = Path(csv_output) if csv_output else None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.undo_script = self.target_dir / f"UNDO_RENAMES_{timestamp}.sh"

    def is_good_name(self, filename: str) -> bool:
        """Check if filename is already good"""
        for pattern in self.GOOD_NAME_PATTERNS:
            if re.match(pattern, filename):
                return True

        # Also good if descriptive (15+ chars with underscores)
        if len(filename) >= 15 and "_" in filename:
            # Not a bad pattern
            for bad_pattern in self.BAD_NAME_PATTERNS:
                if re.match(bad_pattern, filename):
                    return False
            return True

        return False

    def is_bad_name(self, filename: str) -> bool:
        """Check if filename is bad and needs renaming"""
        for pattern in self.BAD_NAME_PATTERNS:
            if re.match(pattern, filename):
                return True
        return False

    def simplify_name(self, filename: str) -> str:
        """Simplify by removing redundant words"""
        name = filename

        # Remove redundant prefixes
        for word in self.REDUNDANT_WORDS:
            name = name.replace(word, "")

        # Clean up version numbers: _1.py → _v1.py or just .py
        name = re.sub(r"_1\.py$", ".py", name)  # _1 becomes nothing
        name = re.sub(r"_(\d+)\.py$", r"_v\1.py", name)  # _2+ becomes _v2+

        # Remove "copy" suffix
        name = re.sub(r"\s*copy\s*", "", name)

        # Clean up spaces
        name = name.replace(" ", "_")

        # Handle ProperCase names (YouTubeBot, WhisperTranscriber)
        if any(c.isupper() for c in name):
            # Keep ProperCase, just clean up
            name = re.sub(r"[^\w\-.]", "_", name)
            # vidgenUI → VidGen (capitalize properly)
            if name.endswith("UI.py"):
                base = name[:-5]  # Remove UI.py
                name = base.capitalize() + ".py"
        else:
            # Lowercase names stay lowercase
            name = name.lower()

        # Clean up multiple underscores
        name = re.sub(r"_+", "_", name).strip("_")

        return name

    def get_parent_context(self, filepath: Path) -> List[str]:
        """Extract context from parent folder names"""
        context = []

        # Get all parent directory names
        parents = filepath.parts

        for part in parents:
            part_lower = part.lower()
            for folder_type, keywords in self.FOLDER_CONTEXT.items():
                if any(kw in part_lower for kw in keywords):
                    context.append(folder_type)

        return list(dict.fromkeys(context))  # Unique

    def deep_content_analyze(self, filepath: Path) -> Dict[str, any]:
        """Deep content-aware analysis"""
        analysis = {
            "classes": [],
            "functions": [],
            "imports": [],
            "docstring": None,
            "parent_context": self.get_parent_context(filepath),
            "keywords": [],
        }

        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # AST Analysis
            tree = ast.parse(content)
            analysis["docstring"] = ast.get_docstring(tree)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    analysis["classes"].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("__"):
                        analysis["functions"].append(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis["imports"].append(node.module)

            # Extract keywords from docstring
            if analysis["docstring"]:
                words = re.findall(r"\b[a-z]{5,}\b", analysis["docstring"].lower())
                analysis["keywords"] = [
                    w for w in words if w not in ["python", "script", "function", "class", "import"]
                ][:5]

        except Exception as e:
            analysis["error"] = str(e)

        return analysis

    def analyze_file(self, filepath: Path) -> Optional[str]:
        """Content-aware and parent-folder aware analysis"""
        filename = filepath.name

        # Rule 1: If already good, keep it!
        if self.is_good_name(filename):
            return None  # No change needed

        # Rule 2: If just needs simplification, simplify it
        simplified = self.simplify_name(filename)
        if simplified != filename:
            # Check if simplified version is good enough
            if self.is_good_name(simplified) or (len(simplified) >= 10 and "_" in simplified):
                return simplified

        # Rule 3: Content-aware improvement for bad names
        if self.is_bad_name(filename):
            analysis = self.deep_content_analyze(filepath)

            # Strategy 1: Use main class name (best indicator)
            if analysis["classes"]:
                main_class = analysis["classes"][0]
                if len(main_class) > 5 and main_class != "Main":
                    return f"{main_class}.py"

            # Strategy 2: Use parent folder context + main function
            if analysis["parent_context"] and analysis["functions"]:
                context = analysis["parent_context"][0]
                main_func = analysis["functions"][0]
                if main_func not in ["main", "run", "init", "setup"]:
                    return f"{context}_{main_func}.py"

            # Strategy 3: Use keywords from docstring
            if len(analysis["keywords"]) >= 2:
                return f"{analysis['keywords'][0]}_{analysis['keywords'][1]}.py"

            # Strategy 4: Parent context + generic purpose
            if analysis["parent_context"]:
                context = analysis["parent_context"][0]

                # Determine purpose from imports
                imports_str = " ".join(analysis["imports"]).lower()
                if "requests" in imports_str or "httpx" in imports_str:
                    return f"{context}_api_client.py"
                elif "selenium" in imports_str or "beautifulsoup" in imports_str:
                    return f"{context}_scraper.py"
                elif "upload" in " ".join(analysis["functions"]).lower():
                    return f"{context}_uploader.py"
                elif "download" in " ".join(analysis["functions"]).lower():
                    return f"{context}_downloader.py"
                else:
                    return f"{context}_tool.py"

        # Default: just simplify if different
        return simplified if simplified != filename else None

    def scan_and_plan(self) -> None:
        """Scan directory and create rename plan - CONTENT & PARENT AWARE"""
        logger.info(f"\n{Colors.CYAN}{Colors.BOLD}🔍 Scanning: {self.target_dir}{Colors.END}")
        logger.info(f"{Colors.YELLOW}   (Content-aware + Parent-folder context){Colors.END}\n")

        file_count = 0
        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if not d.startswith((".", "__pycache__", "node_modules"))]

            # Show current directory being scanned
            rel_dir = Path(root).relative_to(self.target_dir)
            if rel_dir != Path("."):
                logger.info(f"{Colors.CYAN}📁 {rel_dir}/{Colors.END}")

            for filename in files:
                if not filename.endswith(".py") or filename.startswith("."):
                    continue

                file_count += 1
                filepath = Path(root) / filename

                # Get parent context
                parent_dir = filepath.parent.name

                # Content-aware analysis
                new_name = self.analyze_file(filepath)

                if new_name and new_name != filename:
                    # Check if it's actually better
                    if len(new_name) < len(filename) - 10:  # Avoid over-simplification
                        # Make sure we're not losing important context
                        pass

                    self.rename_plan.append(
                        {
                            "old_path": filepath,
                            "new_path": filepath.parent / new_name,
                            "old_name": filename,
                            "new_name": new_name,
                            "parent_dir": str(rel_dir),
                            "parent_context": parent_dir,
                            "reason": self.get_rename_reason(filename, new_name),
                        }
                    )

        logger.info(f"\n{Colors.GREEN}✅ Scanned {file_count} Python files{Colors.END}")
        logger.info(f"{Colors.GREEN}✅ Found {len(self.rename_plan)} files to rename{Colors.END}")

    def get_rename_reason(self, old_name: str, new_name: str) -> str:
        """Explain why renaming"""
        if any(word in old_name for word in self.REDUNDANT_WORDS):
            return "Removed redundant prefix"
        elif "copy" in old_name:
            return 'Removed "copy" suffix'
        elif re.match(r"^[a-z]{1,4}\.py$", old_name):
            return "Added descriptive context (was too short)"
        elif "--" in old_name or ".." in old_name:
            return "Fixed malformed filename"
        elif re.search(r"\d+\.py$", old_name):
            return "Cleaned version number"
        else:
            return "Content-aware improvement"

    def execute_plan(self) -> None:
        """Execute rename plan - showing parent context"""
        logger.info(f"\n{Colors.BOLD}📋 RENAME PLAN ({len(self.rename_plan)} files):{Colors.END}\n")

        # Group by parent directory for better organization
        by_parent = {}
        for item in self.rename_plan:
            parent = item.get("parent_dir", ".")
            if parent not in by_parent:
                by_parent[parent] = []
            by_parent[parent].append(item)

        undo_commands = []
        idx = 1

        for parent_dir in sorted(by_parent.keys()):
            items = by_parent[parent_dir]

            logger.info(f"{Colors.BOLD}{Colors.MAGENTA}📁 {parent_dir}/{Colors.END}")

            for item in items:
                logger.info(f"  {Colors.BOLD}[{idx}]{Colors.END} {item['old_name']}")
                logger.info(f"      → {Colors.GREEN}{item['new_name']}{Colors.END}")
                logger.info(f"      {Colors.CYAN}Context: {item.get('parent_context', 'none')}{Colors.END}")
                logger.info(f"      {Colors.YELLOW}{item['reason']}{Colors.END}")

                if not self.dry_run:
                    try:
                        item["old_path"].rename(item["new_path"])
                        undo_commands.append(f"mv '{item['new_path']}' '{item['old_path']}'")
                        logger.info(f"      {Colors.GREEN}✅ Renamed{Colors.END}\n")
                    except Exception as e:
                        logger.info(f"      {Colors.RED}❌ Error: {e}{Colors.END}\n")
                else:
                    logger.info(f"      {Colors.YELLOW}[DRY RUN]{Colors.END}\n")

                idx += 1

            print()

        # Generate undo script
        if undo_commands and not self.dry_run:
            with open(self.undo_script, "w") as f:
                f.write("#!/bin/bash\n")
                f.write("# Undo renames\n\n")
                for cmd in reversed(undo_commands):
                    f.write(f"{cmd}\n")
            self.undo_script.chmod(0o755)
            logger.info(f"\n{Colors.GREEN}✅ Undo script: {self.undo_script}{Colors.END}")

        # Generate CSV output
        if self.csv_output:
            self.generate_csv_report()

        if self.dry_run:
            logger.info(f"\n{Colors.YELLOW}⚠️  DRY RUN - use --live to apply{Colors.END}")
        else:
            logger.info(f"\n{Colors.GREEN}✅ {len(self.rename_plan)} files renamed!{Colors.END}")

    def generate_csv_report(self) -> None:
        """Generate CSV report with old --> new mappings"""
        try:
            with open(self.csv_output, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Header
                writer.writerow(
                    ["Old Name", "New Name", "Full Old Path", "Full New Path", "Parent Directory", "Reason", "Status"]
                )

                # Data rows
                for item in self.rename_plan:
                    status = "Renamed" if not self.dry_run else "Dry Run"
                    writer.writerow(
                        [
                            item["old_name"],
                            item["new_name"],
                            str(item["old_path"]),
                            str(item["new_path"]),
                            item.get("parent_dir", "."),
                            item["reason"],
                            status,
                        ]
                    )

            logger.info(f"{Colors.GREEN}📊 CSV Report: {self.csv_output}{Colors.END}")

        except Exception as e:
            logger.info(f"{Colors.RED}❌ CSV Error: {e}{Colors.END}")

    def run(self) -> None:
        """Run the renamer"""
        logger.info(f"{Colors.BOLD}{Colors.MAGENTA}")
        logger.info("╔═══════════════════════════════════════════════════════════════════╗")
        logger.info("║          🎯 SMART CONSERVATIVE RENAMER 🧠                         ║")
        logger.info("║      (Keeps good names, fixes bad ones - YOUR style!)            ║")
        logger.info("╚═══════════════════════════════════════════════════════════════════╝")
        logger.info(f"{Colors.END}")

        self.scan_and_plan()

        if not self.rename_plan:
            logger.info(f"{Colors.GREEN}✅ All files have good names already!{Colors.END}")
            return

        self.execute_plan()


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else Path(str(Path.home()) + "/Documents/python")
    live = "--live" in sys.argv

    # CSV output location
    csv_output = None
    for arg in sys.argv:
        if arg.startswith("--csv="):
            csv_output = arg.split("=", 1)[1]

    # Default CSV to home directory
    if not csv_output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_output = fstr(Path.home()) + "/rename_results_{timestamp}.csv"

    renamer = SmartConservativeRenamer(target, dry_run=not live, csv_output=csv_output)
    renamer.run()
