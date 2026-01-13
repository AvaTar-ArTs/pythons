#!/usr/bin/env python3
"""
Integrate existing Python projects with Creative AI Empire
"""

import os
import shutil
from pathlib import Path

def integrate_python_projects():
    """Integrate existing Python projects with the empire"""
    
    # Source and destination paths
    source_python = Path("/Users/steven/Documents/python")
    empire_python = Path("/Users/steven/ai-sites/legacy-python-projects")
    
    # Create legacy projects directory
    empire_python.mkdir(exist_ok=True)
    
    # Categories to integrate
    categories = {
        'ai_tools': ['04_ai_tools', '03_ai_creative_tools'],
        'automation': ['08_automation', '02_youtube_automation'],
        'production': ['00_production'],
        'experiments': ['01_experiments', '07_experimental'],
        'utilities': ['03_utilities', '06_utilities']
    }
    
    integrated_count = 0
    
    for category, dirs in categories.items():
        category_path = empire_python / category
        category_path.mkdir(exist_ok=True)
        
        for dir_name in dirs:
            source_dir = source_python / dir_name
            if source_dir.exists():
                dest_dir = category_path / dir_name
                if not dest_dir.exists():
                    shutil.copytree(source_dir, dest_dir)
                    integrated_count += 1
                    print(f"Integrated: {dir_name} -> {category}")
    
    print(f"✅ Integrated {integrated_count} Python project directories")
    
    # Create integration manifest
    manifest = {
        'integrated_projects': integrated_count,
        'categories': list(categories.keys()),
        'source_path': str(source_python),
        'destination_path': str(empire_python)
    }
    
    import json
    with open(empire_python / 'integration_manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    integrate_python_projects()
