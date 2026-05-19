#!/usr/bin/env python3
"""
Setup script for Deep Research Tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = (
    readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
)

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")
    requirements = [
        req.strip() for req in requirements if req.strip() and not req.startswith("#")
    ]

setup(
    name="deep-research-tool",
    version="1.0.0",
    description="Intelligent folder structure analysis with GitHub and codex optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Deep Research Tool Team",
    author_email="team@deepresearchtool.com",
    url="https://github.com/deep-research-tool/deep-research-tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "advanced": [
            "scikit-learn>=1.1.0",
            "nltk>=3.7",
        ],
    },
    entry_points={
        "console_scripts": [
            "deep-research=scripts.run_analysis:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="folder analysis, file organization, github optimization, codex configuration, ai tools",
    project_urls={
        "Bug Reports": "https://github.com/deep-research-tool/deep-research-tool/issues",
        "Source": "https://github.com/deep-research-tool/deep-research-tool",
        "Documentation": "https://github.com/deep-research-tool/deep-research-tool/blob/main/README.md",
    },
)
