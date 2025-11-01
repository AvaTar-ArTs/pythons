
import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_500 = 500
CONSTANT_1000 = 1000
CONSTANT_1024 = 1024

#!/usr/bin/env python3
"""
Deep ZIP Directory Content Awareness Analyzer
Comprehensive analysis of large ZIP collections with deep folder scanning
"""

import os
import zipfile
import json
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import re
from collections import defaultdict, Counter
import mimetypes

class DeepZipAnalyzer:
    def __init__(self, zip_dir=None):
        self.zip_dir = Path(zip_dir or Path("/Volumes/2T-Xx/zip"))
        self.analysis_dir = self.zip_dir / "00_analysis"
        self.analysis_dir.mkdir(exist_ok=True)
        
        # Analysis results
        self.results = {
            'total_files': 0,
            'total_directories': 0,
            'total_size': 0,
            'file_types': Counter(),
            'duplicate_files': [],
            'large_files': [],
            'zip_files': [],
            'directory_structure': {},
            'content_categories': defaultdict(list),
            'optimization_opportunities': []
        }
    
    def analyze_directory_structure(self):
        """Analyze the deep directory structure"""
        logger.info("📁 Analyzing Directory Structure (Deep Scan)")
        logger.info("=" * 60)
        
        structure = {}
        total_files = 0
        total_dirs = 0
        total_size = 0
        
        for root, dirs, files in os.walk(self.zip_dir):
            # Skip analysis directory
            if '00_analysis' in root:
                continue
                
            rel_path = os.path.relpath(root, self.zip_dir)
            if rel_path == '.':
                rel_path = 'root'
            
            # Count files and size
            file_count = len(files)
            dir_count = len(dirs)
            dir_size = sum(os.path.getsize(os.path.join(root, f)) for f in files if os.path.isfile(os.path.join(root, f)))
            
            structure[rel_path] = {
                'files': file_count,
                'directories': dir_count,
                'size': dir_size,
                'depth': len(rel_path.split(os.sep)) if rel_path != 'root' else 0
            }
            
            total_files += file_count
            total_dirs += dir_count
            total_size += dir_size
        
        self.results['total_files'] = total_files
        self.results['total_directories'] = total_dirs
        self.results['total_size'] = total_size
        self.results['directory_structure'] = structure
        
        logger.info(f"📊 Structure Analysis Complete:")
        logger.info(f"  📁 Total directories: {total_dirs}")
        logger.info(f"  📄 Total files: {total_files}")
        logger.info(f"  💾 Total size: {self.format_size(total_size)}")
        logger.info(f"  📏 Max depth: {max(s['depth'] for s in structure.values())}")
        
        return structure
    
    def analyze_file_types(self):
        """Analyze file types and extensions"""
        logger.info("\n📄 Analyzing File Types")
        logger.info("=" * 60)
        
        file_types = Counter()
        large_files = []
        zip_files = []
        
        for root, dirs, files in os.walk(self.zip_dir):
            if '00_analysis' in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Get file extension
                    ext = Path(file).suffix.lower()
                    if not ext:
                        ext = 'no_extension'
                    
                    file_types[ext] += 1
                    
                    # Get file size
                    file_size = os.path.getsize(file_path)
                    
                    # Track large files (>100MB)
                    if file_size > CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024:
                        large_files.append({
                            'path': file_path,
                            'size': file_size,
                            'extension': ext
                        })
                    
                    # Track ZIP files
                    if ext == '.zip':
                        zip_files.append({
                            'path': file_path,
                            'size': file_size,
                            'name': file
                        })
                        
                except (OSError, IOError):
                    continue
        
        self.results['file_types'] = file_types
        self.results['large_files'] = large_files
        self.results['zip_files'] = zip_files
        
        logger.info(f"📊 File Type Analysis Complete:")
        logger.info(f"  📄 File types found: {len(file_types)}")
        logger.info(f"  📦 ZIP files: {len(zip_files)}")
        logger.info(f"  📏 Large files (>100MB): {len(large_files)}")
        
        # Show top file types
        logger.info(f"\n🔝 Top 10 File Types:")
        for ext, count in file_types.most_common(10):
            logger.info(f"  {ext}: {count:,} files")
        
        return file_types, large_files, zip_files
    
    def find_duplicates(self):
        """Find duplicate files using hash comparison"""
        logger.info("\n🔄 Finding Duplicates (Hash-based)")
        logger.info("=" * 60)
        
        file_hashes = defaultdict(list)
        duplicates = []
        
        logger.info("  🔍 Computing file hashes...")
        processed = 0
        
        for root, dirs, files in os.walk(self.zip_dir):
            if '00_analysis' in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Compute MD5 hash
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    
                    file_hashes[file_hash].append({
                        'path': file_path,
                        'name': file,
                        'size': os.path.getsize(file_path)
                    })
                    
                    processed += 1
                    if processed % CONSTANT_1000 == 0:
                        logger.info(f"    Processed {processed:,} files...")
                        
                except (OSError, IOError):
                    continue
        
        # Find duplicates
        for file_hash, files in file_hashes.items():
            if len(files) > 1:
                # Sort by size (keep largest) and path length (keep shortest)
                files.sort(key=lambda x: (-x['size'], len(x['path'])))
                
                duplicates.append({
                    'hash': file_hash,
                    'count': len(files),
                    'total_size': sum(f['size'] for f in files),
                    'files': files,
                    'keep': files[0],  # Keep the largest/shortest path
                    'remove': files[1:]  # Remove the rest
                })
        
        self.results['duplicate_files'] = duplicates
        
        logger.info(f"📊 Duplicate Analysis Complete:")
        logger.info(f"  🔄 Duplicate groups: {len(duplicates)}")
        logger.info(f"  📄 Duplicate files: {sum(d['count'] for d in duplicates)}")
        logger.info(f"  💾 Space wasted: {self.format_size(sum(d['total_size'] - d['keep']['size'] for d in duplicates))}")
        
        return duplicates
    
    def categorize_content(self):
        """Categorize content based on filenames and paths"""
        logger.info("\n🏷️  Categorizing Content")
        logger.info("=" * 60)
        
        categories = defaultdict(list)
        
        # Define category patterns
        category_patterns = {
            'halloween': ['halloween', 'spooky', 'witch', 'ghost', 'skeleton', 'pumpkin'],
            'christmas': ['christmas', 'xmas', 'santa', 'reindeer', 'snowman', 'holiday'],
            'valentine': ['valentine', 'love', 'heart', 'romance', 'couple'],
            'birthday': ['birthday', 'party', 'celebration', 'cake', 'balloon'],
            'baby': ['baby', 'infant', 'newborn', 'toddler', 'kids', 'child'],
            'wedding': ['wedding', 'bride', 'groom', 'marriage', 'ceremony'],
            'graduation': ['graduation', 'graduate', 'diploma', 'cap', 'gown'],
            'business': ['business', 'corporate', 'office', 'professional', 'work'],
            'sports': ['sports', 'football', 'basketball', 'soccer', 'baseball', 'gym'],
            'animals': ['animal', 'dog', 'cat', 'pet', 'wildlife', 'zoo'],
            'nature': ['nature', 'forest', 'mountain', 'ocean', 'landscape', 'garden'],
            'vintage': ['vintage', 'retro', 'classic', 'old', 'antique'],
            'modern': ['modern', 'contemporary', 'minimalist', 'clean', 'simple'],
            'funny': ['funny', 'humor', 'joke', 'comedy', 'laugh', 'silly'],
            'inspirational': ['inspire', 'motivation', 'quote', 'positive', 'success']
        }
        
        for root, dirs, files in os.walk(self.zip_dir):
            if '00_analysis' in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                file_lower = file.lower()
                path_lower = root.lower()
                
                # Check each category
                for category, patterns in category_patterns.items():
                    if any(pattern in file_lower or pattern in path_lower for pattern in patterns):
                        categories[category].append({
                            'path': file_path,
                            'name': file,
                            'size': os.path.getsize(file_path) if os.path.isfile(file_path) else 0
                        })
                        break
                else:
                    # Uncategorized
                    categories['uncategorized'].append({
                        'path': file_path,
                        'name': file,
                        'size': os.path.getsize(file_path) if os.path.isfile(file_path) else 0
                    })
        
        self.results['content_categories'] = dict(categories)
        
        logger.info(f"📊 Content Categorization Complete:")
        for category, files in categories.items():
            total_size = sum(f['size'] for f in files)
            logger.info(f"  {category.title()}: {len(files):,} files ({self.format_size(total_size)})")
        
        return categories
    
    def analyze_zip_files(self):
        """Analyze ZIP files for content and optimization opportunities"""
        logger.info("\n📦 Analyzing ZIP Files")
        logger.info("=" * 60)
        
        zip_analysis = []
        
        for zip_info in self.results['zip_files']:
            zip_path = zip_info['path']
            logger.info(f"  🔍 Analyzing {zip_info['name']}...")
            
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    file_list = zip_file.namelist()
                    
                    # Basic stats
                    total_files = len(file_list)
                    total_size = sum(info.file_size for info in zip_file.infolist())
                    compression_ratio = (1 - zip_info['size'] / total_size) * CONSTANT_100 if total_size > 0 else 0
                    
                    # File type analysis
                    file_types = Counter()
                    for file_name in file_list:
                        ext = Path(file_name).suffix.lower()
                        file_types[ext] += 1
                    
                    # Content analysis
                    content_keywords = []
                    for file_name in file_list:
                        name_lower = file_name.lower()
                        if any(kw in name_lower for kw in ['design', 'template', 'mockup', 'bundle']):
                            content_keywords.append('design')
                        if any(kw in name_lower for kw in ['svg', 'png', 'jpg', 'jpeg']):
                            content_keywords.append('graphics')
                        if any(kw in name_lower for kw in ['psd', 'ai', 'eps']):
                            content_keywords.append('source')
                    
                    zip_analysis.append({
                        'name': zip_info['name'],
                        'path': zip_path,
                        'size': zip_info['size'],
                        'files_inside': total_files,
                        'uncompressed_size': total_size,
                        'compression_ratio': compression_ratio,
                        'file_types': dict(file_types),
                        'content_keywords': list(set(content_keywords)),
                        'recommendation': self.get_zip_recommendation(total_size, compression_ratio, file_types)
                    })
                    
            except Exception as e:
                zip_analysis.append({
                    'name': zip_info['name'],
                    'path': zip_path,
                    'size': zip_info['size'],
                    'error': str(e),
                    'recommendation': 'skip'
                })
        
        logger.info(f"📊 ZIP Analysis Complete:")
        logger.info(f"  📦 ZIPs analyzed: {len(zip_analysis)}")
        logger.info(f"  ✅ Successful: {len([z for z in zip_analysis if 'error' not in z])}")
        logger.info(f"  ❌ Errors: {len([z for z in zip_analysis if 'error' in z])}")
        
        return zip_analysis
    
    def get_zip_recommendation(self, uncompressed_size, compression_ratio, file_types):
        """Get recommendation for ZIP file handling"""
        if uncompressed_size > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024:  # 500MB
            return 'extract_and_organize'
        elif uncompressed_size > CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024:  # 100MB
            if compression_ratio > 50:
                return 'keep_zipped'
            else:
                return 'extract'
        elif uncompressed_size > 10 * CONSTANT_1024 * CONSTANT_1024:  # 10MB
            if 'design' in file_types or 'graphics' in file_types:
                return 'extract'
            else:
                return 'keep_zipped'
        else:
            return 'keep_zipped'
    
    def identify_optimization_opportunities(self):
        """Identify optimization opportunities"""
        logger.info("\n🎯 Identifying Optimization Opportunities")
        logger.info("=" * 60)
        
        opportunities = []
        
        # Duplicate removal opportunities
        duplicate_savings = sum(d['total_size'] - d['keep']['size'] for d in self.results['duplicate_files'])
        if duplicate_savings > 0:
            opportunities.append({
                'type': 'duplicate_removal',
                'description': f'Remove {len(self.results["duplicate_files"])} duplicate groups',
                'files_affected': sum(d['count'] for d in self.results['duplicate_files']),
                'space_savings': duplicate_savings,
                'priority': 'high'
            })
        
        # Large file optimization
        large_files = [f for f in self.results['large_files'] if f['size'] > CONSTANT_500 * CONSTANT_1024 * CONSTANT_1024]
        if large_files:
            opportunities.append({
                'type': 'large_file_optimization',
                'description': f'Optimize {len(large_files)} large files (>500MB)',
                'files_affected': len(large_files),
                'space_savings': 0,  # Unknown without analysis
                'priority': 'medium'
            })
        
        # ZIP extraction opportunities
        zip_files = [z for z in self.results['zip_files'] if z['size'] > CONSTANT_100 * CONSTANT_1024 * CONSTANT_1024]
        if zip_files:
            opportunities.append({
                'type': 'zip_extraction',
                'description': f'Extract content from {len(zip_files)} large ZIP files',
                'files_affected': len(zip_files),
                'space_savings': 0,  # Unknown without analysis
                'priority': 'medium'
            })
        
        # Directory consolidation
        deep_dirs = [d for d in self.results['directory_structure'].items() if d[1]['depth'] > 5]
        if deep_dirs:
            opportunities.append({
                'type': 'directory_consolidation',
                'description': f'Consolidate {len(deep_dirs)} deeply nested directories',
                'files_affected': sum(d[1]['files'] for d in deep_dirs),
                'space_savings': 0,
                'priority': 'low'
            })
        
        self.results['optimization_opportunities'] = opportunities
        
        logger.info(f"📊 Optimization Opportunities Found:")
        for opp in opportunities:
            logger.info(f"  {opp['priority'].upper()}: {opp['description']}")
            if opp['space_savings'] > 0:
                logger.info(f"    💾 Space savings: {self.format_size(opp['space_savings'])}")
        
        return opportunities
    
    def format_size(self, size_bytes):
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < CONSTANT_1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= CONSTANT_1024.0
        return f"{size_bytes:.1f} PB"
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        logger.info("\n📋 Generating Comprehensive Report")
        logger.info("=" * 60)
        
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'directory_path': str(self.zip_dir),
            'summary': {
                'total_files': self.results['total_files'],
                'total_directories': self.results['total_directories'],
                'total_size': self.results['total_size'],
                'formatted_size': self.format_size(self.results['total_size'])
            },
            'file_analysis': {
                'file_types': dict(self.results['file_types']),
                'large_files': self.results['large_files'],
                'zip_files': self.results['zip_files']
            },
            'duplicate_analysis': {
                'duplicate_groups': len(self.results['duplicate_files']),
                'duplicate_files': sum(d['count'] for d in self.results['duplicate_files']),
                'space_wasted': sum(d['total_size'] - d['keep']['size'] for d in self.results['duplicate_files']),
                'duplicates': self.results['duplicate_files']
            },
            'content_categories': dict(self.results['content_categories']),
            'optimization_opportunities': self.results['optimization_opportunities'],
            'directory_structure': self.results['directory_structure']
        }
        
        # Save detailed report
        report_file = self.analysis_dir / f"deep_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate summary report
        summary_file = self.analysis_dir / f"analysis_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self.generate_markdown_summary(summary_file, report)
        
        logger.info(f"📋 Reports saved:")
        logger.info(f"  📄 Detailed JSON: {report_file}")
        logger.info(f"  📄 Summary MD: {summary_file}")
        
        return report
    
    def generate_markdown_summary(self, output_file, report):
        """Generate markdown summary report"""
        with open(output_file, 'w') as f:
            f.write("# Deep ZIP Directory Analysis Report\n\n")
            f.write(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Directory**: {self.zip_dir}\n\n")
            
            # Summary
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Files**: {report['summary']['total_files']:,}\n")
            f.write(f"- **Total Directories**: {report['summary']['total_directories']:,}\n")
            f.write(f"- **Total Size**: {report['summary']['formatted_size']}\n\n")
            
            # File types
            f.write("## 📄 File Types\n\n")
            f.write("| Extension | Count |\n")
            f.write("|-----------|-------|\n")
            for ext, count in sorted(report['file_analysis']['file_types'].items(), key=lambda x: x[1], reverse=True)[:20]:
                f.write(f"| {ext} | {count:,} |\n")
            f.write(Path("\n"))
            
            # Duplicates
            f.write("## 🔄 Duplicates\n\n")
            f.write(f"- **Duplicate Groups**: {report['duplicate_analysis']['duplicate_groups']}\n")
            f.write(f"- **Duplicate Files**: {report['duplicate_analysis']['duplicate_files']}\n")
            f.write(f"- **Space Wasted**: {self.format_size(report['duplicate_analysis']['space_wasted'])}\n\n")
            
            # Content categories
            f.write("## 🏷️ Content Categories\n\n")
            f.write("| Category | Files | Size |\n")
            f.write("|----------|-------|------|\n")
            for category, files in report['content_categories'].items():
                total_size = sum(f['size'] for f in files)
                f.write(f"| {category.title()} | {len(files):,} | {self.format_size(total_size)} |\n")
            f.write(Path("\n"))
            
            # Optimization opportunities
            f.write("## 🎯 Optimization Opportunities\n\n")
            for opp in report['optimization_opportunities']:
                f.write(f"### {opp['type'].replace('_', ' ').title()}\n")
                f.write(f"- **Priority**: {opp['priority'].upper()}\n")
                f.write(f"- **Description**: {opp['description']}\n")
                f.write(f"- **Files Affected**: {opp['files_affected']:,}\n")
                if opp['space_savings'] > 0:
                    f.write(f"- **Space Savings**: {self.format_size(opp['space_savings'])}\n")
                f.write(Path("\n"))
    
    def run_comprehensive_analysis(self):
        """Run complete comprehensive analysis"""
        logger.info("🔍 Deep ZIP Directory Content Awareness Analysis")
        logger.info("=" * 80)
        logger.info(f"📁 Target Directory: {self.zip_dir}")
        logger.info(f"💾 Directory Size: {self.format_size(sum(os.path.getsize(os.path.join(root, file)) for root, dirs, files in os.walk(self.zip_dir) for file in files if os.path.isfile(os.path.join(root, file))))}")
        logger.info("=" * 80)
        
        # Run all analyses
        self.analyze_directory_structure()
        self.analyze_file_types()
        self.find_duplicates()
        self.categorize_content()
        self.analyze_zip_files()
        self.identify_optimization_opportunities()
        
        # Generate reports
        report = self.generate_comprehensive_report()
        
        logger.info(f"\n🎉 Analysis Complete!")
        logger.info(f"📊 Total files analyzed: {self.results['total_files']:,}")
        logger.info(f"💾 Total size analyzed: {self.format_size(self.results['total_size'])}")
        logger.info(f"🔄 Duplicates found: {len(self.results['duplicate_files'])} groups")
        logger.info(f"🎯 Optimization opportunities: {len(self.results['optimization_opportunities'])}")
        
        return report

if __name__ == "__main__":
    analyzer = DeepZipAnalyzer()
    analyzer.run_comprehensive_analysis()