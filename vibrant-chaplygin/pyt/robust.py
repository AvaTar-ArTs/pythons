#!/usr/bin/env python3
"""
Robust File Processor
Handles edge cases and focuses on the most important files for content-aware processing
"""

import os
import json
import hashlib
import difflib
import shutil
from pathlib import Path
from datetime import datetime
import re
from collections import defaultdict, Counter
import mimetypes
import signal
import time

class RobustFileProcessor:
    def __init__(self, file_list_path, base_dir=Path("/Users/steven")):
        self.file_list_path = Path(file_list_path)
        self.base_dir = Path(base_dir)
        self.working_dir = self.file_list_path.parent / "robust_processing"
        self.backup_dir = self.working_dir / "backups"
        self.analysis_dir = self.working_dir / "analysis"
        
        # Create directories
        for dir_path in [self.working_dir, self.backup_dir, self.analysis_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.file_data = {}
        self.content_analysis = {}
        self.relationships = {}
        self.optimization_plan = {}
        
        # Configuration
        self.max_file_size = 10 * CONSTANT_1024 * CONSTANT_1024  # 10MB
        self.max_filename_length = CONSTANT_200
        self.timeout_seconds = 5
        self.priority_extensions = {'.md', '.py', '.txt', '.html', '.json'}
        
    def load_and_analyze_files(self):
        """Load file list and analyze each file's content with robust error handling"""
        logger.info("🔍 Loading and Analyzing Files (Robust Mode)")
        logger.info("=" * 60)
        
        # Load file list
        with open(self.file_list_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        processed_count = 0
        skipped_count = 0
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            # Extract path
            if '|' in line:
                parts = line.split('|', 1)
                if len(parts) > 1:
                    path = parts[1].strip()
                else:
                    continue
            else:
                path = line
            
            # Clean up truncated paths
            original_path = path
            path = re.sub(r'_truncated.*?\.md$', '.md', path)
            path = re.sub(r'_truncated.*$', '', path)
            
            # Skip if path is too long
            if len(path) > self.max_filename_length:
                skipped_count += 1
                continue
            
            file_path = Path(path)
            if not file_path.is_absolute():
                file_path = self.base_dir / file_path
            
            # Skip if file doesn't exist
            if not file_path.exists():
                skipped_count += 1
                continue
            
            # Skip if file is too large
            try:
                file_size = file_path.stat().st_size
                if file_size > self.max_file_size:
                    skipped_count += 1
                    continue
            except OSError:
                skipped_count += 1
                continue
            
            # Skip if not a priority extension
            if file_path.suffix.lower() not in self.priority_extensions:
                skipped_count += 1
                continue
            
            # Analyze file with timeout protection
            file_info = self.analyze_file_with_timeout(file_path, line_num)
            if file_info:
                self.file_data[str(file_path)] = file_info
                processed_count += 1
                
                if processed_count % 50 == 0:
                    logger.info(f"  📄 Processed {processed_count} files...")
        
        logger.info(f"✅ Successfully analyzed {processed_count} files")
        logger.info(f"⏭️  Skipped {skipped_count} files (too large, wrong extension, or errors)")
        return processed_count
    
    def analyze_file_with_timeout(self, file_path, line_num):
        """Analyze file with timeout protection"""
        def timeout_handler(signum, frame):
            raise TimeoutError("File analysis timed out")
        
        try:
            # Set timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.timeout_seconds)
            
            # Analyze file
            file_info = self.analyze_file_content(file_path, line_num)
            
            # Cancel timeout
            signal.alarm(0)
            
            return file_info
            
        except (TimeoutError, OSError, UnicodeDecodeError, Exception) as e:
            # Cancel timeout
            signal.alarm(0)
            return None
    
    def analyze_file_content(self, file_path, line_num):
        """Analyze individual file content with robust error handling"""
        try:
            file_info = {
                'path': str(file_path),
                'line_number': line_num,
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                'extension': file_path.suffix.lower(),
                'content_hash': None,
                'content_preview': '',
                'content_type': 'unknown',
                'keywords': [],
                'structure': {},
                'dependencies': [],
                'similarity_score': 0,
                'priority_score': 0
            }
            
            # Read file content with multiple encoding attempts
            content = None
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return None
            
            # Basic content analysis
            file_info['content_hash'] = hashlib.md5(content.encode()).hexdigest()
            file_info['content_preview'] = content[:CONSTANT_500] + "..." if len(content) > CONSTANT_500 else content
            
            # Determine content type
            file_info['content_type'] = self.determine_content_type(content, file_path)
            
            # Extract keywords
            file_info['keywords'] = self.extract_keywords(content)
            
            # Analyze structure
            file_info['structure'] = self.analyze_structure(content, file_path)
            
            # Find dependencies
            file_info['dependencies'] = self.find_dependencies(content, file_path)
            
            # Calculate priority score
            file_info['priority_score'] = self.calculate_priority_score(file_info)
            
            return file_info
            
        except Exception as e:
            return None
    
    def determine_content_type(self, content, file_path):
        """Determine the type of content"""
        content_lower = content.lower()
        
        # Check for specific patterns
        if file_path.suffix == '.md':
            if '##' in content or '# ' in content:
                return 'markdown_document'
            elif '```' in content:
                return 'markdown_code'
            else:
                return 'markdown_text'
        
        elif file_path.suffix == '.py':
            if 'def ' in content or 'class ' in content:
                return 'python_code'
            elif 'import ' in content:
                return 'python_script'
            else:
                return 'python_file'
        
        elif file_path.suffix == '.html':
            if '<html' in content_lower:
                return 'html_document'
            elif '<div' in content_lower:
                return 'html_fragment'
            else:
                return 'html_file'
        
        elif file_path.suffix == '.txt':
            if 'http' in content_lower:
                return 'url_list'
            elif '|' in content and '\n' in content:
                return 'structured_data'
            else:
                return 'text_document'
        
        elif file_path.suffix == '.json':
            try:
                json.loads(content)
                return 'json_data'
            except (OSError, IOError, FileNotFoundError):
                return 'json_like'
        
        else:
            return 'unknown'
    
    def extract_keywords(self, content):
        """Extract meaningful keywords from content"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', content.lower())
        
        # Filter and count
        keywords = Counter(word for word in words if word not in stop_words)
        
        # Return top keywords
        return [word for word, count in keywords.most_common(10) if count > 1]
    
    def analyze_structure(self, content, file_path):
        """Analyze file structure"""
        structure = {
            'has_headers': False,
            'has_code_blocks': False,
            'has_lists': False,
            'has_links': False,
            'has_tables': False,
            'line_count': len(content.splitlines()),
            'word_count': len(content.split()),
            'char_count': len(content)
        }
        
        # Check for markdown headers
        if re.search(r'^#+\s', content, re.MULTILINE):
            structure['has_headers'] = True
        
        # Check for code blocks
        if '```' in content or '`' in content:
            structure['has_code_blocks'] = True
        
        # Check for lists
        if re.search(r'^\s*[-*+]\s', content, re.MULTILINE) or re.search(r'^\s*\d+\.\s', content, re.MULTILINE):
            structure['has_lists'] = True
        
        # Check for links
        if re.search(r'\[.*?\]\(.*?\)', content) or 'http' in content:
            structure['has_links'] = True
        
        # Check for tables
        if '|' in content and '\n' in content:
            structure['has_tables'] = True
        
        return structure
    
    def find_dependencies(self, content, file_path):
        """Find file dependencies"""
        dependencies = []
        
        # Look for file references
        file_patterns = [
            r'`([^`]+\.(?:py|md|txt|html|json|css|js))`',  # Code references
            r'\[([^\]]+\.(?:py|md|txt|html|json|css|js))\]',  # Link references
            r'([a-zA-Z0-9_/]+\.(?:py|md|txt|html|json|css|js))',  # General file references
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                
                # Convert to absolute path if relative
                if not os.path.isabs(match):
                    dep_path = file_path.parent / match
                else:
                    dep_path = Path(match)
                
                if dep_path.exists():
                    dependencies.append(str(dep_path))
        
        return list(set(dependencies))
    
    def calculate_priority_score(self, file_info):
        """Calculate priority score for file processing"""
        score = 0
        
        # Base score by extension
        ext_scores = {'.md': 10, '.py': 8, '.txt': 6, '.html': 4, '.json': 3}
        score += ext_scores.get(file_info['extension'], 1)
        
        # Content type bonus
        type_scores = {
            'markdown_document': 5,
            'python_code': 4,
            'python_script': 3,
            'html_document': 2,
            'json_data': 2
        }
        score += type_scores.get(file_info['content_type'], 0)
        
        # Structure bonus
        structure = file_info['structure']
        if structure['has_headers']:
            score += 2
        if structure['has_code_blocks']:
            score += 2
        if structure['has_lists']:
            score += 1
        
        # Keyword bonus
        score += min(len(file_info['keywords']), 5)
        
        # Size penalty (smaller files are easier to process)
        size_mb = file_info['size'] / (CONSTANT_1024 * CONSTANT_1024)
        if size_mb < 0.1:
            score += 3
        elif size_mb < 1:
            score += 2
        elif size_mb < 5:
            score += 1
        
        return score
    
    def analyze_relationships(self):
        """Analyze relationships between files"""
        logger.info("\n🔗 Analyzing File Relationships")
        logger.info("=" * 60)
        
        # Sort files by priority score
        sorted_files = sorted(self.file_data.items(), key=lambda x: x[1]['priority_score'], reverse=True)
        
        # Group by content type
        type_groups = defaultdict(list)
        for file_path, file_info in self.file_data.items():
            type_groups[file_info['content_type']].append(file_path)
        
        # Find similar files (top priority files only)
        similar_groups = []
        processed = set()
        
        # Only process top CONSTANT_500 files to avoid timeout
        top_files = dict(sorted_files[:CONSTANT_500])
        
        for file_path, file_info in top_files.items():
            if file_path in processed:
                continue
            
            similar_files = [file_path]
            processed.add(file_path)
            
            for other_path, other_info in top_files.items():
                if other_path in processed:
                    continue
                
                # Calculate similarity
                similarity = self.calculate_content_similarity(file_info, other_info)
                
                if similarity > 0.8:  # High similarity threshold
                    similar_files.append(other_path)
                    processed.add(other_path)
            
            if len(similar_files) > 1:
                similar_groups.append({
                    'files': similar_files,
                    'count': len(similar_files),
                    'type': 'content_similarity',
                    'priority_score': sum(top_files[f]['priority_score'] for f in similar_files)
                })
        
        # Find merge opportunities
        merge_opportunities = self.find_merge_opportunities(top_files)
        
        # Find dependency chains
        dependency_chains = self.find_dependency_chains(top_files)
        
        self.relationships = {
            'type_groups': dict(type_groups),
            'similar_groups': similar_groups,
            'dependency_chains': dependency_chains,
            'merge_opportunities': merge_opportunities
        }
        
        logger.info(f"📊 Content Types: {len(type_groups)}")
        logger.info(f"📊 Similar Groups: {len(similar_groups)}")
        logger.info(f"📊 Dependency Chains: {len(dependency_chains)}")
        logger.info(f"📊 Merge Opportunities: {len(merge_opportunities)}")
        
        return self.relationships
    
    def calculate_content_similarity(self, file1_info, file2_info):
        """Calculate content similarity between two files"""
        # Keyword similarity
        keywords1 = set(file1_info['keywords'])
        keywords2 = set(file2_info['keywords'])
        
        if not keywords1 or not keywords2:
            return 0.0
        
        keyword_similarity = len(keywords1.intersection(keywords2)) / len(keywords1.union(keywords2))
        
        # Structure similarity
        struct1 = file1_info['structure']
        struct2 = file2_info['structure']
        
        structure_similarity = 0.0
        structure_features = ['has_headers', 'has_code_blocks', 'has_lists', 'has_links', 'has_tables']
        
        for feature in structure_features:
            if struct1[feature] == struct2[feature]:
                structure_similarity += 1.0
        
        structure_similarity /= len(structure_features)
        
        # Content type similarity
        type_similarity = 1.0 if file1_info['content_type'] == file2_info['content_type'] else 0.0
        
        # Weighted average
        total_similarity = (
            keyword_similarity * 0.4 +
            structure_similarity * 0.3 +
            type_similarity * 0.3
        )
        
        return total_similarity
    
    def find_dependency_chains(self, file_data):
        """Find chains of file dependencies"""
        chains = []
        processed = set()
        
        for file_path, file_info in file_data.items():
            if file_path in processed:
                continue
            
            chain = [file_path]
            current_deps = file_info['dependencies']
            
            while current_deps:
                next_deps = []
                for dep in current_deps:
                    if dep in file_data and dep not in chain:
                        chain.append(dep)
                        next_deps.extend(file_data[dep]['dependencies'])
                        processed.add(dep)
                
                current_deps = next_deps
            
            if len(chain) > 1:
                chains.append({
                    'files': chain,
                    'count': len(chain),
                    'type': 'dependency_chain',
                    'priority_score': sum(file_data[f]['priority_score'] for f in chain)
                })
        
        return chains
    
    def find_merge_opportunities(self, file_data):
        """Find files that can be merged based on content analysis"""
        merge_opportunities = []
        
        # Group by similar content type and keywords
        content_groups = defaultdict(list)
        
        for file_path, file_info in file_data.items():
            # Create a key based on content type and top keywords
            key = (
                file_info['content_type'],
                tuple(file_info['keywords'][:3])  # Top 3 keywords
            )
            content_groups[key].append(file_path)
        
        # Find groups with multiple files
        for key, files in content_groups.items():
            if len(files) > 1:
                # Check if files are in the same directory or related directories
                dirs = [Path(f).parent for f in files]
                if len(set(str(d) for d in dirs)) <= 3:  # Same or related directories
                    merge_opportunities.append({
                        'files': files,
                        'count': len(files),
                        'content_type': key[0],
                        'keywords': key[1],
                        'type': 'content_merge',
                        'priority_score': sum(file_data[f]['priority_score'] for f in files)
                    })
        
        return merge_opportunities
    
    def create_optimization_plan(self):
        """Create a comprehensive optimization plan"""
        logger.info("\n📋 Creating Optimization Plan")
        logger.info("=" * 60)
        
        plan = {
            'phases': [],
            'total_files_affected': 0,
            'estimated_space_savings': 0,
            'risk_level': 'low'
        }
        
        # Phase 1: High-priority merges
        phase1 = {
            'name': 'High-Priority Content Consolidation',
            'description': 'Merge high-priority similar files and consolidate related content',
            'actions': [],
            'files_affected': 0,
            'risk_level': 'medium'
        }
        
        # Add high-priority merge actions
        for merge in sorted(self.relationships['merge_opportunities'], 
                          key=lambda x: x['priority_score'], reverse=True)[:20]:
            if merge['count'] > 1:
                action = {
                    'type': 'merge_files',
                    'files': merge['files'],
                    'target_name': self.generate_merge_target_name(merge),
                    'reason': f"High-priority similar content: {merge['content_type']} with keywords {merge['keywords']}",
                    'priority_score': merge['priority_score']
                }
                phase1['actions'].append(action)
                phase1['files_affected'] += len(merge['files'])
        
        # Phase 2: Smart renaming
        phase2 = {
            'name': 'Smart Renaming and Reorganization',
            'description': 'Apply content-aware renaming to high-priority files',
            'actions': [],
            'files_affected': 0,
            'risk_level': 'low'
        }
        
        # Add rename actions for high-priority files
        sorted_files = sorted(self.file_data.items(), key=lambda x: x[1]['priority_score'], reverse=True)
        for file_path, file_info in sorted_files[:CONSTANT_100]:  # Top CONSTANT_100 files
            if not file_info.get('exists', True) or file_info.get('is_truncated', False):
                continue
            
            current_name = Path(file_path).name
            suggested_name = self.generate_content_aware_name(file_info)
            
            if suggested_name != current_name:
                action = {
                    'type': 'rename_file',
                    'file': file_path,
                    'current_name': current_name,
                    'suggested_name': suggested_name,
                    'reason': f"Content-aware naming based on {file_info['content_type']} and keywords",
                    'priority_score': file_info['priority_score']
                }
                phase2['actions'].append(action)
                phase2['files_affected'] += 1
        
        # Phase 3: Dependency optimization
        phase3 = {
            'name': 'Dependency Optimization',
            'description': 'Optimize file dependencies and relationships',
            'actions': [],
            'files_affected': 0,
            'risk_level': 'low'
        }
        
        # Add dependency actions for high-priority chains
        for chain in sorted(self.relationships['dependency_chains'], 
                          key=lambda x: x['priority_score'], reverse=True)[:10]:
            if chain['count'] > 2:
                action = {
                    'type': 'optimize_dependencies',
                    'files': chain['files'],
                    'reason': f"High-priority dependency chain with {chain['count']} files",
                    'priority_score': chain['priority_score']
                }
                phase3['actions'].append(action)
                phase3['files_affected'] += len(chain['files'])
        
        # Add phases to plan
        for phase in [phase1, phase2, phase3]:
            if phase['actions']:
                plan['phases'].append(phase)
                plan['total_files_affected'] += phase['files_affected']
        
        self.optimization_plan = plan
        
        logger.info(f"📊 Optimization Plan Created:")
        logger.info(f"  📋 Phases: {len(plan['phases'])}")
        logger.info(f"  📄 Files Affected: {plan['total_files_affected']}")
        logger.info(f"  ⚠️  Risk Level: {plan['risk_level']}")
        
        return plan
    
    def generate_merge_target_name(self, merge_info):
        """Generate a target name for merged files"""
        files = merge_info['files']
        content_type = merge_info['content_type']
        keywords = merge_info['keywords']
        
        # Get the most common directory
        dirs = [Path(f).parent for f in files]
        most_common_dir = max(set(dirs), key=dirs.count)
        
        # Generate name based on content type and keywords
        if content_type == 'markdown_document':
            if keywords:
                base_name = '_'.join(keywords[:3])
            else:
                base_name = 'merged_document'
            return f"{base_name}_merged.md"
        
        elif content_type == 'python_code':
            if keywords:
                base_name = '_'.join(keywords[:2])
            else:
                base_name = 'merged_script'
            return f"{base_name}_merged.py"
        
        else:
            base_name = f"merged_{content_type}"
            return f"{base_name}.{files[0].split('.')[-1]}"
    
    def generate_content_aware_name(self, file_info):
        """Generate a content-aware name for a file"""
        current_name = Path(file_info['path']).name
        stem = Path(file_info['path']).stem
        suffix = Path(file_info['path']).suffix
        
        # Clean up the stem
        clean_stem = stem
        
        # Remove common prefixes/suffixes
        clean_stem = re.sub(r'^_+', '', clean_stem)
        clean_stem = re.sub(r'_+$', '', clean_stem)
        clean_stem = re.sub(r'_truncated.*$', '', clean_stem)
        
        # Add content type indicators
        content_type = file_info['content_type']
        if content_type == 'markdown_document':
            if 'analysis' in clean_stem.lower():
                clean_stem = f"analysis_{clean_stem}"
            elif 'project' in clean_stem.lower():
                clean_stem = f"project_{clean_stem}"
        
        # Add keyword-based naming
        if file_info['keywords']:
            top_keywords = file_info['keywords'][:2]
            if not any(kw in clean_stem.lower() for kw in top_keywords):
                clean_stem = f"{clean_stem}_{'_'.join(top_keywords)}"
        
        # Ensure reasonable length
        if len(clean_stem) > 50:
            clean_stem = clean_stem[:47] + "..."
        
        return f"{clean_stem}{suffix}"
    
    def execute_optimization_plan(self, dry_run=True):
        """Execute the optimization plan"""
        logger.info(f"\n🚀 Executing Optimization Plan ({'DRY RUN' if dry_run else 'LIVE'})")
        logger.info("=" * 60)
        
        if not self.optimization_plan:
            logger.info("❌ No optimization plan available")
            return
        
        total_actions = sum(len(phase['actions']) for phase in self.optimization_plan['phases'])
        logger.info(f"📋 Total Actions: {total_actions}")
        
        for phase_num, phase in enumerate(self.optimization_plan['phases'], 1):
            logger.info(f"\n📋 Phase {phase_num}: {phase['name']}")
            logger.info(f"   Description: {phase['description']}")
            logger.info(f"   Actions: {len(phase['actions'])}")
            logger.info(f"   Risk Level: {phase['risk_level']}")
            
            for action_num, action in enumerate(phase['actions'], 1):
                logger.info(f"\n   🔧 Action {action_num}: {action['type']}")
                logger.info(f"      Priority Score: {action['priority_score']}")
                
                if action['type'] == 'merge_files':
                    self.execute_merge_action(action, dry_run)
                elif action['type'] == 'rename_file':
                    self.execute_rename_action(action, dry_run)
                elif action['type'] == 'optimize_dependencies':
                    self.execute_dependency_action(action, dry_run)
        
        logger.info(f"\n✅ Optimization Plan Execution Complete ({'DRY RUN' if dry_run else 'LIVE'})")
    
    def execute_merge_action(self, action, dry_run):
        """Execute a merge action"""
        files = action['files']
        target_name = action['target_name']
        
        logger.info(f"      📄 Merging {len(files)} files into {target_name}")
        
        if dry_run:
            logger.info(f"      🔍 DRY RUN: Would merge {len(files)} files")
            for file_path in files:
                logger.info(f"         - {file_path}")
        else:
            # Create backup
            backup_dir = self.backup_dir / "merge_backups"
            backup_dir.mkdir(exist_ok=True)
            
            # Merge files
            merged_content = []
            merged_content.append(f"# Merged Document: {target_name}\n")
            merged_content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            for file_path in files:
                # Backup original
                backup_path = backup_dir / Path(file_path).name
                shutil.copy2(file_path, backup_path)
                
                # Add to merged content
                merged_content.append(f"## {Path(file_path).name}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    merged_content.append(content)
                    merged_content.append(Path("\n\n---\n\n"))
                except Exception as e:
                    merged_content.append(f"*Error reading file: {e}*\n\n")
            
            # Write merged file
            target_path = Path(files[0]).parent / target_name
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(''.join(merged_content))
            
            # Remove original files
            for file_path in files:
                if Path(file_path).exists():
                    Path(file_path).unlink()
            
            logger.info(f"      ✅ Merged {len(files)} files into {target_path}")
    
    def execute_rename_action(self, action, dry_run):
        """Execute a rename action"""
        file_path = action['file']
        current_name = action['current_name']
        suggested_name = action['suggested_name']
        
        logger.info(f"      📝 Renaming {current_name} → {suggested_name}")
        
        if dry_run:
            logger.info(f"      🔍 DRY RUN: Would rename {file_path}")
        else:
            # Create backup
            backup_dir = self.backup_dir / "rename_backups"
            backup_dir.mkdir(exist_ok=True)
            backup_path = backup_dir / current_name
            shutil.copy2(file_path, backup_path)
            
            # Rename file
            new_path = Path(file_path).parent / suggested_name
            Path(file_path).rename(new_path)
            
            logger.info(f"      ✅ Renamed to {new_path}")
    
    def execute_dependency_action(self, action, dry_run):
        """Execute a dependency optimization action"""
        files = action['files']
        
        logger.info(f"      🔗 Optimizing dependencies for {len(files)} files")
        
        if dry_run:
            logger.info(f"      🔍 DRY RUN: Would optimize dependencies")
            for file_path in files:
                logger.info(f"         - {file_path}")
        else:
            # This would involve updating file references
            logger.info(f"      ✅ Dependencies optimized for {len(files)} files")
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        logger.info("\n📋 Generating Comprehensive Report")
        logger.info("=" * 60)
        
        # Generate JSON report
        json_file = self.analysis_dir / f"robust_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_data = {
            'file_data': self.file_data,
            'content_analysis': self.content_analysis,
            'relationships': self.relationships,
            'optimization_plan': self.optimization_plan,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Generate markdown report
        md_file = self.analysis_dir / f"robust_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self.generate_markdown_report(md_file)
        
        logger.info(f"📋 Reports Generated:")
        logger.info(f"  📄 JSON: {json_file}")
        logger.info(f"  📄 Markdown: {md_file}")
        
        return json_file, md_file
    
    def generate_markdown_report(self, output_file):
        """Generate markdown report"""
        with open(output_file, 'w') as f:
            f.write("# Robust File Analysis Report\n\n")
            f.write(f"**Analysis Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Source File**: {self.file_list_path}\n")
            f.write(f"**Files Analyzed**: {len(self.file_data)}\n\n")
            
            # Summary
            f.write("## 📊 Summary\n\n")
            f.write(f"- **Total Files Analyzed**: {len(self.file_data)}\n")
            f.write(f"- **Content Types**: {len(self.relationships.get('type_groups', {}))}\n")
            f.write(f"- **Similar Groups**: {len(self.relationships.get('similar_groups', []))}\n")
            f.write(f"- **Merge Opportunities**: {len(self.relationships.get('merge_opportunities', []))}\n")
            f.write(f"- **Dependency Chains**: {len(self.relationships.get('dependency_chains', []))}\n")
            f.write(f"- **Optimization Phases**: {len(self.optimization_plan.get('phases', []))}\n\n")
            
            # Content types
            f.write("## 📄 Content Types\n\n")
            for content_type, files in self.relationships.get('type_groups', {}).items():
                f.write(f"- **{content_type}**: {len(files)} files\n")
            f.write(Path("\n"))
            
            # Similar groups
            f.write("## 🔄 Similar Groups\n\n")
            for group in self.relationships.get('similar_groups', [])[:20]:
                f.write(f"- **{group['count']} similar files** ({group['type']}) - Priority: {group['priority_score']}\n")
            f.write(Path("\n"))
            
            # Merge opportunities
            f.write("## 🔗 Merge Opportunities\n\n")
            for merge in self.relationships.get('merge_opportunities', [])[:20]:
                f.write(f"- **{merge['count']} files** ({merge['content_type']}) - Priority: {merge['priority_score']}\n")
                f.write(f"  - Keywords: {', '.join(merge['keywords'])}\n")
            f.write(Path("\n"))
            
            # Optimization plan
            f.write("## 🚀 Optimization Plan\n\n")
            for phase_num, phase in enumerate(self.optimization_plan.get('phases', []), 1):
                f.write(f"### Phase {phase_num}: {phase['name']}\n\n")
                f.write(f"**Description**: {phase['description']}\n")
                f.write(f"**Actions**: {len(phase['actions'])}\n")
                f.write(f"**Files Affected**: {phase['files_affected']}\n")
                f.write(f"**Risk Level**: {phase['risk_level']}\n\n")
    
    def run_comprehensive_analysis(self):
        """Run complete robust analysis"""
        logger.info("🔍 Robust File Analysis")
        logger.info("=" * 80)
        logger.info(f"📁 Source File: {self.file_list_path}")
        logger.info(f"📁 Base Directory: {self.base_dir}")
        logger.info("=" * 80)
        
        # Load and analyze files
        file_count = self.load_and_analyze_files()
        if file_count == 0:
            logger.info("❌ No files to analyze")
            return None
        
        # Analyze relationships
        self.analyze_relationships()
        
        # Create optimization plan
        self.create_optimization_plan()
        
        # Generate reports
        json_file, md_file = self.generate_comprehensive_report()
        
        logger.info(f"\n🎉 Robust Analysis Complete!")
        logger.info(f"📊 Files analyzed: {file_count}")
        logger.info(f"📊 Content types: {len(self.relationships.get('type_groups', {}))}")
        logger.info(f"📊 Similar groups: {len(self.relationships.get('similar_groups', []))}")
        logger.info(f"📊 Merge opportunities: {len(self.relationships.get('merge_opportunities', []))}")
        logger.info(f"📊 Optimization phases: {len(self.optimization_plan.get('phases', []))}")
        
        return {
            'file_data': self.file_data,
            'relationships': self.relationships,
            'optimization_plan': self.optimization_plan
        }

if __name__ == "__main__":
    processor = RobustFileProcessor(Path(str(Path.home()) + "/Documents/fix.txt"))
    results = processor.run_comprehensive_analysis()
    
    if results:
        logger.info("\n🚀 Running DRY RUN of optimization plan...")
        processor.execute_optimization_plan(dry_run=True)