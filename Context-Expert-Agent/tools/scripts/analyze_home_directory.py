#!/usr/bin/env python3
"""
Home Directory Deep Analysis
Comprehensive scan of ~/  to map development environment, projects, and configurations
"""

import os
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import json

class HomeDirectoryAnalyzer:
    def __init__(self, home_dir=None):
        self.home = Path(home_dir or Path.home())
        self.analysis = {
            'overview': {},
            'major_directories': {},
            'dev_environment': {},
            'config_files': {},
            'project_directories': {},
            'hidden_configs': {},
            'api_keys': {},
            'languages': Counter(),
            'frameworks': Counter(),
            'tools': set()
        }

    def analyze_size(self, path, max_depth=1):
        """Get directory size and file count"""
        total_size = 0
        total_files = 0

        try:
            for item in path.rglob('*'):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                        total_files += 1
                    except:
                        pass
        except:
            pass

        return total_size, total_files

    def detect_project_type(self, path):
        """Detect what type of project this is"""
        indicators = {
            'Python': ['setup.py', 'pyproject.toml', 'requirements.txt', 'Pipfile'],
            'Node.js': ['package.json', 'package-lock.json', 'yarn.lock'],
            'Ruby': ['Gemfile', 'Rakefile', '.ruby-version'],
            'Go': ['go.mod', 'go.sum'],
            'Rust': ['Cargo.toml', 'Cargo.lock'],
            'PHP': ['composer.json', 'composer.lock'],
            'Java': ['pom.xml', 'build.gradle', 'gradlew'],
            'C#': ['.csproj', '.sln'],
            'Frontend': ['webpack.config.js', 'vite.config.js', 'next.config.js'],
            'Docker': ['Dockerfile', 'docker-compose.yml'],
            'AI/ML': ['model.pkl', 'checkpoint', '.ipynb'],
        }

        detected = set()
        try:
            for file in path.iterdir():
                if file.is_file():
                    for lang, files in indicators.items():
                        if file.name in files:
                            detected.add(lang)
        except:
            pass

        return list(detected)

    def scan_major_directories(self):
        """Scan main directories in home"""
        print("📂 Scanning major directories...")

        major_dirs = [
            'AVATARARTS', 'Documents', 'Downloads', 'Music', 'GitHub',
            'Desktop', 'Claude-Courses', 'scripts', 'pythons'
        ]

        for dirname in major_dirs:
            dir_path = self.home / dirname
            if dir_path.exists():
                size, files = self.analyze_size(dir_path)
                project_types = self.detect_project_type(dir_path)

                self.analysis['major_directories'][dirname] = {
                    'path': str(dir_path),
                    'size_bytes': size,
                    'size_gb': size / (1024**3),
                    'file_count': files,
                    'project_types': project_types
                }

                print(f"   ✓ {dirname}: {size/(1024**3):.2f} GB, {files:,} files")

    def scan_hidden_configs(self):
        """Scan hidden configuration files and directories"""
        print("\n🔧 Scanning configuration files...")

        config_patterns = {
            'Shell': ['.bashrc', '.bash_profile', '.zshrc', '.zprofile'],
            'Git': ['.gitconfig', '.gitignore_global'],
            'Editor': ['.vimrc', '.nanorc'],
            'Python': ['.pypirc', '.condarc'],
            'Node': ['.npmrc', '.yarnrc'],
            'Claude': ['.claude.json', '.claude/CLAUDE.md'],
            'AI Tools': ['.aider.conf.yml', '.cursor'],
        }

        for category, files in config_patterns.items():
            found = []
            for filename in files:
                filepath = self.home / filename
                if filepath.exists():
                    try:
                        size = filepath.stat().st_size if filepath.is_file() else 0
                        found.append({
                            'file': filename,
                            'size': size,
                            'path': str(filepath)
                        })
                    except:
                        pass

            if found:
                self.analysis['config_files'][category] = found
                print(f"   ✓ {category}: {len(found)} files")

    def scan_env_directory(self):
        """Deep scan of ~/.env.d/ for API keys and configs"""
        print("\n🔑 Scanning API key management...")

        env_dir = self.home / '.env.d'
        if not env_dir.exists():
            return

        env_files = defaultdict(list)
        api_inventory = []

        try:
            for file in env_dir.iterdir():
                if file.is_file() and file.suffix == '.env':
                    category = file.stem
                    env_files[category].append(str(file.name))

                    # Count API keys
                    try:
                        with open(file, 'r') as f:
                            content = f.read()
                            keys = len([line for line in content.split('\n')
                                      if '=' in line and not line.strip().startswith('#')])
                            api_inventory.append({
                                'file': file.name,
                                'keys': keys
                            })
                    except:
                        pass

            self.analysis['api_keys'] = {
                'total_env_files': len(env_files),
                'categories': dict(env_files),
                'inventory': api_inventory,
                'management_scripts': [
                    str(f.name) for f in env_dir.iterdir()
                    if f.suffix in ['.sh', '.py']
                ]
            }

            total_keys = sum(item['keys'] for item in api_inventory)
            print(f"   ✓ Found {len(env_files)} .env files with ~{total_keys} API keys")
            print(f"   ✓ Management scripts: {len(self.analysis['api_keys']['management_scripts'])}")

        except Exception as e:
            print(f"   ⚠️  Error scanning .env.d: {e}")

    def detect_development_environment(self):
        """Detect installed development tools and environments"""
        print("\n🛠️  Detecting development environment...")

        tools = {
            'Python Environments': [
                ('.pyenv', 'pyenv'),
                ('.conda', 'Anaconda/Miniconda'),
                ('/usr/local/Caskroom/miniforge', 'Miniforge'),
            ],
            'Version Control': [
                ('.gitconfig', 'Git'),
                ('.gh', 'GitHub CLI'),
            ],
            'AI Tools': [
                ('.aider', 'Aider'),
                ('.cursor', 'Cursor'),
                ('.claude', 'Claude Code'),
                ('.chatgpt', 'ChatGPT CLI'),
                ('.gemini', 'Gemini CLI'),
            ],
            'Package Managers': [
                ('.npm', 'npm'),
                ('.yarn', 'Yarn'),
                ('.bun', 'Bun'),
                ('.cargo', 'Cargo (Rust)'),
                ('.gem', 'RubyGems'),
            ],
            'Editors & IDEs': [
                ('.vscode', 'VS Code'),
                ('.cursor', 'Cursor'),
                ('.config/nvim', 'Neovim'),
            ]
        }

        for category, checks in tools.items():
            found = []
            for path_check, tool_name in checks:
                check_path = self.home / path_check
                if check_path.exists():
                    found.append(tool_name)
                    self.analysis['tools'].add(tool_name)

            if found:
                self.analysis['dev_environment'][category] = found
                print(f"   ✓ {category}: {', '.join(found)}")

    def scan_project_directories(self):
        """Identify and categorize project directories"""
        print("\n📦 Scanning project directories...")

        project_roots = ['GitHub', 'pythons', 'scripts', 'AVATARARTS']

        for root_name in project_roots:
            root_path = self.home / root_name
            if not root_path.exists():
                continue

            projects = []
            try:
                for item in root_path.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        project_types = self.detect_project_type(item)
                        if project_types:
                            size, files = self.analyze_size(item)
                            projects.append({
                                'name': item.name,
                                'types': project_types,
                                'size_mb': size / (1024**2),
                                'files': files
                            })

                self.analysis['project_directories'][root_name] = {
                    'total_projects': len(projects),
                    'projects': sorted(projects, key=lambda x: x['size_mb'], reverse=True)[:20]
                }

                print(f"   ✓ {root_name}: {len(projects)} projects")
            except Exception as e:
                print(f"   ⚠️  Error scanning {root_name}: {e}")

    def generate_overview(self):
        """Generate high-level overview statistics"""
        print("\n📊 Generating overview...")

        self.analysis['overview'] = {
            'home_directory': str(self.home),
            'scan_time': datetime.now().isoformat(),
            'total_major_dirs': len(self.analysis['major_directories']),
            'total_size_gb': sum(
                d['size_gb'] for d in self.analysis['major_directories'].values()
            ),
            'total_files': sum(
                d['file_count'] for d in self.analysis['major_directories'].values()
            ),
            'config_categories': len(self.analysis['config_files']),
            'dev_tools_detected': len(self.analysis['tools']),
        }

    def generate_markdown_report(self, output_path):
        """Generate comprehensive Markdown report"""
        md = f"""# Home Directory Deep Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Home Directory:** `{self.home}`
**Total Size:** {self.analysis['overview']['total_size_gb']:.2f} GB
**Total Files:** {self.analysis['overview']['total_files']:,}

---

## 📊 Overview

| Metric | Value |
|--------|------:|
| Major Directories Scanned | {self.analysis['overview']['total_major_dirs']} |
| Total Storage Used | {self.analysis['overview']['total_size_gb']:.2f} GB |
| Total Files | {self.analysis['overview']['total_files']:,} |
| Configuration Categories | {self.analysis['overview']['config_categories']} |
| Development Tools Detected | {self.analysis['overview']['dev_tools_detected']} |

---

## 📂 Major Directories

| Directory | Size (GB) | Files | Project Types |
|-----------|----------:|------:|---------------|
"""

        for name, data in sorted(
            self.analysis['major_directories'].items(),
            key=lambda x: x[1]['size_gb'],
            reverse=True
        ):
            types = ', '.join(data['project_types']) if data['project_types'] else '-'
            md += f"| `{name}` | {data['size_gb']:.2f} | {data['file_count']:,} | {types} |\n"

        md += "\n---\n\n## 🛠️  Development Environment\n\n"

        for category, tools in self.analysis['dev_environment'].items():
            md += f"### {category}\n\n"
            for tool in tools:
                md += f"- ✅ {tool}\n"
            md += "\n"

        md += "---\n\n## 🔧 Configuration Files\n\n"

        for category, files in self.analysis['config_files'].items():
            md += f"### {category}\n\n"
            for file_info in files:
                size_kb = file_info['size'] / 1024
                md += f"- `{file_info['file']}` ({size_kb:.1f} KB)\n"
            md += "\n"

        if self.analysis['api_keys']:
            md += "---\n\n## 🔑 API Key Management (~/.env.d/)\n\n"
            api_data = self.analysis['api_keys']
            md += f"**Total .env files:** {api_data['total_env_files']}\n"
            md += f"**Management scripts:** {len(api_data.get('management_scripts', []))}\n\n"

            md += "### Environment Files\n\n"
            for file_info in api_data.get('inventory', []):
                md += f"- `{file_info['file']}` - {file_info['keys']} keys\n"

            md += "\n### Management Scripts\n\n"
            for script in api_data.get('management_scripts', []):
                md += f"- `{script}`\n"

        md += "\n---\n\n## 📦 Project Directories\n\n"

        for root_name, data in self.analysis['project_directories'].items():
            md += f"### {root_name} ({data['total_projects']} projects)\n\n"
            md += "| Project | Types | Size (MB) | Files |\n"
            md += "|---------|-------|----------:|------:|\n"

            for proj in data['projects'][:15]:
                types = ', '.join(proj['types'])
                md += f"| `{proj['name']}` | {types} | {proj['size_mb']:.1f} | {proj['files']:,} |\n"

            md += "\n"

        md += """---

## 🎯 Key Findings

### Storage Distribution
"""

        sorted_dirs = sorted(
            self.analysis['major_directories'].items(),
            key=lambda x: x[1]['size_gb'],
            reverse=True
        )[:5]

        for name, data in sorted_dirs:
            percentage = (data['size_gb'] / self.analysis['overview']['total_size_gb']) * 100
            md += f"- **{name}**: {data['size_gb']:.2f} GB ({percentage:.1f}%)\n"

        md += f"""

### Development Setup
- **Primary Languages:** {', '.join(sorted(self.analysis['tools']))[:100]}
- **Total Tools:** {len(self.analysis['tools'])}

### Organization Opportunities
- Downloads directory: {self.analysis['major_directories'].get('Downloads', {}).get('size_gb', 0):.2f} GB (consider cleanup)
- Music directory: {self.analysis['major_directories'].get('Music', {}).get('size_gb', 0):.2f} GB (organized with nocTurneMeLoDieS)
- Documents: {self.analysis['major_directories'].get('Documents', {}).get('size_gb', 0):.2f} GB

---

*Report generated by Home Directory Analyzer*
"""

        with open(output_path, 'w') as f:
            f.write(md)

        print(f"\n✅ Report saved to: {output_path}")
        return output_path

    def generate_json_export(self, output_path):
        """Export analysis as JSON"""
        # Convert sets to lists for JSON serialization
        export_data = self.analysis.copy()
        export_data['tools'] = list(export_data['tools'])
        export_data['languages'] = dict(export_data['languages'])
        export_data['frameworks'] = dict(export_data['frameworks'])

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✅ JSON export saved to: {output_path}")
        return output_path

    def run_full_analysis(self):
        """Run complete home directory analysis"""
        print("=" * 60)
        print("HOME DIRECTORY DEEP ANALYSIS")
        print("=" * 60)
        print()

        self.scan_major_directories()
        self.scan_hidden_configs()
        self.scan_env_directory()
        self.detect_development_environment()
        self.scan_project_directories()
        self.generate_overview()

        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETE")
        print("=" * 60)

        # Generate reports
        md_path = Path.cwd() / "HOME_DIRECTORY_ANALYSIS.md"
        json_path = Path.cwd() / "home_directory_analysis.json"

        self.generate_markdown_report(md_path)
        self.generate_json_export(json_path)

        print(f"\n📊 Summary:")
        print(f"   Total storage: {self.analysis['overview']['total_size_gb']:.2f} GB")
        print(f"   Total files: {self.analysis['overview']['total_files']:,}")
        print(f"   Development tools: {len(self.analysis['tools'])}")
        print()

def main():
    analyzer = HomeDirectoryAnalyzer()
    analyzer.run_full_analysis()

if __name__ == "__main__":
    main()
