#!/usr/bin/env python3
"""
Comprehensive analysis of Python projects for Miniforge/Mamba setup.
Analyzes ~/pythons, ~/pythons-sort, and ~/ directories.
"""
import os
import re
import json
from pathlib import Path
from collections import defaultdict
import subprocess

# Directories to analyze
directories = [
    Path.home() / 'pythons',
    Path.home() / 'pythons-sort',
    # Path.home()  # Excluding home directory due to Google Drive sync issues
]

output_dir = Path('/Users/steven/Miniforge_Mamba_Analysis')
output_dir.mkdir(exist_ok=True)

# Standard library modules (don't need to be installed)
STDLIB_MODULES = {
    'abc', 'argparse', 'ast', 'asyncio', 'base64', 'binascii', 'bisect',
    'builtins', 'bz2', 'calendar', 'collections', 'copy', 'csv', 'datetime',
    'decimal', 'difflib', 'email', 'encodings', 'enum', 'fileinput', 'fnmatch',
    'fractions', 'functools', 'gc', 'getopt', 'getpass', 'glob', 'gzip',
    'hashlib', 'heapq', 'html', 'http', 'importlib', 'inspect', 'io',
    'itertools', 'json', 'keyword', 'linecache', 'locale', 'logging',
    'math', 'mimetypes', 'multiprocessing', 'netrc', 'numbers', 'operator',
    'os', 'pathlib', 'pickle', 'pkgutil', 'platform', 'plistlib', 'pprint',
    'profile', 'pstats', 'queue', 'quopri', 'random', 're', 'readline',
    'reprlib', 'resource', 'runpy', 'secrets', 'select', 'shlex', 'shutil',
    'signal', 'socket', 'socketserver', 'sqlite3', 'ssl', 'stat', 'statistics',
    'string', 'stringprep', 'struct', 'subprocess', 'sys', 'tarfile', 'tempfile',
    'termios', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token',
    'tokenize', 'trace', 'traceback', 'tracemalloc', 'tty', 'turtle', 'types',
    'typing', 'unicodedata', 'unittest', 'urllib', 'uu', 'uuid', 'venv',
    'warnings', 'wave', 'weakref', 'webbrowser', 'winreg', 'winsound',
    'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipfile', 'zipimport', 'zlib',
    '__future__', '__main__', '_abc', '_ast', '_bisect', '_blake2', '_codecs',
    '_collections', '_collections_abc', '_compat_pickle', '_compression',
    '_csv', '_datetime', '_decimal', '_elementtree', '_functools', '_hashlib',
    '_heapq', '_imp', '_io', '_json', '_locale', '_lsprof', '_lzma', '_md5',
    '_multibytecodec', '_multiprocessing', '_opcode', '_operator', '_pickle',
    '_posixsubprocess', '_py_abc', '_pydecimal', '_random', '_sha1', '_sha256',
    '_sha512', '_signal', '_socket', '_sre', '_ssl', '_stat', '_statistics',
    '_string', '_struct', '_symtable', '_thread', '_threading_local', '_tkinter',
    '_tracemalloc', '_warnings', '_weakref', '_weakrefset', '_winapi', '_winreg',
    '_xxsubinterpreters', 'array', 'atexit', 'audioop', 'binascii', 'cgi',
    'cgitb', 'chunk', 'cmd', 'code', 'codecs', 'codeop', 'colorsys', 'compileall',
    'concurrent', 'configparser', 'contextlib', 'contextvars', 'copyreg',
    'crypt', 'ctypes', 'curses', 'dbm', 'dis', 'distutils', 'doctest', 'dummy_threading',
    'ensurepip', 'errno', 'faulthandler', 'fcntl', 'formatter', 'ftplib', 'gettext',
    'grp', 'gzip', 'hashlib', 'hmac', 'html', 'http', 'idlelib', 'imaplib',
    'imp', 'inspect', 'ipaddress', 'lib2to3', 'mailbox', 'mailcap', 'marshal',
    'msilib', 'msvcrt', 'nis', 'nntplib', 'nt', 'ntpath', 'nturl2path', 'optparse',
    'os2', 'os2emxpath', 'pdb', 'pickletools', 'pipes', 'pkg_resources', 'posix',
    'posixpath', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri',
    'rlcompleter', 'sched', 'selectors', 'shelve', 'site', 'smtpd', 'smtplib',
    'sndhdr', 'spwd', 'sqlite3', 'sre_compile', 'sre_constants', 'sre_parse',
    'ssl', 'stat', 'statistics', 'stringprep', 'sunau', 'symbol', 'symtable',
    'sysconfig', 'tabnanny', 'telnetlib', 'test', 'textwrap', 'this', 'time',
    'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback', 'tracemalloc',
    'tty', 'turtle', 'types', 'typing', 'unicodedata', 'unittest', 'urllib',
    'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg',
    'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipfile', 'zipimport', 'zlib'
}

def extract_imports(file_path):
    """Extract import statements from a Python file"""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Remove comments and docstrings
            lines = []
            in_docstring = False
            for line in content.split('\n'):
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = not in_docstring
                    continue
                if in_docstring:
                    continue
                if '#' in line:
                    line = line[:line.index('#')]
                lines.append(line)
            
            content = '\n'.join(lines)
            
            # Find import statements
            import_pattern = r'^(?:import\s+(\S+)|from\s+(\S+)\s+import)'
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                match = re.match(import_pattern, line)
                if match:
                    module = match.group(1) or match.group(2)
                    if module:
                        # Clean up module name
                        module = module.split('.')[0].split(' as ')[0].strip('"\'')
                        if module and not module.startswith('.'):
                            imports.add(module)
    except Exception as e:
        pass
    return imports

def get_package_mapping():
    """Map import names to conda/mamba package names"""
    # Common mappings
    mappings = {
        'PIL': 'pillow',
        'cv2': 'opencv',
        'yaml': 'pyyaml',
        'sklearn': 'scikit-learn',
        'bs4': 'beautifulsoup4',
        'lxml': 'lxml',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'matplotlib': 'matplotlib',
        'scipy': 'scipy',
        'requests': 'requests',
        'flask': 'flask',
        'django': 'django',
        'tensorflow': 'tensorflow',
        'torch': 'pytorch',
        'IPython': 'ipython',
        'jupyter': 'jupyter',
        'notebook': 'notebook',
        'pytest': 'pytest',
        'selenium': 'selenium',
        'beautifulsoup4': 'beautifulsoup4',
    }
    return mappings

def analyze_directory(directory):
    """Analyze a directory for Python dependencies"""
    print(f"\nAnalyzing: {directory}")
    
    all_imports = defaultdict(set)
    file_count = 0
    python_files = []
    
    if not directory.exists():
        print(f"  Directory does not exist: {directory}")
        return all_imports, file_count, python_files
    
    # Additional exclude patterns for home directory
    home_excludes = ['Library/CloudStorage', '.cache', '.local', '.conda', 
                    '.mamba', 'Downloads/google-cloud-sdk', 'Downloads/us.sitesucker']
    
    try:
        for py_file in directory.rglob('*.py'):
            # Skip common exclude patterns
            skip_patterns = ['venv', '.venv', '__pycache__', '.git', 'node_modules',
                            'google-cloud-sdk', 'site-packages', '.pytest_cache',
                            'Library/CloudStorage', '.cache', '.local']
            if any(pattern in str(py_file) for pattern in skip_patterns):
                continue
            
            # Additional home directory exclusions
            if directory == Path.home():
                if any(excl in str(py_file) for excl in home_excludes):
                    continue
        
        file_count += 1
        python_files.append(str(py_file.relative_to(directory)))
        
        imports = extract_imports(py_file)
        for imp in imports:
            all_imports[imp].add(str(py_file.relative_to(directory)))
        
            if file_count % 1000 == 0:
                print(f"  Processed {file_count} files...")
    except (TimeoutError, PermissionError, OSError) as e:
        print(f"  Warning: Stopped scanning due to: {type(e).__name__}")
        print(f"  Processed {file_count} files before stopping")
    
    print(f"  Total Python files: {file_count}")
    print(f"  Unique imports: {len(all_imports)}")
    
    return all_imports, file_count, python_files

def generate_environment_yml(imports_dict, directory_name, output_path):
    """Generate environment.yml for conda/mamba"""
    # Filter out stdlib and get third-party packages
    third_party = {}
    package_mapping = get_package_mapping()
    
    for module, files in imports_dict.items():
        if module not in STDLIB_MODULES and not module.startswith('_'):
            # Map to conda package name
            conda_name = package_mapping.get(module, module.lower().replace('_', '-'))
            if conda_name not in third_party:
                third_party[conda_name] = {'module': module, 'files': len(files)}
    
    # Sort by frequency
    sorted_packages = sorted(third_party.items(), key=lambda x: x[1]['files'], reverse=True)
    
    with open(output_path, 'w') as f:
        f.write(f"# Environment file for {directory_name}\n")
        f.write("# Generated automatically from Python import analysis\n")
        f.write("# Use: mamba env create -f {}\n".format(output_path.name))
        f.write("# Or: conda env create -f {}\n\n".format(output_path.name))
        f.write("name: {}\n".format(directory_name.replace('/', '_').replace('-', '_')))
        f.write("channels:\n")
        f.write("  - conda-forge\n")
        f.write("  - defaults\n")
        f.write("dependencies:\n")
        f.write("  - python=3.12\n")
        f.write("  - pip\n")
        f.write("  # Most frequently used packages:\n")
        
        for conda_name, info in sorted_packages[:50]:  # Top 50
            f.write(f"  - {conda_name}  # {info['module']} (used in {info['files']} files)\n")
        
        f.write("\n  # Additional packages via pip (if not available in conda):\n")
        f.write("  - pip:\n")
        for conda_name, info in sorted_packages[50:100]:  # Next 50 via pip
            f.write(f"    - {info['module']}  # {conda_name}\n")
    
    return sorted_packages

print("="*70)
print("MINIFORGE/MAMBA ANALYSIS FOR PYTHON PROJECTS")
print("="*70)

all_results = {}
combined_imports = defaultdict(set)

for directory in directories:
    imports, file_count, python_files = analyze_directory(directory)
    dir_name = directory.name if directory != Path.home() else 'home'
    all_results[dir_name] = {
        'imports': imports,
        'file_count': file_count,
        'python_files': python_files,
        'directory': str(directory)
    }
    
    # Combine for overall analysis
    for module, files in imports.items():
        combined_imports[module].update(files)

# Generate individual environment files
print("\n" + "="*70)
print("GENERATING ENVIRONMENT FILES")
print("="*70)

for dir_name, results in all_results.items():
    env_file = output_dir / f"{dir_name}_environment.yml"
    print(f"\nGenerating: {env_file.name}")
    packages = generate_environment_yml(results['imports'], dir_name, env_file)
    print(f"  Top packages: {len(packages)}")

# Generate combined environment file
print("\nGenerating combined environment file...")
combined_env = output_dir / "combined_environment.yml"
packages = generate_environment_yml(combined_imports, "combined_all_projects", combined_env)
print(f"  Total packages: {len(packages)}")

# Generate comprehensive report
report_file = output_dir / "analysis_report.md"
with open(report_file, 'w') as f:
    f.write("# Miniforge/Mamba Analysis Report\n\n")
    f.write("## Summary\n\n")
    f.write(f"- **Directories Analyzed:** {len(directories)}\n")
    f.write(f"- **Total Python Files:** {sum(r['file_count'] for r in all_results.values())}\n")
    f.write(f"- **Unique Import Modules:** {len(combined_imports)}\n\n")
    
    f.write("## Directory Breakdown\n\n")
    for dir_name, results in all_results.items():
        f.write(f"### {dir_name}\n\n")
        f.write(f"- **Directory:** `{results['directory']}`\n")
        f.write(f"- **Python Files:** {results['file_count']:,}\n")
        f.write(f"- **Unique Imports:** {len(results['imports'])}\n")
        f.write(f"- **Environment File:** `{dir_name}_environment.yml`\n\n")
        
        # Top 20 imports
        sorted_imports = sorted(results['imports'].items(), 
                               key=lambda x: len(x[1]), reverse=True)
        f.write("**Top 20 Most Used Imports:**\n\n")
        for module, files in sorted_imports[:20]:
            f.write(f"- `{module}` - used in {len(files)} files\n")
        f.write("\n")
    
    f.write("## Combined Analysis\n\n")
    f.write("**Top 30 Most Used Imports Across All Projects:**\n\n")
    sorted_combined = sorted(combined_imports.items(), 
                           key=lambda x: len(x[1]), reverse=True)
    for module, files in sorted_combined[:30]:
        f.write(f"- `{module}` - used in {len(files)} files\n")
    f.write("\n")
    
    f.write("## Usage Instructions\n\n")
    f.write("### Install Miniforge/Mamba\n\n")
    f.write("```bash\n")
    f.write("# Download and install Miniforge from:\n")
    f.write("# https://github.com/conda-forge/miniforge\n\n")
    f.write("# Or install via Homebrew:\n")
    f.write("brew install miniforge\n")
    f.write("```\n\n")
    
    f.write("### Create Environments\n\n")
    f.write("```bash\n")
    f.write("# Using mamba (faster):\n")
    for dir_name in all_results.keys():
        f.write(f"mamba env create -f {dir_name}_environment.yml\n")
    f.write("mamba env create -f combined_environment.yml\n\n")
    f.write("# Using conda:\n")
    for dir_name in all_results.keys():
        f.write(f"conda env create -f {dir_name}_environment.yml\n")
    f.write("conda env create -f combined_environment.yml\n")
    f.write("```\n\n")
    
    f.write("### Activate Environment\n\n")
    f.write("```bash\n")
    f.write("mamba activate <environment_name>\n")
    f.write("# or\n")
    f.write("conda activate <environment_name>\n")
    f.write("```\n\n")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print(f"{'='*70}")
print(f"\nReports saved to: {output_dir}")
print(f"  - Individual environment files for each directory")
print(f"  - Combined environment file")
print(f"  - Analysis report: {report_file.name}")
print(f"\n{'='*70}\n")
