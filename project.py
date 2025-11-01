"""
Project

This module provides functionality for project.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)

#!/usr/bin/env python3
"""
AvaTarArTs Project Manager
Manages ongoing updates and project organization
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import subprocess


class AvaTarArTsProjectManager:
    """Manages AvaTarArTs projects and updates"""

    def __init__(self):
        """__init__ function."""

        self.base_dir = Path(Path("/Users/steven"))
        self.avatararts_dir = Path(Path(str(Path.home()) + "/AvatararTs"))
        self.backup_base = Path(Path(str(Path.home()) + "/AvaTarArTs_Work_Backup"))

        # Find latest backup
        self.latest_backup = self._find_latest_backup()

        # Project structure
        self.projects = {
            "as_a_man_thinketh": {
                "name": "As a Man Thinketh TTS System",
                "description": "Complete text-to-speech and visual analysis system",
                "main_files": [
                    "as_a_man_thinketh_ultimate_tts.py",
                    "visual_analysis_system.py",
                    "system_tts_system.py",
                ],
                "output_dirs": [
                    "as_a_man_thinketh_audio_mp3",
                    "as_a_man_thinketh_visual_analysis",
                ],
            },
            "grid_systems": {
                "name": "Grid Systems",
                "description": "Multi-grid file browser systems",
                "main_files": [
                    "multi_grid_generator.py",
                    "professional_grid_generator.py",
                    "launch_professional.py",
                ],
                "output_dirs": ["grid_views", "professional_grids"],
            },
            "visual_enhancements": {
                "name": "Visual Enhancements",
                "description": "Content-aware visual analysis and enhancements",
                "main_files": ["content_aware_enhancer.py", "creative_enhancements.py"],
                "output_dirs": [],
            },
        }

    def _find_latest_backup(self):
        """Find the latest backup directory"""
        if not self.backup_base.exists():
            return None

        backup_dirs = [d for d in self.backup_base.iterdir() if d.is_dir()]
        if not backup_dirs:
            return None

        # Sort by creation time, get latest
        latest = max(backup_dirs, key=lambda x: x.stat().st_ctime)
        return latest

    def create_project_structure(self):
        """Create organized project structure"""
        logger.info("📁 Creating project structure...")

        # Create main project directory
        project_dir = self.base_dir / "AvaTarArTs_Projects"
        project_dir.mkdir(exist_ok=True)

        # Create project subdirectories
        for project_key, project_info in self.projects.items():
            proj_dir = project_dir / project_key
            proj_dir.mkdir(exist_ok=True)

            # Create subdirectories
            (proj_dir / "scripts").mkdir(exist_ok=True)
            (proj_dir / "outputs").mkdir(exist_ok=True)
            (proj_dir / "docs").mkdir(exist_ok=True)
            (proj_dir / "backups").mkdir(exist_ok=True)

        logger.info(f"✅ Project structure created: {project_dir}")
        return project_dir

    def organize_existing_work(self, project_dir: Path):
        """Organize existing work into project structure"""
        logger.info("📦 Organizing existing work...")

        # As a Man Thinketh project
        as_man_dir = project_dir / "as_a_man_thinketh"

        # Copy TTS scripts
        tts_files = [
            "as_a_man_thinketh_tts.py",
            "as_a_man_thinketh_enhanced_tts.py",
            "as_a_man_thinketh_ultimate_tts.py",
            "creative_tts_features.py",
            "system_tts_system.py",
            "manual_openai_tts.py",
            "convert_to_mp3.py",
            "visual_analysis_system.py",
            "test_tts.py",
            "fallback_tts_system.py",
            "refined_openai_tts.py",
            "openai_tts_system.py",
            "requirements.txt",
        ]

        for file_name in tts_files:
            source = self.base_dir / file_name
            if source.exists():
                dest = as_man_dir / "scripts" / file_name
                shutil.copy2(source, dest)
                logger.info(f"  ✓ {file_name}")

        # Copy outputs
        output_dirs = [
            "as_a_man_thinketh_audio_mp3",
            "as_a_man_thinketh_audio_system",
            "as_a_man_thinketh_visual_analysis",
        ]

        for dir_name in output_dirs:
            source = self.base_dir / dir_name
            if source.exists():
                dest = as_man_dir / "outputs" / dir_name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(source, dest)
                logger.info(f"  ✓ {dir_name}/")

        # Copy documentation
        doc_files = [
            "README.md",
            "ULTIMATE_README.md",
            "COMPLETE_PROJECT_SUMMARY.md",
            "AUDIO_SUMMARY.md",
        ]

        for file_name in doc_files:
            source = self.base_dir / file_name
            if source.exists():
                dest = as_man_dir / "docs" / file_name
                shutil.copy2(source, dest)
                logger.info(f"  ✓ {file_name}")

        # Grid Systems project
        grid_dir = project_dir / "grid_systems"

        grid_files = [
            "multi_grid_generator.py",
            "professional_grid_generator.py",
            "launch_grids.py",
            "launch_professional.py",
            "content_aware_enhancer.py",
            "creative_enhancements.py",
        ]

        for file_name in grid_files:
            source = self.avatararts_dir / file_name
            if source.exists():
                dest = grid_dir / "scripts" / file_name
                shutil.copy2(source, dest)
                logger.info(f"  ✓ {file_name}")

        # Copy grid outputs
        grid_output_dirs = ["grid_views", "professional_grids"]

        for dir_name in grid_output_dirs:
            source = self.avatararts_dir / dir_name
            if source.exists():
                dest = grid_dir / "outputs" / dir_name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(source, dest)
                logger.info(f"  ✓ {dir_name}/")

        # Copy grid documentation
        grid_docs = [
            "MULTI_GRID_SUMMARY.md",
            "PROFESSIONAL_GRID_SUMMARY.md",
            "README_GRIDS.md",
        ]

        for file_name in grid_docs:
            source = self.avatararts_dir / file_name
            if source.exists():
                dest = grid_dir / "docs" / file_name
                shutil.copy2(source, dest)
                logger.info(f"  ✓ {file_name}")

        logger.info("✅ Work organized into project structure")

    def create_project_manifests(self, project_dir: Path):
        """Create project manifests for each project"""
        logger.info("📋 Creating project manifests...")

        for project_key, project_info in self.projects.items():
            proj_dir = project_dir / project_key

            manifest = {
                "project_name": project_info["name"],
                "description": project_info["description"],
                "created": datetime.now().isoformat(),
                "main_files": project_info["main_files"],
                "output_directories": project_info["output_dirs"],
                "scripts_location": str(proj_dir / "scripts"),
                "outputs_location": str(proj_dir / "outputs"),
                "docs_location": str(proj_dir / "docs"),
                "backups_location": str(proj_dir / "backups"),
            }

            with open(proj_dir / "project_manifest.json", "w") as f:
                json.dump(manifest, f, indent=2)

            logger.info(f"  ✓ {project_key} manifest created")

    def create_update_system(self, project_dir: Path):
        """Create update and management system"""
        logger.info("🔄 Creating update system...")

        # Create main update script
        update_script = f"""#!/usr/bin/env python3
'''
AvaTarArTs Project Update System
Updates all projects and creates backups
'''

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def update_project(project_name, project_dir):
    \"\"\"Update a specific project\"\"\"
    logger.info(f"🔄 Updating {{project_name}}...")
    
    # Run project-specific update if it exists
    update_script = project_dir / "update.py"
    if update_script.exists():
        subprocess.run([sys.executable, str(update_script)])
    else:
        logger.info(f"  No update script found for {{project_name}}")
    
    logger.info(f"✅ {{project_name}} updated")

def main():
    \"\"\"Main update function\"\"\"
    project_base = Path("{project_dir}")
    
    logger.info("🚀 Starting AvaTarArTs project updates...")
    
    # Update each project
    for project_dir in project_base.iterdir():
        if project_dir.is_dir() and (project_dir / "project_manifest.json").exists():
            update_project(project_dir.name, project_dir)
    
    # Create backup
    logger.info("📦 Creating backup...")
    subprocess.run([sys.executable, Path(str(Path.home()) + "/simple_backup.py")])
    
    logger.info("🎉 All projects updated and backed up!")

if __name__ == "__main__":
    main()
"""

        with open(project_dir / "update_all.py", "w") as f:
            f.write(update_script)

        os.chmod(project_dir / "update_all.py", 0o755)

        # Create individual project update scripts
        for project_key, project_info in self.projects.items():
            proj_dir = project_dir / project_key

            if project_key == "as_a_man_thinketh":
                update_script = f"""#!/usr/bin/env python3
'''
As a Man Thinketh Project Update
'''

import sys
import subprocess
from pathlib import Path

def main():
    project_dir = Path("{proj_dir}")
    scripts_dir = project_dir / "scripts"
    
    logger.info("🔄 Updating As a Man Thinketh project...")
    
    # Run visual analysis
    logger.info("  Running visual analysis...")
    subprocess.run([sys.executable, str(scripts_dir / "visual_analysis_system.py")])
    
    # Run TTS system
    logger.info("  Running TTS system...")
    subprocess.run([sys.executable, str(scripts_dir / "as_a_man_thinketh_ultimate_tts.py")])
    
    logger.info("✅ As a Man Thinketh project updated")

if __name__ == "__main__":
    main()
"""
            elif project_key == "grid_systems":
                update_script = f"""#!/usr/bin/env python3
'''
Grid Systems Project Update
'''

import sys
import subprocess
from pathlib import Path

def main():
    project_dir = Path("{proj_dir}")
    scripts_dir = project_dir / "scripts"
    
    logger.info("🔄 Updating Grid Systems project...")
    
    # Run professional grid generator
    logger.info("  Generating professional grids...")
    subprocess.run([sys.executable, str(scripts_dir / "professional_grid_generator.py")])
    
    # Run multi-grid generator
    logger.info("  Generating multi-grids...")
    subprocess.run([sys.executable, str(scripts_dir / "multi_grid_generator.py")])
    
    logger.info("✅ Grid Systems project updated")

if __name__ == "__main__":
    main()
"""
            else:
                update_script = f"""#!/usr/bin/env python3
'''
{{project_info['name']}} Project Update
'''

def main():
    logger.info("🔄 Updating {{project_info['name']}}...")
    logger.info("  No specific update actions defined")
    logger.info("✅ {{project_info['name']}} updated")

if __name__ == "__main__":
    main()
"""

            with open(proj_dir / "update.py", "w") as f:
                f.write(update_script)

            os.chmod(proj_dir / "update.py", 0o755)

        logger.info("✅ Update system created")

    def create_main_readme(self, project_dir: Path):
        """Create main project README"""
        logger.info("📚 Creating main README...")

        readme_content = f"""# AvaTarArTs Projects

**Project Manager**: AvaTarArTs Project Management System
**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Location**: {project_dir}

## 🚀 Quick Start

### Update All Projects:
```bash
python3 update_all.py
```

### Individual Project Updates:
```bash
cd as_a_man_thinketh && python3 update.py
cd grid_systems && python3 update.py
```

## 📁 Project Structure

### 1. As a Man Thinketh (`as_a_man_thinketh/`)
Complete text-to-speech and visual analysis system for James Allen's "As a Man Thinketh"

**Scripts**: `scripts/`
- `as_a_man_thinketh_ultimate_tts.py` - Main TTS system
- `visual_analysis_system.py` - Visual analysis
- `system_tts_system.py` - System TTS fallback

**Outputs**: `outputs/`
- `as_a_man_thinketh_audio_mp3/` - Generated MP3 files
- `as_a_man_thinketh_visual_analysis/` - Analysis data

**Documentation**: `docs/`
- Complete project documentation

### 2. Grid Systems (`grid_systems/`)
Multi-grid file browser systems for directory navigation

**Scripts**: `scripts/`
- `professional_grid_generator.py` - Professional grids
- `multi_grid_generator.py` - Multi-grid system
- `launch_professional.py` - Grid launcher

**Outputs**: `outputs/`
- `professional_grids/` - Professional grid layouts
- `grid_views/` - Multi-grid layouts

**Documentation**: `docs/`
- Grid system documentation

### 3. Visual Enhancements (`visual_enhancements/`)
Content-aware visual analysis and enhancement systems

**Scripts**: `scripts/`
- `content_aware_enhancer.py` - Content-aware enhancements
- `creative_enhancements.py` - Creative improvements

## 🔄 Update Process

1. **Individual Updates**: Run `python3 update.py` in each project directory
2. **All Projects**: Run `python3 update_all.py` from the main directory
3. **Backup**: Automatic backup after updates
4. **Documentation**: Updated automatically

## 📊 Project Status

- **As a Man Thinketh**: ✅ Complete with TTS and visual analysis
- **Grid Systems**: ✅ Complete with professional and multi-grid layouts
- **Visual Enhancements**: ✅ Complete with content-aware features

## 🎯 Next Steps

1. **Regular Updates**: Run update scripts to keep projects current
2. **New Features**: Add new functionality to existing projects
3. **New Projects**: Create new project directories as needed
4. **Documentation**: Keep documentation updated

---
*Generated by AvaTarArTs Project Manager*
"""

        with open(project_dir / "README.md", "w") as f:
            f.write(readme_content)

        logger.info("✅ Main README created")

    def run_setup(self):
        """Run complete project setup"""
        logger.info("🚀 Setting up AvaTarArTs Project Manager...")

        # Create project structure
        project_dir = self.create_project_structure()

        # Organize existing work
        self.organize_existing_work(project_dir)

        # Create manifests
        self.create_project_manifests(project_dir)

        # Create update system
        self.create_update_system(project_dir)

        # Create main README
        self.create_main_readme(project_dir)

        logger.info(f"\n🎉 Project Manager Setup Complete!")
        logger.info(f"📁 Project Directory: {project_dir}")
        logger.info(f"🔄 Update All: python3 {project_dir}/update_all.py")
        logger.info(f"📚 Documentation: {project_dir}/README.md")


def main():
    """Main function"""
    manager = AvaTarArTsProjectManager()
    manager.run_setup()


if __name__ == "__main__":
    main()
