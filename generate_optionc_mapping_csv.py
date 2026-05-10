#!/usr/bin/env python3
"""
Generate Option C-style before/after mapping CSV for AVATARARTS.

Creates a reviewable CSV with current_path -> proposed_path,
depths, file counts, sizes, and change type.
"""

import csv
from pathlib import Path
from typing import Tuple, Optional

ROOT = Path("/Users/steven/AVATARARTS")
OUTPUT = ROOT / "ACTIVE" / "OPTION_C_BEFORE_AFTER.csv"

EXCLUDE_PREFIXES = {".git", ".github", ".history", ".vscode", ".idea"}


def count_files_and_size(path: Path) -> Tuple[int, float]:
    files = 0
    size_bytes = 0
    try:
        for item in path.rglob("*"):
            if item.is_file():
                files += 1
                try:
                    size_bytes += item.stat().st_size
                except OSError:
                    pass
    except OSError:
        pass
    size_mb = round(size_bytes / (1024 * 1024), 2)
    return files, size_mb


def proposed_path_for(rel_path: Path) -> Tuple[str, str]:
    """
    Return (proposed_path, rationale).
    Use Option C style with flexibility where it improves clarity.
    """
    parts = rel_path.parts
    if not parts:
        return (str(rel_path), "root")

    top = parts[0]

    # Keep system folders as-is
    if top in EXCLUDE_PREFIXES:
        return (str(rel_path), "system")

    # ACTIVE -> content/documentation/analysis/ACTIVE
    if top == "ACTIVE":
        return ("content/documentation/analysis/ACTIVE", "analysis_docs")

    # docs -> content/documentation/docs
    if top == "docs":
        return ("content/documentation/docs", "documentation")

    # assets -> content/assets (or keep if already under content)
    if top == "assets":
        return ("content/assets", "shared_assets")

    # data mapping
    if top == "data":
        if len(parts) > 1:
            if parts[1] == "master-databases":
                return ("data/databases", "databases")
            if parts[1] == "processing_scripts":
                return ("data/processing", "data_processing")
        return ("data", "data_root")

    # business mapping
    if top == "business":
        if len(parts) == 1:
            return ("business", "business_root")
        second = parts[1]
        if second == "enterprise":
            return ("business/platforms/enterprise", "enterprise_platforms")
        if second == "content_tools":
            return ("business/tools/content-tools", "business_tools")
        if second == "monetization":
            return ("business/revenue/monetization", "revenue")
        if second == "active":
            return ("business/marketing/active", "marketing_active")
        return (f"business/{second}", "business_subcategory")

    # development mapping
    if top == "development":
        if len(parts) == 1:
            return ("development", "development_root")
        second = parts[1]
        if second == "ecosystem":
            return ("development/tools/ecosystem", "development_tools")
        if second == "scripts":
            return ("development/tools/scripts", "development_tools")
        return (f"development/{second}", "development_subcategory")

    # consolidated mapping
    if top == "consolidated":
        if len(parts) > 1 and parts[1] == "utilities":
            return ("development/tools/utilities", "utilities")
        return ("development/tools/consolidated", "consolidated_tools")

    # consolidation mapping (archive)
    if top == "consolidation":
        return ("archives/migration-staging/consolidation", "archive_migration")

    # super-flat mapping
    if top == "super-flat":
        if len(parts) > 1 and parts[1] == "active":
            if len(parts) > 2:
                name = parts[2].lower()
                if "heavenlyhands" in name:
                    return ("business/websites/heavenlyHands", "website_project")
                if "steven-chaplinski" in name:
                    return ("business/websites/steven-chaplinski", "website_project")
                if "portfolio" in name:
                    return ("business/websites/portfolio-builder", "website_project")
                if "creative-ai-agency" in name:
                    return ("business/products/creative-ai-agency", "product")
                if "creative-ai-marketplace" in name:
                    return ("business/products/creative-ai-marketplace", "product")
                if "retention" in name:
                    return ("business/products/retention-suite", "product")
                if "monetization" in name or "revenue" in name:
                    return ("business/revenue", "revenue")
                if "seo" in name:
                    return ("business/seo", "seo")
                if "marketing" in name:
                    return ("business/marketing", "marketing")
                if "automation" in name or "n8n" in name:
                    return ("development/automations", "automation")
                if "ai" in name or "ml" in name:
                    return ("development/tools/ai-tools", "ai_tools")
                if "gallery" in name or "assets" in name:
                    return ("content/assets/galleries", "assets")
                if "docs" in name or "report" in name:
                    return ("content/documentation/reports", "documentation")
            return ("content/creative/super-flat", "review_needed")
        return ("archives/migration-staging/super-flat", "archive_super_flat")

    # content mapping (if already)
    if top == "content":
        return (str(rel_path), "content_root")

    # archives mapping
    if top == "archives":
        return (str(rel_path), "archives_root")

    # default: keep
    return (str(rel_path), "keep_default")


def main() -> None:
    if not ROOT.exists():
        raise SystemExit(f"Root not found: {ROOT}")

    rows = []
    for path in ROOT.rglob("*"):
        if not path.is_dir():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts and rel.parts[0] in EXCLUDE_PREFIXES:
            continue

        current_path = str(rel)
        proposed_path, rationale = proposed_path_for(rel)

        current_depth = len(rel.parts)
        proposed_depth = len(Path(proposed_path).parts) if proposed_path else current_depth

        files, size_mb = count_files_and_size(path)

        if proposed_path == current_path:
            change_type = "KEEP"
        elif proposed_path.startswith("archives/"):
            change_type = "ARCHIVE"
        elif rationale in {"review_needed"}:
            change_type = "REVIEW"
        else:
            change_type = "MOVE"

        rows.append({
            "current_path": current_path,
            "proposed_path": proposed_path,
            "current_depth": current_depth,
            "proposed_depth": proposed_depth,
            "files": files,
            "size_mb": size_mb,
            "change_type": change_type,
            "rationale": rationale,
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "current_path",
                "proposed_path",
                "current_depth",
                "proposed_depth",
                "files",
                "size_mb",
                "change_type",
                "rationale",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ CSV generated: {OUTPUT}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
