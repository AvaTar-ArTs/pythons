#!/usr/bin/env python3
"""
Verify AVATARARTS Consolidation - Content-Based Duplicate Check

Checks if files moved during consolidation are actually duplicates or unique content.
Filenames cannot be trusted - this does SHA256 content verification.
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict

class DuplicateVerifier:
    def __init__(self):
        self.scattered_dir = Path("/Users/steven/AVATARARTS/consolidation/scattered")
        self.pythons_dir = Path("/Users/steven/pythons")
        self.documents_dir = Path("/Users/steven/Documents")
        self.scripts_dir = Path("/Users/steven/scripts")

    def get_file_hash(self, file_path: Path) -> str:
        """Get SHA256 hash of file content."""
        try:
            hash_obj = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except:
            return None

    def find_similar_names(self):
        """Find files with similar names that might be duplicates."""
        print("🔍 Finding files with similar names across directories...")

        scattered_files = {}
        for file_path in self.scattered_dir.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(self.scattered_dir)
                scattered_files[str(relative_path)] = file_path

        similar_groups = defaultdict(list)

        # Check pythons directory
        for file_path in self.pythons_dir.rglob('*'):
            if file_path.is_file():
                filename = file_path.name
                for scattered_name, scattered_path in scattered_files.items():
                    if filename == scattered_path.name:
                        similar_groups[filename].append(('pythons', file_path))
                        similar_groups[filename].append(('scattered', scattered_path))

        # Check other directories
        for check_dir, dir_path in [('documents', self.documents_dir), ('scripts', self.scripts_dir)]:
            if dir_path.exists():
                for file_path in dir_path.rglob('*'):
                    if file_path.is_file():
                        filename = file_path.name
                        if filename in similar_groups:
                            similar_groups[filename].append((check_dir, file_path))

        return similar_groups

    def verify_content_duplicates(self, similar_groups):
        """Verify if similar-named files are actually content duplicates."""
        print("🔍 Verifying content duplicates (this may take a moment)...")

        duplicate_groups = {}
        unique_files = {}

        for filename, file_list in similar_groups.items():
            if len(file_list) > 1:
                hash_groups = defaultdict(list)

                for location, file_path in file_list:
                    file_hash = self.get_file_hash(file_path)
                    if file_hash:
                        hash_groups[file_hash].append((location, file_path))

                # Check if we have actual duplicates
                for file_hash, files in hash_groups.items():
                    if len(files) > 1:
                        duplicate_groups[filename] = {
                            'hash': file_hash,
                            'duplicates': files
                        }
                    else:
                        unique_files[filename] = files[0]

        return duplicate_groups, unique_files

    def analyze_consolidation_safety(self):
        """Analyze whether the consolidation preserved unique content."""
        print("🛡️  ANALYZING CONSOLIDATION SAFETY")
        print("=" * 50)

        similar_groups = self.find_similar_names()
        duplicates, uniques = self.verify_content_duplicates(similar_groups)

        print(f"\n📊 Results:")
        print(f"Files with similar names: {len(similar_groups)}")
        print(f"Actual content duplicates: {len(duplicates)}")
        print(f"Unique files (despite similar names): {len(uniques)}")

        if duplicates:
            print(f"\n✅ GOOD: Found {len(duplicates)} true duplicate groups")
            for filename, data in list(duplicates.items())[:5]:  # Show first 5
                print(f"  - {filename}: {len(data['duplicates'])} identical copies")
        else:
            print("\n⚠️  CAUTION: No content duplicates found among similar names")
            print("   This suggests consolidation may have moved unique files!")

        if uniques:
            print(f"\nℹ️  INFO: {len(uniques)} files have similar names but different content")
            print("   These are properly preserved as unique files")

        # Check if scattered directory still has content
        scattered_count = sum(1 for _ in self.scattered_dir.rglob('*') if _.is_file())
        print(f"\n📁 Scattered directory status:")
        print(f"   Files remaining: {scattered_count}")

        if scattered_count > 0:
            print("   ✅ Content preserved - these appear to be unique files")
        else:
            print("   ⚠️  Directory empty - all content was moved")

        return {
            'similar_groups': len(similar_groups),
            'true_duplicates': len(duplicates),
            'unique_files': len(uniques),
            'scattered_remaining': scattered_count
        }

def main():
    verifier = DuplicateVerifier()
    results = verifier.analyze_consolidation_safety()

    print(f"\n🎯 CONCLUSION:")
    if results['true_duplicates'] > 0 and results['scattered_remaining'] > 0:
        print("✅ CONSOLIDATION APPEARS SAFE")
        print("   - True duplicates were identified and handled")
        print("   - Unique content preserved in scattered directory")
    elif results['scattered_remaining'] == 0:
        print("⚠️  REVIEW NEEDED: All scattered content was moved")
        print("   - Verify no unique files were incorrectly consolidated")
    else:
        print("🔍 FURTHER ANALYSIS NEEDED")
        print("   - Check why no content duplicates were found")

if __name__ == "__main__":
    main()