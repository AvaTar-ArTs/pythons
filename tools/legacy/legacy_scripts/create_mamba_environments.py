#!/usr/bin/env python3
"""
Create Miniforge/Mamba environment files from requirements.txt files
and analyze ~/pythons, ~/pythons-sort directories.
"""

from pathlib import Path
import re

output_dir = Path("/Users/steven/Miniforge_Mamba_Analysis")
output_dir.mkdir(exist_ok=True)

# Package mappings for conda-forge
CONDA_MAPPINGS = {
    "pillow": "PIL",
    "opencv": "cv2",
    "pyyaml": "yaml",
    "scikit-learn": "sklearn",
    "beautifulsoup4": "bs4",
    "lxml": "lxml",
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "scipy": "scipy",
    "requests": "requests",
    "flask": "flask",
    "django": "django",
    "tensorflow": "tensorflow",
    "pytorch": "torch",
    "ipython": "IPython",
    "jupyter": "jupyter",
    "notebook": "notebook",
    "pytest": "pytest",
    "selenium": "selenium",
    "seaborn": "seaborn",
    "plotly": "plotly",
    "keras": "keras",
    "torch": "torch",
    "transformers": "transformers",
    "openai": "openai",
    "anthropic": "anthropic",
    "langchain": "langchain",
    "aiohttp": "aiohttp",
    "httpx": "httpx",
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "sqlalchemy": "sqlalchemy",
    "pymongo": "pymongo",
    "redis": "redis",
    "celery": "celery",
    "pydantic": "pydantic",
    "click": "click",
    "rich": "rich",
    "tqdm": "tqdm",
    "python-dotenv": "dotenv",
}

# Reverse mapping
REVERSE_MAPPING = {v: k for k, v in CONDA_MAPPINGS.items()}

STDLIB = {
    "json",
    "random",
    "datetime",
    "collections",
    "os",
    "sys",
    "pathlib",
    "re",
    "subprocess",
    "shutil",
    "glob",
    "itertools",
    "functools",
    "operator",
    "copy",
    "pickle",
    "csv",
    "io",
    "string",
    "textwrap",
    "argparse",
    "logging",
    "time",
    "threading",
    "multiprocessing",
    "urllib",
    "http",
    "socket",
    "ssl",
    "hashlib",
    "base64",
    "zlib",
    "gzip",
    "tarfile",
    "zipfile",
    "tempfile",
    "fileinput",
    "linecache",
    "pprint",
    "reprlib",
    "enum",
    "dataclasses",
    "typing",
    "abc",
    "contextlib",
    "weakref",
    "gc",
    "inspect",
    "traceback",
    "warnings",
    "unittest",
    "doctest",
    "pdb",
    "profile",
    "cProfile",
    "trace",
    "__future__",
    "__main__",
    "builtins",
    "importlib",
    "pkgutil",
    "site",
    "sysconfig",
    "platform",
    "errno",
    "signal",
    "atexit",
    "math",
    "cmath",
    "decimal",
    "fractions",
    "statistics",
    "array",
    "struct",
    "codecs",
    "unicodedata",
    "stringprep",
    "readline",
    "rlcompleter",
    "getpass",
    "curses",
    "termios",
    "tty",
    "pty",
    "pwd",
    "spwd",
    "grp",
    "crypt",
    "termios",
    "tty",
    "select",
    "selectors",
    "asyncio",
    "concurrent",
    "queue",
    "sched",
    "socketserver",
    "xml",
    "html",
    "email",
    "mimetypes",
    "base64",
    "binascii",
    "quopri",
    "uu",
    "binhex",
    "plistlib",
    "configparser",
    "netrc",
    "xdrlib",
    "mailcap",
    "mailbox",
    "mmap",
    "dbm",
    "sqlite3",
    "zlib",
    "gzip",
    "bz2",
    "lzma",
    "zipfile",
    "tarfile",
    "shutil",
    "filecmp",
    "stat",
    "fileinput",
    "linecache",
    "tempfile",
    "glob",
    "fnmatch",
    "pathlib",
    "os.path",
    "shutil",
    "pickle",
    "copy",
    "marshal",
    "dbm",
    "sqlite3",
    "zlib",
    "gzip",
    "bz2",
    "lzma",
    "zipfile",
    "tarfile",
    "csv",
    "configparser",
    "netrc",
    "xdrlib",
    "plistlib",
    "logging",
    "getopt",
    "argparse",
    "shlex",
    "configparser",
    "logging",
    "getpass",
    "curses",
    "platform",
    "errno",
    "io",
    "codecs",
    "unicodedata",
    "stringprep",
    "readline",
    "rlcompleter",
    "getpass",
    "curses",
    "termios",
    "tty",
    "pty",
    "pwd",
    "spwd",
    "grp",
    "crypt",
    "termios",
    "tty",
    "select",
    "selectors",
    "asyncio",
    "concurrent",
    "queue",
    "sched",
    "socketserver",
    "xml",
    "html",
    "email",
    "mimetypes",
    "base64",
    "binascii",
    "quopri",
    "uu",
    "binhex",
    "plistlib",
    "configparser",
    "netrc",
    "xdrlib",
    "mailcap",
    "mailbox",
    "mmap",
    "dbm",
    "sqlite3",
    "zlib",
    "gzip",
    "bz2",
    "lzma",
    "zipfile",
    "tarfile",
    "shutil",
    "filecmp",
    "stat",
    "fileinput",
    "linecache",
    "tempfile",
    "glob",
    "fnmatch",
    "pathlib",
    "os.path",
}


def read_requirements(file_path):
    """Read requirements from a file"""
    if not file_path.exists():
        return []

    modules = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # Remove version specifiers
                module = re.split(r"[>=<!=]", line)[0].strip()
                if module:
                    modules.append(module)
    return modules


def get_conda_package(module):
    """Get conda package name for a module"""
    # Check reverse mapping first
    if module in REVERSE_MAPPING:
        return REVERSE_MAPPING[module]

    # Check if it's in our mappings
    for conda_name, py_module in CONDA_MAPPINGS.items():
        if py_module == module:
            return conda_name

    # Default: use module name with hyphens
    return module.lower().replace("_", "-")


def generate_environment_yml(modules, env_name, output_path):
    """Generate environment.yml file"""
    # Filter out stdlib
    third_party = [m for m in modules if m not in STDLIB and not m.startswith("_")]

    # Get conda packages
    conda_packages = {}
    pip_packages = []

    for module in third_party:
        conda_name = get_conda_package(module)
        # Common conda packages
        if conda_name in [
            "numpy",
            "pandas",
            "matplotlib",
            "scipy",
            "scikit-learn",
            "jupyter",
            "ipython",
            "notebook",
            "pytest",
            "requests",
            "flask",
            "django",
            "tensorflow",
            "pytorch",
            "opencv",
            "pillow",
            "pyyaml",
            "beautifulsoup4",
            "lxml",
            "selenium",
        ]:
            conda_packages[conda_name] = module
        else:
            pip_packages.append(module)

    with open(output_path, "w") as f:
        f.write(f"# Environment file for {env_name}\n")
        f.write("# Generated for Miniforge/Mamba\n")
        f.write("# Usage: mamba env create -f {}\n".format(output_path.name))
        f.write("#        conda env create -f {}\n\n".format(output_path.name))
        f.write("name: {}\n".format(env_name.replace("/", "_").replace("-", "_")))
        f.write("channels:\n")
        f.write("  - conda-forge\n")
        f.write("  - defaults\n")
        f.write("dependencies:\n")
        f.write("  - python=3.12\n")
        f.write("  - pip\n")
        f.write("  # Conda packages:\n")

        for conda_name in sorted(conda_packages.keys()):
            f.write(f"  - {conda_name}\n")

        if pip_packages:
            f.write("\n  # Pip packages (if not available in conda):\n")
            f.write("  - pip:\n")
            for pkg in sorted(set(pip_packages))[:100]:  # Limit to 100
                f.write(f"    - {pkg}\n")

    return len(conda_packages), len(pip_packages)


# Read existing requirements files
print("Reading requirements files...")
pythons_req = read_requirements(Path.home() / "pythons-sort" / "requirements.txt")
downloads_req = read_requirements(Path.home() / "Downloads" / "requirements.txt")

# Also scan directories directly for Python files
print("\nScanning directories for Python imports...")


def quick_scan(directory, max_files=1000):
    """Quick scan of directory for imports"""
    imports = set()
    count = 0
    for py_file in directory.rglob("*.py"):
        if any(
            x in str(py_file) for x in ["venv", "__pycache__", ".git", "site-packages"]
        ):
            continue
        if count >= max_files:
            break
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("import ") or line.startswith("from "):
                        match = re.match(
                            r"(?:import\s+(\S+)|from\s+(\S+)\s+import)", line
                        )
                        if match:
                            module = (
                                (match.group(1) or match.group(2))
                                .split(".")[0]
                                .split(" as ")[0]
                            )
                            if (
                                module
                                and not module.startswith("_")
                                and module not in STDLIB
                            ):
                                imports.add(module)
        except:
            pass
        count += 1
    return imports


pythons_imports = quick_scan(Path.home() / "pythons", max_files=500)
pythons_sort_imports = quick_scan(Path.home() / "pythons-sort", max_files=500)

# Combine
all_pythons = set(pythons_req) | pythons_imports
all_pythons_sort = set(pythons_req) | pythons_sort_imports
all_combined = all_pythons | all_pythons_sort | set(downloads_req)

print("\nFound modules:")
print(f"  pythons: {len(all_pythons)}")
print(f"  pythons-sort: {len(all_pythons_sort)}")
print(f"  combined: {len(all_combined)}")

# Generate environment files
print("\nGenerating environment files...")

env1 = output_dir / "pythons_environment.yml"
conda1, pip1 = generate_environment_yml(all_pythons, "pythons", env1)
print(f"  pythons_environment.yml: {conda1} conda, {pip1} pip packages")

env2 = output_dir / "pythons_sort_environment.yml"
conda2, pip2 = generate_environment_yml(all_pythons_sort, "pythons_sort", env2)
print(f"  pythons_sort_environment.yml: {conda2} conda, {pip2} pip packages")

env3 = output_dir / "combined_environment.yml"
conda3, pip3 = generate_environment_yml(all_combined, "combined_all", env3)
print(f"  combined_environment.yml: {conda3} conda, {pip3} pip packages")

# Generate report
report = output_dir / "mamba_analysis_report.md"
with open(report, "w") as f:
    f.write("# Miniforge/Mamba Environment Analysis\n\n")
    f.write("## Summary\n\n")
    f.write(f"- **pythons directory:** {len(all_pythons)} unique modules\n")
    f.write(f"- **pythons-sort directory:** {len(all_pythons_sort)} unique modules\n")
    f.write(f"- **Combined:** {len(all_combined)} unique modules\n\n")

    f.write("## Top Modules Found\n\n")
    f.write("### pythons\n")
    for mod in sorted(all_pythons)[:30]:
        f.write(f"- `{mod}`\n")
    f.write("\n### pythons-sort\n")
    for mod in sorted(all_pythons_sort)[:30]:
        f.write(f"- `{mod}`\n")
    f.write("\n### Combined\n")
    for mod in sorted(all_combined)[:50]:
        f.write(f"- `{mod}`\n")

    f.write("\n## Installation Instructions\n\n")
    f.write("```bash\n")
    f.write("# Install Miniforge (includes mamba)\n")
    f.write("brew install miniforge\n")
    f.write("# or download from: https://github.com/conda-forge/miniforge\n\n")
    f.write("# Create environments\n")
    f.write("mamba env create -f pythons_environment.yml\n")
    f.write("mamba env create -f pythons_sort_environment.yml\n")
    f.write("mamba env create -f combined_environment.yml\n\n")
    f.write("# Activate environment\n")
    f.write("mamba activate pythons\n")
    f.write("# or\n")
    f.write("conda activate pythons\n")
    f.write("```\n")

print(f"\nAnalysis complete! Files saved to: {output_dir}")
print("  - pythons_environment.yml")
print("  - pythons_sort_environment.yml")
print("  - combined_environment.yml")
print("  - mamba_analysis_report.md")
