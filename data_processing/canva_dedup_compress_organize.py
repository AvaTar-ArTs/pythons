#!/usr/bin/env python3
"""
Canva Archive Deduplication, Compression & Organization Tool
============================================================

This script performs three main operations:
1. DEDUPLICATION: Find and remove duplicate files across archives
2. COMPRESSION: Recompress archives using 7zip for better ratios
3. ORGANIZATION: Organize files by size and content type

Usage: python3 canva_dedup_compress_organize.py [options]
"""

import sys
import zipfile
import hashlib
import shutil
import subprocess
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("canva_processing.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class CanvaArchiveProcessor:
    def __init__(self, source_dir, output_dir, temp_dir=None):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir) if temp_dir else Path("/tmp/canva_processing")

        # Create directories
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # File tracking
        self.file_hashes = defaultdict(list)  # hash -> [(archive, file_path, size)]
        self.archive_contents = {}  # archive -> {files: [], total_size: int}
        self.duplicates = {}  # hash -> list of duplicate files
        self.stats = {
            "total_archives": 0,
            "total_files": 0,
            "duplicate_files": 0,
            "space_saved": 0,
            "compression_ratio": 0,
        }

        # Check for 7zip
        self.seven_zip_cmd = self._find_7zip()
        if not self.seven_zip_cmd:
            logger.warning("7zip not found. Will use Python's zipfile for compression.")

    def _find_7zip(self):
        """Find 7zip executable"""
        for cmd in ["7z", "7za"]:
            try:
                subprocess.run([cmd], capture_output=True, check=True)
                return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        return None

    def analyze_archives(self):
        """Analyze all archives to build file hash database"""
        logger.info("🔍 Analyzing archives for duplicates...")

        archives = list(self.source_dir.glob("*.zip"))
        self.stats["total_archives"] = len(archives)

        for i, archive_path in enumerate(archives, 1):
            logger.info(f"Processing archive {i}/{len(archives)}: {archive_path.name}")

            try:
                with zipfile.ZipFile(archive_path, "r") as zip_file:
                    archive_info = {"files": [], "total_size": 0, "file_count": 0}

                    for file_info in zip_file.filelist:
                        if file_info.file_size > 0:  # Skip directories and empty files
                            # Read file content and calculate hash
                            file_data = zip_file.read(file_info.filename)
                            file_hash = hashlib.md5(file_data).hexdigest()

                            # Store file info
                            file_entry = {
                                "archive": archive_path.name,
                                "file_path": file_info.filename,
                                "size": file_info.file_size,
                                "hash": file_hash,
                                "compressed_size": file_info.compress_size,
                            }

                            archive_info["files"].append(file_entry)
                            archive_info["total_size"] += file_info.file_size
                            archive_info["file_count"] += 1

                            # Add to global hash database
                            self.file_hashes[file_hash].append(file_entry)

                    self.archive_contents[archive_path.name] = archive_info
                    self.stats["total_files"] += archive_info["file_count"]

            except Exception as e:
                logger.error(f"Error processing {archive_path.name}: {e}")

        logger.info(
            f"✅ Analysis complete: {self.stats['total_files']} files processed"
        )

    def find_duplicates(self):
        """Identify duplicate files across archives"""
        logger.info("🔍 Finding duplicate files...")

        for file_hash, file_entries in self.file_hashes.items():
            if len(file_entries) > 1:
                # Sort by size (keep largest) and then by archive name
                file_entries.sort(key=lambda x: (-x["size"], x["archive"]))

                # Keep the first (largest) file, mark others as duplicates
                keep_file = file_entries[0]
                duplicates = file_entries[1:]

                self.duplicates[file_hash] = {
                    "keep": keep_file,
                    "duplicates": duplicates,
                }

                self.stats["duplicate_files"] += len(duplicates)
                self.stats["space_saved"] += sum(dup["size"] for dup in duplicates)

        logger.info(f"✅ Found {len(self.duplicates)} sets of duplicates")
        logger.info(
            f"💾 Potential space savings: {self.stats['space_saved'] / (1024 * 1024):.1f} MB"
        )

    def create_deduplicated_archives(self):
        """Create new archives with duplicates removed"""
        logger.info("📦 Creating deduplicated archives...")

        # Create deduplication mapping
        file_keep_map = {}
        for file_hash, dup_info in self.duplicates.items():
            dup_info["keep"]
            for dup_file in dup_info["duplicates"]:
                file_keep_map[dup_file["archive"]] = file_keep_map.get(
                    dup_file["archive"], []
                )
                file_keep_map[dup_file["archive"]].append(dup_file["file_path"])

        # Process each original archive
        for archive_name, archive_info in self.archive_contents.items():
            original_archive = self.source_dir / archive_name
            dedup_archive = self.temp_dir / f"dedup_{archive_name}"

            logger.info(f"Creating deduplicated version: {archive_name}")

            try:
                with zipfile.ZipFile(original_archive, "r") as source_zip:
                    with zipfile.ZipFile(
                        dedup_archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9
                    ) as dest_zip:
                        files_to_skip = set(file_keep_map.get(archive_name, []))

                        for file_info in source_zip.filelist:
                            if (
                                file_info.filename not in files_to_skip
                                and file_info.file_size > 0
                            ):
                                # Copy file to new archive
                                file_data = source_zip.read(file_info.filename)
                                dest_zip.writestr(file_info, file_data)

                        logger.info(
                            f"✅ Deduplicated {archive_name}: {len(files_to_skip)} files removed"
                        )

            except Exception as e:
                logger.error(f"Error creating deduplicated archive {archive_name}: {e}")

    def compress_archives(self):
        """Recompress archives using 7zip for better compression"""
        logger.info("🗜️ Recompressing archives with 7zip...")

        if not self.seven_zip_cmd:
            logger.warning("7zip not available, skipping recompression")
            return

        dedup_archives = list(self.temp_dir.glob("dedup_*.zip"))

        for i, archive_path in enumerate(dedup_archives, 1):
            logger.info(f"Recompressing {i}/{len(dedup_archives)}: {archive_path.name}")

            # Extract to temporary directory
            extract_dir = self.temp_dir / f"extract_{archive_path.stem}"
            extract_dir.mkdir(exist_ok=True)

            try:
                # Extract archive
                with zipfile.ZipFile(archive_path, "r") as zip_file:
                    zip_file.extractall(extract_dir)

                # Recompress with 7zip
                compressed_archive = (
                    self.temp_dir
                    / f"compressed_{archive_path.name.replace('.zip', '.7z')}"
                )
                cmd = [
                    self.seven_zip_cmd,
                    "a",
                    "-t7z",
                    "-mx9",
                    "-m0=lzma2",
                    str(compressed_archive),
                    str(extract_dir / "*"),
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    # Calculate compression ratio
                    original_size = archive_path.stat().st_size
                    compressed_size = compressed_archive.stat().st_size
                    ratio = (1 - compressed_size / original_size) * 100

                    logger.info(f"✅ Compressed {archive_name}: {ratio:.1f}% reduction")

                    # Clean up extraction directory
                    shutil.rmtree(extract_dir)
                else:
                    logger.error(f"7zip compression failed: {result.stderr}")

            except Exception as e:
                logger.error(f"Error compressing {archive_path.name}: {e}")

    def organize_archives(self):
        """Organize archives by size and content type"""
        logger.info("📁 Organizing archives by size and content...")

        # Create organization structure
        org_structure = {
            "Large_Archives": self.output_dir / "Large_Archives",  # > 1GB
            "Medium_Archives": self.output_dir / "Medium_Archives",  # 50MB - 1GB
            "Small_Archives": self.output_dir / "Small_Archives",  # < 50MB
            "Resources": self.output_dir / "Resources",  # Resource packs
            "Deduplicated": self.output_dir / "Deduplicated",  # Deduplicated versions
            "Compressed": self.output_dir / "Compressed",  # 7zip compressed versions
        }

        for category_dir in org_structure.values():
            category_dir.mkdir(exist_ok=True)

        # Organize original archives
        for archive_path in self.source_dir.glob("*.zip"):
            size_mb = archive_path.stat().st_size / (1024 * 1024)

            if "Glitch-Arts" in archive_path.name:
                target_dir = org_structure["Resources"]
            elif size_mb > 1000:
                target_dir = org_structure["Large_Archives"]
            elif size_mb > 50:
                target_dir = org_structure["Medium_Archives"]
            else:
                target_dir = org_structure["Small_Archives"]

            # Copy to organized location
            dest_path = target_dir / archive_path.name
            shutil.copy2(archive_path, dest_path)
            logger.info(f"📁 Organized {archive_path.name} -> {target_dir.name}")

        # Move deduplicated archives
        for dedup_archive in self.temp_dir.glob("dedup_*.zip"):
            dest_path = org_structure["Deduplicated"] / dedup_archive.name
            shutil.move(str(dedup_archive), str(dest_path))
            logger.info(f"📁 Moved deduplicated {dedup_archive.name}")

        # Move compressed archives
        for comp_archive in self.temp_dir.glob("compressed_*.7z"):
            dest_path = org_structure["Compressed"] / comp_archive.name
            shutil.move(str(comp_archive), str(dest_path))
            logger.info(f"📁 Moved compressed {comp_archive.name}")

    def generate_reports(self):
        """Generate detailed reports"""
        logger.info("📊 Generating reports...")

        # Create summary report
        report_path = self.output_dir / "PROCESSING_REPORT.md"
        with open(report_path, "w") as f:
            f.write("# Canva Archive Processing Report\n\n")
            f.write(
                f"**Processing Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write(f"**Source Directory:** {self.source_dir}\n")
            f.write(f"**Output Directory:** {self.output_dir}\n\n")

            f.write("## Statistics\n\n")
            f.write(f"- **Total Archives Processed:** {self.stats['total_archives']}\n")
            f.write(f"- **Total Files Analyzed:** {self.stats['total_files']}\n")
            f.write(f"- **Duplicate Files Found:** {self.stats['duplicate_files']}\n")
            f.write(
                f"- **Space Saved:** {self.stats['space_saved'] / (1024 * 1024):.1f} MB\n"
            )
            f.write(
                f"- **Compression Ratio:** {self.stats['compression_ratio']:.1f}%\n\n"
            )

            f.write("## Duplicate Files\n\n")
            for file_hash, dup_info in self.duplicates.items():
                f.write(f"### Hash: {file_hash[:16]}...\n")
                f.write(
                    f"- **Keep:** {dup_info['keep']['archive']} - {dup_info['keep']['file_path']}\n"
                )
                f.write("- **Duplicates:**\n")
                for dup in dup_info["duplicates"]:
                    f.write(f"  - {dup['archive']} - {dup['file_path']}\n")
                f.write("\n")

        # Create CSV inventory
        csv_path = self.output_dir / "ARCHIVE_INVENTORY.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Archive", "File_Path", "Size_Bytes", "Hash", "Is_Duplicate"]
            )

            for archive_name, archive_info in self.archive_contents.items():
                for file_info in archive_info["files"]:
                    is_duplicate = file_info["file_path"] in [
                        dup["file_path"]
                        for dup in self.duplicates.get(file_info["hash"], {}).get(
                            "duplicates", []
                        )
                    ]
                    writer.writerow(
                        [
                            archive_name,
                            file_info["file_path"],
                            file_info["size"],
                            file_info["hash"],
                            is_duplicate,
                        ]
                    )

        logger.info(f"📊 Reports generated: {report_path} and {csv_path}")

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        logger.info("🧹 Cleaning up temporary files...")
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("✅ Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Could not clean up temp directory: {e}")

    def process_all(self):
        """Run the complete processing pipeline"""
        logger.info("🚀 Starting Canva Archive Processing Pipeline")
        logger.info("=" * 60)

        try:
            # Step 1: Analyze archives
            self.analyze_archives()

            # Step 2: Find duplicates
            self.find_duplicates()

            # Step 3: Create deduplicated archives
            self.create_deduplicated_archives()

            # Step 4: Compress archives
            self.compress_archives()

            # Step 5: Organize archives
            self.organize_archives()

            # Step 6: Generate reports
            self.generate_reports()

            # Step 7: Cleanup
            self.cleanup_temp_files()

            logger.info("=" * 60)
            logger.info("🎉 Processing complete!")
            logger.info(f"📁 Output directory: {self.output_dir}")
            logger.info(
                f"💾 Space saved: {self.stats['space_saved'] / (1024 * 1024):.1f} MB"
            )

        except Exception as e:
            logger.error(f"❌ Processing failed: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Canva Archive Deduplication, Compression & Organization"
    )
    parser.add_argument(
        "--source",
        default="/Volumes/2T-Xx/AvaTarArTs/canva/Compressed",
        help="Source directory containing Canva archives",
    )
    parser.add_argument(
        "--output",
        default="/Volumes/2T-Xx/AvaTarArTs/canva/Compressed_Processed",
        help="Output directory for processed archives",
    )
    parser.add_argument(
        "--temp",
        default="/tmp/canva_processing",
        help="Temporary directory for processing",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually processing",
    )

    args = parser.parse_args()

    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - Analyzing what would be processed")
        processor = CanvaArchiveProcessor(args.source, args.output, args.temp)
        processor.analyze_archives()
        processor.find_duplicates()
        logger.info(f"Would process {processor.stats['total_archives']} archives")
        logger.info(f"Would find {len(processor.duplicates)} duplicate file sets")
        logger.info(
            f"Would save {processor.stats['space_saved'] / (1024 * 1024):.1f} MB"
        )
        return

    # Validate source directory
    if not Path(args.source).exists():
        logger.error(f"Source directory does not exist: {args.source}")
        sys.exit(1)

    # Create processor and run
    processor = CanvaArchiveProcessor(args.source, args.output, args.temp)
    processor.process_all()


if __name__ == "__main__":
    main()
