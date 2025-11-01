"""
Detailed

This module provides functionality for detailed.

Author: Auto-generated
Date: 2025-11-01
"""

import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_100 = 100
CONSTANT_333 = 333
CONSTANT_495057 = 495057

#!/usr/bin/env python3
"""
Detailed Comparison Report Generator
===================================
Generate a comprehensive report showing the differences between
original and content-aware analysis approaches.
"""

import json
import csv
from pathlib import Path
from datetime import datetime


def generate_detailed_report():
    """Generate a detailed comparison report"""

    # Load the comparison data
    comparison_file = Path(
        Path(
            str(Path.home()) + "/Documents/python/comparison_analysis/comparison_analysis_20251026_010632.json"
        )
    )

    if not comparison_file.exists():
        logger.info("❌ Comparison data not found")
        return

    with open(comparison_file, "r") as f:
        data = json.load(f)

    # Generate detailed report
    report = generate_html_report(data)

    # Save report
    output_file = Path(
        Path(
            str(Path.home()) + "/Documents/python/comparison_analysis/detailed_comparison_report.html"
        )
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

    logger.info(f"✅ Detailed report generated: {output_file}")
    return output_file


def generate_html_report(data):
    """Generate comprehensive HTML report"""

    scripts = data["scripts_analyzed"]
    summary = data["comparison_summary"]
    improvements = data["improvements_demonstrated"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Analysis Comparison Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            color: #CONSTANT_333;
            background-color: #f8f9fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .card h3 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #CONSTANT_333;
        }}
        
        .script-analysis {{
            background: white;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .script-header {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .script-content {{
            padding: 20px;
        }}
        
        .comparison-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .analysis-section {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }}
        
        .analysis-section h4 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .metrics-list {{
            list-style: none;
            padding: 0;
        }}
        
        .metrics-list li {{
            padding: 5px 0;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .metrics-list li:last-child {{
            border-bottom: none;
        }}
        
        .metric-name {{
            font-weight: bold;
            color: #CONSTANT_495057;
        }}
        
        .metric-value {{
            color: #6c757d;
            float: right;
        }}
        
        .improvements {{
            background: #e8f5e8;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
        }}
        
        .improvements h4 {{
            color: #28a745;
            margin-bottom: 10px;
        }}
        
        .capabilities {{
            background: white;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        
        .capabilities h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .capability-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .capability-section {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
        }}
        
        .capability-section h3 {{
            color: #CONSTANT_495057;
            margin-bottom: 10px;
        }}
        
        .capability-list {{
            list-style: none;
            padding: 0;
        }}
        
        .capability-list li {{
            padding: 5px 0;
            color: #6c757d;
        }}
        
        .capability-list li:before {{
            content: "✅ ";
            color: #28a745;
        }}
        
        .conclusion {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 CONSTANT_100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .conclusion h2 {{
            margin-bottom: 15px;
        }}
        
        .conclusion p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        @media (max-width: 768px) {{
            .comparison-grid {{
                grid-template-columns: 1fr;
            }}
            
            .summary-cards {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔬 Content Analysis Comparison Report</h1>
            <p>Original vs Content-Aware Analysis on 3 Random Python Scripts</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <h3>Scripts Analyzed</h3>
                <div class="number">{summary['total_scripts']}</div>
            </div>
            <div class="card">
                <h3>Original Metrics</h3>
                <div class="number">{summary['original_metrics_total']}</div>
            </div>
            <div class="card">
                <h3>Content-Aware Metrics</h3>
                <div class="number">{summary['content_aware_metrics_total']}</div>
            </div>
            <div class="card">
                <h3>Improvement</h3>
                <div class="number">+{summary['metrics_improvement']}</div>
            </div>
            <div class="card">
                <h3>Improvement %</h3>
                <div class="number">{summary['improvement_percentage']:.1f}%</div>
            </div>
        </div>
        
        <h2 style="color: #667eea; margin-bottom: 20px;">📊 Individual Script Analysis</h2>
        
        {generate_script_analyses(scripts)}
        
        <div class="capabilities">
            <h2>🧠 New Analysis Capabilities</h2>
            <div class="capability-grid">
                <div class="capability-section">
                    <h3>🔍 Advanced Analysis</h3>
                    <ul class="capability-list">
                        {generate_capability_list(improvements['new_analysis_capabilities'][:8])}
                    </ul>
                </div>
                <div class="capability-section">
                    <h3>🚀 Intelligence Enhancements</h3>
                    <ul class="capability-list">
                        {generate_capability_list(improvements['intelligence_enhancements'])}
                    </ul>
                </div>
                <div class="capability-section">
                    <h3>💡 Practical Benefits</h3>
                    <ul class="capability_list">
                        {generate_capability_list(improvements['practical_benefits'])}
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="conclusion">
            <h2>🎯 Key Findings</h2>
            <p>The content-aware analysis provides <strong>{summary['improvement_percentage']:.1f}% more comprehensive insights</strong> compared to basic analysis.</p>
            <p>This enables better decision-making, enhanced code understanding, and improved project planning.</p>
        </div>
    </div>
</body>
</html>"""

    return html


def generate_script_analyses(scripts):
    """Generate HTML for individual script analyses"""
    html = ""

    for i, script in enumerate(scripts, 1):
        original = script["original_analysis"]
        content_aware = script["content_aware_analysis"]
        improvements = script["improvements"]

        html += f"""
        <div class="script-analysis">
            <div class="script-header">
                <h3>📁 Script {i}: {script['script_name']}</h3>
                <p>Path: {script['script_path']}</p>
            </div>
            <div class="script-content">
                <div class="comparison-grid">
                    <div class="analysis-section">
                        <h4>📈 Original Analysis</h4>
                        <ul class="metrics-list">
                            <li><span class="metric-name">File Size:</span> <span class="metric-value">{original['file_size']:,} bytes</span></li>
                            <li><span class="metric-name">Lines:</span> <span class="metric-value">{original['line_count']}</span></li>
                            <li><span class="metric-name">Functions:</span> <span class="metric-value">{original['function_count']}</span></li>
                            <li><span class="metric-name">Classes:</span> <span class="metric-value">{original['class_count']}</span></li>
                            <li><span class="metric-name">Imports:</span> <span class="metric-value">{original['import_count']}</span></li>
                            <li><span class="metric-name">Comments:</span> <span class="metric-value">{original['comment_lines']}</span></li>
                            <li><span class="metric-name">Complexity:</span> <span class="metric-value">{original['complexity_score']}</span></li>
                            <li><span class="metric-name">Technologies:</span> <span class="metric-value">{len(original.get('technologies', {}))}</span></li>
                        </ul>
                    </div>
                    <div class="analysis-section">
                        <h4>🧠 Content-Aware Analysis</h4>
                        <ul class="metrics-list">
                            <li><span class="metric-name">File Size:</span> <span class="metric-value">{content_aware['file_size']:,} bytes</span></li>
                            <li><span class="metric-name">Lines:</span> <span class="metric-value">{content_aware['line_count']}</span></li>
                            <li><span class="metric-name">Functions:</span> <span class="metric-value">{content_aware['function_count']}</span></li>
                            <li><span class="metric-name">Classes:</span> <span class="metric-value">{content_aware['class_count']}</span></li>
                            <li><span class="metric-name">Imports:</span> <span class="metric-value">{content_aware['import_count']}</span></li>
                            <li><span class="metric-name">Comments:</span> <span class="metric-value">{content_aware['comment_lines']}</span></li>
                            <li><span class="metric-name">Complexity:</span> <span class="metric-value">{content_aware.get('complexity_score', 0)}</span></li>
                            <li><span class="metric-name">Technologies:</span> <span class="metric-value">{len(content_aware.get('technology_stack', {}))}</span></li>
                        </ul>
                    </div>
                </div>
                
                <div class="analysis-section">
                    <h4>🔍 Advanced Metrics (Content-Aware Only)</h4>
                    <ul class="metrics-list">
                        <li><span class="metric-name">Code Quality Score:</span> <span class="metric-value">{content_aware.get('code_quality', {}).get('quality_score', 0):.1f}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Business Value:</span> <span class="metric-value">{content_aware.get('business_value', {}).get('overall_business_value', 0):.1f}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Maintainability:</span> <span class="metric-value">{content_aware.get('maintainability', {}).get('maintainability_score', 0)}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Security Score:</span> <span class="metric-value">{content_aware.get('security_analysis', {}).get('security_score', 0)}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Performance Score:</span> <span class="metric-value">{content_aware.get('performance_indicators', {}).get('performance_score', 0)}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Innovation Score:</span> <span class="metric-value">{content_aware.get('innovation_score', {}).get('innovation_score', 0)}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Scalability Score:</span> <span class="metric-value">{content_aware.get('scalability_potential', {}).get('scalability_score', 0)}/CONSTANT_100</span></li>
                        <li><span class="metric-name">Documentation Score:</span> <span class="metric-value">{content_aware.get('documentation_quality', {}).get('documentation_score', 0):.1f}/CONSTANT_100</span></li>
                    </ul>
                </div>
                
                <div class="improvements">
                    <h4>✨ Improvements Demonstrated</h4>
                    <ul class="metrics-list">
                        <li><span class="metric-name">Additional Metrics:</span> <span class="metric-value">+{improvements['metrics_added']}</span></li>
                        <li><span class="metric-name">Analysis Depth:</span> <span class="metric-value">{improvements['analysis_depth']}</span></li>
                        <li><span class="metric-name">New Insights:</span> <span class="metric-value">{len(improvements['insights_gained'])}</span></li>
                        <li><span class="metric-name">Value Added:</span> <span class="metric-value">+{improvements['value_added']} metrics</span></li>
                    </ul>
                </div>
            </div>
        </div>
        """

    return html


def generate_capability_list(capabilities):
    """Generate HTML list for capabilities"""
    return Path("\n").join([f"<li>{capability}</li>" for capability in capabilities])


if __name__ == "__main__":
    generate_detailed_report()
