import os
import csv
import hashlib
from pathlib import Path
from datetime import datetime

local_dir = '/Users/steven/Music/nocTurneMeLoDieS'
csv_path = '/Users/steven/Music/nocTurneMeLoDieS/AI_ENHANCED_ORGANIZATION/DATA/COMPLETE_MUSIC_COLLECTION_INVENTORY.csv'

def generate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as afile:
        buf = afile.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(65536)
    return hasher.hexdigest()

def get_file_metadata(file_path):
    stat = file_path.stat()
    return {
        "File Path": str(file_path),
        "File Type": file_path.suffix,
        "Size (bytes)": stat.st_size,
        "Modified Date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "Directory": str(file_path.parent),
        "File Hash": generate_md5(file_path),
        # Placeholder for other fields that would come from AI/Manual tagging
        "Album Series": "",
        "Thematic Category": "",
        "Content Type": ""
    }

def update_music_inventory():
    print("🚀 Generating fresh local music inventory...")
    new_inventory_data = []
    
    for root, _, files in os.walk(local_dir):
        for f in files:
            if f.endswith('.mp3'):
                file_path = Path(root) / f
                new_inventory_data.append(get_file_metadata(file_path))
    
    # Load existing CSV data to merge
    existing_data = {}
    if Path(csv_path).exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_data[os.path.basename(row.get("File Path", ""))] = row
    
    # Merge new data, keeping existing metadata for old files
    final_data = []
    updated_count = 0
    added_count = 0
    
    for new_item in new_inventory_data:
        file_name = os.path.basename(new_item["File Path"])
        if file_name in existing_data:
            # Update hash and size, keep existing rich metadata
            merged_item = existing_data[file_name]
            merged_item["File Hash"] = new_item["File Hash"]
            merged_item["Size (bytes)"] = new_item["Size (bytes)"]
            merged_item["Modified Date"] = new_item["Modified Date"]
            merged_item["File Path"] = new_item["File Path"] # Update path in case it moved
            final_data.append(merged_item)
            updated_count += 1
        else:
            # Add new item
            final_data.append(new_item)
            added_count += 1
            
    # Add back any entries from existing_data that are not in new_inventory_data (e.g., deleted files)
    # This scenario is complex if files are truly deleted. For now, we only add/update present files.

    # Ensure all columns are present (for new headers if any)
    fieldnames = list(new_inventory_data[0].keys()) if new_inventory_data else []
    if existing_data:
        # Combine fieldnames from both, ensuring no duplicates
        all_fieldnames = set(fieldnames)
        for row in existing_data.values():
            all_fieldnames.update(row.keys())
        fieldnames = sorted(list(all_fieldnames), key=lambda x: (x != "File Path", x)) # Keep File Path first

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_data)
        
    print(f"✅ Master Music Inventory updated at {csv_path}!")
    print(f"   Added {added_count} new tracks.")
    print(f"   Updated {updated_count} existing tracks.")
    print(f"   Total tracks in CSV: {len(final_data)}")

if __name__ == "__main__":
    update_music_inventory()
