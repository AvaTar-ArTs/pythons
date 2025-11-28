import os
import sys
import ast
import csv
import json
import subprocess
import platform
import datetime
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import radon
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from pylint import epylint as lint

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_150 = 150
CONSTANT_800 = 800
CONSTANT_1024 = 1024


class AdvancedPythonAnalyzer:
    def __init__(self, directory):
        """__init__ function."""

        self.directory = directory
        self.results = {}
        self.summary = defaultdict(int)
        self.path_graph = nx.DiGraph()
        self.report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.system_info = self.get_system_info()

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
        # First pass: basic analysis
        for filename in os.listdir(self.directory):
            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(self.directory, filename)
            self.analyze_file(filepath)

        # Second pass: path-based analysis
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
            file_data.update(self.ast_analysis(tree))

            # Run analysis tools
            self.run_analysis_tools(filepath, file_data)

            # Complexity analysis
            file_data["complexity"] = self.complexity_analysis(content)

            # Update summary
            self.update_summary(file_data)

        except Exception as e:
            file_data["error"] = str(e)
            logger.info(f"Error analyzing {filename}: {str(e)}")

        self.results[filename] = file_data
        return file_data

    def analyze_path_relationships(self):
        """Analyze relationships between files based on imports"""
        # Add nodes to graph
        for filename, data in self.results.items():
            self.path_graph.add_node(filename, **data["metrics"])

        # Add edges based on imports
        for filename, data in self.results.items():
            for imp in data["imports"]:
                # Find which local files match this import
                for other_file in self.results.keys():
                    module_name = os.path.splitext(other_file)[0]
                    if imp == module_name or imp.startswith(module_name + "."):
                        self.path_graph.add_edge(
                            filename, other_file, relationship="imports"
                        )

            # Add edges based on function calls
            for call in data["calls"]:
                if call["target"] in self.results:
                    self.path_graph.add_edge(
                        filename,
                        call["target"],
                        relationship="calls",
                        function=call["function"],
                    )

    def get_file_metrics(self, filepath, content):
        """Get basic file metrics"""
        return {
            "lines": len(content.splitlines()),
            "size_kb": round(os.path.getsize(filepath) / CONSTANT_1024, 2),
            "encoding": "utf-8",
            "created": datetime.datetime.fromtimestamp(
                os.path.getctime(filepath)
            ).strftime("%Y-%m-%d"),
            "modified": datetime.datetime.fromtimestamp(
                os.path.getmtime(filepath)
            ).strftime("%Y-%m-%d"),
        }

    def ast_analysis(self, tree):
        """Perform AST-based analysis"""
        data = {"functions": [], "classes": [], "imports": set(), "calls": []}

        # Track function definitions for call analysis
        function_defs = {}

        for node in ast.walk(tree):
            # Function definitions
            if isinstance(node, ast.FunctionDef):
                func_data = {
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node) or "",
                    "params": [arg.arg for arg in node.args.args],
                    "returns": bool(node.returns),
                }
                data["functions"].append(func_data)
                function_defs[node.name] = func_data

            # Class definitions
            elif isinstance(node, ast.ClassDef):
                class_data = {
                    "name": node.name,
                    "line": node.lineno,
                    "docstring": ast.get_docstring(node) or "",
                    "methods": [
                        n.name for n in node.body if isinstance(n, ast.FunctionDef)
                    ],
                }
                data["classes"].append(class_data)

            # Import statements
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    data["imports"].add(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    data["imports"].add(node.module)

            # Function calls
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    # Local function call
                    data["calls"].append(
                        {"function": node.func.id, "line": node.lineno}
                    )
                elif isinstance(node.func, ast.Attribute) and isinstance(
                    node.func.value, ast.Name
                ):
                    # Method call on an object
                    data["calls"].append(
                        {
                            "target": node.func.value.id,
                            "function": node.func.attr,
                            "line": node.lineno,
                        }
                    )

        return data

    def run_analysis_tools(self, filepath, file_data):
        """Run various analysis tools"""
        # Pylint
        try:
            pylint_out, _ = lint.py_run(
                f"{filepath} --output-format=json", return_std=True
            )
            pylint_data = json.loads(pylint_out.getvalue())
            file_data["issues"]["pylint"] = [
                {"type": msg["symbol"], "message": msg["message"], "line": msg["line"]}
                for msg in pylint_data
            ]
        except Exception as e:
            file_data["issues"]["pylint"] = [{"error": f"Pylint failed: {str(e)}"}]

        # Flake8
        try:
            result = subprocess.run(
                ["flake8", filepath, "--format=json"], capture_output=True, text=True
            )
            if result.stdout.strip():
                file_data["issues"]["flake8"] = json.loads(result.stdout)
        except Exception as e:
            file_data["issues"]["flake8"] = [{"error": f"Flake8 failed: {str(e)}"}]

        # Mypy
        try:
            result = subprocess.run(
                [
                    "mypy",
                    filepath,
                    "--strict",
                    "--no-error-summary",
                    "--show-column-numbers",
                ],
                capture_output=True,
                text=True,
            )
            if result.stdout.strip():
                file_data["issues"]["mypy"] = [
                    {
                        "message": line.strip(),
                        "line": int(line.split(":")[1]) if ":" in line else 0,
                    }
                    for line in result.stdout.splitlines()
                    if line.strip()
                ]
        except Exception as e:
            file_data["issues"]["mypy"] = [{"error": f"Mypy failed: {str(e)}"}]

    def complexity_analysis(self, content):
        """Calculate code complexity metrics"""
        try:
            # Cyclomatic complexity
            blocks = cc_visit(content)
            cc_scores = [b.complexity for b in blocks]

            # Maintainability index
            mi = mi_visit(content, multi=True)[1]  # Get MI rank

            return {
                "cyclomatic": {
                    "total": sum(cc_scores),
                    "average": sum(cc_scores) / len(cc_scores) if cc_scores else 0,
                    "max": max(cc_scores) if cc_scores else 0,
                },
                "maintainability_index": mi,
                "halstead": radon.metrics.h_visit(content).total,
            }
        except Exception as e:
            return {"error": str(e)}

    def update_summary(self, file_data):
        """Update summary statistics"""
        self.summary["files"] += 1
        self.summary["lines"] += file_data["metrics"]["lines"]
        self.summary["functions"] += len(file_data["functions"])
        self.summary["classes"] += len(file_data["classes"])

        if "complexity" in file_data:
            comp = file_data["complexity"]
            if "cyclomatic" in comp:
                self.summary["total_complexity"] += comp["cyclomatic"]["total"]

        for tool in ["pylint", "flake8", "mypy"]:
            if tool in file_data["issues"]:
                self.summary[f"{tool}_issues"] += len(file_data["issues"][tool])

    def generate_path_visualization(self, output_path):
        """Generate visualization of file relationships"""
        plt.figure(figsize=(16, 12))

        # Use spring layout for better visualization of relationships
        pos = nx.spring_layout(self.path_graph, k=0.5, iterations=50)

        # Node coloring based on complexity
        complexities = [
            self.results[node]["complexity"].get("cyclomatic", {}).get("total", 0)
            for node in self.path_graph.nodes()
        ]

        # Edge styling
        edge_colors = []
        edge_styles = []
        for u, v, data in self.path_graph.edges(data=True):
            if data.get("relationship") == "imports":
                edge_colors.append("blue")
                edge_styles.append("solid")
            else:  # calls
                edge_colors.append("green")
                edge_styles.append("dashed")

        # Draw the graph
        nx.draw_networkx_nodes(
            self.path_graph,
            pos,
            node_size=CONSTANT_800,
            node_color=complexities,
            cmap=plt.cm.Reds,
            alpha=0.8,
        )

        nx.draw_networkx_edges(
            self.path_graph,
            pos,
            edge_color=edge_colors,
            style=edge_styles,
            width=1.5,
            alpha=0.7,
        )

        # Label nodes with filenames
        labels = {node: node for node in self.path_graph.nodes()}
        nx.draw_networkx_labels(self.path_graph, pos, labels, font_size=9)

        # Add edge labels for relationships
        edge_labels = {}
        for u, v, data in self.path_graph.edges(data=True):
            if data.get("relationship") == "calls":
                edge_labels[(u, v)] = data.get("function", "call")

        nx.draw_networkx_edge_labels(
            self.path_graph,
            pos,
            edge_labels=edge_labels,
            font_color="green",
            font_size=8,
        )

        # Create legend
        plt.plot([], [], "o", color="blue", alpha=0.8, label="Import Relationship")
        plt.plot([], [], "--", color="green", label="Function Call")
        plt.legend(loc="best")

        # Add title and save
        plt.title(
            "Python File Relationships\nLine thickness = Import Dependency, Dashed = Function Calls",
            fontsize=14,
        )
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=CONSTANT_150)
        plt.close()

        return output_path

    def generate_html_report(self, output_path, visualization_path):
        """Generate HTML report with path visualization"""
        # HTML template with embedded visualization
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Advanced Python Code Analysis</title>
            <style>
                /* (Keep the same styles as before) */
                .visualization-section {{
                    text-align: center;
                    padding: 20px;
                    background: #f8f9fa;
                    border-top: 1px solid #e9ecef;
                    border-bottom: 1px solid #e9ecef;
                    margin: 20px 0;
                }}
                
                .visualization-section img {{
                    max-width: CONSTANT_100%;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                
                .legend {{
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                    margin-top: 10px;
                    font-size: 0.9rem;
                }}
                
                .legend-item {{
                    display: flex;
                    align-items: center;
                    gap: 5px;
                }}
                
                .legend-color {{
                    display: inline-block;
                    width: 20px;
                    height: 3px;
                }}
                
                .import-legend {{ background: blue; }}
                .call-legend {{ background: green; }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Python Code Analysis with Path Visualization</h1>
                    <div class="subtitle">Comprehensive Code Structure & Relationships</div>
                </header>
                
                <div class="report-meta">
                    <div>Generated: {self.report_time}</div>
                    <div>System: {self.system_info['platform']} {self.system_info['release']}</div>
                    <div>Python: {self.system_info['python_version']}</div>
                </div>
                
                <!-- Visualization Section -->
                <div class="visualization-section">
                    <h3>Code Path Visualization</h3>
                    <img src="{os.path.basename(visualization_path)}" alt="Code Path Visualization">
                    <div class="legend">
                        <div class="legend-item">
                            <span class="legend-color import-legend"></span>
                            Import Relationship
                        </div>
                        <div class="legend-item">
                            <span class="legend-color call-legend"></span>
                            Function Call
                        </div>
                    </div>
                    <p class="visualization-caption">
                        Node size represents file complexity. Redder nodes indicate higher complexity.
                    </p>
                </div>
                
                <!-- (Rest of the report remains the same) -->
        """

        # (Rest of the HTML structure remains the same)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path

    def generate_reports(self, output_dir):
        """Generate all reports"""
        os.makedirs(output_dir, exist_ok=True)

        # Generate path visualization
        vis_path = os.path.join(output_dir, "path_visualization.png")
        self.generate_path_visualization(vis_path)

        # Generate HTML report
        html_path = os.path.join(output_dir, "python_analysis_report.html")
        self.generate_html_report(html_path, vis_path)

        # Generate CSV report
        csv_path = os.path.join(output_dir, "python_analysis_report.csv")
        self.generate_csv_report(csv_path)

        return {"html": html_path, "csv": csv_path, "visualization": vis_path}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.info("Usage: python advanced_analyzer.py <directory> [output_dir]")
        sys.exit(1)

    directory = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "python_analysis_reports"

    if not os.path.isdir(directory):
        logger.info(f"Error: Directory not found - {directory}")
        sys.exit(1)

    logger.info(f"🔍 Analyzing Python files in: {directory}")
    analyzer = AdvancedPythonAnalyzer(directory)
    results = analyzer.analyze()

    if not results:
        logger.info("No Python files found in the directory")
        sys.exit(0)

    # Generate reports
    report_paths = analyzer.generate_reports(output_dir)

    logger.info(f"\n✅ Analysis complete!")
    logger.info(f"📊 HTML Report: {report_paths['html']}")
    logger.info(f"📈 Path Visualization: {report_paths['visualization']}")
    logger.info(f"📝 CSV Report: {report_paths['csv']}")
    logger.info(f"\n🔍 Files analyzed: {len(results)}")
    logger.info(f"📏 Total lines: {analyzer.summary['lines']}")
    logger.info(
        f"⚠️  Total issues: {analyzer.summary.get('pylint_issues', 0) + analyzer.summary.get('flake8_issues', 0)}"
    )
