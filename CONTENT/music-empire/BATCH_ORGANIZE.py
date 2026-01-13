#!/usr/bin/env python3
"""
?? Batch Organization - Process 13,007 Files
==============================================

Organizes all audio in manageable batches based on analysis.

Author: Steven Chaplinski
Date: November 4, 2025
"""

import shutil
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class BatchOrganizer:
    """Organize in batches"""
    
    def __init__(self):
        self.workspace = Path.home() / 'workspace' / 'music-empire'
        self.target_dir = Path.home() / 'Music' / 'nocTurneMeLoDieS' / 'ORGANIZED'
        
        self.catalog = {}
        self.inventory = []
        self.seen_hashes = set()
        
        self.stats = {
            'total': 0,
            'suno_matched': 0,
            'suno_unmatched': 0,
            'other': 0,
            'duplicates': 0,
            'organized': 0,
            'errors': 0
        }
    
    def load_data(self):
        """Load catalog and inventory"""
        
        print("?? Loading data...\n")
        
        # Load catalog (find latest)
        catalog_files = list(self.workspace.glob('MASTER_SUNO_COLLECTION_*.csv'))
        if not catalog_files:
            catalog_files = list(self.workspace.glob('COMPLETE_EXTRACTED_*.csv'))
        
        if not catalog_files:
            print("   ??  No catalog found, will use inventory only")
            return
        
        catalog_file = sorted(catalog_files)[-1]
        print(f"   Using catalog: {catalog_file.name}")
        
        with open(catalog_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                song_id = row.get('id', '').strip()
                if song_id:
                    self.catalog[song_id] = row
        
        print(f"   ? Catalog: {len(self.catalog)} songs")
        
        # Load inventory
        inventory_file = self.workspace / 'COMPLETE_FILE_INVENTORY.csv'
        with open(inventory_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.inventory.append(row)
        
        print(f"   ? Inventory: {len(self.inventory)} files\n")
    
    def create_structure(self):
        """Create organized folder structure"""
        
        folders = {
            'suno_matched': self.target_dir / 'YOUR_SUNO_SONGS' / 'MATCHED_TO_CATALOG',
            'suno_unmatched': self.target_dir / 'YOUR_SUNO_SONGS' / 'UNMATCHED',
            'other': self.target_dir / 'OTHER_MUSIC',
            'duplicates_log': self.target_dir / 'DUPLICATES_SKIPPED'
        }
        
        for folder in folders.values():
            folder.mkdir(parents=True, exist_ok=True)
        
        return folders
    
    def process_files(self, folders):
        """Process all files"""
        
        print("?? Processing files in batches...\n")
        
        batch_size = 100
        total = len(self.inventory)
        
        for i in range(0, total, batch_size):
            batch = self.inventory[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total // batch_size) + 1
            
            print(f"?? Batch {batch_num}/{total_batches} ({len(batch)} files)")
            
            for file_info in batch:
                try:
                    source_path = Path(file_info['path'])
                    
                    if not source_path.exists():
                        continue
                    
                    # Check for duplicate
                    file_hash = file_info['hash']
                    if file_hash in self.seen_hashes:
                        self.stats['duplicates'] += 1
                        continue
                    
                    self.seen_hashes.add(file_hash)
                    
                    # Determine destination
                    in_catalog = file_info['in_catalog'] == 'YES'
                    
                    if in_catalog:
                        target_folder = folders['suno_matched']
                        self.stats['suno_matched'] += 1
                    else:
                        # Check if Suno-related
                        filename_lower = source_path.name.lower()
                        if any(word in filename_lower for word in ['suno', 'nocturne', 'avatararts']):
                            target_folder = folders['suno_unmatched']
                            self.stats['suno_unmatched'] += 1
                        else:
                            target_folder = folders['other']
                            self.stats['other'] += 1
                    
                    # Copy file
                    target_path = target_folder / source_path.name
                    
                    if not target_path.exists():
                        shutil.copy2(source_path, target_path)
                        self.stats['organized'] += 1
                    
                    self.stats['total'] += 1
                
                except Exception as e:
                    self.stats['errors'] += 1
            
            print(f"   ? Processed {min(i + batch_size, total)}/{total}")
            print(f"   ?? Organized: {self.stats['organized']} | Dupes: {self.stats['duplicates']}\n")
    
    def summary(self):
        """Print final summary"""
        
        print("=" * 70)
        print("?? ORGANIZATION COMPLETE!")
        print("=" * 70)
        
        print(f"\n?? Results:")
        print(f"   Total processed: {self.stats['total']}")
        print(f"   ? Organized: {self.stats['organized']}")
        print(f"   ?? Duplicates skipped: {self.stats['duplicates']}")
        print(f"   ? Errors: {self.stats['errors']}")
        
        print(f"\n?? By category:")
        print(f"   Your Suno (matched): {self.stats['suno_matched']}")
        print(f"   Your Suno (unmatched): {self.stats['suno_unmatched']}")
        print(f"   Other music: {self.stats['other']}")
        
        print(f"\n?? Everything organized in:")
        print(f"   {self.target_dir}")
        
        print(f"\n?? Next: Create albums from YOUR_SUNO_SONGS folder!")
    
    def run(self):
        """Run batch organization"""
        
        print("?? BATCH ORGANIZATION")
        print("=" * 70)
        print()
        
        self.load_data()
        folders = self.create_structure()
        self.process_files(folders)
        self.summary()


def main():
    organizer = BatchOrganizer()
    organizer.run()


if __name__ == '__main__':
    main()
