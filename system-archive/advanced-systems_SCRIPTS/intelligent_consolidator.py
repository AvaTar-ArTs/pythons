#!/usr/bin/env python3
"""
Intelligent Environment Variable Consolidator
Uses content-awareness to merge duplicates intelligently
"""

import os
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

class IntelligentConsolidator:
    """Smart consolidation of duplicate environment variables"""

    def __init__(self, env_dir: str = "~/.env.d"):
        self.env_dir = Path(env_dir).expanduser()
        self.variables = defaultdict(list)
        self.categories = defaultdict(list)

    def scan_files(self):
        """Scan all env files and categorize variables"""

        print(f"\n{'='*80}")
        print(f"🔍 INTELLIGENT ENVIRONMENT CONSOLIDATION")
        print(f"{'='*80}\n")
        print(f"Scanning: {self.env_dir}\n")

        # Only scan .env files, explicitly skipping files named MASTER_CONSOLIDATED.env
        for file_path in self.env_dir.glob("*.env"):
            if file_path.is_file() and file_path.name != "MASTER_CONSOLIDATED.env":
                self._scan_file(file_path)

        # Optionally, also scan .sh files if truly wanted (unusual for .env content)
        for file_path in self.env_dir.glob("*.sh"):
            if file_path.is_file():
                self._scan_file(file_path)

    def _scan_file(self, file_path: Path):
        """Scan individual file"""

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # Extract variables
            var_pattern = r"^(?:export\s+)?([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$"
            matches = re.findall(var_pattern, content, re.MULTILINE)

            for var_name, var_value in matches:
                # Clean value
                var_value = var_value.strip().strip("\"'")

                # Determine category from file name, but skip master file
                if file_path.name.lower() == "master_consolidated.env":
                    # Do not include variables from the master file in analysis
                    continue
                category = self._determine_category(file_path.stem)

                self.variables[var_name].append(
                    {
                        "file": file_path.name,
                        "value": var_value,
                        "category": category,
                        "path": str(file_path),
                    }
                )

                self.categories[category].append(var_name)

        except Exception as e:
            print(f"⚠️  Error reading {file_path.name}: {e}")

    def _determine_category(self, filename: str) -> str:
        """Intelligently determine category from filename"""

        categories = {
            "llm": ["llm", "openai", "anthropic", "ai", "gpt"],
            "communication": ["twilio", "notification", "sms", "email"],
            "cloud": ["aws", "azure", "gcp", "cloud"],
            "database": ["db", "database", "mongo", "postgres", "supabase"],
            "audio": ["audio", "music", "sound", "speech"],
            "vision": ["vision", "image", "art", "video"],
            "automation": ["automation", "agent", "workflow"],
            "analytics": ["analytics", "seo", "tracking"],
            "document": ["document", "notion", "docs"],
            "system": ["loader", "aliases", "validate"],
        }

        filename_lower = filename.lower()

        for category, keywords in categories.items():
            if any(keyword in filename_lower for keyword in keywords):
                return category

        return "other"

    def analyze_duplicates(self):
        """Analyze duplicate variables intelligently"""

        print(f"📊 Analyzing duplicates...\n")

        duplicates = {k: v for k, v in self.variables.items() if len(v) > 1}

        if not duplicates:
            print("✅ No duplicates found!\n")
            return []

        print(f"Found {len(duplicates)} duplicate variables:\n")

        consolidation_plan = []

        for var_name, occurrences in sorted(duplicates.items()):
            # Analyze intelligently
            analysis = self._analyze_duplicate(var_name, occurrences)
            consolidation_plan.append(analysis)

            # Print summary
            status = "🟢" if analysis["action"] == "keep_first" else "🟡"
            print(f"{status} {var_name}")
            print(f"   Occurrences: {len(occurrences)}")
            print(f"   Files: {', '.join([o['file'] for o in occurrences])}")
            print(f"   Action: {analysis['action']}")
            print(f"   Reason: {analysis['reason']}")
            print()

        return consolidation_plan

    def _analyze_duplicate(self, var_name: str, occurrences: List[Dict]) -> Dict:
        """Intelligently analyze a duplicate variable"""

        # Get all unique values
        unique_values = list(set([o["value"] for o in occurrences]))

        # Case 1: All values are identical
        if len(unique_values) == 1:
            return {
                "variable": var_name,
                "action": "keep_first",
                "reason": "All values identical",
                "keep_value": unique_values[0],
                "keep_file": occurrences[0]["file"],
                "category": occurrences[0]["category"],
                "remove_from": [o["file"] for o in occurrences[1:]],
            }

        # Case 2: Different values - need intelligent decision

        # Check if it's a system variable (colors, paths)
        if any(
            keyword in var_name
            for keyword in ["COLOR", "RED", "GREEN", "BLUE", "NC", "ENV_DIR"]
        ):
            return {
                "variable": var_name,
                "action": "keep_first",
                "reason": "System variable - keep first occurrence",
                "keep_value": occurrences[0]["value"],
                "keep_file": occurrences[0]["file"],
                "category": "system",
                "remove_from": [o["file"] for o in occurrences[1:]],
            }

        # Check if values are variations (with/without quotes, etc.)
        normalized_values = [self._normalize_value(v) for v in unique_values]
        if len(set(normalized_values)) == 1:
            return {
                "variable": var_name,
                "action": "keep_first",
                "reason": "Values are equivalent (formatting differs)",
                "keep_value": occurrences[0]["value"],
                "keep_file": occurrences[0]["file"],
                "category": occurrences[0]["category"],
                "remove_from": [o["file"] for o in occurrences[1:]],
            }

        # Case 3: Genuinely different values - keep most specific
        return {
            "variable": var_name,
            "action": "review_needed",
            "reason": "Different values - manual review recommended",
            "values": [{"file": o["file"], "value": o["value"]} for o in occurrences],
            "category": occurrences[0]["category"],
        }

    def _normalize_value(self, value: str) -> str:
        """Normalize value for comparison"""
        return value.strip().strip("\"'").strip("${}")

    def create_consolidated_master(self, consolidation_plan: List[Dict]):
        """Create consolidated master file with navigation"""

        print(f"{'='*80}")
        print(f"📝 Creating consolidated master file...")
        print(f"{'='*80}\n")

        master_file = self.env_dir / "MASTER_CONSOLIDATED.env"
        backup_dir = self.env_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        # Group variables by category
        by_category = defaultdict(list)

        for item in consolidation_plan:
            if item["action"] in ["keep_first", "keep_most_specific"]:
                category = item["category"]
                by_category[category].append(item)

        # Also add non-duplicate variables
        for var_name, occurrences in self.variables.items():
            if len(occurrences) == 1:
                category = occurrences[0]["category"]
                by_category[category].append(
                    {
                        "variable": var_name,
                        "keep_value": occurrences[0]["value"],
                        "keep_file": occurrences[0]["file"],
                        "category": category,
                        "action": "original",
                    }
                )

        # Write consolidated file
        with open(master_file, "w", encoding="utf-8") as f:
            self._write_header(f)
            self._write_navigation(f, by_category)

            for category in sorted(by_category.keys()):
                self._write_category_section(f, category, by_category[category])

            self._write_footer(f)

        print(f"✅ Master file created: {master_file}")
        print(f"📁 Backup location: {backup_dir}")

        # Generate diff report
        self._generate_diff_report(consolidation_plan)

        return master_file

    def _write_header(self, f):
        """Write file header"""
        f.write(
            f"""#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════
# CONSOLIDATED MASTER ENVIRONMENT VARIABLES
# ═══════════════════════════════════════════════════════════════════════════
#
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Purpose: Consolidated environment variables from multiple files
# Source: ~/.env.d/
#
# This file consolidates all environment variables, removing duplicates and
# organizing by category for easy navigation and maintenance.
#
# ═══════════════════════════════════════════════════════════════════════════

"""
        )

    def _write_navigation(self, f, by_category: Dict):
        """Write navigation section"""
        f.write(
            "# ╔═══════════════════════════════════════════════════════════════════════════╗\n"
        )
        f.write(
            "# ║                           NAVIGATION INDEX                                ║\n"
        )
        f.write(
            "# ╚═══════════════════════════════════════════════════════════════════════════╝\n"
        )
        f.write("#\n")
        f.write("# Jump to sections:\n")
        f.write("#\n")

        for i, category in enumerate(sorted(by_category.keys()), 1):
            count = len(by_category[category])
            f.write(f"#   {i}. {category.upper():<20} ({count} variables)\n")

        f.write("#\n")
        f.write(
            "# ═══════════════════════════════════════════════════════════════════════════\n\n"
        )

    def _write_category_section(self, f, category: str, variables: List[Dict]):
        """Write a category section"""

        # Section header
        f.write(f"\n{'#'*80}\n")
        f.write(f"# {category.upper()}\n")
        f.write(f"{'#'*80}\n")
        f.write(f"# Variables: {len(variables)}\n")
        f.write(f"# Category: {category}\n")
        f.write(f"{'#'*80}\n\n")

        # Sort variables alphabetically
        for item in sorted(variables, key=lambda x: x["variable"]):
            var_name = item["variable"]
            value = item["keep_value"]
            source = item.get("keep_file", "unknown")

            # Add comment with source
            f.write(f"# Source: {source}\n")

            # Write variable
            if value:
                f.write(f'export {var_name}="{value}"\n')
            else:
                f.write(f'export {var_name}=""\n')

            f.write("\n")

    def _write_footer(self, f):
        """Write file footer"""
        f.write(
            "\n# ═══════════════════════════════════════════════════════════════════════════\n"
        )
        f.write("# END OF CONSOLIDATED ENVIRONMENT VARIABLES\n")
        f.write(
            "# ═══════════════════════════════════════════════════════════════════════════\n"
        )
        f.write("#\n")
        f.write("# To use this file:\n")
        f.write("#   source ~/.env.d/MASTER_CONSOLIDATED.env\n")
        f.write("#\n")
        f.write("# To update ~/.zshrc or ~/.bashrc:\n")
        f.write("#   echo 'source ~/.env.d/MASTER_CONSOLIDATED.env' >> ~/.zshrc\n")
        f.write("#\n")
        f.write(
            "# ═══════════════════════════════════════════════════════════════════════════\n"
        )

    def _generate_diff_report(self, consolidation_plan: List[Dict]):
        """Generate diff report showing what was consolidated"""

        report_file = self.env_dir / "CONSOLIDATION_REPORT.md"

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# Environment Consolidation Report\n\n")
            f.write(
                f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            f.write("## Summary\n\n")
            f.write(f"- **Total Variables Analyzed**: {len(self.variables)}\n")
            f.write(f"- **Duplicates Found**: {len(consolidation_plan)}\n")

            needs_review = [
                p for p in consolidation_plan if p["action"] == "review_needed"
            ]
            f.write(f"- **Needs Review**: {len(needs_review)}\n\n")

            f.write("## Consolidation Actions\n\n")

            # Group by action
            by_action = defaultdict(list)
            for item in consolidation_plan:
                by_action[item["action"]].append(item)

            for action, items in sorted(by_action.items()):
                f.write(f"### {action.replace('_', ' ').title()} ({len(items)})\n\n")

                for item in sorted(items, key=lambda x: x["variable"]):
                    f.write(f"#### `{item['variable']}`\n\n")
                    f.write(f"- **Reason**: {item['reason']}\n")

                    if action == "review_needed":
                        f.write("- **Values Found**:\n")
                        for val in item.get("values", []):
                            f.write(f"  - `{val['file']}`: `{val['value']}`\n")
                    else:
                        f.write(
                            f"- **Kept Value**: `{item.get('keep_value', 'N/A')}`\n"
                        )
                        f.write(f"- **From File**: `{item.get('keep_file', 'N/A')}`\n")
                        if "remove_from" in item:
                            f.write(
                                f"- **Removed From**: {', '.join(f'`{f}`' for f in item['remove_from'])}\n"
                            )

                    f.write("\n")

            f.write("## Categories\n\n")

            for category in sorted(self.categories.keys()):
                vars_in_cat = len(set(self.categories[category]))
                f.write(f"- **{category.title()}**: {vars_in_cat} variables\n")

            f.write("\n## Next Steps\n\n")
            f.write("1. Review the `MASTER_CONSOLIDATED.env` file\n")
            f.write("2. Check variables marked as 'review_needed'\n")
            f.write("3. Update your shell configuration to source the master file\n")
            f.write("4. Test in a new shell session\n")
            f.write("5. Backup original files are in `~/.env.d/backups/`\n")

        print(f"📄 Report created: {report_file}")

    def _backup_file(self, file_path: Path, backup_dir: Path) -> Path:
        """Create a timestamped backup copy of a file in backup_dir."""
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{file_path.name}.{timestamp}.bak"
        shutil.copy2(file_path, backup_path)
        return backup_path

    def prune_duplicate_sources(
        self, consolidation_plan: List[Dict], dry_run: bool = False
    ) -> Dict[str, Any]:
        """Remove redundant variable definitions from non-canonical source files.

        - Only prunes items with action == 'keep_first'.
        - Does NOT delete any files; it edits files in place to remove matching lines.
        - Creates timestamped backups before each edit.

        Returns a summary dict with counts and edited files.
        """

        print(
            "🧹 Pruning duplicate variable lines from source files (preserving structure)...\n"
        )

        changes_by_file: Dict[str, int] = {}
        edited_files: List[str] = []

        # Regex template to match an env assignment line for a specific var
        def assignment_regex(var: str) -> re.Pattern:
            # Matches lines like: VAR=..., export VAR=..., spaces around '=', quoted/unquoted
            pattern = rf"^(?:export\s+)?{re.escape(var)}\s*=.*$"
            return re.compile(pattern, re.MULTILINE)

        backup_dir = self.env_dir / "backups" / "pruned_sources"

        for item in consolidation_plan:
            if item.get("action") != "keep_first":
                continue

            var_name = item["variable"]
            remove_from_files = item.get("remove_from", [])

            for filename in remove_from_files:
                # Skip MASTER_CONSOLIDATED.env
                if filename.lower() == "master_consolidated.env":
                    continue
                file_path = self.env_dir / filename
                if not file_path.exists() or not file_path.is_file():
                    continue

                try:
                    original_text = file_path.read_text(
                        encoding="utf-8", errors="ignore"
                    )
                except Exception:
                    continue

                regex = assignment_regex(var_name)
                matches = list(regex.finditer(original_text))

                if not matches:
                    continue

                new_text = regex.sub("", original_text)

                # Remove any now-empty lines produced by the substitution
                new_text = re.sub(r"^\s*$\n", "", new_text, flags=re.MULTILINE)

                if new_text != original_text:
                    if not dry_run:
                        # Backup once per file before first write
                        if filename not in edited_files:
                            self._backup_file(file_path, backup_dir)
                            edited_files.append(filename)
                        file_path.write_text(new_text, encoding="utf-8")

                    changes_by_file[filename] = changes_by_file.get(filename, 0) + len(
                        matches
                    )

        print("✅ Pruning complete.\n")
        return {
            "edited_files": edited_files,
            "changes_by_file": changes_by_file,
            "dry_run": dry_run,
        }

    def create_loader_script(self):
        """Create smart loader script"""

        loader_file = self.env_dir / "load_master.sh"

        with open(loader_file, "w", encoding="utf-8") as f:
            f.write(
                """#!/bin/bash
# Smart Environment Loader
# Loads the consolidated master environment file

ENV_DIR="${HOME}/.env.d"
MASTER_FILE="${ENV_DIR}/MASTER_CONSOLIDATED.env"

if [ -f "$MASTER_FILE" ]; then
    echo "🔄 Loading consolidated environment..."
    source "$MASTER_FILE"
    echo "✅ Environment loaded successfully!"
    echo "📊 Loaded from: $MASTER_FILE"
else
    echo "❌ Master file not found: $MASTER_FILE"
    exit 1
fi

# Optional: Export count
export ENV_LOADED="true"
export ENV_LOADED_AT="$(date '+%Y-%m-%d %H:%M:%S')"
"""
            )

        # Make executable
        loader_file.chmod(0o755)

        print(f"🔧 Loader script created: {loader_file}")
        print(f"   Usage: source {loader_file}")

def main():
    """Main execution"""

    consolidator = IntelligentConsolidator()

    # Scan files
    consolidator.scan_files()

    # Analyze duplicates
    consolidation_plan = consolidator.analyze_duplicates()

    if not consolidation_plan:
        print("✅ No duplicates found - environment is already clean!")
        return

    # Ask for confirmation
    print(f"\n{'='*80}")
    print("📋 Ready to consolidate!")
    print(f"{'='*80}\n")

    response = input("Create consolidated master file? [Y/n]: ").strip().lower()

    if response and response != "y":
        print("\n❌ Consolidation cancelled.")
        return

    # Create master file
    master_file = consolidator.create_consolidated_master(consolidation_plan)

    # Create loader
    consolidator.create_loader_script()

    # Optional: prune duplicates from source files while preserving structure
    print(
        "\nWould you like to remove duplicate variable lines from their non-canonical files (original files remain, only redundant lines removed)?"
    )
    prune_answer = input("Prune duplicates now? [Y/n]: ").strip().lower()
    if not prune_answer or prune_answer == "y":
        summary = consolidator.prune_duplicate_sources(
            consolidation_plan, dry_run=False
        )
        if summary["edited_files"]:
            print("🗂️ Files edited:")
            for fname in summary["edited_files"]:
                print(
                    f"   • {fname} (removed {summary['changes_by_file'].get(fname, 0)} duplicate line(s))"
                )
        else:
            print("ℹ️  No source files required changes.")
    else:
        print("⏭️  Skipped pruning of source files.")

    print(f"\n{'='*80}")
    print("✅ CONSOLIDATION COMPLETE!")
    print(f"{'='*80}\n")

    print("📁 Created files:")
    print(f"   • MASTER_CONSOLIDATED.env (consolidated variables)")
    print(f"   • CONSOLIDATION_REPORT.md (detailed report)")
    print(f"   • load_master.sh (loader script)")

    print("\n🚀 Next steps:")
    print("   1. Review: cat ~/.env.d/MASTER_CONSOLIDATED.env | less")
    print("   2. Test: source ~/.env.d/load_master.sh")
    print("   3. Add to shell: echo 'source ~/.env.d/load_master.sh' >> ~/.zshrc")
    print()


if __name__ == "__main__":
    main()
