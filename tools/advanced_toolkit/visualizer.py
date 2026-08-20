#!/usr/bin/env python3
"""
File Intelligence Visualizer
Creates visual reports and dashboards
"""

from pathlib import Path
from typing import Dict, List
import json
from collections import defaultdict
from file_intelligence import FileAnalyzer


class Visualizer:
    """Generate HTML visualizations of file intelligence data"""
    
    def __init__(self, analyzer: FileAnalyzer):
        self.analyzer = analyzer
    
    def generate_dashboard(self, output_path: Path):
        """Generate interactive HTML dashboard"""
        stats = self.analyzer.db.get_statistics()
        duplicates = self.analyzer.db.find_duplicates()
        
        html = self._create_html(stats, duplicates)
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        print(f"Dashboard generated: {output_path}")
    
    def _create_html(self, stats: Dict, duplicates: Dict) -> str:
        """Create HTML dashboard"""
        
        # Calculate duplicate statistics
        dup_count = len(duplicates)
        dup_waste = sum(
            Path(paths[0]).stat().st_size * (len(paths) - 1)
            for paths in duplicates.values()
            if Path(paths[0]).exists()
        )
        
        # Create extension chart data
        ext_data = []
        for ext_info in stats.get('top_extensions', [])[:10]:
            ext_data.append({
                'name': ext_info['ext'] or 'no extension',
                'count': ext_info['count'],
                'size': ext_info['size']
            })
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>File Intelligence Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }}
        
        .chart-title {{
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #333;
            text-align: center;
        }}
        
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .duplicate-list {{
            max-height: 400px;
            overflow-y: auto;
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .duplicate-item {{
            padding: 10px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }}
        
        .file-path {{
            font-family: monospace;
            font-size: 0.9em;
            color: #666;
            word-break: break-all;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>?? File Intelligence Dashboard</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_files']:,}</div>
                <div class="stat-label">Total Files</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{self._format_size(stats['total_size'])}</div>
                <div class="stat-label">Total Size</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{stats['unique_extensions']}</div>
                <div class="stat-label">File Types</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{dup_count}</div>
                <div class="stat-label">Duplicate Sets</div>
            </div>
        </div>
        
        {self._format_duplicate_warning(dup_count, dup_waste)}
        
        <div class="chart-container">
            <div class="chart-title">?? Files by Extension</div>
            <canvas id="extensionChart"></canvas>
        </div>
        
        <div class="chart-container">
            <div class="chart-title">?? Storage by Extension</div>
            <canvas id="sizeChart"></canvas>
        </div>
        
        {self._create_duplicate_list(duplicates)}
    </div>
    
    <script>
        // Extension count chart
        const extCtx = document.getElementById('extensionChart').getContext('2d');
        new Chart(extCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps([d['name'] for d in ext_data])},
                datasets: [{{
                    label: 'File Count',
                    data: {json.dumps([d['count'] for d in ext_data])},
                    backgroundColor: 'rgba(102, 126, 234, 0.8)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Size chart
        const sizeCtx = document.getElementById('sizeChart').getContext('2d');
        new Chart(sizeCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps([d['name'] for d in ext_data])},
                datasets: [{{
                    data: {json.dumps([d['size'] for d in ext_data])},
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#43e97b', '#fa709a', '#fee140', '#30cfd0',
                        '#a8edea', '#fed6e3'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const size = context.parsed;
                                return context.label + ': ' + formatSize(size);
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        function formatSize(bytes) {{
            const units = ['B', 'KB', 'MB', 'GB', 'TB'];
            let size = bytes;
            let unitIndex = 0;
            while (size >= 1024 && unitIndex < units.length - 1) {{
                size /= 1024;
                unitIndex++;
            }}
            return size.toFixed(2) + ' ' + units[unitIndex];
        }}
    </script>
</body>
</html>
        """
        
        return html
    
    def _format_duplicate_warning(self, count: int, waste: int) -> str:
        """Format duplicate warning section"""
        if count == 0:
            return ""
        
        return f"""
        <div class="warning">
            <strong>?? Duplicates Detected!</strong><br>
            Found {count} sets of duplicate files wasting <strong>{self._format_size(waste)}</strong> of storage.
            Run <code>master_control.py remove-duplicates</code> to clean up.
        </div>
        """
    
    def _create_duplicate_list(self, duplicates: Dict) -> str:
        """Create HTML list of duplicates"""
        if not duplicates:
            return ""
        
        items = []
        for hash_val, paths in list(duplicates.items())[:20]:
            paths = [Path(p) for p in paths if Path(p).exists()]
            if not paths:
                continue
            
            size = paths[0].stat().st_size
            waste = size * (len(paths) - 1)
            
            paths_html = '<br>'.join(
                f'<div class="file-path">? {p}</div>'
                for p in paths
            )
            
            items.append(f"""
            <div class="duplicate-item">
                <strong>Duplicate Set ({len(paths)} copies)</strong><br>
                Size: {self._format_size(size)} each | Wasted: {self._format_size(waste)}<br><br>
                {paths_html}
            </div>
            """)
        
        if len(duplicates) > 20:
            items.append(f"<div class='duplicate-item'><em>... and {len(duplicates) - 20} more sets</em></div>")
        
        return f"""
        <div class="chart-container">
            <div class="chart-title">?? Duplicate Files</div>
            <div class="duplicate-list">
                {''.join(items)}
            </div>
        </div>
        """
    
    def _format_size(self, size: int) -> str:
        """Format size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"


if __name__ == '__main__':
    import sys
    
    db_path = Path.home() / '.file_intelligence.db'
    analyzer = FileAnalyzer(db_path)
    
    viz = Visualizer(analyzer)
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dashboard.html')
    
    viz.generate_dashboard(output_path)
    
    analyzer.close()
