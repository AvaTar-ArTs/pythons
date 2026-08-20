#!/usr/bin/env python3
"""
Canva Archive Batch Processor
============================

Processes Canva archives in small batches to avoid memory issues.
Handles deduplication, compression, and organization in manageable chunks.

Usage: python3 canva_batch_processor.py [options]
"""

import os
import sys
import zipfile
import hashlib
import shutil
import subprocess
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import argparse
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('canva_batch_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CanvaBatchProcessor:
    def __init__(self, source_dir, output_dir, temp_dir=None, batch_size=3):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir) if temp_dir else Path('/tmp/canva_batch_processing')
        self.batch_size = batch_size
        
        # Create directories
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # File tracking
        self.global_file_hashes = defaultdict(list)  # hash -> [(archive, file_path, size)]
        self.processed_archives = set()
        self.stats = {
            'total_archives': 0,
            'total_files': 0,
            'duplicate_files': 0,
            'space_saved': 0,
            'batches_processed': 0
        }
        
        # Check for 7zip
        self.seven_zip_cmd = self._find_7zip()
        if not self.seven_zip_cmd:
            logger.warning("7zip not found. Will use Python's zipfile for compression.")
    
    def _find_7zip(self):
        """Find 7zip executable"""
        for cmd in ['7z', '7za']:
            try:
                subprocess.run([cmd], capture_output=True, check=True)
                return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        return None
    
    def get_archive_batches(self):
        """Split archives into batches for processing"""
        all_archives = list(self.source_dir.glob("*.zip"))
        self.stats['total_archives'] = len(all_archives)
        
        # Sort by size (smallest first) to process easier files first
        all_archives.sort(key=lambda x: x.stat().st_size)
        
        batches = []
        for i in range(0, len(all_archives), self.batch_size):
            batch = all_archives[i:i + self.batch_size]
            batches.append(batch)
        
        logger.info(f"📦 Split {len(all_archives)} archives into {len(batches)} batches of {self.batch_size}")
        return batches
    
    def process_single_archive(self, archive_path):
        """Process a single archive and return its file information"""
        logger.info(f"🔍 Processing: {archive_path.name}")
        
        archive_info = {
            'archive_name': archive_path.name,
            'files': [],
            'total_size': 0,
            'file_count': 0,
            'success': False
        }
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_file:
                for file_info in zip_file.filelist:
                    if file_info.file_size > 0:  # Skip directories and empty files
                        # Read file content and calculate hash
                        file_data = zip_file.read(file_info.filename)
                        file_hash = hashlib.md5(file_data).hexdigest()
                        
                        # Store file info
                        file_entry = {
                            'archive': archive_path.name,
                            'file_path': file_info.filename,
                            'size': file_info.file_size,
                            'hash': file_hash,
                            'compressed_size': file_info.compress_size
                        }
                        
                        archive_info['files'].append(file_entry)
                        archive_info['total_size'] += file_info.file_size
                        archive_info['file_count'] += 1
                        
                        # Add to global hash database
                        self.global_file_hashes[file_hash].append(file_entry)
                
                archive_info['success'] = True
                self.stats['total_files'] += archive_info['file_count']
                logger.info(f"✅ Processed {archive_path.name}: {archive_info['file_count']} files")
                
        except Exception as e:
            logger.error(f"❌ Error processing {archive_path.name}: {e}")
            archive_info['error'] = str(e)
        
        return archive_info
    
    def process_batch(self, batch_archives):
        """Process a batch of archives"""
        batch_num = self.stats['batches_processed'] + 1
        logger.info(f"🚀 Processing Batch {batch_num}: {len(batch_archives)} archives")
        
        batch_results = []
        
        for archive_path in batch_archives:
            if archive_path.name not in self.processed_archives:
                result = self.process_single_archive(archive_path)
                batch_results.append(result)
                self.processed_archives.add(archive_path.name)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
        
        self.stats['batches_processed'] += 1
        return batch_results
    
    def find_duplicates_in_batch(self, batch_results):
        """Find duplicates within the current batch and against global database"""
        logger.info(f"🔍 Finding duplicates in batch...")
        
        batch_duplicates = {}
        
        for result in batch_results:
            if not result['success']:
                continue
                
            for file_info in result['files']:
                file_hash = file_info['hash']
                
                # Check if this file hash appears in multiple places
                if len(self.global_file_hashes[file_hash]) > 1:
                    # Sort by size (keep largest) and then by archive name
                    file_entries = self.global_file_hashes[file_hash]
                    file_entries.sort(key=lambda x: (-x['size'], x['archive']))
                    
                    # Keep the first (largest) file, mark others as duplicates
                    keep_file = file_entries[0]
                    duplicates = file_entries[1:]
                    
                    if file_hash not in batch_duplicates:
                        batch_duplicates[file_hash] = {
                            'keep': keep_file,
                            'duplicates': duplicates
                        }
        
        return batch_duplicates
    
    def create_deduplicated_archives_batch(self, batch_results, batch_duplicates):
        """Create deduplicated versions of archives in this batch"""
        logger.info(f"📦 Creating deduplicated archives for batch...")
        
        # Create deduplication mapping for this batch
        files_to_remove = defaultdict(list)
        for file_hash, dup_info in batch_duplicates.items():
            keep_file = dup_info['keep']
            for dup_file in dup_info['duplicates']:
                if dup_file['archive'] in [r['archive_name'] for r in batch_results]:
                    files_to_remove[dup_file['archive']].append(dup_file['file_path'])
        
        # Process each archive in the batch
        for result in batch_results:
            if not result['success']:
                continue
                
            archive_name = result['archive_name']
            original_archive = self.source_dir / archive_name
            dedup_archive = self.temp_dir / f"dedup_{archive_name}"
            
            files_to_skip = set(files_to_remove.get(archive_name, []))
            
            if not files_to_skip:
                logger.info(f"📁 No duplicates to remove from {archive_name}")
                continue
            
            logger.info(f"📦 Deduplicating {archive_name}: removing {len(files_to_skip)} files")
            
            try:
                with zipfile.ZipFile(original_archive, 'r') as source_zip:
                    with zipfile.ZipFile(dedup_archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as dest_zip:
                        
                        for file_info in source_zip.filelist:
                            if file_info.filename not in files_to_skip and file_info.file_size > 0:
                                # Copy file to new archive
                                file_data = source_zip.read(file_info.filename)
                                dest_zip.writestr(file_info, file_data)
                        
                        logger.info(f"✅ Created deduplicated {archive_name}")
                        
            except Exception as e:
                logger.error(f"❌ Error creating deduplicated archive {archive_name}: {e}")
    
    def compress_archives_batch(self, batch_results):
        """Compress archives in this batch using 7zip"""
        logger.info(f"🗜️ Compressing archives in batch...")
        
        if not self.seven_zip_cmd:
            logger.warning("7zip not available, skipping compression")
            return
        
        for result in batch_results:
            if not result['success']:
                continue
                
            archive_name = result['archive_name']
            dedup_archive = self.temp_dir / f"dedup_{archive_name}"
            
            if not dedup_archive.exists():
                # If no deduplicated version, use original
                dedup_archive = self.source_dir / archive_name
            
            logger.info(f"🗜️ Compressing {archive_name}")
            
            # Extract to temporary directory
            extract_dir = self.temp_dir / f"extract_{archive_name.replace('.zip', '')}"
            extract_dir.mkdir(exist_ok=True)
            
            try:
                # Extract archive
                with zipfile.ZipFile(dedup_archive, 'r') as zip_file:
                    zip_file.extractall(extract_dir)
                
                # Recompress with 7zip
                compressed_archive = self.temp_dir / f"compressed_{archive_name.replace('.zip', '.7z')}"
                cmd = [
                    self.seven_zip_cmd, 'a', '-t7z', '-mx9', '-m0=lzma2',
                    str(compressed_archive), str(extract_dir / '*')
                ]
                
                result_cmd = subprocess.run(cmd, capture_output=True, text=True)
                if result_cmd.returncode == 0:
                    # Calculate compression ratio
                    original_size = dedup_archive.stat().st_size
                    compressed_size = compressed_archive.stat().st_size
                    ratio = (1 - compressed_size / original_size) * 100
                    
                    logger.info(f"✅ Compressed {archive_name}: {ratio:.1f}% reduction")
                    
                    # Clean up extraction directory
                    shutil.rmtree(extract_dir)
                else:
                    logger.error(f"7zip compression failed for {archive_name}: {result_cmd.stderr}")
                    
            except Exception as e:
                logger.error(f"❌ Error compressing {archive_name}: {e}")
    
    def organize_archives_batch(self, batch_results):
        """Organize archives in this batch by size and content type"""
        logger.info(f"📁 Organizing archives in batch...")
        
        # Create organization structure
        org_structure = {
            'Large_Archives': self.output_dir / 'Large_Archives',      # > 1GB
            'Medium_Archives': self.output_dir / 'Medium_Archives',    # 50MB - 1GB
            'Small_Archives': self.output_dir / 'Small_Archives',      # < 50MB
            'Resources': self.output_dir / 'Resources',                # Resource packs
            'Deduplicated': self.output_dir / 'Deduplicated',          # Deduplicated versions
            'Compressed': self.output_dir / 'Compressed'               # 7zip compressed versions
        }
        
        for category_dir in org_structure.values():
            category_dir.mkdir(exist_ok=True)
        
        # Organize original archives
        for result in batch_results:
            if not result['success']:
                continue
                
            archive_name = result['archive_name']
            archive_path = self.source_dir / archive_name
            size_mb = archive_path.stat().st_size / (1024 * 1024)
            
            if 'Glitch-Arts' in archive_name:
                target_dir = org_structure['Resources']
            elif size_mb > 1000:
                target_dir = org_structure['Large_Archives']
            elif size_mb > 50:
                target_dir = org_structure['Medium_Archives']
            else:
                target_dir = org_structure['Small_Archives']
            
            # Copy to organized location
            dest_path = target_dir / archive_name
            shutil.copy2(archive_path, dest_path)
            logger.info(f"📁 Organized {archive_name} -> {target_dir.name}")
        
        # Move deduplicated archives
        for dedup_archive in self.temp_dir.glob("dedup_*.zip"):
            dest_path = org_structure['Deduplicated'] / dedup_archive.name
            shutil.move(str(dedup_archive), str(dest_path))
            logger.info(f"📁 Moved deduplicated {dedup_archive.name}")
        
        # Move compressed archives
        for comp_archive in self.temp_dir.glob("compressed_*.7z"):
            dest_path = org_structure['Compressed'] / comp_archive.name
            shutil.move(str(comp_archive), str(dest_path))
            logger.info(f"📁 Moved compressed {comp_archive.name}")
    
    def generate_batch_report(self, batch_num, batch_results, batch_duplicates):
        """Generate a report for this batch"""
        report_path = self.output_dir / f'BATCH_{batch_num:02d}_REPORT.md'
        
        with open(report_path, 'w') as f:
            f.write(f"# Batch {batch_num} Processing Report\n\n")
            f.write(f"**Processing Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Batch Statistics\n\n")
            f.write(f"- **Archives Processed:** {len(batch_results)}\n")
            f.write(f"- **Successful Archives:** {sum(1 for r in batch_results if r['success'])}\n")
            f.write(f"- **Total Files:** {sum(r['file_count'] for r in batch_results if r['success'])}\n")
            f.write(f"- **Duplicate Sets Found:** {len(batch_duplicates)}\n")
            
            f.write("\n## Archive Details\n\n")
            for result in batch_results:
                f.write(f"### {result['archive_name']}\n")
                f.write(f"- **Status:** {'✅ Success' if result['success'] else '❌ Failed'}\n")
                if result['success']:
                    f.write(f"- **Files:** {result['file_count']}\n")
                    f.write(f"- **Size:** {result['total_size'] / (1024*1024):.1f} MB\n")
                else:
                    f.write(f"- **Error:** {result.get('error', 'Unknown error')}\n")
                f.write("\n")
            
            if batch_duplicates:
                f.write("## Duplicate Files Found\n\n")
                for file_hash, dup_info in batch_duplicates.items():
                    f.write(f"### Hash: {file_hash[:16]}...\n")
                    f.write(f"- **Keep:** {dup_info['keep']['archive']} - {dup_info['keep']['file_path']}\n")
                    f.write(f"- **Duplicates:**\n")
                    for dup in dup_info['duplicates']:
                        f.write(f"  - {dup['archive']} - {dup['file_path']}\n")
                    f.write("\n")
        
        logger.info(f"📊 Batch {batch_num} report generated: {report_path}")
    
    def process_all_batches(self):
        """Process all archives in batches"""
        logger.info("🚀 Starting Canva Batch Processing Pipeline")
        logger.info("=" * 60)
        
        batches = self.get_archive_batches()
        all_duplicates = {}
        
        try:
            for batch_num, batch_archives in enumerate(batches, 1):
                logger.info(f"\n🔄 Processing Batch {batch_num}/{len(batches)}")
                logger.info("-" * 40)
                
                # Process batch
                batch_results = self.process_batch(batch_archives)
                
                # Find duplicates in this batch
                batch_duplicates = self.find_duplicates_in_batch(batch_results)
                all_duplicates.update(batch_duplicates)
                
                # Create deduplicated archives
                self.create_deduplicated_archives_batch(batch_results, batch_duplicates)
                
                # Compress archives
                self.compress_archives_batch(batch_results)
                
                # Organize archives
                self.organize_archives_batch(batch_results)
                
                # Generate batch report
                self.generate_batch_report(batch_num, batch_results, batch_duplicates)
                
                # Update global stats
                self.stats['duplicate_files'] += sum(len(dup['duplicates']) for dup in batch_duplicates.values())
                self.stats['space_saved'] += sum(
                    sum(dup['size'] for dup in dup_info['duplicates']) 
                    for dup_info in batch_duplicates.values()
                )
                
                logger.info(f"✅ Batch {batch_num} complete")
                
                # Small delay between batches
                time.sleep(1)
            
            # Generate final summary
            self.generate_final_report(all_duplicates)
            
            logger.info("=" * 60)
            logger.info("🎉 All batches processed successfully!")
            logger.info(f"📁 Output directory: {self.output_dir}")
            logger.info(f"💾 Total space saved: {self.stats['space_saved'] / (1024*1024):.1f} MB")
            logger.info(f"🔄 Total batches: {self.stats['batches_processed']}")
            
        except Exception as e:
            logger.error(f"❌ Batch processing failed: {e}")
            raise
    
    def generate_final_report(self, all_duplicates):
        """Generate final summary report"""
        report_path = self.output_dir / 'FINAL_PROCESSING_REPORT.md'
        
        with open(report_path, 'w') as f:
            f.write("# Canva Archive Batch Processing - Final Report\n\n")
            f.write(f"**Processing Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Source Directory:** {self.source_dir}\n")
            f.write(f"**Output Directory:** {self.output_dir}\n\n")
            
            f.write("## Final Statistics\n\n")
            f.write(f"- **Total Archives Processed:** {self.stats['total_archives']}\n")
            f.write(f"- **Total Files Analyzed:** {self.stats['total_files']}\n")
            f.write(f"- **Total Duplicate Files Found:** {self.stats['duplicate_files']}\n")
            f.write(f"- **Total Space Saved:** {self.stats['space_saved'] / (1024*1024):.1f} MB\n")
            f.write(f"- **Batches Processed:** {self.stats['batches_processed']}\n")
            f.write(f"- **Duplicate Sets:** {len(all_duplicates)}\n\n")
            
            f.write("## Organization Structure\n\n")
            f.write("```\n")
            f.write("Compressed_Processed/\n")
            f.write("├── Large_Archives/     # > 1GB\n")
            f.write("├── Medium_Archives/    # 50MB - 1GB\n")
            f.write("├── Small_Archives/     # < 50MB\n")
            f.write("├── Resources/          # Resource packs\n")
            f.write("├── Deduplicated/       # Deduplicated versions\n")
            f.write("├── Compressed/         # 7zip compressed versions\n")
            f.write("└── BATCH_*_REPORT.md  # Individual batch reports\n")
            f.write("```\n")
        
        logger.info(f"📊 Final report generated: {report_path}")
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        logger.info("🧹 Cleaning up temporary files...")
        try:
            shutil.rmtree(self.temp_dir)
            logger.info("✅ Temporary files cleaned up")
        except Exception as e:
            logger.warning(f"Could not clean up temp directory: {e}")

def main():
    parser = argparse.ArgumentParser(description='Canva Archive Batch Processor')
    parser.add_argument('--source', default='/Volumes/2T-Xx/AvaTarArTs/canva/Compressed',
                       help='Source directory containing Canva archives')
    parser.add_argument('--output', default='/Volumes/2T-Xx/AvaTarArTs/canva/Compressed_Processed',
                       help='Output directory for processed archives')
    parser.add_argument('--temp', default='/tmp/canva_batch_processing',
                       help='Temporary directory for processing')
    parser.add_argument('--batch-size', type=int, default=3,
                       help='Number of archives to process per batch')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without actually processing')
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("🔍 DRY RUN MODE - Analyzing what would be processed")
        processor = CanvaBatchProcessor(args.source, args.output, args.temp, args.batch_size)
        batches = processor.get_archive_batches()
        logger.info(f"Would process {len(batches)} batches of {args.batch_size} archives each")
        return
    
    # Validate source directory
    if not Path(args.source).exists():
        logger.error(f"Source directory does not exist: {args.source}")
        sys.exit(1)
    
    # Create processor and run
    processor = CanvaBatchProcessor(args.source, args.output, args.temp, args.batch_size)
    processor.process_all_batches()

if __name__ == "__main__":
    main()