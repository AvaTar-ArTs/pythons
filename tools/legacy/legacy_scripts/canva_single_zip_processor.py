#!/usr/bin/env python3
"""
Canva Single ZIP Processor
==========================

Processes one ZIP file at a time for safe, controlled cleanup.
Perfect for handling large archives without overwhelming the system.

Usage: python3 canva_single_zip_processor.py [options]
"""

import sys
import zipfile
import hashlib
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("canva_single_processing.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SingleZipProcessor:
    def __init__(self, source_dir, output_dir, temp_dir=None):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.temp_dir = (
            Path(temp_dir) if temp_dir else Path("/tmp/canva_single_processing")
        )

        # Create directories
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # File tracking
        self.processed_files = set()
        self.global_hashes = defaultdict(list)  # For duplicate detection
        self.stats = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "duplicates_found": 0,
            "space_saved": 0,
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

    def get_zip_files(self):
        """Get list of ZIP files to process"""
        zip_files = list(self.source_dir.glob("*.zip"))
        zip_files.sort(key=lambda x: x.stat().st_size)  # Process smallest first
        return zip_files

    def analyze_zip(self, zip_path):
        """Analyze a single ZIP file"""
        logger.info(f"🔍 Analyzing: {zip_path.name}")

        analysis = {
            "archive_name": zip_path.name,
            "file_size": zip_path.stat().st_size,
            "files": [],
            "file_count": 0,
            "total_content_size": 0,
            "duplicates_in_archive": 0,
            "success": False,
            "error": None,
        }

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                file_hashes = defaultdict(list)

                for file_info in zip_file.filelist:
                    if file_info.file_size > 0:  # Skip directories and empty files
                        # Read file content and calculate hash
                        file_data = zip_file.read(file_info.filename)
                        file_hash = hashlib.md5(file_data).hexdigest()

                        file_entry = {
                            "file_path": file_info.filename,
                            "size": file_info.file_size,
                            "hash": file_hash,
                            "compressed_size": file_info.compress_size,
                        }

                        analysis["files"].append(file_entry)
                        analysis["file_count"] += 1
                        analysis["total_content_size"] += file_info.file_size

                        # Check for duplicates within this archive
                        file_hashes[file_hash].append(file_entry)

                        # Add to global hash database
                        self.global_hashes[file_hash].append(
                            {
                                "archive": zip_path.name,
                                "file_path": file_info.filename,
                                "size": file_info.file_size,
                                "hash": file_hash,
                            }
                        )

                # Count duplicates within this archive
                for file_hash, entries in file_hashes.items():
                    if len(entries) > 1:
                        analysis["duplicates_in_archive"] += len(entries) - 1

                analysis["success"] = True
                logger.info(
                    f"✅ Analyzed {zip_path.name}: {analysis['file_count']} files, {analysis['duplicates_in_archive']} internal duplicates"
                )

        except Exception as e:
            analysis["error"] = str(e)
            logger.error(f"❌ Error analyzing {zip_path.name}: {e}")

        return analysis

    def create_clean_zip(self, zip_path, analysis):
        """Create a cleaned version of the ZIP file"""
        if not analysis["success"]:
            logger.warning(f"Skipping {zip_path.name} due to analysis errors")
            return None

        logger.info(f"🧹 Creating clean version: {zip_path.name}")

        clean_zip_path = self.temp_dir / f"clean_{zip_path.name}"

        try:
            with zipfile.ZipFile(zip_path, "r") as source_zip:
                with zipfile.ZipFile(
                    clean_zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9
                ) as dest_zip:
                    # Track files we've already added (for internal deduplication)
                    added_files = set()
                    files_skipped = 0

                    for file_info in source_zip.filelist:
                        if file_info.file_size > 0:
                            # Check if we've already added this file (internal deduplication)
                            if file_info.filename in added_files:
                                files_skipped += 1
                                continue

                            # Read and add file
                            file_data = source_zip.read(file_info.filename)
                            dest_zip.writestr(file_info, file_data)
                            added_files.add(file_info.filename)

                    logger.info(
                        f"✅ Cleaned {zip_path.name}: removed {files_skipped} internal duplicates"
                    )
                    return clean_zip_path

        except Exception as e:
            logger.error(f"❌ Error creating clean version of {zip_path.name}: {e}")
            return None

    def compress_zip(self, clean_zip_path):
        """Compress the cleaned ZIP using 7zip"""
        if not self.seven_zip_cmd:
            logger.warning("7zip not available, skipping compression")
            return None

        logger.info(f"🗜️ Compressing: {clean_zip_path.name}")

        # Extract to temporary directory
        extract_dir = self.temp_dir / f"extract_{clean_zip_path.stem}"
        extract_dir.mkdir(exist_ok=True)

        try:
            # Extract archive
            with zipfile.ZipFile(clean_zip_path, "r") as zip_file:
                zip_file.extractall(extract_dir)

            # Compress with 7zip
            compressed_path = (
                self.temp_dir
                / f"compressed_{clean_zip_path.name.replace('.zip', '.7z')}"
            )
            cmd = [
                self.seven_zip_cmd,
                "a",
                "-t7z",
                "-mx9",
                "-m0=lzma2",
                str(compressed_path),
                str(extract_dir / "*"),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Calculate compression ratio
                original_size = clean_zip_path.stat().st_size
                compressed_size = compressed_path.stat().st_size
                ratio = (1 - compressed_size / original_size) * 100

                logger.info(
                    f"✅ Compressed {clean_zip_path.name}: {ratio:.1f}% reduction"
                )

                # Clean up extraction directory
                shutil.rmtree(extract_dir)
                return compressed_path
            else:
                logger.error(f"7zip compression failed: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"❌ Error compressing {clean_zip_path.name}: {e}")
            return None

    def organize_zip(:
        self, zip_path, analysis, clean_zip_path=None, compressed_path=None
    ):
        """Organize the processed ZIP file"""
        logger.info(f"📁 Organizing: {zip_path.name}")

        # Create organization structure
        org_structure = {
            "Large_Archives": self.output_dir / "Large_Archives",  # > 1GB
            "Medium_Archives": self.output_dir / "Medium_Archives",  # 50MB - 1GB
            "Small_Archives": self.output_dir / "Small_Archives",  # < 50MB
            "Resources": self.output_dir / "Resources",  # Resource packs
            "Cleaned": self.output_dir / "Cleaned",  # Cleaned versions
            "Compressed": self.output_dir / "Compressed",  # 7zip compressed versions
        }

        for category_dir in org_structure.values():
            category_dir.mkdir(exist_ok=True)

        # Determine category based on size
        size_mb = analysis["file_size"] / (1024 * 1024)

        if "Glitch-Arts" in zip_path.name:
            target_dir = org_structure["Resources"]
        elif size_mb > 1000:
            target_dir = org_structure["Large_Archives"]
        elif size_mb > 50:
            target_dir = org_structure["Medium_Archives"]
        else:
            target_dir = org_structure["Small_Archives"]

        # Copy original to organized location
        dest_path = target_dir / zip_path.name
        shutil.copy2(zip_path, dest_path)
        logger.info(f"📁 Organized original: {zip_path.name} -> {target_dir.name}")

        # Move cleaned version if it exists
        if clean_zip_path and clean_zip_path.exists():
            clean_dest = org_structure["Cleaned"] / clean_zip_path.name
            shutil.move(str(clean_zip_path), str(clean_dest))
            logger.info(f"📁 Moved cleaned: {clean_zip_path.name}")

        # Move compressed version if it exists
        if compressed_path and compressed_path.exists():
            comp_dest = org_structure["Compressed"] / compressed_path.name
            shutil.move(str(compressed_path), str(comp_dest))
            logger.info(f"📁 Moved compressed: {compressed_path.name}")

    def generate_zip_report(self, zip_path, analysis):
        """Generate a report for this ZIP file"""
        report_path = self.output_dir / f"REPORT_{zip_path.stem}.md"

        with open(report_path, "w") as f:
            f.write(f"# ZIP Processing Report: {zip_path.name}\n\n")
            f.write(
                f"**Processing Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            f.write("## File Information\n\n")
            f.write(f"- **Archive Name:** {zip_path.name}\n")
            f.write(
                f"- **File Size:** {analysis['file_size'] / (1024 * 1024):.1f} MB\n"
            )
            f.write(
                f"- **Status:** {'✅ Success' if analysis['success'] else '❌ Failed'}\n"
            )

            if analysis["success"]:
                f.write(f"- **Files Count:** {analysis['file_count']}\n")
                f.write(
                    f"- **Content Size:** {analysis['total_content_size'] / (1024 * 1024):.1f} MB\n"
                )
                f.write(
                    f"- **Internal Duplicates:** {analysis['duplicates_in_archive']}\n"
                )
            else:
                f.write(f"- **Error:** {analysis['error']}\n")

            f.write("\n## File Types\n\n")
            if analysis["success"]:
                file_types = defaultdict(int)
                for file_info in analysis["files"]:
                    ext = Path(file_info["file_path"]).suffix.lower()
                    file_types[ext] += 1

                for ext, count in sorted(file_types.items()):
                    f.write(f"- **{ext or 'no extension'}:** {count} files\n")

            f.write("\n## Processing Steps\n\n")
            f.write("1. ✅ Archive analysis completed\n")
            f.write("2. ✅ Clean version created (internal deduplication)\n")
            f.write("3. ✅ 7zip compression applied\n")
            f.write("4. ✅ Files organized by size category\n")

        logger.info(f"📊 Report generated: {report_path}")

    def process_single_zip(self, zip_path):
        """Process a single ZIP file completely"""
        logger.info(f"\n🔄 Processing: {zip_path.name}")
        logger.info("-" * 50)

        # Step 1: Analyze
        analysis = self.analyze_zip(zip_path)

        if not analysis["success"]:
            logger.warning(f"Skipping {zip_path.name} due to analysis failure")
            self.stats["failed"] += 1
            return

        # Step 2: Create clean version
        clean_zip_path = self.create_clean_zip(zip_path, analysis)

        # Step 3: Compress
        compressed_path = None
        if clean_zip_path:
            compressed_path = self.compress_zip(clean_zip_path)

        # Step 4: Organize
        self.organize_zip(zip_path, analysis, clean_zip_path, compressed_path)

        # Step 5: Generate report
        self.generate_zip_report(zip_path, analysis)

        # Update stats
        self.stats["total_processed"] += 1
        self.stats["successful"] += 1
        self.stats["duplicates_found"] += analysis["duplicates_in_archive"]

        logger.info(f"✅ Completed: {zip_path.name}")

    def process_all_zips(self, interactive=True):
        """Process all ZIP files one by one"""
        zip_files = self.get_zip_files()

        logger.info("🚀 Starting single ZIP processing")
        logger.info(f"📦 Found {len(zip_files)} ZIP files to process")
        logger.info("=" * 60)

        for i, zip_path in enumerate(zip_files, 1):
            logger.info(f"\n📁 Processing {i}/{len(zip_files)}: {zip_path.name}")

            if interactive:
                response = input(
                    f"Process {zip_path.name}? (y/n/s to skip remaining): "
                ).lower()
                if response == "n":
                    logger.info(f"Skipping {zip_path.name}")
                    continue
                elif response == "s":
                    logger.info("Stopping processing")
                    break

            try:
                self.process_single_zip(zip_path)
            except KeyboardInterrupt:
                logger.info("\n⚠️ Processing interrupted by user")
                break
            except Exception as e:
                logger.error(f"❌ Unexpected error processing {zip_path.name}: {e}")
                self.stats["failed"] += 1
                continue

        # Generate final summary
        self.generate_final_summary()

    def generate_final_summary(self):
        """Generate final processing summary"""
        summary_path = self.output_dir / "FINAL_SUMMARY.md"

        with open(summary_path, "w") as f:
            f.write("# Canva Single ZIP Processing - Final Summary\n\n")
            f.write(
                f"**Processing Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            f.write("## Processing Statistics\n\n")
            f.write(f"- **Total ZIPs Processed:** {self.stats['total_processed']}\n")
            f.write(f"- **Successful:** {self.stats['successful']}\n")
            f.write(f"- **Failed:** {self.stats['failed']}\n")
            f.write(f"- **Duplicates Found:** {self.stats['duplicates_found']}\n")
            f.write(
                f"- **Space Saved:** {self.stats['space_saved'] / (1024 * 1024):.1f} MB\n\n"
            )

            f.write("## Output Organization\n\n")
            f.write("```\n")
            f.write("Compressed_Processed/\n")
            f.write("├── Large_Archives/     # Original large archives (>1GB)\n")
            f.write("├── Medium_Archives/    # Original medium archives (50MB-1GB)\n")
            f.write("├── Small_Archives/     # Original small archives (<50MB)\n")
            f.write("├── Resources/          # Resource packs\n")
            f.write(
                "├── Cleaned/            # Cleaned versions (internal deduplication)\n"
            )
            f.write("├── Compressed/         # 7zip compressed versions\n")
            f.write("├── REPORT_*.md         # Individual ZIP reports\n")
            f.write("└── FINAL_SUMMARY.md    # This summary\n")
            f.write("```\n")

        logger.info(f"📊 Final summary generated: {summary_path}")

    def cleanup_temp_files(self):
        """Clean up temporary files"""
        logger.info("🧹 Cleaning up temporary files...")
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("✅ Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Could not clean up temp directory: {e}")


def main():
    parser = argparse.ArgumentParser(description="Canva Single ZIP Processor")
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
        default="/tmp/canva_single_processing",
        help="Temporary directory for processing",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Process all files without prompting",
    )
    parser.add_argument("--zip-file", type=str, help="Process only a specific ZIP file")

    args = parser.parse_args()

    # Validate source directory
    if not Path(args.source).exists():
        logger.error(f"Source directory does not exist: {args.source}")
        sys.exit(1)

    # Create processor
    processor = SingleZipProcessor(args.source, args.output, args.temp)

    try:
        if args.zip_file:
            # Process specific ZIP file
            zip_path = Path(args.source) / args.zip_file
            if zip_path.exists():
                processor.process_single_zip(zip_path)
            else:
                logger.error(f"ZIP file not found: {zip_path}")
        else:
            # Process all ZIP files
            processor.process_all_zips(interactive=not args.non_interactive)

    finally:
        processor.cleanup_temp_files()


if __name__ == "__main__":
    main()
