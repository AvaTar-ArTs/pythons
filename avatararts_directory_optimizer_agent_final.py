#!/usr/bin/env python3
"""
AVATARARTS DirectoryOptimizer Agent
A specialized automation agent for continuous directory structure optimization
based on content-aware intelligence and functional organization principles.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import hashlib
import re
import logging
import time
from typing import Dict, List, Any


class DirectoryOptimizerAgent:
    """
    AVATARARTS DirectoryOptimizer Agent
    Continuously monitors, analyzes, and optimizes directory structures
    """
    
    def __init__(self, base_path: str = "/Users/steven/AVATARARTS"):
        self.base_path = Path(base_path)
        self.backup_dir = Path(f"{base_path}_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.functional_categories = [
            "AUTOMATION",
            "REVENUE", 
            "BUSINESS_INTELLIGENCE",
            "AI_ML",
            "DATA_PROCESSING",
            "DEVELOPMENT_TOOLS",
            "DOCUMENTATION",
            "MEDIA_PROCESSING",
            "API_INTEGRATION",
            "PORTFOLIO_MANAGEMENT",
            "CONTENT_CREATION",
            "SEO_MARKETING",
            "ARCHIVES",
            "UTILITIES",
            "CONFIGURATIONS",
            "MISCELLANEOUS"
        ]
        self.numbered_pattern = re.compile(r'^[0-9]{2}_')
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for the agent"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'/Users/steven/avatararts_optimizer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def analyze_current_structure(self) -> Dict[str, Any]:
        """Analyze the current directory structure for optimization opportunities"""
        analysis = {
            'total_directories': 0,
            'total_files': 0,
            'deeply_nested_directories': [],
            'numbered_directories': [],
            'files_by_extension': defaultdict(int),
            'directory_depths': defaultdict(int)
        }
        
        for root, dirs, files in os.walk(self.base_path):
            # Count directories and files
            analysis['total_directories'] += len(dirs)
            analysis['total_files'] += len(files)
            
            # Calculate directory depth relative to base path
            try:
                rel_path = Path(root).relative_to(self.base_path)
                depth = len(rel_path.parts) if str(rel_path) != '.' else 0
                analysis['directory_depths'][depth] += 1
                
                # Identify deeply nested directories (>3 levels)
                if depth > 3:
                    analysis['deeply_nested_directories'].append(root)
            except ValueError:
                # Handle case where root is not relative to base_path
                pass
                
            # Identify numbered directories
            for dir_name in dirs:
                if self.numbered_pattern.match(dir_name):
                    full_path = Path(root) / dir_name
                    analysis['numbered_directories'].append(str(full_path))
                    
            # Count file extensions
            for file in files:
                ext = Path(file).suffix.lower()
                analysis['files_by_extension'][ext] += 1
                
        return analysis
        
    def identify_optimization_targets(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify directories that need optimization"""
        targets = []
        
        # Add numbered directories to optimization targets
        targets.extend(analysis['numbered_directories'])
        
        # Add deeply nested directories to optimization targets
        targets.extend(analysis['deeply_nested_directories'])
        
        # Remove duplicates
        return list(set(targets))
        
    def classify_content(self, file_path: Path) -> str:
        """Classify file content to determine appropriate functional category"""
        try:
            # Read file content for classification (first 1000 characters for efficiency)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1000).lower()
                
            # Determine category based on content
            if any(keyword in content for keyword in ['automation', 'automate', 'suite', 'workflow', 'orchestrate', 'bot', 'agent']):
                return 'AUTOMATION'
            elif any(keyword in content for keyword in ['revenue', 'income', 'profit', 'monetiz', 'launch', 'sales', 'earn', 'money']):
                return 'REVENUE'
            elif any(keyword in content for keyword in ['dashboard', 'analytics', 'intelligence', 'report', 'metric', 'kpi', 'chart', 'graph']):
                return 'BUSINESS_INTELLIGENCE'
            elif any(keyword in content for keyword in ['ai', 'ml', 'model', 'neural', 'tensor', 'torch', 'openai', 'claude', 'gemini', 'grok', 'ollama']):
                return 'AI_ML'
            elif any(keyword in content for keyword in ['data', 'process', 'csv', 'pandas', 'json', 'xml', 'excel', 'transform', 'analyze']):
                return 'DATA_PROCESSING'
            elif any(keyword in content for keyword in ['api', 'endpoint', 'client', 'integration', 'request', 'auth', 'oauth']):
                return 'API_INTEGRATION'
            elif any(keyword in content for keyword in ['dev', 'tool', 'util', 'script', 'build', 'test', 'debug']):
                return 'DEVELOPMENT_TOOLS'
            elif any(keyword in content for keyword in ['doc', 'manual', 'guide', 'tutorial', 'readme', 'howto']):
                return 'DOCUMENTATION'
            elif any(keyword in content for keyword in ['media', 'audio', 'video', 'image', 'mp3', 'mp4', 'jpg', 'png']):
                return 'MEDIA_PROCESSING'
            elif any(keyword in content for keyword in ['portfolio', 'invest', 'finance', 'stock', 'trade', 'asset']):
                return 'PORTFOLIO_MANAGEMENT'
            elif any(keyword in content for keyword in ['content', 'create', 'design', 'write', 'copy', 'text']):
                return 'CONTENT_CREATION'
            elif any(keyword in content for keyword in ['seo', 'marketing', 'campaign', 'keyword', 'rank', 'traffic']):
                return 'SEO_MARKETING'
            elif any(keyword in content for keyword in ['archive', 'backup', 'old', 'historical', 'deprecated']):
                return 'ARCHIVES'
            elif any(keyword in content for keyword in ['util', 'helper', 'common', 'sync', 'clean', 'organize']):
                return 'UTILITIES'
            elif any(keyword in content for keyword in ['.env', 'config', 'setting', 'ini', 'yaml', 'yml', 'json']):
                return 'CONFIGURATIONS'
            else:
                # Default to utilities if no clear category found
                return 'UTILITIES'
        except Exception as e:
            self.logger.warning(f"Could not classify {file_path}: {e}")
            return 'MISCELLANEOUS'
            
    def create_functional_structure(self):
        """Create the functional directory structure"""
        for category in self.functional_categories:
            category_path = self.base_path / category
            category_path.mkdir(exist_ok=True)
            self.logger.info(f"Created functional directory: {category_path}")
            
    def move_to_functional_category(self, file_path: Path, category: str):
        """Move a file to its appropriate functional category"""
        try:
            target_dir = self.base_path / category
            target_path = target_dir / file_path.name
            
            # Handle duplicate filenames
            counter = 1
            original_target = target_path
            while target_path.exists():
                name_without_ext = original_target.stem
                ext = original_target.suffix
                target_path = target_dir / f"{name_without_ext}_{counter}{ext}"
                counter += 1
                
            # Move the file
            shutil.move(str(file_path), str(target_path))
            self.logger.info(f"Moved {file_path.name} to {category}/")
            return str(target_path)
        except Exception as e:
            self.logger.error(f"Failed to move {file_path} to {category}: {e}")
            return None
            
    def optimize_directories(self, targets: List[str]):
        """Optimize the identified target directories"""
        self.logger.info(f"Starting optimization of {len(targets)} directories...")
        
        # Create functional structure first
        self.create_functional_structure()
        
        # Process each target directory
        for target_path in targets:
            target = Path(target_path)
            
            if target.is_dir():
                self.logger.info(f"Processing directory: {target}")
                
                # Walk through the directory and move files to appropriate categories
                for root, dirs, files in os.walk(target, topdown=False):  # topdown=False to process subdirs first
                    for file in files:
                        file_path = Path(root) / file
                        
                        # Classify the file content
                        category = self.classify_content(file_path)
                        
                        # Move to appropriate functional category
                        new_path = self.move_to_functional_category(file_path, category)
                        
                        if new_path:
                            self.logger.info(f"  - Moved {file} to {category}/")
                            
                # After moving all files, remove the now-empty numbered directory if it's empty
                try:
                    if not any(target.iterdir()):  # If directory is empty
                        target.rmdir()
                        self.logger.info(f"  - Removed empty directory: {target}")
                except OSError:
                    self.logger.warning(f"  - Could not remove directory (not empty): {target}")
                    
    def create_backup(self):
        """Create a backup of the current structure before optimization"""
        self.logger.info(f"Creating backup at: {self.backup_dir}")
        shutil.copytree(str(self.base_path), str(self.backup_dir), dirs_exist_ok=True)
        self.logger.info("Backup created successfully")
        
    def run_optimization_cycle(self, create_backup: bool = True):
        """Run a complete optimization cycle"""
        self.logger.info("Starting AVATARARTS Directory Optimization Cycle")
        
        # Create backup if requested
        if create_backup:
            self.create_backup()
            
        # Analyze current structure
        self.logger.info("Analyzing current directory structure...")
        analysis = self.analyze_current_structure()
        
        self.logger.info(f"Analysis complete:")
        self.logger.info(f"  - Total directories: {analysis['total_directories']}")
        self.logger.info(f"  - Total files: {analysis['total_files']}")
        self.logger.info(f"  - Deeply nested directories: {len(analysis['deeply_nested_directories'])}")
        self.logger.info(f"  - Numbered directories: {len(analysis['numbered_directories'])}")
        
        # Identify optimization targets
        targets = self.identify_optimization_targets(analysis)
        
        if not targets:
            self.logger.info("No optimization targets found. Structure is already optimized.")
            return
            
        self.logger.info(f"Found {len(targets)} optimization targets")
        
        # Optimize the identified targets
        self.optimize_directories(targets)
        
        # Final analysis to show improvements
        final_analysis = self.analyze_current_structure()
        self.logger.info("Optimization cycle complete!")
        self.logger.info(f"Final structure:")
        self.logger.info(f"  - Total directories: {final_analysis['total_directories']}")
        self.logger.info(f"  - Total files: {final_analysis['total_files']}")
        
    def monitor_and_optimize(self, interval_minutes: int = 60):
        """Continuously monitor and optimize the directory structure"""
        self.logger.info(f"Starting continuous monitoring (checking every {interval_minutes} minutes)")
        
        while True:
            try:
                self.run_optimization_cycle(create_backup=False)  # Don't create backup on every cycle
                self.logger.info(f"Waiting {interval_minutes} minutes for next optimization cycle...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Error during monitoring cycle: {e}")
                time.sleep(interval_minutes * 60)  # Wait before retrying


def main():
    parser = argparse.ArgumentParser(description='AVATARARTS DirectoryOptimizer Agent')
    parser.add_argument('--path', default='/Users/steven/AVATARARTS', help='Base path to optimize')
    parser.add_argument('--backup', action='store_true', help='Create backup before optimization')
    parser.add_argument('--monitor', action='store_true', help='Run in continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=60, help='Monitoring interval in minutes')
    parser.add_argument('--analyze', action='store_true', help='Just analyze without making changes')
    
    args = parser.parse_args()
    
    agent = DirectoryOptimizerAgent(base_path=args.path)
    
    if args.analyze:
        analysis = agent.analyze_current_structure()
        print("Current Structure Analysis:")
        print(f"  Total directories: {analysis['total_directories']}")
        print(f"  Total files: {analysis['total_files']}")
        print(f"  Deeply nested directories: {len(analysis['deeply_nested_directories'])}")
        print(f"  Numbered directories: {len(analysis['numbered_directories'])}")
        print(f"  Directory depths: {dict(analysis['directory_depths'])}")
        print(f"  Top file extensions: {dict(list(analysis['files_by_extension'].items())[:10])}")
    elif args.monitor:
        agent.monitor_and_optimize(interval_minutes=args.interval)
    else:
        agent.run_optimization_cycle(create_backup=args.backup)


if __name__ == "__main__":
    main()