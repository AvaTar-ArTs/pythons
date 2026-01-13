#!/usr/bin/env python3
"""
⚡ QUICK DUPLICATE SCAN
Fast scan to identify duplicates for the content-aware merger
"""

import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def quick_scan():
    base_path = Path("/Users/steven/tehSiTes/New_Folder_With_Items_3_ORGANIZED")

    results = {
        "documents": {"duplicates": [], "stats": {}},
        "html_files": {"duplicates": [], "stats": {}},
        "images": {"duplicates": [], "stats": {}},
        "summary": {},
    }

    # Quick image scan
    print("📸 Quick image scan...")
    images_path = base_path / "images"
    if images_path.exists():
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
        image_files = []

        for ext in image_extensions:
            image_files.extend(list(images_path.glob(f"*{ext}")))
            image_files.extend(list(images_path.glob(f"*{ext.upper()}")))

        hash_to_files = defaultdict(list)

        for i, filepath in enumerate(image_files[:1000]):  # Limit for speed
            if i % 100 == 0:
                print(f"   Processed {i} images...")

            try:
                with open(filepath, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()

                hash_to_files[file_hash].append(
                    {
                        "path": str(filepath),
                        "name": filepath.name,
                        "size": filepath.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            filepath.stat().st_mtime
                        ).isoformat(),
                    }
                )
            except:
                continue

        # Find duplicates
        duplicate_groups = []
        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                duplicate_groups.append(
                    {
                        "hash": file_hash,
                        "count": len(files),
                        "size_each": files[0]["size"],
                        "total_wasted": files[0]["size"] * (len(files) - 1),
                        "files": files,
                    }
                )

        results["images"]["duplicates"] = sorted(
            duplicate_groups, key=lambda x: x["total_wasted"], reverse=True
        )
        results["images"]["stats"] = {
            "total_files": len(image_files),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_files": sum(
                len(group["files"]) - 1 for group in duplicate_groups
            ),
        }

    # Quick document scan
    print("📄 Quick document scan...")
    docs_path = base_path / "documents"
    if docs_path.exists():
        doc_files = list(docs_path.glob("*.txt")) + list(docs_path.glob("*.md"))

        content_hash_to_files = defaultdict(list)

        for i, filepath in enumerate(doc_files[:500]):  # Limit for speed
            if i % 50 == 0:
                print(f"   Processed {i} documents...")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Normalize content
                normalized = " ".join(content.lower().split())
                content_hash = hashlib.sha256(normalized.encode()).hexdigest()

                content_hash_to_files[content_hash].append(
                    {
                        "path": str(filepath),
                        "name": filepath.name,
                        "size": filepath.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            filepath.stat().st_mtime
                        ).isoformat(),
                    }
                )
            except:
                continue

        # Find duplicates
        duplicate_groups = []
        for content_hash, files in content_hash_to_files.items():
            if len(files) > 1:
                duplicate_groups.append(
                    {"hash": content_hash, "count": len(files), "files": files}
                )

        results["documents"]["duplicates"] = sorted(
            duplicate_groups, key=lambda x: x["count"], reverse=True
        )
        results["documents"]["stats"] = {
            "total_files": len(doc_files),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_files": sum(
                len(group["files"]) - 1 for group in duplicate_groups
            ),
        }

    # Quick HTML scan
    print("🌐 Quick HTML scan...")
    html_path = base_path / "html_files"
    if html_path.exists():
        html_files = list(html_path.glob("*.html"))

        content_hash_to_files = defaultdict(list)

        for i, filepath in enumerate(html_files[:300]):  # Limit for speed
            if i % 50 == 0:
                print(f"   Processed {i} HTML files...")

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Normalize content
                normalized = " ".join(content.lower().split())
                content_hash = hashlib.sha256(normalized.encode()).hexdigest()

                content_hash_to_files[content_hash].append(
                    {
                        "path": str(filepath),
                        "name": filepath.name,
                        "size": filepath.stat().st_size,
                        "modified": datetime.fromtimestamp(
                            filepath.stat().st_mtime
                        ).isoformat(),
                    }
                )
            except:
                continue

        # Find duplicates
        duplicate_groups = []
        for content_hash, files in content_hash_to_files.items():
            if len(files) > 1:
                duplicate_groups.append(
                    {"hash": content_hash, "count": len(files), "files": files}
                )

        results["html_files"]["duplicates"] = sorted(
            duplicate_groups, key=lambda x: x["count"], reverse=True
        )
        results["html_files"]["stats"] = {
            "total_files": len(html_files),
            "duplicate_groups": len(duplicate_groups),
            "duplicate_files": sum(
                len(group["files"]) - 1 for group in duplicate_groups
            ),
        }

    # Save results
    report_path = base_path / "DUPLICATE_ANALYSIS_REPORT.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Quick scan complete! Report saved to {report_path}")

    # Print summary
    total_duplicates = (
        results["images"]["stats"].get("duplicate_files", 0)
        + results["documents"]["stats"].get("duplicate_files", 0)
        + results["html_files"]["stats"].get("duplicate_files", 0)
    )

    print(f"\n📊 QUICK SCAN SUMMARY:")
    print(
        f"   📸 Images: {results['images']['stats'].get('duplicate_files', 0)} duplicates"
    )
    print(
        f"   📄 Documents: {results['documents']['stats'].get('duplicate_files', 0)} duplicates"
    )
    print(
        f"   🌐 HTML: {results['html_files']['stats'].get('duplicate_files', 0)} duplicates"
    )
    print(f"   🎯 Total: {total_duplicates} duplicate files found")


if __name__ == "__main__":
    quick_scan()
