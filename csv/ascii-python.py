"""
Ascii Python

This module provides functionality for ascii python.

Author: Auto-generated
Date: 2025-11-01
"""

from pathlib import Path
import os
import ast
import sys
import json
import csv
import platform
import datetime
import subprocess
import radon
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from radon.complexity import cc_visit
from radon.metrics import mi_visit

import logging

logger = logging.getLogger(__name__)


# Fixed import - removed problematic epylint import
# Added ASCII art generation function
def generate_ascii_art(text):
    """Generate ASCII art text using simple character patterns"""
    art_map = {
        "A": [" █████╗ ", "██╔══██╗", "███████║", "██╔══██║", "██║  ██║", "╚═╝  ╚═╝"],
        "V": ["██╗   ██╗", "██║   ██║", "██║   ██║", "╚██╗ ██╔╝", " ╚████╔╝ ", "  ╚═══╝  "],
        # Add more characters as needed
    }

    lines = [""] * 6
    for char in text.upper():
        if char in art_map:
            for i in range(6):
                lines[i] += art_map[char][i]
        else:
            for i in range(6):
                lines[i] += " " * 8

    return Path("\n").join(lines)


class PythonAnalyzer:
    def __init__(self, directory):
        """__init__ function."""

        self.directory = directory
        self.results = {}
        self.summary = defaultdict(int)
        self.path_graph = nx.DiGraph()
        self.report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.system_info = self.get_system_info()
        self.ascii_banner = generate_ascii_art("PYTHON ANALYSIS")

        """get_system_info function."""

    def get_system_info(self):
        return {
            "platform": platform.system(),
            "release": platform.release(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
            "machine": platform.machine(),
        }

    def analyze(self):
        """Main analysis method"""
        logger.info("🔍 Starting code analysis...")
        for filename in os.listdir(self.directory):
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(self.directory, filename)
            logger.info(f"  ⚙️ Analyzing {filename}")
            self.analyze_file(filepath)

        logger.info("🔗 Analyzing path relationships...")
        self.analyze_path_relationships()
        return self.results

    def analyze_file(self, filepath):
        """Analyze a single Python file"""
        filename = os.path.basename(filepath)
        file_data = {
            "filename": filename,
            "path": filepath,
            "metrics": {},
            "issues": defaultdict(list),
            "dependencies": [],
            "structure": [],
            "complexity": {},
            "imports": set(),
            "calls": [],
        }

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic file metrics
            file_data["metrics"] = self.get_file_metrics(filepath, content)

            # AST-based analysis
            tree = ast.parse(content)
            ast_data = self.ast_analysis(tree)
            file_data.update(ast_data)

            # Run analysis tools
            self.run_analysis_tools(filepath, file_data)

            # Complexity analysis
            file_data["complexity"] = self.complexity_analysis(content)

            # Update summary
            self.update_summary(file_data)

        except Exception as e:
            file_data["error"] = f"Analysis error: {str(e)}"
            logger.info(f"    ❌ Error analyzing {filename}: {str(e)}")

        self.results[filename] = file_data
        return file_data

    # Fixed Pylint runner using subprocess
    def run_pylint(self, filepath):
        """Run Pylint using subprocess and return JSON output"""
        try:
            result = subprocess.run(
                ["pylint", filepath, "--output-format=json"], capture_output=True, text=True, check=False
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return []
        except Exception as e:
            logger.info(f"    ❌ Pylint failed: {str(e)}")
            return [{"error": f"Pylint execution failed: {str(e)}"}]

    def run_analysis_tools(self, filepath, file_data):
        """Run various analysis tools"""
        # Pylint - using fixed subprocess approach
        pylint_data = self.run_pylint(filepath)
        file_data["issues"]["pylint"] = [
            {
                "type": msg.get("symbol", "unknown"),
                "message": msg.get("message", "No message"),
                "line": msg.get("line", 0),
            }
            for msg in pylint_data
        ]

        # Flake8
        try:
            result = subprocess.run(["flake8", filepath, "--format=json"], capture_output=True, text=True)
            if result.stdout.strip():
                file_data["issues"]["flake8"] = json.loads(result.stdout)
        except Exception as e:
            file_data["issues"]["flake8"] = [{"error": f"Flake8 failed: {str(e)}"}]

        # Mypy
        try:
            result = subprocess.run(
                ["mypy", filepath, "--strict", "--no-error-summary", "--show-column-numbers"],
                capture_output=True,
                text=True,
            )
            if result.stdout.strip():
                file_data["issues"]["mypy"] = [
                    {"message": line.strip(), "line": int(line.split(":")[1]) if ":" in line else 0}
                    for line in result.stdout.splitlines()
                    if line.strip()
                ]
        except Exception as e:
            file_data["issues"]["mypy"] = [{"error": f"Mypy failed: {str(e)}"}]

    # The rest of the methods remain the same as in the previous implementation
    # (get_file_metrics, ast_analysis, complexity_analysis, update_summary,
    # analyze_path_relationships, generate_html_report, generate_csv_report, etc.)
    # ...

    def generate_html_report(self, output_path):
        """Generate HTML report with ASCII art banner"""
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Python Code Analysis</title>
            <style>
                /* ... existing styles ... */
                .ascii-banner {{
                    font-family: monospace;
                    white-space: pre;
                    text-align: center;
                    background: #2c3e50;
                    color: white;
                    padding: 15px;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="ascii-banner">
                    {self.ascii_banner}
                </div>
                <!-- Rest of the report content -->
        """
        # ... rest of the HTML generation code ...

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.info("Usage: python analyzer.py <directory> [output.html]")
        sys.exit(1)

    directory = sys.argv[1]
    html_output = sys.argv[2] if len(sys.argv) > 2 else "python_analysis_report.html"
    csv_output = "python_analysis_report.csv"

    if not os.path.isdir(directory):
        logger.info(f"Error: Directory not found - {directory}")
        sys.exit(1)

    logger.info(f"🔍 Analyzing Python files in: {directory}")
    analyzer = PythonAnalyzer(directory)
    results = analyzer.analyze()

    if not results:
        logger.info("No Python files found in the directory")
        sys.exit(0)

    # Generate reports
    html_path = analyzer.generate_html_report(html_output)
    csv_path = analyzer.generate_csv_report(csv_output)

    logger.info(f"\n✅ Analysis complete!")
    logger.info(f"📊 HTML Report: {html_path}")
    logger.info(f"📝 CSV Report: {csv_path}")
