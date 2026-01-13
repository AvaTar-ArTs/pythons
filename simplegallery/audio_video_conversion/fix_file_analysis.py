#!/usr/bin/env python3
"""
Fix file type analysis - properly categorize by actual file type, not content
"""

import shutil
from pathlib import Path


def analyze_file_type(file_path):
    """Analyze file based on actual file type, not content"""
    
    file_name = file_path.name.lower()
    file_ext = file_path.suffix.lower()
    
    # Compiled Python files
    if (file_ext == '.pyc' or 
        '.cpython-' in file_name or 
        file_name.endswith('.pyc') or
        file_name.endswith('.pyo')):
        return "Compiled_Python"
    
    # Cython files
    if (file_ext == '.pxd' or 
        file_ext == '.pyx' or 
        '.cython-' in file_name or
        file_name.endswith('.pxd') or
        file_name.endswith('.pyx')):
        return "Cython_Files"
    
    # Shared libraries and binaries
    if (file_ext == '.so' or 
        file_ext == '.dll' or 
        file_ext == '.dylib' or
        file_name.endswith('.so') or
        file_name.endswith('.dll') or
        file_name.endswith('.dylib') or
        '.so' in file_name):
        return "Binaries_Libraries"
    
    # Node modules and dependencies
    if (file_name == 'package.json' or
        file_name == 'node_modules' or
        'node_modules' in str(file_path) or
        file_name.endswith('.lock')):
        return "Node_Modules"
    
    # Git and version control
    if (file_name.startswith('.git') or
        file_name == '.gitignore' or
        file_name == '.gitattributes' or
        file_name.endswith('.git')):
        return "Git_Files"
    
    # Configuration files
    if (file_ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'] or
        file_name in ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile']):
        return "Config_Files"
    
    # Documentation
    if (file_ext in ['.md', '.txt', '.rst', '.doc', '.docx'] or
        file_name in ['readme', 'license', 'changelog', 'history']):
        return "Documentation"
    
    # Images
    if file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.bmp', '.tiff']:
        return "Images"
    
    # Videos and audio
    if file_ext in ['.mp4', '.avi', '.mov', '.wmv', '.mp3', '.wav', '.flac', '.aac']:
        return "Media_Files"
    
    # Archives
    if file_ext in ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2']:
        return "Archives"
    
    # Python source files (actual .py files)
    if file_ext == '.py':
        return analyze_python_content(file_path)
    
    # HTML files
    if file_ext in ['.html', '.htm']:
        return "HTML_Files"
    
    # CSS files
    if file_ext in ['.css', '.scss', '.sass', '.less']:
        return "CSS_Files"
    
    # JavaScript files
    if file_ext in ['.js', '.jsx', '.ts', '.tsx', '.mjs']:
        return "JavaScript_Files"
    
    # Shell scripts
    if file_ext in ['.sh', '.bash', '.zsh', '.fish'] or file_name.startswith('.'):
        return "Shell_Scripts"
    
    # Default fallback
    return "Other_Files"

def analyze_python_content(file_path):
    """Analyze Python source files by content"""
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1024)  # Read first 1KB
    except:
        return "Python_General"
    
    content_lower = content.lower()
    
    # AI/ML Python files
    ai_keywords = [
        'import tensorflow', 'import torch', 'import sklearn', 'import pandas',
        'import numpy', 'neural network', 'machine learning', 'deep learning',
        'artificial intelligence', 'openai', 'gpt', 'whisper', 'transcription',
        'audio_to_text', 'text_to_speech', 'tts', 'stt', 'ai', 'ml'
    ]
    
    if any(keyword in content_lower for keyword in ai_keywords):
        return "Python_AI"
    
    # Web Python files
    web_keywords = [
        'flask', 'django', 'fastapi', 'requests', 'urllib', 'http', 'api',
        'web', 'html', 'css', 'javascript', 'frontend', 'backend', 'server'
    ]
    
    if any(keyword in content_lower for keyword in web_keywords):
        return "Python_Web"
    
    # Tool/Utility Python files
    tool_keywords = [
        'automation', 'tool', 'utility', 'script', 'batch', 'process',
        'file', 'organize', 'manage', 'helper', 'util'
    ]
    
    if any(keyword in content_lower for keyword in tool_keywords):
        return "Python_Tools"
    
    # Default Python files
    return "Python_General"

def reorganize_files():
    """Reorganize files by actual file type"""
    
    base_dir = Path("/Users/steven/Documents/Code")
    
    # Create proper file type folders
    file_type_folders = {
        "Python_AI": "AI and ML Python source files",
        "Python_Web": "Web development Python source files", 
        "Python_Tools": "Tool and utility Python source files",
        "Python_General": "General Python source files",
        "Compiled_Python": "Compiled Python bytecode (.pyc, .pyo)",
        "Cython_Files": "Cython files (.pxd, .pyx)",
        "Binaries_Libraries": "Shared libraries and binaries (.so, .dll, .dylib)",
        "Node_Modules": "Node.js modules and dependencies",
        "Git_Files": "Git and version control files",
        "Config_Files": "Configuration files (.json, .yaml, .txt)",
        "Documentation": "Documentation files (.md, .txt, .rst)",
        "Images": "Image files (.png, .jpg, .svg, etc.)",
        "Media_Files": "Video and audio files",
        "Archives": "Compressed archives (.zip, .tar, .gz)",
        "HTML_Files": "HTML files and templates",
        "CSS_Files": "CSS and styling files",
        "JavaScript_Files": "JavaScript and TypeScript files",
        "Shell_Scripts": "Shell scripts (.sh, .bash, .zsh)",
        "Other_Files": "Other file types"
    }
    
    # Create folders
    for folder, desc in file_type_folders.items():
        folder_path = base_dir / folder
        folder_path.mkdir(exist_ok=True)
        print(f"✅ Created {folder}: {desc}")
    
    # Process all current folders
    current_folders = [
        "Python_AI", "Python_Tools", "Python_Utils", "Python_Web",
        "Web_HTML", "Web_CSS", "Web_JS", "Web_Projects",
        "Assets_Docs", "Assets_Images", "Scripts_All"
    ]
    
    for folder in current_folders:
        folder_path = base_dir / folder
        if folder_path.exists():
            print(f"\n🔍 Processing {folder}...")
            process_folder(folder_path, base_dir)

def process_folder(source_folder, base_dir):
    """Process a folder and move files to correct type folders"""
    
    if not source_folder.exists():
        return
        
    file_count = 0
    for file_path in source_folder.rglob("*"):
        if file_path.is_file():
            # Skip system files
            if file_path.name.startswith('.') and not file_path.name.startswith('.git'):
                continue
                
            # Analyze file type
            target_folder = analyze_file_type(file_path)
            
            if target_folder:
                target_path = base_dir / target_folder / file_path.name
                
                # Handle duplicate names
                counter = 1
                original_target = target_path
                while target_path.exists():
                    stem = original_target.stem
                    suffix = original_target.suffix
                    target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                try:
                    shutil.move(str(file_path), str(target_path))
                    print(f"  📄 {file_path.name} → {target_folder}/")
                    file_count += 1
                except Exception as e:
                    print(f"  ❌ Error moving {file_path.name}: {e}")
    
    print(f"  ✅ Moved {file_count} files from {source_folder.name}")

if __name__ == "__main__":
    print("🚀 Starting proper file type analysis and reorganization...")
    print("📊 Analyzing files by actual type, not content...")
    reorganize_files()
    print("\n✅ Proper file type organization complete!")