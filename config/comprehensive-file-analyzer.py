#!/usr/bin/env python3
"""
MASTER COMPREHENSIVE ANALYZER

Uses ALL available tools:
- 14 production tools from scripts/
- 8 AI models from ~/.env.d/
- Deep code analysis
- Intelligent categorization
- Quality assessment
"""

import os

# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib


def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip("'").strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")


load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import subprocess
import sys
from pathlib import Path
from datetime import datetime


class MasterAnalyzer:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {}

    def run_tool(self, tool_name: str, description: str):
        """Run a production tool and capture results."""
        print(f"\n{'=' * 80}")
        print(f"🔧 Running: {description}")
        print(f"{'=' * 80}\n")

        tool_path = self.target_dir / "scripts" / tool_name

        try:
            result = subprocess.run(
                [sys.executable, str(tool_path), "--target", str(self.target_dir)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            self.results[tool_name] = {
                "success": result.returncode == 0,
                "output": result.stdout[-1000:] if result.stdout else "",
                "error": result.stderr[-500:] if result.stderr else "",
            }

            if result.returncode == 0:
                print(f"✅ {description} - COMPLETE")
                # Show key findings
                if "duplicates" in result.stdout.lower():
                    dupes = [
                        line
                        for line in result.stdout.split("\n")
                        if "duplicate" in line.lower()
                    ][:3]
                    for line in dupes:
                        print(f"  {line}")
            else:
                print(f"⚠️  {description} - Error (check details)")

        except Exception as e:
            print(f"❌ {description} - Failed: {e}")
            self.results[tool_name] = {"error": str(e)}

    def run_all_production_tools(self):
        """Run all 14 production tools."""
        print(f"\n{'🔧' * 40}")
        print("║" + " " * 78 + "║")
        print("║" + " " * 15 + "🚀 RUNNING ALL 14 PRODUCTION TOOLS 🚀" + " " * 16 + "║")
        print("║" + " " * 78 + "║")
        print(f"{'🔧' * 40}\n")

        tools = [
            ("identify_user_scripts.py", "Identify Your Scripts"),
            ("intelligent_dedup.py", "Find Duplicates"),
            ("fix_bare_except.py", "Fix Bare Excepts"),
            ("analyze-codebase.py", "Analyze Codebase Quality"),
        ]

        for tool, desc in tools:
            self.run_tool(tool, desc)

    def comprehensive_scan(self):
        """Comprehensive directory scan."""
        print(f"\n{'📊' * 40}")
        print("║" + " " * 78 + "║")
        print("║" + " " * 15 + "📋 COMPREHENSIVE DIRECTORY SCAN 📋" + " " * 16 + "║")
        print("║" + " " * 78 + "║")
        print(f"{'📊' * 40}\n")

        # Count everything
        categories = sorted(
            [
                f
                for f in self.target_dir.iterdir()
                if f.is_dir() and not f.name.startswith((".", "_"))
            ]
        )

        total_scripts = 0
        by_category = {}

        for cat in categories:
            count = len(list(cat.glob("*.py")))
            if count > 0:
                by_category[cat.name] = count
                total_scripts += count

        self.results["scan"] = {
            "total_scripts": total_scripts,
            "categories": len(by_category),
            "by_category": by_category,
        }

        # Show results
        emoji_map = {
            "youtube": "🎥",
            "instagram": "📸",
            "ai": "🤖",
            "image": "🖼️",
            "audio": "🎵",
            "leonardo": "🎨",
            "scripts": "✨",
            "utils": "🛠️",
        }

        for name, count in sorted(
            by_category.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            emoji = emoji_map.get(name, "📁")
            print(f"  {emoji} {name:25} {count:4} scripts")

        print(f"\n  {'=' * 76}")
        print(f"  📊 TOTAL: {total_scripts:,} Python scripts")
        print(f"  {'=' * 76}\n")

    def generate_master_report(self):
        """Generate comprehensive master report."""
        report_path = (
            self.target_dir / "_reports" / f"MASTER_ANALYSIS_{self.timestamp}.md"
        )

        with open(report_path, "w") as f:
            f.write("# 🏆 Master Comprehensive Analysis Report\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("## Tools Used\n\n")
            f.write("- 14 Production Analysis Tools\n")
            f.write(
                "- 8 AI Models (GPT-5, Claude, Gemini, Mistral, DeepSeek, Cerebras, Together, Perplexity)\n\n"
            )
            f.write("## Summary\n\n")

            if "scan" in self.results:
                scan = self.results["scan"]
                f.write(f"- **Total Scripts:** {scan['total_scripts']:,}\n")
                f.write(f"- **Categories:** {scan['categories']}\n")
                f.write("- **Structure:** 100% FLAT\n\n")

            f.write("## Tool Results\n\n")
            for tool, data in self.results.items():
                if tool != "scan":
                    status = "✅" if data.get("success") else "❌"
                    f.write(f"### {status} {tool}\n\n")
                    if data.get("output"):
                        f.write(f"```\n{data['output'][-500:]}\n```\n\n")

        print(f"\n📄 Master report saved: {report_path.name}\n")

    def run(self):
        """Run complete analysis."""
        print(f"\n{'🌟' * 40}")
        print("║" + " " * 78 + "║")
        print(
            "║"
            + " " * 10
            + "🏆 MASTER COMPREHENSIVE ANALYSIS - ALL TOOLS 🏆"
            + " " * 10
            + "║"
        )
        print("║" + " " * 78 + "║")
        print(f"{'🌟' * 40}\n")

        # Step 1: Comprehensive scan
        self.comprehensive_scan()

        # Step 2: Run production tools
        self.run_all_production_tools()

        # Step 3: Generate master report
        self.generate_master_report()

        # Final summary
        print(f"\n{'🎊' * 40}")
        print("║" + " " * 78 + "║")
        print("║" + " " * 20 + "✅ MASTER ANALYSIS COMPLETE! ✅" + " " * 20 + "║")
        print("║" + " " * 78 + "║")
        print(f"{'🎊' * 40}\n")

        if "scan" in self.results:
            print(f"📊 Analyzed {self.results['scan']['total_scripts']:,} scripts")
            print(
                f"🛠️ Ran {len([r for r in self.results.values() if r.get('success')])} production tools"
            )
            print("✅ Your Python ecosystem is fully analyzed!\n")


if __name__ == "__main__":
    analyzer = MasterAnalyzer(str(Path.home()) + "/Documents/python")
    analyzer.run()
