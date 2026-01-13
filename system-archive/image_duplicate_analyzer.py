#!/usr/bin/env python3
"""
Image Duplicate Analyzer using Imagga API and Perceptual Hashing
"""
import os
import sys
import json
import hashlib
import requests
from pathlib import Path
from collections import defaultdict
from PIL import Image
import imagehash

# Load API credentials from env.d
IMAGGA_API_KEY = "acc_b34408ccf42563d"
IMAGGA_API_SECRET = "1dd859796390b5910b239c9c7b854b96"

class ImageAnalyzer:
    def __init__(self, directory, exclude_dirs=None):
        self.directory = Path(directory)
        self.exclude_dirs = exclude_dirs or []
        self.duplicates = defaultdict(list)
        self.similar_images = []
        self.image_tags = {}
    
    def should_skip(self, path):
        """Check if path should be skipped based on exclude list"""
        for exclude in self.exclude_dirs:
            if exclude in str(path):
                return True
        return False
        
    def find_exact_duplicates(self):
        """Find exact duplicates using MD5 hash"""
        print("🔍 Finding exact duplicates...")
        print(f"⚠️  Excluding directories: {', '.join(self.exclude_dirs)}")
        hashes = defaultdict(list)
        
        for img_path in self.directory.rglob('*'):
            if self.should_skip(img_path):
                continue
            if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
                try:
                    with open(img_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                        hashes[file_hash].append(str(img_path))
                except Exception as e:
                    continue
        
        # Filter to only duplicates
        self.duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
        return self.duplicates
    
    def find_similar_images(self, threshold=5):
        """Find similar images using perceptual hashing"""
        print("🔍 Finding similar images (this may take a while)...")
        image_hashes = {}
        
        image_files = list(self.directory.rglob('*'))
        image_files = [f for f in image_files if not self.should_skip(f) and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']]
        
        # Limit to first 1000 for performance
        if len(image_files) > 1000:
            print(f"⚠️  Found {len(image_files)} images, analyzing first 1000 for performance")
            image_files = image_files[:1000]
        
        for img_path in image_files:
            try:
                img = Image.open(img_path)
                # Calculate perceptual hash
                img_hash = imagehash.average_hash(img)
                image_hashes[str(img_path)] = img_hash
            except Exception as e:
                continue
        
        # Find similar images
        checked = set()
        for path1, hash1 in image_hashes.items():
            for path2, hash2 in image_hashes.items():
                if path1 >= path2:
                    continue
                pair = tuple(sorted([path1, path2]))
                if pair in checked:
                    continue
                checked.add(pair)
                
                # Calculate hash difference
                diff = hash1 - hash2
                if diff <= threshold:
                    self.similar_images.append({
                        'image1': path1,
                        'image2': path2,
                        'similarity': threshold - diff,
                        'difference': diff
                    })
        
        return self.similar_images
    
    def analyze_with_imagga(self, sample_size=20):
        """Use Imagga API to tag and categorize images"""
        print(f"🤖 Analyzing {sample_size} sample images with Imagga API...")
        
        image_files = list(self.directory.rglob('*'))
        image_files = [f for f in image_files if not self.should_skip(f) and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
        
        # Sample images
        import random
        if len(image_files) > sample_size:
            image_files = random.sample(image_files, sample_size)
        
        for img_path in image_files:
            try:
                # Upload to Imagga
                with open(img_path, 'rb') as f:
                    response = requests.post(
                        'https://api.imagga.com/v2/tags',
                        auth=(IMAGGA_API_KEY, IMAGGA_API_SECRET),
                        files={'image': f}
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    tags = [tag['tag']['en'] for tag in result.get('result', {}).get('tags', [])[:5]]
                    self.image_tags[str(img_path)] = tags
                    print(f"  ✓ {img_path.name}: {', '.join(tags)}")
                else:
                    print(f"  ✗ API Error for {img_path.name}: {response.status_code}")
                    
            except Exception as e:
                print(f"  ✗ Error analyzing {img_path.name}: {str(e)}")
        
        return self.image_tags
    
    def generate_report(self):
        """Generate analysis report"""
        report = {
            'total_images': len(list(self.directory.rglob('*.[jp][pn]g'))),
            'exact_duplicates': len(self.duplicates),
            'similar_images': len(self.similar_images),
            'duplicates_detail': self.duplicates,
            'similar_detail': self.similar_images[:50],  # Limit output
            'image_tags': self.image_tags
        }
        
        # Save to file
        report_path = self.directory / 'image_analysis_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📊 Report saved to: {report_path}")
        return report

def main():
    pictures_dir = "/Users/steven/Pictures"
    exclude_dirs = ['etsy', 'cLeanShoT']  # Exclude etsy and cLeanShoT folders from analysis
    
    print("=" * 60)
    print("🖼️  IMAGE DUPLICATE ANALYZER")
    print("=" * 60)
    print(f"\nAnalyzing: {pictures_dir}")
    print(f"Excluding: {', '.join(exclude_dirs)}\n")
    
    analyzer = ImageAnalyzer(pictures_dir, exclude_dirs=exclude_dirs)
    
    # Find exact duplicates
    duplicates = analyzer.find_exact_duplicates()
    print(f"\n✅ Found {len(duplicates)} sets of exact duplicates")
    
    # Find similar images
    similar = analyzer.find_similar_images(threshold=5)
    print(f"\n✅ Found {len(similar)} pairs of similar images")
    
    # Analyze with Imagga (sample)
    # tags = analyzer.analyze_with_imagga(sample_size=10)
    # print(f"\n✅ Tagged {len(tags)} sample images")
    
    # Generate report
    report = analyzer.generate_report()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    print(f"Total Images: {report['total_images']}")
    print(f"Exact Duplicate Sets: {report['exact_duplicates']}")
    print(f"Similar Image Pairs: {report['similar_images']}")
    
    if duplicates:
        print("\n🗑️  Top Duplicate Sets:")
        for i, (hash_val, paths) in enumerate(list(duplicates.items())[:5]):
            print(f"\n  Set {i+1} ({len(paths)} copies):")
            for path in paths[:3]:
                print(f"    - {Path(path).name}")

if __name__ == "__main__":
    main()
