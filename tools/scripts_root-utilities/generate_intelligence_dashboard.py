#!/usr/bin/env python3
"""
Intelligence Dashboard Generator

Generates interactive HTML dashboards from advanced content intelligence analysis.
Creates beautiful visualizations of:
- Code quality distributions
- Category breakdowns
- Architectural pattern detection
- Dependency graphs
- Quality metrics over time

Category: Data Visualization
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter


def generate_dashboard(json_report_path: Path, output_path: Path):
    """Generate interactive dashboard from JSON analysis report"""

    # Load analysis data
    with open(json_report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    analyses = data['analyses']

    # Calculate statistics
    stats = calculate_statistics(analyses)

    # Generate HTML
    html = generate_html(stats, data['generated_at'])

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    logging.info(f"Dashboard generated: {output_path}")


def calculate_statistics(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate all statistics for dashboard"""

    total_files = len(analyses)
    total_loc = sum(a['lines_of_code'] for a in analyses)

    # Category distribution
    categories = Counter(a['category'] for a in analyses)

    # Quality metrics
    quality_scores = [a['code_quality_score'] for a in analyses]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    quality_distribution = {
        'Excellent (90-100)': sum(1 for s in quality_scores if s >= 90),
        'Good (70-89)': sum(1 for s in quality_scores if 70 <= s < 90),
        'Fair (50-69)': sum(1 for s in quality_scores if 50 <= s < 70),
        'Poor (<50)': sum(1 for s in quality_scores if s < 50),
    }

    # Pattern detection
    patterns = Counter()
    for a in analyses:
        for pattern in a['patterns']:
            patterns[pattern['pattern_type']] += 1

    # Language distribution
    languages = Counter(a['language'] for a in analyses)

    # Testing & documentation
    with_tests = sum(1 for a in analyses if a['has_tests'])
    with_docs = sum(1 for a in analyses if a['has_documentation'])

    # Complexity analysis
    complexities = [a['complexity_score'] for a in analyses]
    avg_complexity = sum(complexities) / len(complexities) if complexities else 0

    # Top quality files
    top_quality = sorted(
        analyses,
        key=lambda a: a['code_quality_score'],
        reverse=True
    )[:10]

    # Files needing attention
    needs_attention = sorted(
        analyses,
        key=lambda a: a['code_quality_score']
    )[:10]

    # Dependency analysis
    total_dependencies = sum(len(a.get('depends_on', [])) for a in analyses)
    avg_dependencies = total_dependencies / total_files if total_files else 0

    highly_coupled = sorted(
        analyses,
        key=lambda a: len(a.get('depends_on', [])) + len(a.get('depended_by', [])),
        reverse=True
    )[:10]

    return {
        'total_files': total_files,
        'total_loc': total_loc,
        'avg_quality': avg_quality,
        'avg_complexity': avg_complexity,
        'categories': dict(categories),
        'quality_distribution': quality_distribution,
        'patterns': dict(patterns),
        'languages': dict(languages),
        'with_tests': with_tests,
        'with_docs': with_docs,
        'test_coverage_pct': (with_tests / total_files * 100) if total_files else 0,
        'doc_coverage_pct': (with_docs / total_files * 100) if total_files else 0,
        'avg_dependencies': avg_dependencies,
        'top_quality': top_quality,
        'needs_attention': needs_attention,
        'highly_coupled': highly_coupled,
    }


def generate_html(stats: Dict[str, Any], generated_at: str) -> str:
    """Generate complete HTML dashboard"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Content Intelligence Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}

        h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}

        .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}

        .stat-label {{
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}

        .chart-card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .chart-title {{
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}

        .file-list {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}

        .file-item {{
            padding: 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .file-item:last-child {{
            border-bottom: none;
        }}

        .file-path {{
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #555;
            flex: 1;
        }}

        .file-score {{
            font-weight: bold;
            font-size: 1.2rem;
            padding: 5px 15px;
            border-radius: 20px;
            margin-left: 15px;
        }}

        .score-excellent {{
            background: #10b981;
            color: white;
        }}

        .score-good {{
            background: #3b82f6;
            color: white;
        }}

        .score-fair {{
            background: #f59e0b;
            color: white;
        }}

        .score-poor {{
            background: #ef4444;
            color: white;
        }}

        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 2rem;
            }}

            .charts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Advanced Content Intelligence</h1>
            <p class="subtitle">Deep Code Analysis & Quality Metrics</p>
            <p class="subtitle">Generated: {datetime.fromisoformat(generated_at).strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>

        <!-- Key Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_files']}</div>
                <div class="stat-label">Files Analyzed</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{stats['total_loc']:,}</div>
                <div class="stat-label">Lines of Code</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{stats['avg_quality']:.1f}</div>
                <div class="stat-label">Avg Quality Score</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{stats['test_coverage_pct']:.1f}%</div>
                <div class="stat-label">Test Coverage</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{stats['doc_coverage_pct']:.1f}%</div>
                <div class="stat-label">Documentation</div>
            </div>

            <div class="stat-card">
                <div class="stat-value">{stats['avg_complexity']:.1f}</div>
                <div class="stat-label">Avg Complexity</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
            <div class="chart-card">
                <h2 class="chart-title">Category Distribution</h2>
                <canvas id="categoryChart"></canvas>
            </div>

            <div class="chart-card">
                <h2 class="chart-title">Quality Distribution</h2>
                <canvas id="qualityChart"></canvas>
            </div>

            <div class="chart-card">
                <h2 class="chart-title">Language Breakdown</h2>
                <canvas id="languageChart"></canvas>
            </div>

            <div class="chart-card">
                <h2 class="chart-title">Architectural Patterns</h2>
                <canvas id="patternChart"></canvas>
            </div>
        </div>

        <!-- Top Quality Files -->
        <div class="file-list">
            <h2 class="chart-title">🏆 Top Quality Files</h2>
            {generate_file_list_html(stats['top_quality'], 'top')}
        </div>

        <!-- Files Needing Attention -->
        <div class="file-list">
            <h2 class="chart-title">⚠️ Files Needing Attention</h2>
            {generate_file_list_html(stats['needs_attention'], 'attention')}
        </div>

        <!-- Highly Coupled Files -->
        <div class="file-list">
            <h2 class="chart-title">🔗 Highly Coupled Files</h2>
            {generate_coupled_files_html(stats['highly_coupled'])}
        </div>

        <footer>
            <p>Generated by Advanced Content Intelligence System</p>
        </footer>
    </div>

    <script>
        // Chart configurations
        const chartColors = {{
            primary: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#30cfd0'],
            quality: {{
                excellent: '#10b981',
                good: '#3b82f6',
                fair: '#f59e0b',
                poor: '#ef4444'
            }}
        }};

        // Category Chart
        new Chart(document.getElementById('categoryChart'), {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(stats['categories'].keys()))},
                datasets: [{{
                    data: {json.dumps(list(stats['categories'].values()))},
                    backgroundColor: chartColors.primary,
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});

        // Quality Distribution Chart
        new Chart(document.getElementById('qualityChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(stats['quality_distribution'].keys()))},
                datasets: [{{
                    label: 'Number of Files',
                    data: {json.dumps(list(stats['quality_distribution'].values()))},
                    backgroundColor: [
                        chartColors.quality.excellent,
                        chartColors.quality.good,
                        chartColors.quality.fair,
                        chartColors.quality.poor
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});

        // Language Chart
        new Chart(document.getElementById('languageChart'), {{
            type: 'pie',
            data: {{
                labels: {json.dumps(list(stats['languages'].keys()))},
                datasets: [{{
                    data: {json.dumps(list(stats['languages'].values()))},
                    backgroundColor: chartColors.primary.slice(0, {len(stats['languages'])}),
                    borderWidth: 2,
                    borderColor: '#fff'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});

        // Pattern Chart
        new Chart(document.getElementById('patternChart'), {{
            type: 'horizontalBar',
            data: {{
                labels: {json.dumps(list(stats['patterns'].keys()) if stats['patterns'] else ['No patterns detected'])},
                datasets: [{{
                    label: 'Occurrences',
                    data: {json.dumps(list(stats['patterns'].values()) if stats['patterns'] else [0])},
                    backgroundColor: '#667eea',
                    borderWidth: 0
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""


def generate_file_list_html(files: List[Dict[str, Any]], list_type: str) -> str:
    """Generate HTML for file list"""
    html_items = []

    for file_data in files:
        score = file_data['code_quality_score']
        filepath = file_data['filepath']

        # Determine score class
        if score >= 90:
            score_class = 'score-excellent'
        elif score >= 70:
            score_class = 'score-good'
        elif score >= 50:
            score_class = 'score-fair'
        else:
            score_class = 'score-poor'

        html_items.append(f"""
            <div class="file-item">
                <div class="file-path">{filepath}</div>
                <div class="file-score {score_class}">{score:.1f}</div>
            </div>
        """)

    return '\n'.join(html_items) if html_items else '<p>No files found.</p>'


def generate_coupled_files_html(files: List[Dict[str, Any]]) -> str:
    """Generate HTML for highly coupled files"""
    html_items = []

    for file_data in files:
        filepath = file_data['filepath']
        depends_on = len(file_data.get('depends_on', []))
        depended_by = len(file_data.get('depended_by', []))
        total_coupling = depends_on + depended_by

        html_items.append(f"""
            <div class="file-item">
                <div class="file-path">{filepath}</div>
                <div class="file-score score-fair">
                    ↓{depends_on} ↑{depended_by} (Total: {total_coupling})
                </div>
            </div>
        """)

    return '\n'.join(html_items) if html_items else '<p>No highly coupled files found.</p>'


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate intelligence dashboard')
    parser.add_argument(
        'json_report',
        type=Path,
        help='Path to JSON analysis report'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output HTML path (default: intelligence_dashboard.html)'
    )

    args = parser.parse_args()

    if not args.output:
        args.output = args.json_report.parent / 'intelligence_dashboard.html'

    logging.basicConfig(level=logging.INFO)

    generate_dashboard(args.json_report, args.output)
    print(f"\n✅ Dashboard generated: {args.output}")


if __name__ == '__main__':
    main()
