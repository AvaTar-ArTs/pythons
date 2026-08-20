#!/usr/bin/env python3
"""ZIP Archive Analyzer and Cleanup Tool
Analyzes ZIP files in the Etsy collection for optimization opportunities
"""

import os
import zipfile
import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import re


class ZipArchiveAnalyzer:
    def __init__(self, etsy_dir=None):
        self.etsy_dir = Path(etsy_dir or os.path.expanduser("~/Pictures/etsy"))
        self.zip_dir = self.etsy_dir / "02_zip_archives"
        self.analysis_dir = self.etsy_dir / "00_archives" / "zip_analysis"
        self.analysis_dir.mkdir(parents=True, exist_ok=True)

        # Categories for extracted content
        self.extract_categories = {
            "00_production_ready": "High-quality, ready-to-use designs",
            "01_ideogram_designs": "AI-generated designs from Ideogram",
            "02_halloween_designs": "Halloween and spooky themed designs",
            "03_raccoon_designs": "Raccoon and trash panda designs",
            "04_funny_quotes": "Humorous text and quote designs",
            "05_animal_designs": "Cute animal themed designs",
            "06_holiday_designs": "Holiday and seasonal designs",
            "07_mockups_templates": "Design templates and mockups",
            "08_duplicates": "Duplicate files found in archives",
            "09_archived": "Old or low-quality designs",
        }

        # Create extraction directories
        for category in self.extract_categories.keys():
            (self.etsy_dir / category).mkdir(exist_ok=True)

    def analyze_zip_file(self, zip_path):
        """Analyze a single ZIP file and return detailed information"""
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                file_list = zip_file.namelist()

                # Basic statistics
                total_files = len(file_list)
                total_size = sum(info.file_size for info in zip_file.infolist())

                # File type analysis
                file_types = {}
                for file_name in file_list:
                    ext = Path(file_name).suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1

                # Content analysis
                content_analysis = self.analyze_zip_content(file_list)

                # Duplicate detection within ZIP
                duplicates_in_zip = self.find_duplicates_in_zip(zip_file)

                return {
                    "zip_name": zip_path.name,
                    "zip_size": zip_path.stat().st_size,
                    "total_files": total_files,
                    "total_uncompressed_size": total_size,
                    "compression_ratio": (
                        round((1 - zip_path.stat().st_size / total_size) * 100, 2)
                        if total_size > 0
                        else 0
                    ),
                    "file_types": file_types,
                    "content_analysis": content_analysis,
                    "duplicates_in_zip": duplicates_in_zip,
                    "extraction_recommendation": self.get_extraction_recommendation(
                        content_analysis, total_size,
                    ),
                }

        except Exception as e:
            return {
                "zip_name": zip_path.name,
                "error": str(e),
                "extraction_recommendation": "skip",
            }

    def analyze_zip_content(self, file_list):
        """Analyze the content of files in a ZIP to determine category"""
        all_names = " ".join(file_list).lower()

        # Count different design types
        analysis = {
            "halloween_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower()
                        for kw in ["halloween", "spooky", "skeleton", "ghost", "witch"]
                    )
                ],
            ),
            "raccoon_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower()
                        for kw in ["raccoon", "racoon", "trash", "panda"]
                    )
                ],
            ),
            "funny_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower()
                        for kw in ["funny", "quote", "sarcastic", "pun", "joke"]
                    )
                ],
            ),
            "animal_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower()
                        for kw in ["cat", "dog", "animal", "pet", "cute"]
                    )
                ],
            ),
            "holiday_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower()
                        for kw in [
                            "christmas",
                            "valentine",
                            "easter",
                            "thanksgiving",
                            "holiday",
                        ]
                    )
                ],
            ),
            "tshirt_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower()
                        for kw in ["tshirt", "t-shirt", "shirt", "apparel"]
                    )
                ],
            ),
            "mockup_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower() for kw in ["mockup", "template", "psd", "svg"]
                    )
                ],
            ),
            "ideogram_keywords": len(
                [
                    f
                    for f in file_list
                    if any(
                        kw in f.lower() for kw in ["ideo", "ideogram", "ai-generated"]
                    )
                ],
            ),
            "png_count": len([f for f in file_list if f.lower().endswith(".png")]),
            "jpg_count": len(
                [f for f in file_list if f.lower().endswith((".jpg", ".jpeg"))],
            ),
            "svg_count": len([f for f in file_list if f.lower().endswith(".svg")]),
            "psd_count": len([f for f in file_list if f.lower().endswith(".psd")]),
            "zip_count": len([f for f in file_list if f.lower().endswith(".zip")]),
        }

        # Determine primary category
        category_scores = {
            "halloween": analysis["halloween_keywords"],
            "raccoon": analysis["raccoon_keywords"],
            "funny": analysis["funny_keywords"],
            "animal": analysis["animal_keywords"],
            "holiday": analysis["holiday_keywords"],
            "tshirt": analysis["tshirt_keywords"],
            "mockup": analysis["mockup_keywords"],
            "ideogram": analysis["ideogram_keywords"],
        }

        primary_category = (
            max(category_scores, key=category_scores.get)
            if max(category_scores.values()) > 0
            else "archived"
        )

        return {
            **analysis,
            "primary_category": primary_category,
            "category_score": max(category_scores.values()),
        }

    def find_duplicates_in_zip(self, zip_file):
        """Find duplicate files within a ZIP archive"""
        file_hashes = {}
        duplicates = []

        for file_info in zip_file.infolist():
            if not file_info.is_dir():
                try:
                    file_data = zip_file.read(file_info.filename)
                    file_hash = hashlib.md5(file_data).hexdigest()

                    if file_hash in file_hashes:
                        duplicates.append(
                            {
                                "file1": file_hashes[file_hash],
                                "file2": file_info.filename,
                                "size": file_info.file_size,
                            },
                        )
                    else:
                        file_hashes[file_hash] = file_info.filename
                except:
                    continue

        return duplicates

    def get_extraction_recommendation(self, content_analysis, total_size):
        """Determine if a ZIP should be extracted, kept as-is, or deleted"""
        # Large files with good content should be extracted
        if total_size > 50 * 1024 * 1024:  # 50MB
            if content_analysis["category_score"] > 5:
                return "extract"
            if content_analysis["category_score"] > 2:
                return "extract_partial"

        # Medium files with specific content
        elif total_size > 10 * 1024 * 1024:  # 10MB
            if content_analysis["category_score"] > 3 or content_analysis["png_count"] + content_analysis["jpg_count"] > 20:
                return "extract"

        # Small files
        elif total_size > 1 * 1024 * 1024:  # 1MB
            if content_analysis["category_score"] > 1:
                return "extract"

        # Very small files
        elif content_analysis["category_score"] > 0:
            return "extract"
        else:
            return "keep_zipped"

    def extract_zip_file(self, zip_path, analysis):
        """Extract a ZIP file to appropriate categories"""
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                extracted_files = []
                skipped_files = []

                for file_info in zip_file.infolist():
                    if file_info.is_dir():
                        continue

                    # Determine target category
                    target_category = self.determine_file_category(
                        file_info.filename, analysis["content_analysis"],
                    )
                    target_dir = self.etsy_dir / target_category

                    # Create subdirectory for this ZIP
                    zip_subdir = target_dir / zip_path.stem
                    zip_subdir.mkdir(exist_ok=True)

                    # Extract file
                    try:
                        zip_file.extract(file_info, zip_subdir)
                        extracted_files.append(
                            {
                                "file": file_info.filename,
                                "category": target_category,
                                "size": file_info.file_size,
                            },
                        )
                    except Exception as e:
                        skipped_files.append(
                            {"file": file_info.filename, "error": str(e)},
                        )

                return {
                    "extracted_files": extracted_files,
                    "skipped_files": skipped_files,
                    "total_extracted": len(extracted_files),
                }

        except Exception as e:
            return {"error": str(e), "extracted_files": [], "skipped_files": []}

    def determine_file_category(self, filename, content_analysis):
        """Determine which category a file should go to"""
        filename_lower = filename.lower()

        # Check for specific keywords
        if any(
            kw in filename_lower for kw in ["halloween", "spooky", "skeleton", "ghost"]
        ):
            return "02_halloween_designs"
        if any(
            kw in filename_lower for kw in ["raccoon", "racoon", "trash", "panda"]
        ):
            return "03_raccoon_designs"
        if any(kw in filename_lower for kw in ["funny", "quote", "sarcastic", "pun"]):
            return "04_funny_quotes"
        if any(
            kw in filename_lower for kw in ["cat", "dog", "animal", "pet", "cute"]
        ):
            return "05_animal_designs"
        if any(
            kw in filename_lower
            for kw in ["christmas", "valentine", "easter", "holiday"]
        ):
            return "06_holiday_designs"
        if any(
            kw in filename_lower for kw in ["tshirt", "t-shirt", "shirt", "apparel"]
        ):
            return "00_production_ready"
        if any(kw in filename_lower for kw in ["mockup", "template", "psd", "svg"]):
            return "07_mockups_templates"
        if any(kw in filename_lower for kw in ["ideo", "ideogram", "ai-generated"]):
            return "01_ideogram_designs"
        # Use primary category from content analysis
        category_map = {
            "halloween": "02_halloween_designs",
            "raccoon": "03_raccoon_designs",
            "funny": "04_funny_quotes",
            "animal": "05_animal_designs",
            "holiday": "06_holiday_designs",
            "tshirt": "00_production_ready",
            "mockup": "07_mockups_templates",
            "ideogram": "01_ideogram_designs",
        }
        return category_map.get(content_analysis["primary_category"], "09_archived")

    def analyze_all_zips(self):
        """Analyze all ZIP files in the archive directory"""
        print("🔍 Analyzing ZIP Archives")
        print("=" * 50)

        zip_files = list(self.zip_dir.glob("*.zip"))
        print(f"📦 Found {len(zip_files)} ZIP files to analyze")

        analysis_results = []
        total_zip_size = 0
        total_uncompressed_size = 0

        for zip_file in zip_files:
            print(f"  🔍 Analyzing {zip_file.name}...")
            analysis = self.analyze_zip_file(zip_file)
            analysis_results.append(analysis)

            if "error" not in analysis:
                total_zip_size += analysis["zip_size"]
                total_uncompressed_size += analysis["total_uncompressed_size"]

        # Generate summary
        summary = {
            "total_zips": len(zip_files),
            "total_zip_size": total_zip_size,
            "total_uncompressed_size": total_uncompressed_size,
            "average_compression": (
                round((1 - total_zip_size / total_uncompressed_size) * 100, 2)
                if total_uncompressed_size > 0
                else 0
            ),
            "extraction_recommendations": {
                "extract": len(
                    [
                        a
                        for a in analysis_results
                        if a.get("extraction_recommendation") == "extract"
                    ],
                ),
                "extract_partial": len(
                    [
                        a
                        for a in analysis_results
                        if a.get("extraction_recommendation") == "extract_partial"
                    ],
                ),
                "keep_zipped": len(
                    [
                        a
                        for a in analysis_results
                        if a.get("extraction_recommendation") == "keep_zipped"
                    ],
                ),
                "skip": len(
                    [
                        a
                        for a in analysis_results
                        if a.get("extraction_recommendation") == "skip"
                    ],
                ),
            },
        }

        # Save detailed analysis
        analysis_file = (
            self.analysis_dir
            / f"zip_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(analysis_file, "w") as f:
            json.dump(
                {"summary": summary, "detailed_analysis": analysis_results}, f, indent=2,
            )

        print("\n📊 Analysis Complete!")
        print(f"📦 Total ZIP files: {summary['total_zips']}")
        print(f"💾 Total ZIP size: {self.format_size(summary['total_zip_size'])}")
        print(
            f"📁 Total uncompressed size: {self.format_size(summary['total_uncompressed_size'])}",
        )
        print(f"🗜️  Average compression: {summary['average_compression']}%")
        print(f"📋 Analysis saved to: {analysis_file}")

        return analysis_results, summary

    def format_size(self, size_bytes):
        """Format size in human readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def extract_recommended_zips(self, analysis_results):
        """Extract ZIP files based on recommendations"""
        print("\n📤 Extracting Recommended ZIP Files")
        print("=" * 50)

        extraction_stats = {
            "total_extracted": 0,
            "total_files": 0,
            "total_size": 0,
            "errors": 0,
        }

        for analysis in analysis_results:
            if analysis.get("extraction_recommendation") in [
                "extract",
                "extract_partial",
            ]:
                print(f"  📤 Extracting {analysis['zip_name']}...")

                zip_path = self.zip_dir / analysis["zip_name"]
                extraction_result = self.extract_zip_file(zip_path, analysis)

                if "error" not in extraction_result:
                    extraction_stats["total_extracted"] += 1
                    extraction_stats["total_files"] += extraction_result[
                        "total_extracted"
                    ]
                    print(
                        f"    ✅ Extracted {extraction_result['total_extracted']} files",
                    )
                else:
                    extraction_stats["errors"] += 1
                    print(f"    ❌ Error: {extraction_result['error']}")

        print("\n📊 Extraction Complete!")
        print(f"📦 ZIPs extracted: {extraction_stats['total_extracted']}")
        print(f"📁 Total files extracted: {extraction_stats['total_files']}")
        print(f"❌ Errors: {extraction_stats['errors']}")

        return extraction_stats


if __name__ == "__main__":
    analyzer = ZipArchiveAnalyzer()
    analysis_results, summary = analyzer.analyze_all_zips()

    print("\n🎯 Extraction Recommendations:")
    print(f"  📤 Extract: {summary['extraction_recommendations']['extract']} ZIPs")
    print(
        f"  📤 Extract Partial: {summary['extraction_recommendations']['extract_partial']} ZIPs",
    )
    print(
        f"  📦 Keep Zipped: {summary['extraction_recommendations']['keep_zipped']} ZIPs",
    )
    print(f"  ⏭️  Skip: {summary['extraction_recommendations']['skip']} ZIPs")
