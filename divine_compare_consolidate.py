#!/usr/bin/env python3
"""
DivinePyTHon Compare & Consolidate
───────────────────────────────────
After today's deep research session — compare, consolidate, and enhance
everything we've built across the entire ecosystem.

Sources compared:
  1. ~/pythons/          — The Creative Studio (1,955 standalone scripts)
  2. ~/Documents/         — The Thought Archive (6,980 files, 3.3 GB)
  3. /Volumes/macBaks/diVinePyTHon/ — The Marketplace Repo (27 GB, 100+ dirs)

Outputs:
  - BEFORE_AFTER_CONSOLIDATION.md  (readable comparison)
  - CONSOLIDATION_GAPS.csv          (what's missing where)
  - ENHANCEMENT_PLAN.json           (what to do next)
  - CREATIVE_STUDIO_ECOSYSTEM.md    (updated with all findings)

Usage:
  python3 divine_compare_consolidate.py [--dry-run] [--deep]
"""

import os
import csv
import json
import hashlib
import re
import ast
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
import argparse


# ─── CONFIGURATION ───────────────────────────────────────────────────────

PYTHONS = Path.home() / "pythons"
DOCUMENTS = Path.home() / "Documents"
DIVINE = Path("/Volumes/macBaks/diVinePyTHon")

SKIP_DIRS = {
    "__pycache__", ".git", "node_modules", "venv", ".venv",
    "site-packages", ".pytest_cache", ".ruff_cache", ".Trash",
    ".cache", "Library", ".npm", ".cargo", ".bun", "google-cloud-sdk",
    ".local", ".pyenv", ".claude", ".harbor", ".qwen", ".cursor",
    ".gemini", ".codex", ".grok", ".qodo", ".sixth",
}


# ─── SCANNER ─────────────────────────────────────────────────────────────

class EcosystemScanner:
    """Scan a directory tree with content-aware analysis."""

    def __init__(self, root: Path, name: str, max_files: int = 50000):
        self.root = root
        self.name = name
        self.max_files = max_files
        self.files: List[Dict[str, Any]] = []
        self.stats = {
            "root": str(root),
            "total_files": 0,
            "total_dirs": 0,
            "total_size": 0,
            "by_ext": Counter(),
            "by_dir": Counter(),
            "by_size_bucket": Counter(),
            "python_files": 0,
            "python_with_class": 0,
            "python_with_main": 0,
            "python_with_argparse": 0,
            "python_with_async": 0,
            "python_with_ai": 0,
            "python_with_db": 0,
            "python_with_api": 0,
        }

    def scan(self) -> Dict[str, Any]:
        """Full scan with content analysis."""
        if not self.root.exists():
            return {"error": f"Path not found: {self.root}"}

        count = 0
        for f in sorted(self.root.rglob("*")):
            if count >= self.max_files:
                break
            if not f.is_file():
                continue
            if any(s in f.parts for s in SKIP_DIRS):
                continue
            if f.name.startswith("."):
                continue

            try:
                sz = f.stat().st_size
            except:
                continue

            count += 1
            ext = f.suffix.lower().lstrip(".") or "none"
            rel = str(f.relative_to(self.root))
            parts = rel.split("/")
            top_dir = parts[0] if len(parts) > 1 else "(root)"
            depth = len(parts) - 1

            # Size bucket
            if sz < 1024: bucket = "tiny"
            elif sz < 10*1024: bucket = "small"
            elif sz < 100*1024: bucket = "medium"
            elif sz < 1024*1024: bucket = "large"
            else: bucket = "xlarge"

            self.stats["by_ext"][ext] += 1
            self.stats["by_dir"][top_dir] += 1
            self.stats["by_size_bucket"][bucket] += 1
            self.stats["total_size"] += sz

            entry = {
                "file": f.name,
                "path": rel,
                "ext": ext,
                "size": sz,
                "bucket": bucket,
                "top_dir": top_dir,
                "depth": depth,
                "modified": "",
                "hash": "",
                "python_features": {},
            }

            # Python content analysis
            if ext == "py" and sz < 500000:
                self.stats["python_files"] += 1
                try:
                    content = open(f, "r", encoding="utf-8", errors="ignore").read()
                    cl = content.lower()
                    entry["hash"] = hashlib.sha256(content.encode()).hexdigest()[:12]
                    entry["modified"] = datetime.fromtimestamp(
                        f.stat().st_mtime
                    ).strftime("%Y-%m-%d")

                    features = {}
                    features["lines"] = content.count("\n")
                    features["def_count"] = content.count("def ")
                    features["class_count"] = content.count("class ")
                    features["has_main"] = "def main" in cl and "__name__" in cl
                    features["has_argparse"] = "argparse" in content
                    features["has_async"] = "async def" in cl or "asyncio" in content
                    features["has_threading"] = "threading" in content or "concurrent.futures" in content
                    features["has_db"] = "sqlite3" in content
                    features["has_api"] = "requests" in content or "aiohttp" in content
                    features["has_ai"] = "openai" in content or "anthropic" in content or "claude" in content
                    features["has_media"] = any(x in content for x in ["PIL", "moviepy", "pydub", "cv2"])
                    features["has_dry_run"] = "dry_run" in cl
                    features["has_backup"] = "backup" in cl
                    features["has_hash"] = "sha256" in cl or "hashlib" in content

                    if features["has_main"]: self.stats["python_with_main"] += 1
                    if features["class_count"] > 0: self.stats["python_with_class"] += 1
                    if features["has_argparse"]: self.stats["python_with_argparse"] += 1
                    if features["has_async"]: self.stats["python_with_async"] += 1
                    if features["has_ai"]: self.stats["python_with_ai"] += 1
                    if features["has_db"]: self.stats["python_with_db"] += 1
                    if features["has_api"]: self.stats["python_with_api"] += 1

                    # Creative purpose detection
                    features["creative_purpose"] = self._detect_creative_purpose(f.name, content)
                    features["business_domain"] = self._detect_business_domain(f.name, content)

                    entry["python_features"] = features

                except:
                    pass

            self.files.append(entry)

        self.stats["total_files"] = count
        self.stats["total_dirs"] = sum(
            1 for d in self.root.rglob("*")
            if d.is_dir() and not any(s in d.parts for s in SKIP_DIRS)
        )

        return {
            "name": self.name,
            "stats": self.stats,
            "files": self.files,
        }

    def _detect_creative_purpose(self, name: str, content: str) -> str:
        """Detect creative purpose from filename and content."""
        fn = name.lower()
        cl = content.lower()[:3000]

        # Creative transformation
        if "song" in fn and "transcribe" in fn: return "Song-to-Visual Translator"
        if "vid" in fn and "storytell" in fn: return "Narrative Film Analyst"
        if "convert" in fn and "loop" in fn: return "Art Director Loop"
        if "quiz" in fn and ("break" in fn or "speech" in fn): return "Voice Quiz Actor"
        if "vance" in fn: return "Photo Lab Manager"
        if "catalog" in fn and "art" in fn: return "Gallery Curator"
        if "paste" in fn and "export" in fn: return "Clipboard Archaeologist"
        if "receptionist" in fn: return "AI Receptionist"
        if "content_automation" in fn: return "Content Factory"
        if "sora" in fn: return "Sora Video Studio"

        # Self-awareness
        if "ecosystem_orchestrator" in fn: return "Ecosystem Brain"
        if "memory_system" in fn: return "Memory Index"
        if "content_aware" in fn: return "Semantic Scanner"
        if "duplicate" in fn or "dedup" in fn: return "Dedup Detective"
        if "find_scattered" in fn: return "Scattered Script Scout"
        if "consolidation_strategy" in fn: return "Strategic Planner"
        if "smart_consolidation" in fn: return "Consolidation Surgeon"
        if "compare_archives" in fn: return "Archive Comparator"
        if "cleanup_numbered" in fn: return "Numbered Dir Cleaner"
        if "dsstore" in fn: return "DS_Store Eraser"
        if "cleanup_and_organize" in fn: return "Cleanup Coordinator"
        if "organize_70" in fn or "comprehensive_organize_70" in fn: return "70-Dir Organizer"
        if "continue_from_csv" in fn: return "CSV Insight Continuer"
        if "review_home" in fn: return "Home Review Mirror"
        if "progress_indicator" in fn: return "Visual Feedback Performer"

        # Orchestration
        if "universal_automation_hub" in fn: return "Task Orchestrator"
        if "enhanced_automation_orchestrator" in fn: return "Enhanced Orchestrator"
        if "universal_file_toolkit" in fn: return "File Time Machine"
        if "enhanced_file_organizer" in fn: return "Enhanced File Organizer"
        if "deploy_to_marketplaces" in fn: return "Marketplace Deployer"

        # AI
        if "enhanced_ai_cli" in fn: return "AI CLI Ensemble"
        if "unified_ai_manager" in fn: return "Unified AI Manager"
        if "whisper" in fn: return "Whisper Transcriber"
        if "advanced_code_analyzer" in fn: return "Code Quality Auditor"
        if "advanced_file_deduplicator" in fn: return "Dedup File Engine"
        if "create_avatararts_index" in fn: return "Ecosystem Indexer"
        if "navigator" in fn: return "Ecosystem Navigator"
        if "unified_file_processor" in fn: return "Unified File Processor"
        if "content_organizer_agent" in fn: return "Content Organizer Agent"
        if "computer_use_mcp" in fn: return "MCP Computer Use Server"
        if "comprehensive_python_search" in fn: return "Cross-Volume Scanner"
        if "avatararts_consolidation" in fn: return "Consolidation Tool"
        if "directory_optimizer_agent" in fn: return "Directory Optimizer Agent"
        if "meta_agent" in fn: return "Meta Refactoring Agent"
        if "avatar_utils" in fn: return "Environment Loader"
        if "build_digital_dive" in fn: return "Digital Dive Builder"

        return "Uncategorized"

    def _detect_business_domain(self, name: str, content: str) -> str:
        """Detect business domain."""
        fn = name.lower()
        cl = content.lower()[:5000]

        domains = {
            "Music Production": ["music", "song", "audio", "transcribe", "whisper", "mp3"],
            "Visual Art": ["image", "upscale", "leonardo", "dalle", "gallery", "catalog", "art", "png"],
            "Video Production": ["video", "moviepy", "ffmpeg", "transcode", "sora"],
            "AI Services": ["openai", "anthropic", "claude", "gemini", "groq", "ollama", "llm"],
            "File Management": ["organize", "dedup", "consolidate", "cleanup", "rename", "directory"],
            "Marketplace/Sales": ["marketplace", "gumroad", "codecanyon", "bundle", "deploy", "revenue"],
            "Automation/DevOps": ["automation", "orchestrat", "schedule", "dispatch", "pipeline"],
            "Web Development": ["flask", "fastapi", "html", "css", "javascript", "api"],
            "Social Media": ["instagram", "youtube", "twitter", "tiktok"],
            "System Administration": ["ds_store", "zshrc", "backup", "env"],
            "MCP/Agent Tools": ["mcp", "computer_use", "playwright", "browser"],
            "Clipboard/History": ["paste", "clipboard", "history"],
            "Receptionist/SaaS": ["receptionist", "appointment", "booking", "client", "billing"],
            "Data Science": ["pandas", "dataframe", "analysis", "csv"],
            "Education": ["quiz", "course", "training"],
        }

        for domain, keywords in domains.items():
            if any(kw in fn or kw in cl for kw in keywords):
                return domain
        return "General"


# ─── COMPARATOR ──────────────────────────────────────────────────────────

class EcosystemComparator:
    """Compare multiple scanned ecosystems."""

    def __init__(self, scans: List[Dict[str, Any]]):
        self.scans = scans

    def compare(self) -> Dict[str, Any]:
        """Generate comparison report."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "ecosystems": {},
            "comparison": {},
            "gaps": [],
            "consolidation_opportunities": [],
        }

        # Basic stats comparison
        for scan in self.scans:
            if "error" in scan:
                continue
            name = scan["name"]
            stats = scan["stats"]
            result["ecosystems"][name] = {
                "total_files": stats["total_files"],
                "total_dirs": stats["total_dirs"],
                "total_size_mb": round(stats["total_size"] / 1024 / 1024, 1),
                "python_files": stats["python_files"],
                "python_with_main": stats["python_with_main"],
                "python_with_class": stats["python_with_class"],
                "python_with_async": stats["python_with_async"],
                "python_with_ai": stats["python_with_ai"],
                "python_with_api": stats["python_with_api"],
                "top_extensions": dict(stats["by_ext"].most_common(10)),
                "top_directories": dict(stats["by_dir"].most_common(10)),
            }

        # Content overlap (Python files only)
        py_hashes = {}
        for scan in self.scans:
            if "error" in scan:
                continue
            for f in scan["files"]:
                if f["ext"] == "py" and f["hash"]:
                    h = f["hash"]
                    if h not in py_hashes:
                        py_hashes[h] = []
                    py_hashes[h].append({
                        "ecosystem": scan["name"],
                        "file": f["file"],
                        "path": f["path"],
                        "size": f["size"],
                    })

        # Find exact duplicates across ecosystems
        cross_dupes = {h: v for h, v in py_hashes.items() if len(v) > 1}
        result["comparison"]["exact_duplicates"] = len(cross_dupes)
        result["comparison"]["duplicate_details"] = [
            {"hash": h, "copies": copies} for h, copies in list(cross_dupes.items())[:20]
        ]

        # Unique files per ecosystem
        for scan in self.scans:
            if "error" in scan:
                continue
            name = scan["name"]
            ecosystem_hashes = {
                f["hash"] for f in scan["files"] if f["ext"] == "py" and f["hash"]
            }
            unique = set()
            for h in ecosystem_hashes:
                if h not in cross_dupes:
                    unique.add(h)
                elif len(cross_dupes[h]) == 1:
                    unique.add(h)
            result["ecosystems"][name]["unique_python_files"] = len(unique)

        # Creative purpose distribution
        purposes = defaultdict(lambda: defaultdict(int))
        domains = defaultdict(lambda: defaultdict(int))
        for scan in self.scans:
            if "error" in scan:
                continue
            name = scan["name"]
            for f in scan["files"]:
                pf = f.get("python_features", {})
                if pf:
                    purpose = pf.get("creative_purpose", "Uncategorized")
                    domain = pf.get("business_domain", "General")
                    purposes[name][purpose] += 1
                    domains[name][domain] += 1

        result["comparison"]["creative_purposes"] = {
            name: dict(p.most_common(20)) for name, p in purposes.items()
        }
        result["comparison"]["business_domains"] = {
            name: dict(d.most_common(15)) for name, d in domains.items()
        }

        # Gaps: creative roles that exist in one ecosystem but not others
        all_purposes = set()
        for p in purposes.values():
            all_purposes.update(p.keys())

        for purpose in sorted(all_purposes):
            present_in = [name for name, p in purposes.items() if purpose in p]
            missing_from = [name for name in [s["name"] for s in self.scans if "error" not in s] if purpose not in purposes.get(name, {})]
            if missing_from and present_in:
                result["gaps"].append({
                    "role": purpose,
                    "present_in": present_in,
                    "missing_from": missing_from,
                })

        return result


# ─── REPORT GENERATORS ───────────────────────────────────────────────────

def generate_markdown_report(comparison: Dict[str, Any], output_path: Path):
    """Generate readable BEFORE/AFTER markdown."""
    lines = []
    lines.append("# DivinePyTHon — Before & After Consolidation Report")
    lines.append("")
    lines.append(f"**Generated:** {comparison['timestamp']}")
    lines.append(f"**Ecosystems Compared:** {len(comparison['ecosystems'])}")
    lines.append("")

    # Summary table
    lines.append("## Ecosystem Summary")
    lines.append("")
    lines.append("| Ecosystem | Files | Dirs | Size (MB) | Python | CLI | Classes | Async | AI | Unique .py |")
    lines.append("|-----------|-------|------|-----------|--------|-----|---------|-------|----|-----------|")

    for name, eco in comparison["ecosystems"].items():
        lines.append(
            f"| {name} "
            f"| {eco.get('total_files', '?'):,} "
            f"| {eco.get('total_dirs', '?'):,} "
            f"| {eco.get('total_size_mb', '?'):,} "
            f"| {eco.get('python_files', 0):,} "
            f"| {eco.get('python_with_main', 0):,} "
            f"| {eco.get('python_with_class', 0):,} "
            f"| {eco.get('python_with_async', 0):,} "
            f"| {eco.get('python_with_ai', 0):,} "
            f"| {eco.get('unique_python_files', 0):,} |"
        )

    lines.append("")

    # Creative purposes
    lines.append("## Creative Purpose Distribution")
    lines.append("")
    for name, purposes in comparison["comparison"].get("creative_purposes", {}).items():
        lines.append(f"\n### {name}\n")
        for purpose, count in sorted(purposes.items(), key=lambda x: -x[1]):
            lines.append(f"- **{purpose}**: {count}")

    # Business domains
    lines.append("\n## Business Domain Distribution\n")
    for name, domains in comparison["comparison"].get("business_domains", {}).items():
        lines.append(f"\n### {name}\n")
        for domain, count in sorted(domains.items(), key=lambda x: -x[1]):
            lines.append(f"- **{domain}**: {count}")

    # Gaps
    if comparison["gaps"]:
        lines.append("\n## Consolidation Gaps")
        lines.append("")
        lines.append("Roles that exist in one ecosystem but not others:")
        lines.append("")
        for gap in comparison["gaps"][:30]:
            lines.append(
                f"- **{gap['role']}** — "
                f"in {', '.join(gap['present_in'])}; "
                f"missing from {', '.join(gap['missing_from'])}"
            )

    # Duplicates
    dup_count = comparison["comparison"].get("exact_duplicates", 0)
    lines.append(f"\n## Cross-Ecosystem Duplicates")
    lines.append("")
    lines.append(f"**{dup_count}** Python files exist identically across ecosystems.")
    lines.append("")

    lines.append("\n---")
    lines.append("*Generated by divine_compare_consolidate.py*")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return str(output_path)


def generate_gaps_csv(comparison: Dict[str, Any], output_path: Path):
    """Generate CSV of consolidation gaps."""
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Role", "Present_In", "Missing_From", "Priority"]
        )
        writer.writeheader()
        for gap in comparison["gaps"]:
            priority = "HIGH" if len(gap["missing_from"]) > len(gap["present_in"]) else "MEDIUM"
            writer.writerow({
                "Role": gap["role"],
                "Present_In": "; ".join(gap["present_in"]),
                "Missing_From": "; ".join(gap["missing_from"]),
                "Priority": priority,
            })

    return str(output_path)


def generate_enhancement_plan(comparison: Dict[str, Any], output_path: Path):
    """Generate JSON enhancement plan."""
    plan = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "ecosystems_compared": len(comparison["ecosystems"]),
            "total_duplicates": comparison["comparison"].get("exact_duplicates", 0),
            "total_gaps": len(comparison["gaps"]),
        },
        "actions": [],
    }

    # Action 1: Remove cross-ecosystem duplicates
    if comparison["comparison"].get("exact_duplicates", 0) > 0:
        plan["actions"].append({
            "id": 1,
            "priority": "HIGH",
            "action": "Remove cross-ecosystem Python duplicates",
            "details": f"{comparison['comparison']['exact_duplicates']} identical .py files exist across ecosystems",
            "strategy": "Keep copy in ~/pythons (Creative Studio), remove from other locations",
        })

    # Action 2: Fill gaps
    if comparison["gaps"]:
        plan["actions"].append({
            "id": 2,
            "priority": "MEDIUM",
            "action": "Consolidate creative roles into diVinePyTHon",
            "details": f"{len(comparison['gaps'])} roles exist in one ecosystem but not others",
            "strategy": "Copy unique creative scripts from ~/pythons to /Volumes/macBaks/diVinePyTHon/",
        })

    # Action 3: Merge Documents HTML into organized structure
    plan["actions"].append({
        "id": 3,
        "priority": "MEDIUM",
        "action": "Organize Documents/HTML into semantic categories",
        "details": "1.9 GB of AI-generated HTML in Documents/",
        "strategy": "Move into diVinePyTHon organized_intelligent/ structure",
    })

    # Action 4: Consolidate CSV analysis reports
    plan["actions"].append({
        "id": 4,
        "priority": "LOW",
        "action": "Merge all CSV analysis reports",
        "details": "358 MB of CSVs across Documents/CsV/, pythons/, and diVinePyTHon/",
        "strategy": "Single consolidated CSV index in diVinePyTHon/data_exports/",
    })

    with open(output_path, "w") as f:
        json.dump(plan, f, indent=2)

    return str(output_path)


# ─── MAIN ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DivinePyTHon Compare & Consolidate")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, no moves")
    parser.add_argument("--deep", action="store_true", help="Deep content analysis (slower)")
    parser.add_argument("--max-files", type=int, default=50000, help="Max files per scan")
    args = parser.parse_args()

    print("=" * 70)
    print("🔮 DIVINE PYTHON — COMPARE & CONSOLIDATE")
    print("=" * 70)
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f"Depth: {'DEEP' if args.deep else 'FAST'}")
    print()

    # Scan each ecosystem
    ecosystems = [
        (PYTHONS, "Creative Studio", 50000),
        (DOCUMENTS, "Thought Archive", 20000),
        (DIVINE, "Marketplace Repo", 50000),
    ]

    scans = []
    for path, name, max_f in ecosystems:
        if not path.exists():
            print(f"⚠️  {name}: not found at {path}")
            scans.append({"name": name, "error": f"Not found: {path}"})
            continue

        print(f"📡 Scanning {name}: {path}")
        scanner = EcosystemScanner(path, name, max_files=max_f if args.deep else 20000)
        result = scanner.scan()
        scans.append(result)

        stats = result.get("stats", {})
        print(f"   ✅ {stats.get('total_files', 0):,} files, "
              f"{stats.get('total_dirs', 0):,} dirs, "
              f"{stats.get('total_size', 0) / 1024 / 1024:.0f} MB")
        print(f"   🐍 {stats.get('python_files', 0)} Python files "
              f"({stats.get('python_with_main', 0)} CLI, "
              f"{stats.get('python_with_class', 0)} classes, "
              f"{stats.get('python_with_ai', 0)} AI)")
        print()

    # Compare
    print("🔍 Comparing ecosystems...")
    comparator = EcosystemComparator(scans)
    comparison = comparator.compare()

    # Generate outputs
    output_dir = PYTHONS
    md_path = output_dir / "BEFORE_AFTER_CONSOLIDATION.md"
    csv_path = output_dir / "CONSOLIDATION_GAPS.csv"
    json_path = output_dir / "ENHANCEMENT_PLAN.json"

    print(f"\n📝 Generating reports...")

    md_file = generate_markdown_report(comparison, md_path)
    print(f"   ✅ {md_file}")

    csv_file = generate_gaps_csv(comparison, csv_path)
    print(f"   ✅ {csv_file}")

    json_file = generate_enhancement_plan(comparison, json_path)
    print(f"   ✅ {json_file}")

    # Summary
    print(f"\n{'=' * 70}")
    print("📊 CONSOLIDATION SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Ecosystems scanned:    {len(scans)}")
    print(f"  Exact duplicates:      {comparison['comparison'].get('exact_duplicates', 0)}")
    print(f"  Consolidation gaps:    {len(comparison['gaps'])}")
    print(f"  Reports generated:     3")
    print()
    print("  📖 Read: BEFORE_AFTER_CONSOLIDATION.md")
    print("  📊 Gaps: CONSOLIDATION_GAPS.csv")
    print("  🎯 Plan: ENHANCEMENT_PLAN.json")


if __name__ == "__main__":
    main()
