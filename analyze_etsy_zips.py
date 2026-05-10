import os
import zipfile
from pathlib import Path

# Configuration
ZIP_DIR = Path("/Users/steven/Pictures/etsy/zips")
SEARCH_DIRS = [
    Path("/Users/steven/Pictures/etsy/SVG_Files"),
    Path("/Users/steven/Pictures/etsy/Designs"),
    Path("/Users/steven/Pictures/etsy/Digital_Video_Art"),
    Path("/Users/steven/Pictures/etsy/Halloween"),
    Path("/Users/steven/Pictures/etsy/T-Shirts")
]

def get_all_filenames(dirs):
    """Cache all filenames in search dirs for fast lookup."""
    print("Indexing extracted files...")
    filenames = set()
    for d in dirs:
        if d.exists():
            for root, _, files in os.walk(d):
                for f in files:
                    if not f.startswith('.'):
                        filenames.add(f.lower())
    return filenames

def analyze_zips():
    if not ZIP_DIR.exists():
        print(f"Zip directory not found: {ZIP_DIR}")
        return

    extracted_files = get_all_filenames(SEARCH_DIRS)
    print(f"Indexed {len(extracted_files)} unique extracted files.")
    
    zips = list(ZIP_DIR.glob("*.zip"))
    print(f"Analyzing {len(zips)} zip files...")
    
    fully_extracted = []
    partially_extracted = []
    not_extracted = []
    
    for z in zips:
        try:
            with zipfile.ZipFile(z, 'r') as zf:
                content_list = [n for n in zf.namelist() if not n.endswith('/') and not n.startswith('__MACOSX') and not n.startswith('.')]
                if not content_list:
                    continue
                
                found_count = 0
                for f in content_list:
                    # Check if the filename (basename) exists in our index
                    name = Path(f).name.lower()
                    if name in extracted_files:
                        found_count += 1
                
                ratio = found_count / len(content_list)
                
                if ratio == 1.0:
                    fully_extracted.append(z.name)
                elif ratio > 0.5:
                    partially_extracted.append((z.name, f"{ratio:.1%}"))
                else:
                    not_extracted.append(z.name)
                    
        except zipfile.BadZipFile:
            print(f"Bad zip: {z.name}")

    print("\n=== ANALYSIS RESULTS ===")
    print(f"Total Zips: {len(zips)}")
    print(f"Fully Extracted (Safe to Archive): {len(fully_extracted)}")
    print(f"Partially Extracted: {len(partially_extracted)}")
    print(f"Not Extracted (New Content): {len(not_extracted)}")
    
    print("\n--- Top 10 Fully Extracted (Candidates for Move) ---")
    for z in fully_extracted[:10]:
        print(f"✅ {z}")

    print("\n--- Top 10 Not Extracted (Keep/Review) ---")
    for z in not_extracted[:10]:
        print(f"❌ {z}")

if __name__ == "__main__":
    analyze_zips()
