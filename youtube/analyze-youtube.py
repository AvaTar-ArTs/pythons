"""
Analyze Youtube

This module provides functionality for analyze youtube.

Author: Auto-generated
Date: 2025-11-01
"""

from setuptools import setup

setup(
    name="deepseek-python-analyzer",
    version="0.1.0",
    py_modules=["deepseek_python"],
    install_requires=[
        "matplotlib",
        "networkx",
        "radon",
        "pylint",
        "flake8",
        "mypy",
        "jsonschema",
    ],
    entry_points={
        "console_scripts": [
            "deepseek-python=deepseek_python:main",
        ],
    },
    description="Advanced Python Analyzer with AST- and path-based analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
