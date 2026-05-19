#!/usr/bin/env python3
"""
Marketplace Consolidation Script
─────────────────────────────────
Scans all marketplace content locations, identifies what's ready vs what's
missing, consolidates into upload-ready packages, and generates a clear report.

Sources scanned:
  - ~/pythons/                    — The Creative Studio (source scripts)
  - /Volumes/macBaks/diVinePyTHon — The Marketplace Repo (consolidated)
  - ~/Documents/                  — The Thought Archive (HTML, CSV, notes)

Platforms covered:
  - Gumroad:    https://avatararts.gumroad.com/
  - Codester:   https://www.codester.com/avatararts
  - Payhip:     https://payhip.com/AvaTarArTs
  - Lemon Squeezy: https://buy.avatararts.org/

Usage:
  python3 marketplace_consolidate.py --dry-run      # Analyze only
  python3 marketplace_consolidate.py --execute      # Create packages
  python3 marketplace_consolidate.py --upload-ready # Build final ZIPs
"""

import os
import sys
import csv
import json
import shutil
import hashlib
import zipfile
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional, Tuple
import argparse


# ─── CONFIGURATION ───────────────────────────────────────────────────────

PYTHONS = Path.home() / "pythons"
DIVINE = Path("/Volumes/macBaks/diVinePyTHon")
DOCUMENTS = Path.home() / "Documents"

# Active seller accounts
PLATFORMS = {
    "gumroad": {
        "name": "Gumroad",
        "url": "https://avatararts.gumroad.com/",
        "fee_pct": 10,
        "max_file_mb": 5000,
        "active": True,
    },
    "codester": {
        "name": "Codester",
        "url": "https://www.codester.com/avatararts",
        "fee_pct": 30,
        "max_file_mb": 512,
        "active": True,
    },
    "payhip": {
        "name": "Payhip",
        "url": "https://payhip.com/AvaTarArTs",
        "fee_pct": 5,
        "max_file_mb": 2000,
        "active": True,
    },
    "lemon_squeezy": {
        "name": "Lemon Squeezy",
        "url": "https://buy.avatararts.org/",
        "fee_pct": 0,
        "max_file_mb": 10000,
        "active": True,
    },
    "fiverr": {
        "name": "Fiverr",
        "url": "https://www.fiverr.com/",
        "fee_pct": 20,
        "max_file_mb": 0,  # Service, not files
        "active": True,
    },
    "upwork": {
        "name": "Upwork",
        "url": "https://www.upwork.com/",
        "fee_pct": 10,
        "max_file_mb": 0,  # Service, not files
        "active": True,
    },
}

# The 7 bundles — what each contains, what scripts, what price
BUNDLES = {
    "bundle-1-code-quality": {
        "name": "Python Code Quality Toolkit",
        "price": 97,
        "category": "Development Tools",
        "description": "Professional Python code analysis, deduplication, and optimization tools. Three production-ready tools with full documentation.",
        "tags": ["python", "code-quality", "analyzer", "deduplication", "automation"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "01-code-quality",
        "required_scripts": [
            "advanced_code_analyzer.py",
            "advanced_file_deduplicator.py",
            "avatar_utils.py",
        ],
        "required_docs": ["README.md", "SETUP_GUIDE.md", "EXAMPLES.md"],
    },
    "bundle-2-automation-devops": {
        "name": "Automation & DevOps Powerhouse",
        "price": 147,
        "category": "DevOps",
        "description": "Central automation hub with task orchestration, dependency management, timeout handling, retry with backoff, and plugin system.",
        "tags": ["automation", "devops", "orchestrator", "scheduler", "pipeline"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "05-ai-automation",
        "required_scripts": [
            "universal_automation_hub.py",
            "enhanced_automation_orchestrator.py",
        ],
        "required_docs": ["README.md"],
    },
    "bundle-3-ai-toolkit": {
        "name": "AI Integration Toolkit",
        "price": 197,
        "category": "AI & Machine Learning",
        "description": "Unified CLI for Claude, OpenAI, Groq. Abstract AI provider pattern. 600-line Playwright MCP server for browser automation.",
        "tags": ["ai", "openai", "claude", "groq", "mcp", "automation"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "05-ai-automation",
        "required_scripts": [
            "enhanced_ai_cli.py",
            "unified_ai_manager.py",
            "computer_use_mcp.py",
        ],
        "required_docs": ["README.md"],
    },
    "bundle-4-file-management": {
        "name": "File & Content Management Toolkit",
        "price": 87,
        "category": "File Management",
        "description": "Content-aware file organization (reads Python AST to categorize), multi-algorithm dedup, intelligent renaming.",
        "tags": ["file-organizer", "deduplication", "content-aware", "automation"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy", "codester"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "04-file-content",
        "required_scripts": [
            "universal_file_toolkit.py",
            "enhanced_file_organizer.py",
        ],
        "required_docs": ["README.md"],
    },
    "bundle-5-media-tools": {
        "name": "Media Processing Suite",
        "price": 97,
        "category": "Media Tools",
        "description": "Song-to-visual translator, narrative film analyst, art director loop, batch upscaler. Creative transformation tools.",
        "tags": ["media", "image", "video", "ai-art", "transcription"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "06-media-tools",
        "required_scripts": [
            "song-transcribe-dalle.py",
            "vid-transcribe-storytell.py",
            "convert-loop2.py",
            "vance.py",
        ],
        "required_docs": ["README.md"],
    },
    "bundle-6-business-productivity": {
        "name": "Business Productivity Suite",
        "price": 77,
        "category": "Business",
        "description": "AI receptionist SaaS, content automation system, ecosystem orchestrator with 20 business verticals.",
        "tags": ["business", "saas", "receptionist", "automation", "analytics"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "07-business-productivity",
        "required_scripts": [
            "ai_receptionist.py",
            "content_automation_system.py",
            "ecosystem_orchestrator.py",
        ],
        "required_docs": ["README.md"],
    },
    "bundle-7-starter-pack": {
        "name": "Python Starter Pack",
        "price": 47,
        "category": "Development Tools",
        "description": "Memory system for 4,000+ scripts, ecosystem navigator, scattered script scout. Entry-level automation.",
        "tags": ["python", "starter", "organization", "discovery"],
        "platforms": ["gumroad", "payhip", "lemon_squeezy"],
        "source_dir": DIVINE / "10-gumroad-bundles" / "07-business-productivity",
        "required_scripts": [
            "memory_system.py",
            "navigator.py",
            "find_scattered_pythons.py",
        ],
        "required_docs": ["README.md"],
    },
}

# 10 Codester products
CODESTER_PRODUCTS = {
    "01-python-automation": {
        "name": "Python Automation Toolkit",
        "price": 49,
        "description": "Professional Python automation scripts for common workflows.",
    },
    "02-agent-templates": {
        "name": "AI Agent Templates",
        "price": 79,
        "description": "Ready-to-deploy AI agent templates.",
    },
    "03-mcp-boilerplate": {
        "name": "MCP Server Boilerplate",
        "price": 59,
        "description": "Model Context Protocol server templates.",
    },
    "04-hook-manager": {
        "name": "Hook Management System",
        "price": 39,
        "description": "Event-driven hook management.",
    },
    "05-telemetry-logger": {
        "name": "Telemetry Logger",
        "price": 29,
        "description": "Structured logging and telemetry.",
    },
    "06-file-organizer": {
        "name": "Smart File Organizer",
        "price": 49,
        "description": "Content-aware file organization.",
    },
    "07-messaging-bots": {
        "name": "Messaging Bot Suite",
        "price": 69,
        "description": "Multi-platform messaging automation.",
    },
    "08-sora-automation": {
        "name": "Sora Video Automation",
        "price": 99,
        "description": "OpenAI Sora video generation pipeline.",
    },
    "09-tooluniverse-api": {
        "name": "ToolUniverse API Client",
        "price": 59,
        "description": "API client for ToolUniverse.",
    },
    "10-seo-repo-optimizer": {
        "name": "SEO Repository Optimizer",
        "price": 49,
        "description": "SEO tools and optimization scripts.",
    },
}

# Skip patterns
SKIP_DIRS = {
    "__pycache__", ".git", "node_modules", "venv", ".venv",
    "site-packages", ".pytest_cache", ".ruff_cache", ".Trash",
    ".cache", "Library", ".npm", ".cargo", ".bun",
}


# ─── SCANNER ─────────────────────────────────────────────────────────────

class MarketplaceScanner:
    """Scan all marketplace content locations."""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "bundles": {},
            "codester_products": {},
            "uploaders": {},
            "listings": {},
            "gaps": [],
            "ready_to_upload": [],
            "needs_work": [],
            "total_size_mb": 0,
        }

    def scan_all(self) -> Dict[str, Any]:
        """Full scan of all marketplace content."""
        print("=" * 70)
        print("🔮 MARKETPLACE CONSOLIDATION SCANNER")
        print("=" * 70)
        print()

        # 1. Check 7 Gumroad bundles
        print("📦 Scanning 7 Gumroad Bundles...")
        for bundle_id, bundle in BUNDLES.items():
            status = self._check_bundle(bundle_id, bundle)
            self.results["bundles"][bundle_id] = status

        # 2. Check 10 Codester products
        print("\n🏪 Scanning 10 Codester Products...")
        codester_dir = DIVINE / "04-codester-products"
        for product_id, product in CODESTER_PRODUCTS.items():
            product_dir = codester_dir / product_id
            exists = product_dir.exists()
            file_count = sum(
                1 for f in product_dir.rglob("*")
                if f.is_file() and not any(s in f.parts for s in SKIP_DIRS)
            ) if exists else 0
            has_zip = any(
                f.suffix == ".zip" for f in product_dir.rglob("*")
                if f.is_file()
            ) if exists else False

            self.results["codester_products"][product_id] = {
                "name": product["name"],
                "price": product["price"],
                "exists": exists,
                "file_count": file_count,
                "has_zip": has_zip,
                "path": str(product_dir) if exists else "NOT FOUND",
                "status": "READY" if (exists and file_count > 0) else "MISSING",
            }
            print(f"   {'✅' if exists else '❌'} {product['name']} — {product['price']} — {file_count} files {'(ZIP)' if has_zip else ''}")

        # 3. Check uploaders
        print("\n📤 Scanning Uploaders...")
        uploaders_dir = DIVINE / "TOOLS_UTILITIES" / "uploaders"
        if uploaders_dir.exists():
            for f in sorted(uploaders_dir.glob("*.py")):
                sz = f.stat().st_size
                self.results["uploaders"][f.stem] = {
                    "file": f.name,
                    "path": str(f),
                    "size": sz,
                    "size_kb": round(sz / 1024, 1),
                }
                print(f"   ✅ {f.stem} — {sz / 1024:.1f} KB")
        else:
            print("   ❌ Uploaders directory not found")

        # 4. Check marketplace listings
        print("\n📋 Scanning Marketplace Listings...")
        listings_dir = DIVINE / "MARKETPLACE_LISTINGS"
        if listings_dir.exists():
            platforms_found = []
            total_listing_files = 0
            for d in sorted(listings_dir.iterdir()):
                if d.is_dir() and not d.name.startswith("_"):
                    file_count = sum(1 for f in d.rglob("*") if f.is_file())
                    total_listing_files += file_count
                    platforms_found.append(d.name)
                    print(f"   ✅ {d.name}/ — {file_count} files")
            self.results["listings"] = {
                "platforms": platforms_found,
                "total_files": total_listing_files,
                "path": str(listings_dir),
            }
        else:
            print("   ❌ Listings directory not found")

        # 5. Check launch plan docs
        print("\n📝 Scanning Launch Plan...")
        launch_dir = DIVINE / "13-launch-plan"
        if launch_dir.exists():
            launch_files = list(launch_dir.rglob("*"))
            print(f"   ✅ {len(launch_files)} launch plan files")
        else:
            print("   ❌ Launch plan directory not found")

        # 6. Check source scripts in ~/pythons
        print("\n🔍 Checking Source Scripts in ~/pythons...")
        for bundle_id, bundle in BUNDLES.items():
            for script in bundle["required_scripts"]:
                src = PYTHONS / script
                if src.exists():
                    print(f"   ✅ {script}")
                else:
                    print(f"   ❌ {script} — NOT FOUND in ~/pythons")
                    self.results["gaps"].append({
                        "type": "missing_source",
                        "bundle": bundle_id,
                        "script": script,
                    })

        # Summary
        self._print_summary()

        return self.results

    def _check_bundle(self, bundle_id: str, bundle: Dict) -> Dict:
        """Check if a bundle is ready for upload."""
        source_dir = bundle["source_dir"]
        exists = source_dir.exists()

        # Check required scripts
        scripts_found = []
        scripts_missing = []
        for script in bundle["required_scripts"]:
            # Check in bundle dir first, then ~/pythons
            src = source_dir / script if exists else None
            if src and src.exists():
                scripts_found.append(script)
            else:
                src2 = PYTHONS / script
                if src2.exists():
                    scripts_found.append(script)
                else:
                    scripts_missing.append(script)

        # Check required docs
        docs_found = []
        docs_missing = []
        for doc in bundle["required_docs"]:
            doc_path = source_dir / doc if exists else None
            if doc_path and doc_path.exists():
                docs_found.append(doc)
            else:
                docs_missing.append(doc)

        # Check for existing ZIP
        zip_path = None
        if exists:
            for f in source_dir.rglob("*.zip"):
                zip_path = str(f)
                break

        # Calculate total size
        total_size = 0
        file_count = 0
        if exists:
            for f in source_dir.rglob("*"):
                if f.is_file():
                    total_size += f.stat().st_size
                    file_count += 1

        # Determine status
        if scripts_missing:
            status = "MISSING SCRIPTS"
            self.results["needs_work"].append({
                "bundle": bundle_id,
                "name": bundle["name"],
                "reason": f"Missing scripts: {', '.join(scripts_missing)}",
            })
        elif docs_missing:
            status = "MISSING DOCS"
            self.results["needs_work"].append({
                "bundle": bundle_id,
                "name": bundle["name"],
                "reason": f"Missing docs: {', '.join(docs_missing)}",
            })
        elif file_count > 0:
            status = "READY"
            self.results["ready_to_upload"].append({
                "bundle": bundle_id,
                "name": bundle["name"],
                "price": bundle["price"],
                "platforms": bundle["platforms"],
                "file_count": file_count,
                "size_mb": round(total_size / 1024 / 1024, 2),
                "has_zip": zip_path is not None,
            })
        else:
            status = "EMPTY"
            self.results["needs_work"].append({
                "bundle": bundle_id,
                "name": bundle["name"],
                "reason": "Bundle directory is empty or doesn't exist",
            })

        print(f"   {'✅' if status == 'READY' else '❌'} {bundle['name']} (${bundle['price']}) — {status}")
        if scripts_found:
            print(f"      Scripts: {', '.join(scripts_found[:3])}{'...' if len(scripts_found) > 3 else ''}")
        if scripts_missing:
            print(f"      MISSING: {', '.join(scripts_missing)}")
        if zip_path:
            print(f"      ZIP: {zip_path}")

        return {
            "name": bundle["name"],
            "price": bundle["price"],
            "status": status,
            "scripts_found": scripts_found,
            "scripts_missing": scripts_missing,
            "docs_found": docs_found,
            "docs_missing": docs_missing,
            "file_count": file_count,
            "total_size": total_size,
            "size_mb": round(total_size / 1024 / 1024, 2),
            "has_zip": zip_path is not None,
            "zip_path": zip_path,
            "source_dir": str(source_dir) if exists else "NOT FOUND",
            "platforms": bundle["platforms"],
        }

    def _print_summary(self):
        """Print summary of scan results."""
        ready = self.results["ready_to_upload"]
        needs = self.results["needs_work"]

        print(f"\n{'=' * 70}")
        print("📊 MARKETPLACE READINESS SUMMARY")
        print(f"{'=' * 70}")
        print(f"\n🟢 READY TO UPLOAD ({len(ready)} bundles):")
        for r in ready:
            platforms = ", ".join(r["platforms"])
            zip_status = "✓ ZIP" if r["has_zip"] else "✗ no ZIP"
            print(f"   • {r['name']} (${r['price']}) — {r['file_count']} files, {r['size_mb']} MB — {zip_status} → {platforms}")

        print(f"\n🟡 NEEDS WORK ({len(needs)} bundles):")
        for n in needs:
            print(f"   • {n['name']} — {n['reason']}")

        print(f"\n📈 REVENUE POTENTIAL:")
        total_potential = sum(r["price"] for r in ready)
        total_possible = sum(b["price"] for b in BUNDLES.values())
        print(f"   Ready now: ${total_potential}")
        print(f"   Full portfolio: ${total_possible}")
        print(f"   Completeness: {len(ready)}/{len(BUNDLES)} bundles ({len(ready)/len(BUNDLES)*100:.0f}%)")


# ─── PACKAGE BUILDER ─────────────────────────────────────────────────────

class PackageBuilder:
    """Create upload-ready ZIP packages."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_all(self, scan_results: Dict) -> List[Dict[str, Any]]:
        """Build all ready bundles into ZIPs."""
        built = []

        print(f"\n{'=' * 70}")
        print("📦 BUILDING UPLOAD PACKAGES")
        print(f"{'=' * 70}")
        print(f"Output: {self.output_dir}")
        print()

        for bundle_id, bundle_data in scan_results.get("bundles", {}).items():
            if bundle_data["status"] not in ("READY", "MISSING DOCS"):
                print(f"⏭️  Skipping {bundle_data['name']} — {bundle_data['status']}")
                continue

            bundle_config = BUNDLES.get(bundle_id)
            if not bundle_config:
                continue

            zip_name = f"{bundle_id}_v1.zip"
            zip_path = self.output_dir / zip_name

            # Collect files
            files_to_include = []
            source_dir = Path(bundle_data["source_dir"])

            if source_dir.exists():
                for f in source_dir.rglob("*"):
                    if f.is_file() and not any(s in f.parts for s in SKIP_DIRS):
                        files_to_include.append(f)

            # Also add scripts from ~/pythons if not in bundle dir
            for script in bundle_config["required_scripts"]:
                src = PYTHONS / script
                if src.exists() and src not in files_to_include:
                    files_to_include.append(src)

            if not files_to_include:
                print(f"❌ {bundle_data['name']} — no files to package")
                continue

            # Create ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for f in files_to_include:
                    try:
                        arcname = f.name  # Flat structure in ZIP
                        zf.write(f, arcname)
                    except Exception as e:
                        print(f"   ⚠️  Could not add {f.name}: {e}")

            zip_size = zip_path.stat().st_size
            built.append({
                "bundle": bundle_id,
                "name": bundle_data["name"],
                "zip": str(zip_path),
                "files": len(files_to_include),
                "size": zip_size,
                "size_mb": round(zip_size / 1024 / 1024, 2),
            })
            print(f"✅ {bundle_data['name']} — {zip_name} ({len(files_to_include)} files, {zip_size / 1024 / 1024:.2f} MB)")

        return built


# ─── REPORT GENERATOR ────────────────────────────────────────────────────

def generate_report(scan_results: Dict, built_packages: List[Dict], output_path: Path):
    """Generate readable consolidation report."""
    lines = []
    lines.append("# Marketplace Consolidation Report")
    lines.append("")
    lines.append(f"**Generated:** {scan_results['timestamp']}")
    lines.append(f"**Platforms:** {', '.join(p['name'] for p in PLATFORMS.values() if p['active'])}")
    lines.append("")

    # Ready bundles
    ready = scan_results.get("ready_to_upload", [])
    lines.append(f"## ✅ Ready to Upload ({len(ready)} bundles)")
    lines.append("")
    lines.append("| Bundle | Price | Platforms | Files | Size | ZIP |")
    lines.append("|--------|-------|-----------|-------|------|-----|")
    for r in ready:
        built = next((b for b in built_packages if b["bundle"] in r["bundle"]), None)
        zip_status = f"✅ {built['size_mb']} MB" if built else "❌ not built"
        lines.append(
            f"| {r['name']} | ${r['price']} | {', '.join(r['platforms'])} | "
            f"{r['file_count']} | {r['size_mb']} MB | {zip_status} |"
        )

    # Needs work
    needs = scan_results.get("needs_work", [])
    if needs:
        lines.append(f"\n## 🟡 Needs Work ({len(needs)} bundles)")
        lines.append("")
        for n in needs:
            lines.append(f"- **{n['name']}**: {n['reason']}")

    # Codester products
    codester = scan_results.get("codester_products", {})
    lines.append(f"\n## 🏪 Codester Products ({len(codester)})")
    lines.append("")
    lines.append("| Product | Price | Exists | Files | ZIP |")
    lines.append("|---------|-------|--------|-------|-----|")
    for pid, pdata in codester.items():
        lines.append(
            f"| {pdata['name']} | ${pdata['price']} | "
            f"{'✅' if pdata['exists'] else '❌'} | "
            f"{pdata['file_count']} | "
            f"{'✅' if pdata['has_zip'] else '❌'} |"
        )

    # Uploaders
    uploaders = scan_results.get("uploaders", {})
    if uploaders:
        lines.append(f"\n## 📤 Uploaders ({len(uploaders)})")
        lines.append("")
        for name, udata in uploaders.items():
            lines.append(f"- **{name}** — {udata['size_kb']} KB")

    # Listings
    listings = scan_results.get("listings", {})
    if listings:
        lines.append(f"\n## 📋 Marketplace Listings")
        lines.append("")
        lines.append(f"- **Platforms covered:** {', '.join(listings['platforms'])}")
        lines.append(f"- **Total listing files:** {listings['total_files']}")

    # Revenue summary
    lines.append(f"\n## 💰 Revenue Summary")
    lines.append("")
    ready_revenue = sum(r["price"] for r in ready)
    total_revenue = sum(b["price"] for b in BUNDLES.values())
    lines.append(f"- **Ready now:** ${ready_revenue}")
    lines.append(f"- **Full portfolio:** ${total_revenue}")
    lines.append(f"- **Completeness:** {len(ready)}/{len(BUNDLES)} bundles")

    lines.append(f"\n---")
    lines.append(f"*Generated by marketplace_consolidate.py*")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return str(output_path)


# ─── MAIN ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Marketplace Consolidation")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only")
    parser.add_argument("--execute", action="store_true", help="Analyze + build ZIPs")
    parser.add_argument("--upload-ready", action="store_true", help="Build final upload packages")
    parser.add_argument("--output", type=Path, default=DIVINE / "_UPLOAD_PACKAGES",
                       help="Output directory for ZIPs")
    args = parser.parse_args()

    mode = "DRY RUN" if args.dry_run else ("BUILD" if args.execute or args.upload_ready else "SCAN")
    print(f"Mode: {mode}")
    print()

    # Scan
    scanner = MarketplaceScanner()
    scan_results = scanner.scan_all()

    if args.dry_run:
        print("\n🔍 Dry run complete. No files created.")
        return

    # Build packages
    builder = PackageBuilder(args.output)
    built = builder.build_all(scan_results)

    # Generate report
    report_path = args.output / "CONSOLIDATION_REPORT.md"
    report_file = generate_report(scan_results, built, report_path)

    print(f"\n📝 Report: {report_file}")
    print(f"📦 Packages: {len(built)} ZIPs in {args.output}")
    print(f"\n✅ Done.")


if __name__ == "__main__":
    main()
