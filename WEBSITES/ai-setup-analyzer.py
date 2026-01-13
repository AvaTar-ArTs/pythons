#!/usr/bin/env python3
"""
AI Setup Analyzer with Deep Research Intelligence
===============================================
Intelligently analyzes, deduplicates, and merges AI setup configurations
"""

import os
import json
import hashlib
import difflib
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
import re

@dataclass
class AISetupFile:
    """Represents an AI setup file with metadata"""
    path: str
    content: str
    hash: str
    type: str
    purpose: str
    dependencies: List[str]
    duplicates: List[str]
    similar: List[str]
    quality_score: float
    conflicts: List[str]

class AISetupAnalyzer:
    """Intelligent AI setup analysis and organization system"""
    
    def __init__(self, base_path: str = "/Users/steven/ai-sites/n8n"):
        self.base_path = Path(base_path)
        self.setup_files = {}
        self.duplicate_groups = defaultdict(list)
        self.similar_groups = defaultdict(list)
        self.conflict_groups = defaultdict(list)
        self.dependency_map = defaultdict(list)
        
    def analyze_ai_setups(self) -> Dict[str, Any]:
        """Analyze all AI setup files for intelligence"""
        print("🤖 AI Setup Analyzer with Deep Research Intelligence")
        print("=" * 55)
        
        # Find all AI setup files
        setup_files = self._find_ai_setup_files()
        print(f"📁 Found {len(setup_files)} AI setup files")
        
        # Analyze each file
        for file_path in setup_files:
            self._analyze_setup_file(file_path)
        
        # Perform intelligent analysis
        self._detect_duplicates()
        self._detect_similar_setups()
        self._detect_conflicts()
        self._build_dependency_map()
        
        return self._generate_ai_report()
    
    def _find_ai_setup_files(self) -> List[Path]:
        """Find all AI setup related files"""
        ai_patterns = [
            "*.py", "*.sh", "*.yml", "*.yaml", "*.json", "*.md",
            "*.env", "*.txt", "Dockerfile*", "compose*", "requirements*"
        ]
        
        files = []
        for pattern in ai_patterns:
            files.extend(self.base_path.glob(pattern))
        
        # Also check subdirectories
        for subdir in ["n8n_workflows", "n8n-data"]:
            subdir_path = self.base_path / subdir
            if subdir_path.exists():
                for pattern in ai_patterns:
                    files.extend(subdir_path.glob(pattern))
        
        return files
    
    def _analyze_setup_file(self, file_path: Path):
        """Analyze a single AI setup file"""
        try:
            # Read file content
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # Calculate hash
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Determine file type and purpose
            file_type, purpose = self._classify_file(file_path, content)
            
            # Extract dependencies
            dependencies = self._extract_dependencies(content, file_type)
            
            # Create setup file item
            item = AISetupFile(
                path=str(file_path),
                content=content,
                hash=content_hash,
                type=file_type,
                purpose=purpose,
                dependencies=dependencies,
                duplicates=[],
                similar=[],
                quality_score=0.0,
                conflicts=[]
            )
            
            self.setup_files[str(file_path)] = item
            
        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")
    
    def _classify_file(self, file_path: Path, content: str) -> Tuple[str, str]:
        """Classify file type and purpose"""
        filename = file_path.name.lower()
        
        # File type classification
        if filename.startswith('dockerfile'):
            file_type = 'dockerfile'
        elif filename.startswith('compose'):
            file_type = 'docker_compose'
        elif filename.endswith('.py'):
            file_type = 'python_script'
        elif filename.endswith('.sh'):
            file_type = 'shell_script'
        elif filename.endswith(('.yml', '.yaml')):
            file_type = 'yaml_config'
        elif filename.endswith('.json'):
            file_type = 'json_config'
        elif filename.endswith('.env'):
            file_type = 'environment'
        elif filename.endswith('.md'):
            file_type = 'documentation'
        else:
            file_type = 'other'
        
        # Purpose classification based on content and filename
        purpose = self._determine_purpose(filename, content)
        
        return file_type, purpose
    
    def _determine_purpose(self, filename: str, content: str) -> str:
        """Determine the purpose of the file"""
        content_lower = content.lower()
        
        # AI Agent related
        if any(keyword in filename for keyword in ['ai-agent', 'ai_agent', 'agent']):
            return 'ai_agent'
        elif 'ai-agent' in content_lower or 'ai_agent' in content_lower:
            return 'ai_agent'
        
        # Environment related
        elif any(keyword in filename for keyword in ['env', 'environment']):
            return 'environment'
        elif 'api_key' in content_lower or 'environment' in content_lower:
            return 'environment'
        
        # Docker related
        elif filename.startswith('dockerfile'):
            return 'docker_build'
        elif filename.startswith('compose'):
            return 'docker_orchestration'
        
        # Workflow related
        elif 'workflow' in filename or 'n8n' in filename:
            return 'workflow_automation'
        elif 'workflow' in content_lower or 'n8n' in content_lower:
            return 'workflow_automation'
        
        # Setup/Installation
        elif any(keyword in filename for keyword in ['setup', 'install', 'start']):
            return 'setup_script'
        elif 'install' in content_lower or 'setup' in content_lower:
            return 'setup_script'
        
        # Documentation
        elif filename.endswith('.md'):
            return 'documentation'
        
        # Configuration
        elif any(keyword in filename for keyword in ['config', 'conf', 'settings']):
            return 'configuration'
        
        else:
            return 'general'
    
    def _extract_dependencies(self, content: str, file_type: str) -> List[str]:
        """Extract dependencies from file content"""
        dependencies = []
        
        if file_type == 'python_script':
            # Extract imports
            imports = re.findall(r'^(?:from\s+\S+\s+)?import\s+([^\s,]+)', content, re.MULTILINE)
            dependencies.extend(imports)
            
            # Extract requirements
            req_matches = re.findall(r'pip\s+install\s+([^\n]+)', content, re.IGNORECASE)
            for match in req_matches:
                deps = [dep.strip() for dep in match.split() if not dep.startswith('-')]
                dependencies.extend(deps)
        
        elif file_type == 'shell_script':
            # Extract commands
            commands = re.findall(r'(\w+)\s+[a-zA-Z]', content)
            dependencies.extend(commands)
        
        elif file_type == 'docker_compose':
            # Extract services
            services = re.findall(r'^\s*(\w+):', content, re.MULTILINE)
            dependencies.extend(services)
        
        elif file_type == 'environment':
            # Extract variable names
            vars = re.findall(r'^([A-Z_][A-Z0-9_]*)=', content, re.MULTILINE)
            dependencies.extend(vars)
        
        return list(set(dependencies))
    
    def _detect_duplicates(self):
        """Detect exact duplicate files"""
        hash_groups = defaultdict(list)
        
        for path, item in self.setup_files.items():
            hash_groups[item.hash].append(path)
        
        for content_hash, paths in hash_groups.items():
            if len(paths) > 1:
                self.duplicate_groups[content_hash] = paths
                for path in paths:
                    self.setup_files[path].duplicates = [p for p in paths if p != path]
    
    def _detect_similar_setups(self):
        """Detect similar setup files"""
        paths = list(self.setup_files.keys())
        
        for i, path1 in enumerate(paths):
            for path2 in paths[i+1:]:
                item1 = self.setup_files[path1]
                item2 = self.setup_files[path2]
                
                # Only compare files of similar type and purpose
                if (item1.type == item2.type and 
                    item1.purpose == item2.purpose and
                    item1.purpose != 'documentation'):
                    
                    similarity = self._calculate_similarity(item1.content, item2.content)
                    
                    if similarity > 0.6:  # 60% similarity threshold
                        self.similar_groups[f"{path1}~{path2}"] = [path1, path2]
                        item1.similar.append(path2)
                        item2.similar.append(path1)
    
    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two files"""
        matcher = difflib.SequenceMatcher(None, content1, content2)
        return matcher.ratio()
    
    def _detect_conflicts(self):
        """Detect conflicting configurations"""
        # Group files by purpose
        purpose_groups = defaultdict(list)
        for path, item in self.setup_files.items():
            purpose_groups[item.purpose].append(path)
        
        # Check for conflicts within each purpose group
        for purpose, paths in purpose_groups.items():
            if len(paths) > 1 and purpose in ['environment', 'configuration', 'docker_compose']:
                self._check_configuration_conflicts(purpose, paths)
    
    def _check_configuration_conflicts(self, purpose: str, paths: List[str]):
        """Check for configuration conflicts"""
        if purpose == 'environment':
            self._check_env_conflicts(paths)
        elif purpose == 'docker_compose':
            self._check_docker_conflicts(paths)
    
    def _check_env_conflicts(self, paths: List[str]):
        """Check for environment variable conflicts"""
        env_vars = {}
        
        for path in paths:
            content = self.setup_files[path].content
            for line in content.split('\n'):
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.split('=', 1)
                    if key in env_vars and env_vars[key] != value:
                        self.conflict_groups[f"env_{key}"].append(path)
                    env_vars[key] = value
    
    def _check_docker_conflicts(self, paths: List[str]):
        """Check for Docker configuration conflicts"""
        ports = {}
        
        for path in paths:
            content = self.setup_files[path].content
            port_matches = re.findall(r'(\d+):\d+', content)
            for port in port_matches:
                if port in ports and ports[port] != path:
                    self.conflict_groups[f"port_{port}"].append(path)
                ports[port] = path
    
    def _build_dependency_map(self):
        """Build dependency mapping"""
        for path, item in self.setup_files.items():
            for dep in item.dependencies:
                self.dependency_map[dep].append(path)
    
    def _generate_ai_report(self) -> Dict[str, Any]:
        """Generate comprehensive AI setup report"""
        total_files = len(self.setup_files)
        duplicate_files = sum(len(group) for group in self.duplicate_groups.values())
        similar_pairs = len(self.similar_groups)
        conflict_groups = len(self.conflict_groups)
        
        # File type distribution
        type_distribution = defaultdict(int)
        purpose_distribution = defaultdict(int)
        
        for item in self.setup_files.values():
            type_distribution[item.type] += 1
            purpose_distribution[item.purpose] += 1
        
        return {
            'summary': {
                'total_files': total_files,
                'duplicate_files': duplicate_files,
                'similar_pairs': similar_pairs,
                'conflict_groups': conflict_groups,
                'unique_files': total_files - duplicate_files
            },
            'file_types': dict(type_distribution),
            'purposes': dict(purpose_distribution),
            'duplicates': dict(self.duplicate_groups),
            'similar_files': dict(self.similar_groups),
            'conflicts': dict(self.conflict_groups),
            'dependencies': dict(self.dependency_map),
            'setup_files': {
                path: {
                    'type': item.type,
                    'purpose': item.purpose,
                    'dependencies': item.dependencies,
                    'duplicates': item.duplicates,
                    'similar': item.similar,
                    'conflicts': item.conflicts
                }
                for path, item in self.setup_files.items()
            }
        }
    
    def suggest_consolidation_actions(self) -> List[Dict[str, Any]]:
        """Suggest intelligent consolidation actions"""
        actions = []
        
        # Handle duplicates
        for content_hash, paths in self.duplicate_groups.items():
            if len(paths) > 1:
                actions.append({
                    'type': 'remove_duplicates',
                    'priority': 'high',
                    'description': f'Remove {len(paths)-1} duplicate files',
                    'files': paths,
                    'suggestion': 'Keep the most comprehensive version and remove others'
                })
        
        # Handle similar files
        for pair, paths in self.similar_groups.items():
            actions.append({
                'type': 'merge_similar',
                'priority': 'medium',
                'description': f'Merge similar files: {len(paths)} files',
                'files': paths,
                'suggestion': 'Create a unified version combining best features'
            })
        
        # Handle conflicts
        for conflict_type, paths in self.conflict_groups.items():
            actions.append({
                'type': 'resolve_conflicts',
                'priority': 'high',
                'description': f'Resolve {conflict_type} conflicts',
                'files': paths,
                'suggestion': 'Choose consistent values across all files'
            })
        
        # Suggest master file creation
        if len(self.setup_files) > 10:
            actions.append({
                'type': 'create_master_setup',
                'priority': 'medium',
                'description': 'Create master setup script',
                'files': [],
                'suggestion': 'Create a single master setup script that orchestrates all components'
            })
        
        return actions

def main():
    """Main function for AI setup analysis"""
    print("🤖 AI Setup Analyzer with Deep Research Intelligence")
    print("=" * 55)
    
    analyzer = AISetupAnalyzer()
    results = analyzer.analyze_ai_setups()
    
    # Print summary
    summary = results['summary']
    print(f"\n📊 AI Setup Analysis Summary")
    print("=" * 30)
    print(f"📁 Total files: {summary['total_files']}")
    print(f"🔄 Duplicates: {summary['duplicate_files']}")
    print(f"🔗 Similar pairs: {summary['similar_pairs']}")
    print(f"⚠️  Conflicts: {summary['conflict_groups']}")
    print(f"✅ Unique files: {summary['unique_files']}")
    
    # Print file type distribution
    print(f"\n📋 File Type Distribution")
    print("=" * 25)
    for file_type, count in results['file_types'].items():
        print(f"  {file_type}: {count}")
    
    # Print purpose distribution
    print(f"\n🎯 Purpose Distribution")
    print("=" * 22)
    for purpose, count in results['purposes'].items():
        print(f"  {purpose}: {count}")
    
    # Print conflicts
    if results['conflicts']:
        print(f"\n⚠️  Configuration Conflicts")
        print("=" * 28)
        for conflict, paths in results['conflicts'].items():
            print(f"  {conflict}: {len(paths)} files")
            for path in paths:
                print(f"    - {Path(path).name}")
    
    # Suggest actions
    print(f"\n🎯 Suggested Consolidation Actions")
    print("=" * 35)
    
    actions = analyzer.suggest_consolidation_actions()
    for i, action in enumerate(actions, 1):
        priority_emoji = "🔴" if action['priority'] == 'high' else "🟡" if action['priority'] == 'medium' else "🟢"
        print(f"{i}. {priority_emoji} {action['description']}")
        print(f"   💡 {action['suggestion']}")
        if action['files']:
            print(f"   📁 Files: {len(action['files'])}")
        print()
    
    # Save detailed report
    report_file = Path("/Users/steven/ai-sites/n8n/ai-setup-analysis.json")
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Detailed report saved to: {report_file}")
    print(f"\n🎉 AI setup analysis complete!")

if __name__ == "__main__":
    main()