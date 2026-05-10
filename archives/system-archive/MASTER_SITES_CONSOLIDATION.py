#!/usr/bin/env python3
"""
Deep scan and consolidation of all sites, plans, and documentation
Creates a master index and identifies duplicates/gaps
"""

import json
from pathlib import Path
from collections import defaultdict
import hashlib


class SitesConsolidator:
    def __init__(self):
        self.base_dir = Path("/Users/steven")
        self.ai_sites_dir = self.base_dir / "ai-sites"
        self.ecosystem_dir = self.base_dir / "ECOSYSTEM"
        self.docs_dir = self.base_dir / "Documents" / "python"

        self.sites = {}
        self.plans = {}
        self.duplicates = defaultdict(list)
        self.missing_docs = []

    def scan_ai_sites(self):
        """Scan all directories in ai-sites"""
        print("🔍 Scanning ai-sites directory...")

        if not self.ai_sites_dir.exists():
            print("  ⚠️  ai-sites directory not found")
            return

        for item in self.ai_sites_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                site_info = {
                    "name": item.name,
                    "path": str(item),
                    "size": self.get_dir_size(item),
                    "has_readme": (item / "README.md").exists(),
                    "has_package_json": (item / "package.json").exists(),
                    "has_docs": (item / "docs").exists(),
                    "file_count": len(list(item.rglob("*"))),
                }

                # Check for specific markers
                if (item / ".git").exists():
                    site_info["git_repo"] = True
                if (item / "node_modules").exists():
                    site_info["node_project"] = True
                if (item / "venv").exists() or (item / ".venv").exists():
                    site_info["python_project"] = True

                self.sites[item.name] = site_info

        print(f"  ✅ Found {len(self.sites)} sites/projects")

    def scan_ecosystem_docs(self):
        """Scan ECOSYSTEM documentation"""
        print("\n🔍 Scanning ECOSYSTEM documentation...")

        if not self.ecosystem_dir.exists():
            print("  ⚠️  ECOSYSTEM directory not found")
            return

        docs_by_category = defaultdict(list)

        for md_file in self.ecosystem_dir.rglob("*.md"):
            category = (
                md_file.parent.name if md_file.parent != self.ecosystem_dir else "root"
            )
            docs_by_category[category].append(
                {
                    "name": md_file.name,
                    "path": str(md_file),
                    "size": md_file.stat().st_size,
                }
            )

        self.plans["ecosystem"] = dict(docs_by_category)

        total_docs = sum(len(docs) for docs in docs_by_category.values())
        print(f"  ✅ Found {total_docs} documentation files")
        for category, docs in docs_by_category.items():
            print(f"     • {category}: {len(docs)} files")

    def scan_python_docs(self):
        """Scan Documents/python for planning docs"""
        print("\n🔍 Scanning Documents/python for plans...")

        if not self.docs_dir.exists():
            print("  ⚠️  Documents/python directory not found")
            return

        planning_docs = []
        for pattern in [
            "_*.md",
            "*PLAN*.md",
            "*STRATEGY*.md",
            "*EXECUTION*.md",
            "*SEO*.md",
        ]:
            for doc in self.docs_dir.glob(pattern):
                if doc.is_file():
                    planning_docs.append(
                        {"name": doc.name, "path": str(doc), "size": doc.stat().st_size}
                    )

        self.plans["python_docs"] = planning_docs
        print(f"  ✅ Found {len(planning_docs)} planning documents")

    def find_duplicate_docs(self):
        """Find duplicate documentation by content hash"""
        print("\n🔍 Checking for duplicate documentation...")

        all_docs = []

        # Collect all markdown files
        for location in [self.ecosystem_dir, self.docs_dir]:
            if location.exists():
                all_docs.extend(location.rglob("*.md"))

        # Hash each file
        hashes = defaultdict(list)
        for doc in all_docs:
            try:
                with open(doc, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                    hashes[file_hash].append(str(doc))
            except:
                pass

        # Find duplicates
        duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}

        if duplicates:
            print(f"  ⚠️  Found {len(duplicates)} duplicate document sets")
            for i, (hash_val, paths) in enumerate(list(duplicates.items())[:3], 1):
                print(f"\n  Duplicate Set {i}:")
                for path in paths:
                    print(f"    - {Path(path).name}")
        else:
            print("  ✅ No duplicate documents found")

        self.duplicates = duplicates

    def check_site_documentation(self):
        """Check which sites are missing documentation"""
        print("\n🔍 Checking site documentation coverage...")

        ecosystem_properties = set()
        if (self.ecosystem_dir / "docs" / "PROPERTIES").exists():
            ecosystem_properties = {
                f.stem
                for f in (self.ecosystem_dir / "docs" / "PROPERTIES").glob("*.md")
            }

        missing_docs = []
        for site_name in self.sites.keys():
            # Normalize name for comparison
            normalized = site_name.replace("-", "").replace("_", "").lower()
            found = False

            for prop in ecosystem_properties:
                if normalized in prop.lower().replace("-", "").replace("_", ""):
                    found = True
                    break

            if not found and not self.sites[site_name].get("has_readme"):
                missing_docs.append(site_name)

        self.missing_docs = missing_docs

        if missing_docs:
            print(f"  ⚠️  {len(missing_docs)} sites missing documentation:")
            for site in missing_docs[:10]:
                print(f"     • {site}")
        else:
            print("  ✅ All sites have documentation")

    def get_dir_size(self, path):
        """Get directory size in MB"""
        total = 0
        try:
            for entry in path.rglob("*"):
                if entry.is_file():
                    total += entry.stat().st_size
        except:
            pass
        return round(total / (1024 * 1024), 2)

    def generate_master_index(self):
        """Generate comprehensive master index"""
        print("\n📊 Generating master index...")

        index = {
            "sites": self.sites,
            "ecosystem_docs": self.plans.get("ecosystem", {}),
            "python_docs": self.plans.get("python_docs", []),
            "duplicates": {k: v for k, v in list(self.duplicates.items())[:10]},
            "missing_docs": self.missing_docs,
        }

        # Save to file
        output_file = self.ecosystem_dir / "MASTER_SITES_INDEX.json"
        with open(output_file, "w") as f:
            json.dump(index, f, indent=2)

        print(f"  ✅ Index saved to: {output_file}")

        # Generate markdown report
        self.generate_markdown_report(index)

    def generate_markdown_report(self, index):
        """Generate human-readable markdown report"""
        report_file = self.ecosystem_dir / "MASTER_SITES_REPORT.md"

        from datetime import datetime

        with open(report_file, "w") as f:
            f.write("# 🏗️ MASTER SITES & DOCUMENTATION CONSOLIDATION\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write("---\n\n")

            # Sites section
            f.write("## 📁 AI SITES INVENTORY\n\n")
            f.write(f"**Total Sites:** {len(self.sites)}\n\n")

            # Sort by size
            sorted_sites = sorted(
                self.sites.items(), key=lambda x: x[1]["size"], reverse=True
            )

            f.write("### Top Sites by Size\n\n")
            f.write("| Site | Size (MB) | Files | Status |\n")
            f.write("|------|-----------|-------|--------|\n")
            for name, info in sorted_sites[:15]:
                status = "✅" if info.get("has_readme") else "⚠️"
                f.write(
                    f"| {name} | {info['size']} | {info['file_count']} | {status} |\n"
                )

            # Documentation section
            f.write("\n## 📚 DOCUMENTATION INVENTORY\n\n")

            ecosystem_docs = index.get("ecosystem_docs", {})
            f.write(
                f"**ECOSYSTEM Docs:** {sum(len(docs) for docs in ecosystem_docs.values())} files\n\n"
            )
            for category, docs in ecosystem_docs.items():
                f.write(f"- **{category}:** {len(docs)} files\n")

            python_docs = index.get("python_docs", [])
            f.write(f"\n**Python Docs:** {len(python_docs)} planning documents\n\n")

            # Duplicates section
            if self.duplicates:
                f.write("\n## 🔄 DUPLICATE DOCUMENTS\n\n")
                f.write(f"**Found:** {len(self.duplicates)} duplicate sets\n\n")
                for i, (hash_val, paths) in enumerate(
                    list(self.duplicates.items())[:5], 1
                ):
                    f.write(f"\n### Duplicate Set {i}\n\n")
                    for path in paths:
                        f.write(f"- `{Path(path).name}`\n")

            # Missing docs section
            if self.missing_docs:
                f.write("\n## ⚠️ SITES MISSING DOCUMENTATION\n\n")
                for site in self.missing_docs[:20]:
                    f.write(f"- [ ] {site}\n")

            f.write("\n---\n\n")
            f.write("## 💡 RECOMMENDATIONS\n\n")
            f.write("1. Create documentation for sites missing README\n")
            f.write("2. Consolidate duplicate documentation\n")
            f.write("3. Archive inactive projects\n")
            f.write("4. Update ECOSYSTEM status for all active sites\n")

        print(f"  ✅ Report saved to: {report_file}")


def main():
    print("=" * 70)
    print("🏗️  MASTER SITES & DOCUMENTATION CONSOLIDATOR")
    print("=" * 70)
    print()

    consolidator = SitesConsolidator()

    # Run all scans
    consolidator.scan_ai_sites()
    consolidator.scan_ecosystem_docs()
    consolidator.scan_python_docs()
    consolidator.find_duplicate_docs()
    consolidator.check_site_documentation()
    consolidator.generate_master_index()

    print("\n" + "=" * 70)
    print("✅ CONSOLIDATION COMPLETE")
    print("=" * 70)
    print()
    print("📋 Check these files for full details:")
    print("  • ~/ECOSYSTEM/MASTER_SITES_INDEX.json")
    print("  • ~/ECOSYSTEM/MASTER_SITES_REPORT.md")
    print()


if __name__ == "__main__":
    main()
