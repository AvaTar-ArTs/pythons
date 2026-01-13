"""
Setup configuration for the Python Automation Framework
"""
from setuptools import setup, find_packages
import os

# Read the contents of README file
def read_long_description():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read the requirements from requirements.txt file
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements", "base.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    return []

setup(
    name="python-automation-framework",
    version="1.0.0",
    author="Steven Chaplinski",
    author_email="sjchaplinski@gmail.com",
    description="A comprehensive collection of Python automation, analysis, and organization tools",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/gptjunkie/pythons-sort",
    project_urls={
        "Bug Reports": "https://github.com/gptjunkie/pythons-sort/issues",
        "Source": "https://github.com/gptjunkie/pythons-sort",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Filesystems",
        "Topic :: Text Processing",
        "Topic :: Multimedia",
        "Topic :: Internet",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.8",
            "black>=21.0",
            "mypy>=0.800",
            "isort>=5.0",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
        "analysis": [
            "astroid>=2.0",
            "pylint>=2.0",
            "radon>=4.0",
        ],
        "media": [
            "Pillow>=8.0",
            "moviepy>=1.0",
            "librosa>=0.9",
            "pydub>=0.25",
        ],
        "ai": [
            "openai>=1.0",
            "anthropic>=0.3",
            "google-generativeai>=0.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "pythons-sort=pythons_sort:main",
            "pythons_sort=pythons_sort:main",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "automation", 
        "file management", 
        "code analysis", 
        "deduplication", 
        "organization", 
        "ai integration",
        "media processing",
        "platform integration"
    ],
)