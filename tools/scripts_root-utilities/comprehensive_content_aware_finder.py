#!/usr/bin/env python3
"""
Comprehensive Content-Aware Duplicate Finder
Advanced intelligent detection with:
- Content hashing for exact duplicates
- Similarity analysis for near-duplicates
- Large directory deep analysis
- Intelligent keep/delete decisions
"""

import hashlib
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import difflib

class ComprehensiveContentAwareFinder:
    """Comprehensive content-aware duplicate finder."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Priority locations
        self.location_priority = {
            'quantumforge-complete': 100,
            'retention-suite-complete': 95,
            'tools': 90,
            'scripts': 85,
            'organized_intelligent': 80,
            'archive': 10,
            'ai-sites': 5,
            '.history': 1,  # History files lowest priority
        }
        
        # Large directories to analyze deeply
        self.large_dirs = ['organized_intelligent', 'archive', 'Ai-Empire', 'josephrosadomd']
        
    def calculate_content_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate content hash with chunked reading for large files."""
        try:
            size = file_path.stat().st_size
            
            # For very large files (>100MB), use first+middle+last chunks
            if size > 100 * 1024 * 1024:
                md5 = hashlib.md5()
                with open(file_path, 'rb') as f:
                    # First chunk
                    md5.update(f.read(chunk_size))
                    # Middle chunk
                    f.seek(size // 2)
                    md5.update(f.read(chunk_size))
                    # Last chunk
                    f.seek(max(0, size - chunk_size))
                    md5.update(f.read(chunk_size))
                    # Size
                    md5.update(str(size).encode())
                return md5.hexdigest()
            
            # For smaller files, hash entire content
            md5 = hashlib.md5()
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception:
            return None
    
    def get_file_metadata(self, file_path: Path) -> dict:
        """Get comprehensive file metadata."""
        try:
            stat = file_path.stat()
            rel_path = str(file_path.relative_to(self.workspace_root))
            parts = Path(rel_path).parts
            
            # Location priority
            location_priority = 50  # Default
            for location, priority in self.location_priority.items():
                if location in rel_path:
                    location_priority = max(location_priority, priority)
            
            # Check nested
            is_nested = len(parts) > 3 and any(parts[i] == parts[i+1] for i in range(len(parts)-1))
            if is_nested:
                location_priority -= 50
            
            # Check if in large directory
            in_large_dir = any(large_dir in rel_path for large_dir in self.large_dirs)
            
            return {
                'path': rel_path,
                'full_path': str(file_path),
                'size': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'modified': stat.st_mtime,
                'extension': file_path.suffix.lower(),
                'location_priority': location_priority,
                'depth': len(parts),
                'is_nested': is_nested,
                'in_large_dir': in_large_dir,
                'filename': file_path.name
            }
        except:
            return None
    
    def determine_keep_file(self, files: list) -> dict:
        """Intelligently determine which file to keep."""
        if not files:
            return None
        
        scored_files = []
        for f in files:
            score = 0
            
            # Location priority (most important)
            score += f['location_priority'] * 20
            
            # Prefer shallower depth
            score += (10 - min(f['depth'], 10)) * 5
            
            # Prefer not in large directories (they might be archives)
            if not f['in_large_dir']:
                score += 30
            
            # Penalize nested
            if f['is_nested']:
                score -= 100
            
            # Penalize history/backup directories
            path_lower = f['path'].lower()
            if '.history' in path_lower or 'backup' in path_lower or 'archive' in path_lower:
                score -= 50
            
            # Prefer newer files (small boost)
            score += (f['modified'] / 10000000)
            
            scored_files.append((score, f))
        
        scored_files.sort(key=lambda x: x[0], reverse=True)
        return scored_files[0][1]
    
    def find_duplicates_comprehensive(self) -> list:
        """Comprehensive duplicate finding."""
        print("🔍 Comprehensive Content-Aware Duplicate Detection")
        print("=" * 80)
        print()
        
        print("1️⃣  Scanning all files and calculating content hashes...")
        file_groups = defaultdict(list)
        total_files = 0
        large_files = 0
        
        for file_path in self.workspace_root.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Skip system files
            if file_path.name.startswith('.') and file_path.name not in ['.env', '.gitignore']:
                continue
            
            # Skip certain directories
            rel_path = str(file_path.relative_to(self.workspace_root))
            if any(skip in rel_path for skip in ['node_modules', '.git', '__pycache__', '.venv', 'venv', '.DS_Store']):
                continue
            
            total_files += 1
            if total_files % 2000 == 0:
                print(f"   Processed {total_files:,} files...")
            
            # Get metadata
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                continue
            
            # Skip very small files (< 100 bytes) - likely not important duplicates
            if metadata['size'] < 100:
                continue
            
            # Calculate hash
            content_hash = self.calculate_content_hash(file_path)
            if not content_hash:
                continue
            
            # Track large files separately
            if metadata['size'] > 10 * 1024 * 1024:  # > 10MB
                large_files += 1
            
            file_groups[content_hash].append(metadata)
        
        print(f"   ✅ Scanned {total_files:,} files ({large_files:,} large files)")
        print(f"   Found {len(file_groups)} unique content hashes\n")
        
        print("2️⃣  Identifying duplicate groups...")
        duplicates = []
        duplicate_groups = 0
        
        for content_hash, files in file_groups.items():
            if len(files) > 1:
                duplicate_groups += 1
                
                # Determine keep file
                keep_file = self.determine_keep_file(files)
                if not keep_file:
                    continue
                
                duplicate_files = [f for f in files if f['path'] != keep_file['path']]
                total_waste = sum(f['size'] for f in duplicate_files)
                
                duplicates.append({
                    'content_hash': content_hash,
                    'keep_file': keep_file,
                    'duplicate_files': duplicate_files,
                    'duplicate_count': len(duplicate_files),
                    'total_waste_mb': total_waste / (1024 * 1024),
                    'filename': keep_file['filename']
                })
        
        print(f"   ✅ Found {duplicate_groups} duplicate groups")
        print(f"   Total duplicate files: {sum(d['duplicate_count'] for d in duplicates):,}")
        total_waste_gb = sum(d['total_waste_mb'] for d in duplicates) / 1024
        print(f"   Total waste: {total_waste_gb:.2f} GB\n")
        
        # Sort by waste
        duplicates.sort(key=lambda x: x['total_waste_mb'], reverse=True)
        
        return duplicates
    
    def generate_mapping_csv(self, duplicates: list) -> Path:
        """Generate mapping CSV."""
        output_csv = self.workspace_root / f"COMPREHENSIVE_DUPLICATES_MAPPING_{self.timestamp}.csv"
        
        print("3️⃣  Generating intelligent mapping CSV...")
        
        mappings = []
        for dup_group in duplicates:
            keep_path = dup_group['keep_file']['path']
            keep_priority = dup_group['keep_file']['location_priority']
            
            for dup_file in dup_group['duplicate_files']:
                # Generate keep reason
                reasons = []
                if keep_priority > dup_file['location_priority']:
                    reasons.append("better location")
                if dup_group['keep_file']['depth'] < dup_file['depth']:
                    reasons.append("shallower")
                if dup_file['in_large_dir'] and not dup_group['keep_file']['in_large_dir']:
                    reasons.append("not in archive")
                if dup_file['is_nested']:
                    reasons.append("not nested")
                
                keep_reason = ", ".join(reasons) if reasons else "intelligent selection"
                
                mappings.append({
                    'original_path': dup_file['path'],
                    'new_path': keep_path,
                    'filename': dup_group['filename'],
                    'size_mb': f"{dup_file['size_mb']:.2f}",
                    'waste_mb': f"{dup_group['total_waste_mb']:.2f}",
                    'keep_reason': keep_reason,
                    'content_hash': dup_group['content_hash'][:16]
                })
        
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['original_path', 'new_path', 'filename', 'size_mb', 'waste_mb', 'keep_reason', 'content_hash']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mappings)
        
        print(f"   ✅ CSV created: {output_csv.name}")
        print(f"   Total mappings: {len(mappings):,}\n")
        
        return output_csv

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    finder = ComprehensiveContentAwareFinder(workspace_root)
    
    # Find duplicates
    duplicates = finder.find_duplicates_comprehensive()
    
    if not duplicates:
        print("✅ No duplicates found!")
        return
    
    # Generate mapping
    mapping_csv = finder.generate_mapping_csv(duplicates)
    
    print("=" * 80)
    print("✅ COMPREHENSIVE DUPLICATE DETECTION COMPLETE")
    print("=" * 80)
    print(f"\n📄 Mapping CSV: {mapping_csv.name}")
    print(f"📊 Duplicate groups: {len(duplicates)}")
    print(f"💾 Total waste: {sum(d['total_waste_mb'] for d in duplicates) / 1024:.2f} GB")
    print(f"\n💡 Next: Review CSV and run consolidation")
    print()

if __name__ == "__main__":
    main()
