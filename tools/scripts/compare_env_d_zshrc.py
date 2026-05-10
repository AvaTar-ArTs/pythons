#!/usr/bin/env python3
"""
Compare ~/.env.d with ~/.zshrc
Analyze how environment variables are loaded and used
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

import json
import re
from pathlib import Path
from datetime import datetime


class EnvDZshrcComparator:
    """Compare ~/.env.d with ~/.zshrc"""

    def __init__(self):
        self.home = PathLib.home()
        self.env_d_path = self.home / ".env.d"
        self.zshrc_path = self.home / ".zshrc"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {
            "scan_metadata": {
                "timestamp": self.timestamp,
                "env_d_path": str(self.env_d_path),
                "zshrc_path": str(self.zshrc_path),
            },
            "zshrc_analysis": {},
            "env_d_analysis": {},
            "comparison": {},
            "recommendations": [],
        }

    def analyze_zshrc(self):
        """Analyze ~/.zshrc file"""
        print("📄 Analyzing ~/.zshrc...")

        if not self.zshrc_path.exists():
            print("   ⚠️  ~/.zshrc not found!")
            return

        with open(self.zshrc_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.splitlines()

        analysis = {
            "total_lines": len(lines),
            "file_size": self.zshrc_path.stat().st_size,
            "env_d_references": [],
            "source_statements": [],
            "export_statements": [],
            "env_loading_patterns": [],
            "api_key_references": [],
            "functions": [],
            "aliases": [],
            "paths": [],
        }

        # Find .env.d references
        for i, line in enumerate(lines, 1):
            if ".env.d" in line or "env.d" in line or "ENV_D" in line:
                analysis["env_d_references"].append(
                    {"line": i, "content": line.strip()}
                )

            # Find source statements
            if line.strip().startswith("source "):
                analysis["source_statements"].append(
                    {"line": i, "content": line.strip()}
                )

            # Find export statements
            if line.strip().startswith("export "):
                analysis["export_statements"].append(
                    {
                        "line": i,
                        "content": line.strip()[:100],  # Truncate for privacy
                    }
                )

            # Find environment loading patterns
            if any(
                pattern in line.lower()
                for pattern in ["load", "dotenv", ".env", "export"]
            ):
                if "=" in line or "source" in line:
                    analysis["env_loading_patterns"].append(
                        {"line": i, "content": line.strip()[:100]}
                    )

            # Find API key references (without values)
            if re.search(r"\b(API_KEY|SECRET|TOKEN)\b", line, re.IGNORECASE):
                analysis["api_key_references"].append(
                    {"line": i, "content": line.strip()[:100]}
                )

            # Find function definitions
            if line.strip().startswith("function ") or re.match(
                r"^\w+\(\)\s*\{", line.strip()
            ):
                func_match = re.search(r"(function\s+)?(\w+)", line)
                if func_match:
                    analysis["functions"].append(
                        {
                            "line": i,
                            "name": func_match.group(2)
                            if func_match.group(2)
                            else func_match.group(1),
                        }
                    )

            # Find aliases
            if line.strip().startswith("alias "):
                alias_match = re.search(r"alias\s+(\w+)", line)
                if alias_match:
                    analysis["aliases"].append(
                        {"line": i, "name": alias_match.group(1)}
                    )

            # Find PATH modifications
            if "PATH" in line and ("=" in line or "export" in line):
                analysis["paths"].append({"line": i, "content": line.strip()[:100]})

        self.results["zshrc_analysis"] = analysis
        print(f"   ✓ Analyzed {len(lines)} lines")
        print(f"   ✓ Found {len(analysis['env_d_references'])} .env.d references")
        print(f"   ✓ Found {len(analysis['source_statements'])} source statements")
        print(f"   ✓ Found {len(analysis['export_statements'])} export statements")

    def analyze_env_d(self):
        """Quick analysis of ~/.env.d"""
        print("📁 Analyzing ~/.env.d structure...")

        if not self.env_d_path.exists():
            print("   ⚠️  ~/.env.d not found!")
            return

        files = list(self.env_d_path.glob("*.env"))
        all_keys = set()

        for env_file in files:
            try:
                with open(env_file, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            if line.startswith("export "):
                                line = line[7:]
                            if key:
                                all_keys.add(key)
            except:
                pass

        analysis = {
            "total_files": len(files),
            "file_names": [f.name for f in files],
            "total_keys": len(all_keys),
            "sample_keys": list(all_keys)[:20],  # Sample for comparison
        }

        self.results["env_d_analysis"] = analysis
        print(f"   ✓ Found {len(files)} .env files")
        print(f"   ✓ Found {len(all_keys)} unique keys")

    def compare(self):
        """Compare .env.d with .zshrc"""
        print("🔍 Comparing .env.d with .zshrc...")

        comparison = {
            "integration_status": "unknown",
            "env_d_usage": [],
            "missing_integration": [],
            "direct_exports": [],
            "recommendations": [],
        }

        # Check if .zshrc loads .env.d
        zshrc_refs = self.results["zshrc_analysis"].get("env_d_references", [])
        if zshrc_refs:
            comparison["integration_status"] = "integrated"
            comparison["env_d_usage"] = [ref["content"] for ref in zshrc_refs]
        else:
            comparison["integration_status"] = "not_integrated"
            comparison["missing_integration"] = [
                "No .env.d loading found in .zshrc",
                "Consider adding: source ~/.env.d/loader.sh (if exists)",
                "Or: for file in ~/.env.d/*.env; do source $file; done",
            ]

        # Check for direct exports in .zshrc
        exports = self.results["zshrc_analysis"].get("export_statements", [])
        if len(exports) > 10:  # Threshold
            comparison["direct_exports"] = [
                "Many direct export statements in .zshrc",
                f"Found {len(exports)} export statements",
                "Consider moving to .env.d files for better organization",
            ]

        # Check for API keys in .zshrc
        api_refs = self.results["zshrc_analysis"].get("api_key_references", [])
        if api_refs:
            comparison["recommendations"].append(
                {
                    "priority": "HIGH",
                    "issue": "API key references found in .zshrc",
                    "recommendation": "Move API keys to ~/.env.d files for better security",
                }
            )

        self.results["comparison"] = comparison
        print(f"   ✓ Integration status: {comparison['integration_status']}")

    def generate_recommendations(self):
        """Generate recommendations"""
        print("💡 Generating recommendations...")

        recommendations = []

        # Integration recommendations
        if self.results["comparison"].get("integration_status") == "not_integrated":
            recommendations.append(
                {
                    "priority": "MEDIUM",
                    "category": "Integration",
                    "issue": ".env.d not integrated with .zshrc",
                    "recommendation": "Add .env.d loading to .zshrc for automatic environment setup",
                    "example": 'for file in ~/.env.d/*.env; do [ -f "$file" ] && source "$file"; done',
                }
            )

        # Direct exports recommendations
        exports = self.results["zshrc_analysis"].get("export_statements", [])
        if len(exports) > 20:
            recommendations.append(
                {
                    "priority": "LOW",
                    "category": "Organization",
                    "issue": f"Many direct exports in .zshrc ({len(exports)} statements)",
                    "recommendation": "Consider moving environment variables to .env.d files",
                    "benefit": "Better organization and easier management",
                }
            )

        self.results["recommendations"] = recommendations
        print(f"   ✓ Generated {len(recommendations)} recommendations")

    def save_results(self):
        """Save comparison results"""
        print("💾 Saving results...")

        output_path = (
            PathLib.home() / "pythons" / f"ENV_D_ZSHRC_COMPARISON_{self.timestamp}"
        )
        output_path.mkdir(parents=True, exist_ok=True)

        # Save JSON
        json_path = output_path / "COMPARISON.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, default=str)

        # Generate report
        self.generate_report(output_path)

        print(f"   ✓ Results saved to {output_path}")
        return output_path

    def generate_report(self, output_path: Path):
        """Generate comparison report"""
        report_path = output_path / "COMPARISON_REPORT.md"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# ~/.env.d vs ~/.zshrc Comparison Report\n\n")
            f.write(f"**Generated:** {self.timestamp}\n\n")

            # Zshrc Analysis
            zshrc = self.results["zshrc_analysis"]
            f.write("## 📄 ~/.zshrc Analysis\n\n")
            f.write(f"- **Total Lines:** {zshrc.get('total_lines', 0)}\n")
            f.write(f"- **File Size:** {zshrc.get('file_size', 0) / 1024:.2f} KB\n")
            f.write(
                f"- **.env.d References:** {len(zshrc.get('env_d_references', []))}\n"
            )
            f.write(
                f"- **Source Statements:** {len(zshrc.get('source_statements', []))}\n"
            )
            f.write(
                f"- **Export Statements:** {len(zshrc.get('export_statements', []))}\n"
            )
            f.write(f"- **Functions:** {len(zshrc.get('functions', []))}\n")
            f.write(f"- **Aliases:** {len(zshrc.get('aliases', []))}\n\n")

            # Env.d Analysis
            env_d = self.results["env_d_analysis"]
            f.write("## 📁 ~/.env.d Analysis\n\n")
            f.write(f"- **Total Files:** {env_d.get('total_files', 0)}\n")
            f.write(f"- **Total Keys:** {env_d.get('total_keys', 0)}\n\n")

            # Comparison
            comp = self.results["comparison"]
            f.write("## 🔍 Comparison\n\n")
            f.write(
                f"- **Integration Status:** {comp.get('integration_status', 'unknown')}\n\n"
            )

            if comp.get("env_d_usage"):
                f.write("### .env.d Usage in .zshrc\n\n")
                for usage in comp["env_d_usage"]:
                    f.write(f"- `{usage}`\n")
                f.write("\n")

            if comp.get("missing_integration"):
                f.write("### Missing Integration\n\n")
                for item in comp["missing_integration"]:
                    f.write(f"- {item}\n")
                f.write("\n")

            # Recommendations
            f.write("## 💡 Recommendations\n\n")
            for rec in self.results["recommendations"]:
                f.write(f"### {rec['priority']} Priority: {rec['category']}\n\n")
                f.write(f"**Issue:** {rec['issue']}\n\n")
                f.write(f"**Recommendation:** {rec['recommendation']}\n\n")
                if "example" in rec:
                    f.write(f"**Example:**\n```bash\n{rec['example']}\n```\n\n")
                if "benefit" in rec:
                    f.write(f"**Benefit:** {rec['benefit']}\n\n")

    def run_comparison(self):
        """Run complete comparison"""
        print("🚀 Starting ~/.env.d vs ~/.zshrc Comparison")
        print("=" * 60)
        print()

        self.analyze_zshrc()
        self.analyze_env_d()
        self.compare()
        self.generate_recommendations()

        output_path = self.save_results()

        print("\n" + "=" * 60)
        print("✅ Comparison Complete!")
        print(f"📁 Results saved to: {output_path}")
        print("=" * 60)

        return output_path


if __name__ == "__main__":
    comparator = EnvDZshrcComparator()
    comparator.run_comparison()
