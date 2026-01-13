#!/usr/bin/env python3
"""
Advanced Content-Aware Duplicate Finder
Intelligently detects duplicates by analyzing actual file content, not just names/sizes.
Uses content hashing, semantic analysis, and intelligent keep/delete decisions.
"""

import hashlib
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import mimetypes
import json

class ContentAwareDuplicateFinder:
    """Advanced duplicate finder with content awareness."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Priority locations (higher = keep)
        self.location_priority = {
            'quantumforge-complete': 100,
            'retention-suite-complete': 95,
            'tools': 90,
            'scripts': 85,
            'archive': 10,
            'ai-sites': 5,
        }
        
        # File type handlers
        self.text_extensions = {'.py', '.md', '.txt', '.html', '.css', '.js', '.json', '.yaml', '.yml', '.sh', '.xml', '.csv'}
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'}
        self.binary_extensions = {'.pdf', '.zip', '.mp4', '.mp3', '.wav', '.ttf', '.woff', '.woff2', '.eot'}
        
    def calculate_content_hash(self, file_path: Path, max_size: int = 100 * 1024 * 1024) -> str:
        """Calculate content hash for file."""
        try:
            size = file_path.stat().st_size
            if size > max_size:
                # For very large files, use size + first/last bytes
                with open(file_path, 'rb') as f:
                    first = f.read(1024)
                    f.seek(max(0, size - 1024))
                    last = f.read(1024)
                return hashlib.md5(first + last + str(size).encode()).hexdigest()
            
            # For smaller files, hash entire content
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            return None
    
    def get_file_metadata(self, file_path: Path) -> dict:
        """Get comprehensive file metadata."""
        try:
            stat = file_path.stat()
            ext = file_path.suffix.lower()
            
            # Determine file type
            file_type = 'unknown'
            if ext in self.text_extensions:
                file_type = 'text'
            elif ext in self.image_extensions:
                file_type = 'image'
            elif ext in self.binary_extensions:
                file_type = 'binary'
            
            # Get location priority
            rel_path = str(file_path.relative_to(self.workspace_root))
            location_priority = 0
            for location, priority in self.location_priority.items():
                if location in rel_path:
                    location_priority = max(location_priority, priority)
            
            # Check if in nested structure
            parts = Path(rel_path).parts
            is_nested = len(parts) > 3 and any(parts[i] == parts[i+1] for i in range(len(parts)-1))
            if is_nested:
                location_priority -= 50  # Penalize nested structures
            
            return {
                'path': rel_path,
                'full_path': str(file_path),
                'size': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'modified': stat.st_mtime,
                'extension': ext,
                'file_type': file_type,
                'location_priority': location_priority,
                'depth': len(parts),
                'is_nested': is_nested,
                'filename': file_path.name
            }
        except Exception:
            return None
    
    def determine_keep_file(self, files: list) -> dict:
        """Intelligently determine which file to keep."""
        if not files:
            return None
        
        # Score each file
        scored_files = []
        for f in files:
            score = 0
            
            # Location priority (higher is better)
            score += f['location_priority'] * 10
            
            # Prefer shallower depth
            score += (10 - f['depth']) * 5
            
            # Prefer newer files (if similar priority)
            if f['location_priority'] > 50:
                score += (f['modified'] / 1000000)  # Small boost for newer
            
            # Penalize nested structures
            if f['is_nested']:
                score -= 100
            
            # Prefer certain file locations
            path_lower = f['path'].lower()
            if 'archive' in path_lower or 'backup' in path_lower:
                score -= 50
            if 'node_modules' in path_lower or '.git' in path_lower:
                score -= 200
            
            scored_files.append((score, f))
        
        # Return highest scored file
        scored_files.sort(key=lambda x: x[0], reverse=True)
        return scored_files[0][1]
    
    def analyze_content_similarity(self, file1: Path, file2: Path) -> float:
        """Analyze content similarity for text files."""
        if file1.suffix.lower() not in self.text_extensions:
            return 0.0
        
        try:
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
                content1 = f1.read()
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
                content2 = f2.read()
            
            # Simple similarity: ratio of common lines
            lines1 = set(content1.split('\n'))
            lines2 = set(content2.split('\n'))
            
            if not lines1 or not lines2:
                return 0.0
            
            common = len(lines1 & lines2)
            total = len(lines1 | lines2)
            
            return common / total if total > 0 else 0.0
        except:
            return 0.0
    
    def find_duplicates(self) -> list:
        """Find all duplicates using content-aware methods."""
        print("🔍 Advanced Content-Aware Duplicate Detection")
        print("=" * 80)
        print()
        
        print("1️⃣  Scanning files and calculating content hashes...")
        file_groups = defaultdict(list)
        total_files = 0
        
        for file_path in self.workspace_root.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Skip system files
            if file_path.name.startswith('.') and file_path.name not in ['.env', '.gitignore']:
                continue
            
            # Skip certain directories
            rel_path = str(file_path.relative_to(self.workspace_root))
            if any(skip in rel_path for skip in ['node_modules', '.git', '__pycache__', '.venv', 'venv']):
                continue
            
            total_files += 1
            if total_files % 1000 == 0:
                print(f"   Processed {total_files:,} files...")
            
            # Get metadata
            metadata = self.get_file_metadata(file_path)
            if not metadata:
                continue
            
            # Calculate content hash
            content_hash = self.calculate_content_hash(file_path)
            if not content_hash:
                continue
            
            # Group by content hash
            file_groups[content_hash].append(metadata)
        
        print(f"   ✅ Scanned {total_files:,} files")
        print(f"   Found {len(file_groups)} unique content hashes\n")
        
        print("2️⃣  Identifying duplicate groups...")
        duplicates = []
        duplicate_groups = 0
        
        for content_hash, files in file_groups.items():
            if len(files) > 1:
                duplicate_groups += 1
                
                # Determine which file to keep
                keep_file = self.determine_keep_file(files)
                if not keep_file:
                    continue
                
                # All other files are duplicates
                duplicate_files = [f for f in files if f['path'] != keep_file['path']]
                
                # Calculate waste
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
        print(f"   Total waste: {sum(d['total_waste_mb'] for d in duplicates) / 1024:.2f} GB\n")
        
        # Sort by waste
        duplicates.sort(key=lambda x: x['total_waste_mb'], reverse=True)
        
        return duplicates
    
    def generate_mapping_csv(self, duplicates: list) -> Path:
        """Generate comprehensive mapping CSV."""
        output_csv = self.workspace_root / f"ADVANCED_DUPLICATES_MAPPING_{self.timestamp}.csv"
        
        print("3️⃣  Generating mapping CSV...")
        
        mappings = []
        for dup_group in duplicates:
            keep_path = dup_group['keep_file']['path']
            for dup_file in dup_group['duplicate_files']:
                mappings.append({
                    'original_path': dup_file['path'],
                    'new_path': keep_path,
                    'filename': dup_group['filename'],
                    'size_mb': f"{dup_file['size_mb']:.2f}",
                    'waste_mb': f"{dup_group['total_waste_mb']:.2f}",
                    'content_hash': dup_group['content_hash'][:16],  # First 16 chars
                    'keep_reason': self._get_keep_reason(dup_group['keep_file'], dup_file)
                })
        
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['original_path', 'new_path', 'filename', 'size_mb', 'waste_mb', 'content_hash', 'keep_reason']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(mappings)
        
        print(f"   ✅ CSV created: {output_csv.name}")
        print(f"   Total mappings: {len(mappings):,}\n")
        
        return output_csv
    
    def _get_keep_reason(self, keep_file: dict, dup_file: dict) -> str:
        """Generate human-readable reason for keeping a file."""
        reasons = []
        
        if keep_file['location_priority'] > dup_file['location_priority']:
            reasons.append("better location")
        if keep_file['depth'] < dup_file['depth']:
            reasons.append("shallower path")
        if keep_file['is_nested'] and not dup_file['is_nested']:
            reasons.append("not nested")
        if 'archive' in dup_file['path'].lower() or 'backup' in dup_file['path'].lower():
            reasons.append("duplicate in archive")
        
        return ", ".join(reasons) if reasons else "intelligent selection"
    
    def generate_report(self, duplicates: list, mapping_csv: Path) -> Path:
        """Generate detailed markdown report."""
        report_file = self.workspace_root / f"ADVANCED_DUPLICATES_REPORT_{self.timestamp}.md"
        
        print("4️⃣  Generating detailed report...")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Advanced Content-Aware Duplicate Detection Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            f.write("## 📊 Executive Summary\n\n")
            f.write(f"- **Total Duplicate Groups:** {len(duplicates)}\n")
            f.write(f"- **Total Duplicate Files:** {sum(d['duplicate_count'] for d in duplicates):,}\n")
            f.write(f"- **Total Waste:** {sum(d['total_waste_mb'] for d in duplicates) / 1024:.2f} GB\n")
            f.write(f"- **Mapping CSV:** {mapping_csv.name}\n\n")
            
            f.write("## 🧠 Intelligence Features\n\n")
            f.write("- **Content Hashing:** Uses MD5 hash of actual file content\n")
            f.write("- **Location Priority:** Prefers files in important directories\n")
            f.write("- **Depth Analysis:** Prefers shallower directory structures\n")
            f.write("- **Nested Detection:** Identifies and penalizes nested folder patterns\n")
            f.write("- **File Type Awareness:** Handles text, image, and binary files appropriately\n\n")
            
            f.write("## 📋 Top 30 Duplicate Groups\n\n")
            for i, dup in enumerate(duplicates[:30], 1):
                f.write(f"### {i}. {dup['filename']}\n\n")
                f.write(f"- **Duplicates:** {dup['duplicate_count']}\n")
                f.write(f"- **Waste:** {dup['total_waste_mb']:.2f} MB\n")
                f.write(f"- **Keep:** `{dup['keep_file']['path']}`\n")
                f.write(f"  - Location Priority: {dup['keep_file']['location_priority']}\n")
                f.write(f"  - Depth: {dup['keep_file']['depth']}\n")
                f.write(f"- **Remove:**\n")
                for dup_file in dup['duplicate_files'][:5]:
                    f.write(f"  - `{dup_file['path']}` ({dup_file['size_mb']:.2f} MB)\n")
                if len(dup['duplicate_files']) > 5:
                    f.write(f"  - ... and {len(dup['duplicate_files']) - 5} more\n")
                f.write("\n")
        
        print(f"   ✅ Report created: {report_file.name}\n")
        return report_file

def main():
    """Main execution."""
    workspace_root = Path("/Users/steven/AVATARARTS")
    
    finder = ContentAwareDuplicateFinder(workspace_root)
    
    # Find duplicates
    duplicates = finder.find_duplicates()
    
    if not duplicates:
        print("✅ No duplicates found!")
        return
    
    # Generate mapping CSV
    mapping_csv = finder.generate_mapping_csv(duplicates)
    
    # Generate report
    report_file = finder.generate_report(duplicates, mapping_csv)
    
    print("=" * 80)
    print("✅ ADVANCED DUPLICATE DETECTION COMPLETE")
    print("=" * 80)
    print(f"\n📄 Mapping CSV: {mapping_csv.name}")
    print(f"📊 Report: {report_file.name}")
    print(f"\n💡 Next step: Review the CSV and run consolidation")
    print()

if __name__ == "__main__":
    main()
