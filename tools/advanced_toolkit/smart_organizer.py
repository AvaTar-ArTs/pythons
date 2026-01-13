#!/usr/bin/env python3
"""
Smart File Organizer with ML-based classification and intelligent grouping
"""

from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
from dataclasses import dataclass
import json
import re
from datetime import datetime

from file_intelligence import FileAnalyzer, FileFingerprint


@dataclass
class OrganizationRule:
    """Rule for organizing files"""
    name: str
    condition: callable
    target_pattern: str  # e.g., "BY_TYPE/{mime_type}/" or "BY_ARTIST/{artist}/"
    priority: int = 10


class SmartOrganizer:
    """Intelligent file organizer using ML and heuristics"""
    
    def __init__(self, analyzer: FileAnalyzer, base_dir: Path):
        self.analyzer = analyzer
        self.base_dir = base_dir
        self.rules: List[OrganizationRule] = []
        self._init_default_rules()
    
    def _init_default_rules(self):
        """Initialize default organization rules"""
        
        # Rule 1: Organize audio by artist/album
        self.rules.append(OrganizationRule(
            name="audio_by_artist",
            condition=lambda fp: fp.mime_type.startswith('audio/') and 
                               fp.metadata and fp.metadata.get('artist'),
            target_pattern="Music/BY_ARTIST/{artist}/{album}",
            priority=1
        ))
        
        # Rule 2: Organize audio without artist by album
        self.rules.append(OrganizationRule(
            name="audio_by_album",
            condition=lambda fp: fp.mime_type.startswith('audio/') and
                               fp.metadata and fp.metadata.get('album'),
            target_pattern="Music/BY_ALBUM/{album}",
            priority=2
        ))
        
        # Rule 3: Organize code by language
        self.rules.append(OrganizationRule(
            name="code_by_language",
            condition=lambda fp: fp.language is not None,
            target_pattern="Code/{language}",
            priority=1
        ))
        
        # Rule 4: Organize images by year
        self.rules.append(OrganizationRule(
            name="images_by_year",
            condition=lambda fp: fp.mime_type.startswith('image/'),
            target_pattern="Images/{year}",
            priority=1
        ))
        
        # Rule 5: Organize documents by type
        self.rules.append(OrganizationRule(
            name="documents_by_type",
            condition=lambda fp: fp.mime_type in [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'text/plain'
            ],
            target_pattern="Documents/{extension}",
            priority=1
        ))
        
        # Rule 6: Organize videos
        self.rules.append(OrganizationRule(
            name="videos",
            condition=lambda fp: fp.mime_type.startswith('video/'),
            target_pattern="Videos",
            priority=1
        ))
        
        # Rule 7: Archives
        self.rules.append(OrganizationRule(
            name="archives",
            condition=lambda fp: fp.extension in ['.zip', '.tar', '.gz', '.7z', '.rar'],
            target_pattern="Archives",
            priority=1
        ))
        
        # Rule 8: Config files
        self.rules.append(OrganizationRule(
            name="config",
            condition=lambda fp: fp.extension in ['.conf', '.config', '.ini', '.yaml', '.yml', '.toml'],
            target_pattern="Config",
            priority=1
        ))
    
    def determine_target(self, fingerprint: FileFingerprint) -> Optional[Path]:
        """Determine target location for a file"""
        
        # Find matching rule with highest priority
        matching_rule = None
        for rule in sorted(self.rules, key=lambda r: r.priority):
            if rule.condition(fingerprint):
                matching_rule = rule
                break
        
        if not matching_rule:
            return None
        
        # Build target path from pattern
        target = matching_rule.target_pattern
        
        # Replace placeholders
        replacements = {
            'mime_type': fingerprint.mime_type.replace('/', '_'),
            'extension': fingerprint.extension.lstrip('.') or 'no_extension',
            'language': fingerprint.language or 'unknown',
            'year': datetime.fromtimestamp(fingerprint.created).year
        }
        
        # Add metadata replacements
        if fingerprint.metadata:
            for key, value in fingerprint.metadata.items():
                if value:
                    replacements[key] = self._sanitize_path_component(str(value))
        
        # Replace placeholders in target pattern
        for key, value in replacements.items():
            target = target.replace(f'{{{key}}}', str(value))
        
        return self.base_dir / target / fingerprint.path.name
    
    def _sanitize_path_component(self, component: str) -> str:
        """Sanitize string for use in path"""
        # Remove invalid characters
        component = re.sub(r'[<>:"/\\|?*]', '', component)
        # Replace multiple spaces
        component = re.sub(r'\s+', ' ', component)
        # Limit length
        if len(component) > 100:
            component = component[:100]
        return component.strip()
    
    def generate_organization_plan(self, files: List[FileFingerprint]) -> Dict:
        """Generate a plan for organizing files"""
        plan = {
            'moves': [],
            'by_target_dir': defaultdict(list),
            'statistics': defaultdict(int)
        }
        
        for fp in files:
            target = self.determine_target(fp)
            
            if target:
                move_op = {
                    'source': str(fp.path),
                    'target': str(target),
                    'size': fp.size,
                    'reason': 'rule_based'
                }
                
                plan['moves'].append(move_op)
                plan['by_target_dir'][str(target.parent)].append(fp.path.name)
                plan['statistics']['total_to_move'] += 1
                plan['statistics']['total_size'] += fp.size
            else:
                plan['statistics']['no_rule_match'] += 1
        
        return plan
    
    def execute_plan(self, plan: Dict, dry_run: bool = True):
        """Execute organization plan"""
        if dry_run:
            print("DRY RUN - No files will be moved")
            print()
        
        for move_op in plan['moves']:
            source = Path(move_op['source'])
            target = Path(move_op['target'])
            
            if dry_run:
                print(f"Would move: {source}")
                print(f"       to: {target}")
                print()
            else:
                try:
                    # Create target directory
                    target.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Move file
                    source.rename(target)
                    print(f"Moved: {source.name} -> {target}")
                except Exception as e:
                    print(f"Error moving {source}: {e}")


class DuplicateManager:
    """Manage duplicate files intelligently"""
    
    def __init__(self, analyzer: FileAnalyzer):
        self.analyzer = analyzer
    
    def find_duplicates(self, min_size: int = 1024) -> Dict[str, List[Path]]:
        """Find all duplicate files"""
        return self.analyzer.db.find_duplicates(min_size)
    
    def choose_best_version(self, duplicates: List[Path]) -> Path:
        """Choose the best version from duplicates"""
        # Scoring criteria:
        # - Prefer files in organized directories
        # - Prefer files with better naming
        # - Prefer newer files (all else equal)
        
        scores = {}
        
        for path in duplicates:
            score = 0
            path_str = str(path)
            
            # Prefer organized locations
            if any(keyword in path_str for keyword in ['BY_ARTIST', 'BY_ALBUM', 'ORGANIZED']):
                score += 10
            
            # Penalize temp/cache locations
            if any(keyword in path_str.lower() for keyword in ['temp', 'cache', 'tmp', 'backup']):
                score -= 5
            
            # Prefer descriptive names
            if len(path.stem) > 10 and not path.stem.isdigit():
                score += 3
            
            # Modification time (newer = better, but minor factor)
            score += path.stat().st_mtime / 1e12
            
            scores[path] = score
        
        # Return file with highest score
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def generate_dedup_plan(self, duplicates: Dict[str, List[Path]]) -> Dict:
        """Generate plan for removing duplicates"""
        plan = {
            'actions': [],
            'total_to_remove': 0,
            'space_to_save': 0
        }
        
        for hash_val, paths in duplicates.items():
            paths = [Path(p) for p in paths]
            
            # Choose best version
            keep = self.choose_best_version(paths)
            remove = [p for p in paths if p != keep]
            
            for path in remove:
                plan['actions'].append({
                    'action': 'delete',
                    'path': str(path),
                    'keep_version': str(keep),
                    'size': path.stat().st_size
                })
                plan['total_to_remove'] += 1
                plan['space_to_save'] += path.stat().st_size
        
        return plan


class ContentGrouper:
    """Group related content together"""
    
    def __init__(self, analyzer: FileAnalyzer):
        self.analyzer = analyzer
    
    def find_related_files(self, file_path: Path) -> List[Path]:
        """Find files related to given file"""
        related = []
        
        # Check for files with similar names
        base_name = file_path.stem
        similar_pattern = self._create_fuzzy_pattern(base_name)
        
        # Search in same directory
        if file_path.parent.exists():
            for candidate in file_path.parent.iterdir():
                if candidate != file_path and re.match(similar_pattern, candidate.stem):
                    related.append(candidate)
        
        return related
    
    def _create_fuzzy_pattern(self, base_name: str) -> str:
        """Create regex pattern for fuzzy matching"""
        # Remove numbers and special chars for core name
        core = re.sub(r'[\d_\-\s]+', '', base_name)
        
        if len(core) < 3:
            core = base_name
        
        # Create pattern that matches similar names
        pattern = f".*{re.escape(core)}.*"
        return pattern
    
    def group_by_content(self, files: List[FileFingerprint]) -> Dict[str, List[Path]]:
        """Group files by content similarity"""
        groups = defaultdict(list)
        
        # Group by stem similarity
        for fp in files:
            # Extract base name without numbers/versions
            base = re.sub(r'[-_]?\d+$', '', fp.path.stem)
            base = re.sub(r'[-_]?v\d+$', '', base)
            base = re.sub(r'[-_]part\d+$', '', base, flags=re.IGNORECASE)
            
            groups[base.lower()].append(fp.path)
        
        # Return only groups with multiple files
        return {k: v for k, v in groups.items() if len(v) > 1}


if __name__ == '__main__':
    print("Smart File Organizer")
    print("=" * 80)
