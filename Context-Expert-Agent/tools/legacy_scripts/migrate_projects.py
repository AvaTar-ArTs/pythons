#!/usr/bin/env python3
"""
Automated Python Projects Reorganization Script
Safely migrates your projects to the new organized structure
"""

import json
import shutil
from datetime import datetime
from pathlib import Path


class ProjectMigrator:
    def __init__(self, base_path="/Users/steven/Documents/python"):
        self.base_path = Path(base_path)
        self.migration_log = []
        self.backup_path = self.base_path / "MIGRATION_BACKUP"
        
    def log_action(self, action, source, destination=None, status="SUCCESS"):
        """Log migration actions for rollback capability."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "source": str(source),
            "destination": str(destination) if destination else None,
            "status": status
        }
        self.migration_log.append(log_entry)
        print(f"[{status}] {action}: {source} → {destination}")
    
    def create_backup(self):
        """Create a backup of the current structure."""
        print("🔄 Creating backup...")
        if self.backup_path.exists():
            shutil.rmtree(self.backup_path)
        
        # Copy critical files
        critical_dirs = [
            "transcription_analyzer",
            "Auto-YouTube", 
            "analyze-mp3-transcript-prompts.py",
            "analyze-mp4s.py",
            "analyze.py"
        ]
        
        for item in critical_dirs:
            source = self.base_path / item
            if source.exists():
                dest = self.backup_path / item
                if source.is_dir():
                    shutil.copytree(source, dest)
                else:
                    shutil.copy2(source, dest)
                self.log_action("BACKUP", source, dest)
        
        print(f"✅ Backup created at: {self.backup_path}")
    
    def create_new_structure(self):
        """Create the new organized directory structure."""
        print("🏗️  Creating new directory structure...")
        
        structure = [
            # Core Tools
            "01_core_tools",
            "01_core_tools/content_analyzer",
            "01_core_tools/file_manager",
            "01_core_tools/api_clients",
            "01_core_tools/shared",
            
            # YouTube Automation
            "02_youtube_automation",
            "02_youtube_automation/auto_youtube",
            "02_youtube_automation/shorts_maker", 
            "02_youtube_automation/reddit_to_youtube",
            "02_youtube_automation/video_generators",
            
            # AI Creative Tools
            "03_ai_creative_tools",
            "03_ai_creative_tools/image_generation",
            "03_ai_creative_tools/comic_factory",
            "03_ai_creative_tools/pattern_makers",
            "03_ai_creative_tools/text_generators",
            
            # Web Scraping
            "04_web_scraping",
            "04_web_scraping/backlink_checker",
            "04_web_scraping/fiverr_scraper",
            "04_web_scraping/social_media",
            "04_web_scraping/news_collectors",
            
            # Audio/Video
            "05_audio_video",
            "05_audio_video/audio_processors",
            "05_audio_video/video_editors", 
            "05_audio_video/transcription_tools",
            "05_audio_video/media_converters",
            
            # Utilities
            "06_utilities",
            "06_utilities/file_organizers",
            "06_utilities/duplicate_finders",
            "06_utilities/batch_processors",
            "06_utilities/system_tools",
            
            # Experimental
            "07_experimental",
            "07_experimental/new_features",
            "07_experimental/prototypes",
            "07_experimental/testing",
            
            # Archived
            "08_archived",
            "08_archived/deprecated",
            "08_archived/backups",
            "08_archived/old_versions",
            
            # Documentation
            "09_documentation",
            "09_documentation/setup_guides",
            "09_documentation/api_docs",
            "09_documentation/tutorials"
        ]
        
        for dir_path in structure:
            full_path = self.base_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            self.log_action("CREATE_DIR", dir_path)
        
        print("✅ Directory structure created")
    
    def create_shared_libraries(self):
        """Create shared library files."""
        print("📚 Creating shared libraries...")
        
        # Shared configuration
        config_content = '''"""
Shared configuration for all Python projects
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser("~/.env"))

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Common settings
DEFAULT_MODEL = "gpt-4o"
DEFAULT_TEMPERATURE = 0.3
LOG_LEVEL = "INFO"
'''
        
        config_file = self.base_path / "01_core_tools/shared/config.py"
        config_file.write_text(config_content)
        
        # OpenAI client
        openai_client_content = '''"""
Centralized OpenAI client for all projects
"""
from openai import OpenAI
from .config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_client():
    """Get configured OpenAI client."""
    return client
'''
        
        openai_file = self.base_path / "01_core_tools/shared/openai_client.py"
        openai_file.write_text(openai_client_content)
        
        # File utilities
        file_utils_content = '''"""
Common file operations
"""
import os
from pathlib import Path

def ensure_dir(path):
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_size(file_path):
    """Get file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)
'''
        
        utils_file = self.base_path / "01_core_tools/shared/file_utils.py"
        utils_file.write_text(file_utils_content)
        
        # Init file
        init_content = '''"""
Shared utilities for Python projects
"""
from .config import *
from .openai_client import get_openai_client
from .file_utils import ensure_dir, get_file_size
'''
        
        init_file = self.base_path / "01_core_tools/shared/__init__.py"
        init_file.write_text(init_content)
        
        print("✅ Shared libraries created")
    
    def migrate_analysis_scripts(self):
        """Migrate and consolidate analysis scripts."""
        print("🔍 Migrating analysis scripts...")
        
        # Mapping of old files to new locations
        analysis_mapping = {
            "analyze.py": "01_core_tools/content_analyzer/analyzer.py",
            "analyze-mp3-transcript-prompts.py": "01_core_tools/content_analyzer/transcript_analyzer.py", 
            "analyze-mp4s.py": "01_core_tools/content_analyzer/video_analyzer.py",
            "analyze-shorts.py": "01_core_tools/content_analyzer/shorts_analyzer.py",
            "analyze-prompts.py": "01_core_tools/content_analyzer/prompt_analyzer.py",
            "analyze_suno_files.py": "01_core_tools/content_analyzer/file_analyzer.py"
        }
        
        for old_name, new_path in analysis_mapping.items():
            old_file = self.base_path / old_name
            new_file = self.base_path / new_path
            
            if old_file.exists():
                # Ensure destination directory exists
                new_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Move file
                shutil.move(str(old_file), str(new_file))
                self.log_action("MOVE", old_name, new_path)
                
                # Update imports in the moved file
                self.update_imports(new_file)
    
    def migrate_youtube_projects(self):
        """Migrate YouTube-related projects."""
        print("📺 Migrating YouTube projects...")
        
        youtube_mapping = {
            "Auto-YouTube": "02_youtube_automation/auto_youtube",
            "Auto-YouTube-Shorts-Maker": "02_youtube_automation/shorts_maker",
            "Automated Reddit to Youtube Bot": "02_youtube_automation/reddit_to_youtube",
            "Automatic-Video-Generator-for-youtube": "02_youtube_automation/video_generators",
            "automated-yt-channel": "02_youtube_automation/automated_channel"
        }
        
        for old_name, new_path in youtube_mapping.items():
            old_dir = self.base_path / old_name
            new_dir = self.base_path / new_path
            
            if old_dir.exists():
                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                self.log_action("MOVE_DIR", old_name, new_path)
    
    def migrate_ai_creative_tools(self):
        """Migrate AI and creative tools."""
        print("🎨 Migrating AI creative tools...")
        
        ai_mapping = {
            "DALLe": "03_ai_creative_tools/image_generation/dalle",
            "ai-comic-factory": "03_ai_creative_tools/comic_factory",
            "ai-comic-factory-main": "03_ai_creative_tools/comic_factory/main",
            "cross-stitch-pattern-maker": "03_ai_creative_tools/pattern_makers/cross_stitch",
            "AutoTypographyh - lyrics": "03_ai_creative_tools/text_generators/typography"
        }
        
        for old_name, new_path in ai_mapping.items():
            old_dir = self.base_path / old_name
            new_dir = self.base_path / new_path
            
            if old_dir.exists():
                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                self.log_action("MOVE_DIR", old_name, new_path)
    
    def migrate_web_scraping_tools(self):
        """Migrate web scraping tools."""
        print("🕷️  Migrating web scraping tools...")
        
        scraping_mapping = {
            "backlink_checker": "04_web_scraping/backlink_checker",
            "backlink-checker": "04_web_scraping/backlink_checker_v2",
            "Backlinker": "04_web_scraping/backlinker",
            "fiverr-scraping-api": "04_web_scraping/fiverr_scraper",
            "FB-Script-Auto-Post-All-Group": "04_web_scraping/social_media/facebook"
        }
        
        for old_name, new_path in scraping_mapping.items():
            old_dir = self.base_path / old_name
            new_dir = self.base_path / new_path
            
            if old_dir.exists():
                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                self.log_action("MOVE_DIR", old_name, new_path)
    
    def migrate_audio_video_tools(self):
        """Migrate audio/video processing tools."""
        print("🎵 Migrating audio/video tools...")
        
        av_mapping = {
            "AutoTranscribe": "05_audio_video/transcription_tools/auto_transcribe",
            "audiototext.py": "05_audio_video/transcription_tools/audio_to_text.py",
            "convertors": "05_audio_video/media_converters",
            "quiz-talk": "05_audio_video/audio_processors/quiz_talk"
        }
        
        for old_name, new_path in av_mapping.items():
            old_path = self.base_path / old_name
            new_path_full = self.base_path / new_path
            
            if old_path.exists():
                new_path_full.parent.mkdir(parents=True, exist_ok=True)
                if old_path.is_dir():
                    shutil.move(str(old_path), str(new_path_full))
                    self.log_action("MOVE_DIR", old_name, new_path)
                else:
                    shutil.move(str(old_path), str(new_path_full))
                    self.log_action("MOVE", old_name, new_path)
    
    def migrate_utilities(self):
        """Migrate utility tools."""
        print("🔧 Migrating utilities...")
        
        utility_mapping = {
            "folder-file-sorter": "06_utilities/file_organizers/file_sorter",
            "fdupes": "06_utilities/duplicate_finders/fdupes",
            "clean": "06_utilities/system_tools/cleanup",
            "clean-organizer": "06_utilities/file_organizers/clean_organizer",
            "batch": "06_utilities/batch_processors"
        }
        
        for old_name, new_path in utility_mapping.items():
            old_dir = self.base_path / old_name
            new_dir = self.base_path / new_path
            
            if old_dir.exists():
                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                self.log_action("MOVE_DIR", old_name, new_path)
    
    def archive_old_projects(self):
        """Move old and backup projects to archive."""
        print("📦 Archiving old projects...")
        
        # Move backup directories
        backup_dirs = ["sphinx-docs_backup", "sphinx-docs"]
        for backup_dir in backup_dirs:
            old_dir = self.base_path / backup_dir
            if old_dir.exists():
                new_dir = self.base_path / "08_archived/backups" / backup_dir
                new_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_dir), str(new_dir))
                self.log_action("ARCHIVE", backup_dir, f"08_archived/backups/{backup_dir}")
        
        # Move old numbered files
        for file_path in self.base_path.glob("* (1).py"):
            new_path = self.base_path / "08_archived/old_versions" / file_path.name
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(new_path))
            self.log_action("ARCHIVE", file_path.name, f"08_archived/old_versions/{file_path.name}")
    
    def update_imports(self, file_path):
        """Update import statements in moved files."""
        try:
            content = file_path.read_text()
            
            # Update common import patterns
            replacements = {
                "from dotenv import load_dotenv": "from shared.config import *",
                "load_dotenv(os.path.expanduser(\"~/.env\"))": "# Environment loaded from shared.config",
                "openai.api_key = os.getenv(\"OPENAI_API_KEY\")": "from shared.openai_client import get_openai_client",
                "client = OpenAI(api_key=OPENAI_API_KEY)": "client = get_openai_client()"
            }
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            file_path.write_text(content)
            self.log_action("UPDATE_IMPORTS", file_path.name)
            
        except Exception as e:
            self.log_action("UPDATE_IMPORTS", file_path.name, status=f"ERROR: {e}")
    
    def create_readme_files(self):
        """Create README files for each category."""
        print("📝 Creating README files...")
        
        readme_content = {
            "01_core_tools": """# Core Tools
Essential tools for content analysis, transcription, and file management.

## Contents
- `content_analyzer/` - Consolidated analysis tools
- `file_manager/` - File organization utilities  
- `api_clients/` - API integration tools
- `shared/` - Shared libraries and configuration
""",
            "02_youtube_automation": """# YouTube Automation
Complete suite of tools for automated YouTube content creation.

## Contents
- `auto_youtube/` - Main YouTube automation system
- `shorts_maker/` - YouTube Shorts creation
- `reddit_to_youtube/` - Reddit content pipeline
- `video_generators/` - Video creation tools
""",
            "03_ai_creative_tools": """# AI Creative Tools
AI-powered creative content generation tools.

## Contents
- `image_generation/` - DALL-E and image tools
- `comic_factory/` - Comic generation
- `pattern_makers/` - Pattern creation tools
- `text_generators/` - Text and content generation
""",
            "04_web_scraping": """# Web Scraping Tools
Data collection and web scraping utilities.

## Contents
- `backlink_checker/` - SEO backlink analysis
- `fiverr_scraper/` - Fiverr data collection
- `social_media/` - Social media automation
- `news_collectors/` - News and content scraping
""",
            "05_audio_video": """# Audio/Video Processing
Media processing and conversion tools.

## Contents
- `audio_processors/` - Audio conversion and TTS
- `video_editors/` - Video processing tools
- `transcription_tools/` - Transcription utilities
- `media_converters/` - Format conversion tools
""",
            "06_utilities": """# Utilities
General purpose tools and utilities.

## Contents
- `file_organizers/` - File sorting and organization
- `duplicate_finders/` - Duplicate detection
- `batch_processors/` - Batch operations
- `system_tools/` - System maintenance
"""
        }
        
        for category, content in readme_content.items():
            readme_path = self.base_path / category / "README.md"
            readme_path.write_text(content)
            self.log_action("CREATE_README", f"{category}/README.md")
    
    def save_migration_log(self):
        """Save migration log for rollback capability."""
        log_file = self.base_path / "migration_log.json"
        with open(log_file, 'w') as f:
            json.dump(self.migration_log, f, indent=2)
        print(f"📋 Migration log saved to: {log_file}")
    
    def run_migration(self):
        """Run the complete migration process."""
        print("🚀 Starting Python Projects Migration")
        print("=" * 50)
        
        try:
            # Phase 1: Backup and setup
            self.create_backup()
            self.create_new_structure()
            self.create_shared_libraries()
            
            # Phase 2: Migrate projects
            self.migrate_analysis_scripts()
            self.migrate_youtube_projects()
            self.migrate_ai_creative_tools()
            self.migrate_web_scraping_tools()
            self.migrate_audio_video_tools()
            self.migrate_utilities()
            
            # Phase 3: Cleanup
            self.archive_old_projects()
            self.create_readme_files()
            self.save_migration_log()
            
            print("\n✅ Migration completed successfully!")
            print(f"📊 Total actions: {len(self.migration_log)}")
            print(f"📁 New structure created in: {self.base_path}")
            print(f"💾 Backup available at: {self.backup_path}")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            print("🔄 Check migration_log.json for details")
            print("🔄 Use backup to restore if needed")

if __name__ == "__main__":
    migrator = ProjectMigrator()
    migrator.run_migration()