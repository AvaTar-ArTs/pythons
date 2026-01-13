#!/usr/bin/env python3
"""
Tree Visualizer - Generate interactive HTML tree visualization
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

class TreeVisualizer:
    """Generates interactive HTML tree visualizations."""
    
    def __init__(self):
        self.tree_data = {}
        
    def generate_html_tree(self, result: Any, output_dir: Path):
        """Generate interactive HTML tree visualization."""
        print("   🌳 Generating interactive tree visualization...")
        
        # Prepare tree data
        tree_data = self._prepare_tree_data(result)
        
        # Generate HTML
        html_content = self._generate_tree_html(tree_data, result)
        
        # Save HTML file
        html_path = output_dir / "interactive_tree.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Save tree data as JSON
        json_path = output_dir / "tree_data.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(tree_data, f, indent=2, ensure_ascii=False)
        
        print(f"     🌳 Interactive tree: {html_path}")
        print(f"     📄 Tree data: {json_path}")
    
    def _prepare_tree_data(self, result: Any) -> Dict:
        """Prepare tree data from analysis result."""
        tree_data = {
            'name': Path(result.root_path).name,
            'path': result.root_path,
            'type': 'directory',
            'children': [],
            'metadata': {
                'total_files': result.total_files,
                'total_directories': result.total_directories,
                'max_depth': result.max_depth,
                'analysis_timestamp': result.analysis_timestamp.isoformat()
            }
        }
        
        # Build tree structure from file data
        if hasattr(result, 'files') and result.files:
            tree_data['children'] = self._build_tree_from_files(result.files, result.root_path)
        else:
            # Fallback: create a simple structure based on categories
            tree_data['children'] = self._build_tree_from_categories(result)
        
        return tree_data
    
    def _build_tree_from_files(self, files: List, root_path: str) -> List[Dict]:
        """Build tree structure from file list."""
        tree_nodes = {}
        root_path_obj = Path(root_path)
        
        for file_info in files:
            try:
                file_path = Path(file_info.path)
                relative_path = file_path.relative_to(root_path_obj)
                path_parts = relative_path.parts
                
                # Build tree structure
                current_level = tree_nodes
                for i, part in enumerate(path_parts[:-1]):  # Exclude filename
                    if part not in current_level:
                        current_level[part] = {
                            'name': part,
                            'path': str(root_path_obj / Path(*path_parts[:i+1])),
                            'type': 'directory',
                            'children': {},
                            'metadata': {
                                'file_count': 0,
                                'total_size': 0,
                                'depth': i + 1
                            }
                        }
                    current_level = current_level[part]['children']
                
                # Add file
                filename = path_parts[-1]
                current_level[filename] = {
                    'name': filename,
                    'path': file_info.path,
                    'type': 'file',
                    'children': [],
                    'metadata': {
                        'size_bytes': file_info.size,
                        'size_mb': round(file_info.size / (1024 * 1024), 2),
                        'extension': file_info.extension,
                        'category': file_info.category,
                        'depth': file_info.depth,
                        'modified_time': file_info.modified_time.isoformat(),
                        'is_duplicate': file_info.is_duplicate,
                        'mime_type': file_info.mime_type
                    }
                }
                
                # Update parent directory metadata
                self._update_parent_metadata(tree_nodes, path_parts[:-1], file_info.size)
                
            except (ValueError, OSError):
                # Skip files that can't be processed
                continue
        
        # Convert to list format and sort
        return self._convert_tree_to_list(tree_nodes)
    
    def _build_tree_from_categories(self, result: Any) -> List[Dict]:
        """Build tree structure from categories when file details aren't available."""
        tree_nodes = []
        
        for category, count in sorted(result.categories.items(), key=lambda x: x[1], reverse=True):
            size_bytes = result.size_by_category.get(category, 0)
            tree_nodes.append({
                'name': f"{category} ({count:,} files)",
                'path': f"category/{category}",
                'type': 'category',
                'children': [],
                'metadata': {
                    'file_count': count,
                    'size_bytes': size_bytes,
                    'size_mb': round(size_bytes / (1024 * 1024), 2),
                    'percentage': round((count / result.total_files) * 100, 2) if result.total_files > 0 else 0
                }
            })
        
        return tree_nodes
    
    def _update_parent_metadata(self, tree_nodes: Dict, path_parts: List[str], file_size: int):
        """Update metadata for parent directories."""
        current_level = tree_nodes
        
        for part in path_parts:
            if part in current_level:
                current_level[part]['metadata']['file_count'] += 1
                current_level[part]['metadata']['total_size'] += file_size
                current_level = current_level[part]['children']
            else:
                break
    
    def _convert_tree_to_list(self, tree_nodes: Dict) -> List[Dict]:
        """Convert tree dictionary to list format."""
        result = []
        
        for name, node in tree_nodes.items():
            if isinstance(node, dict):
                if 'children' in node and isinstance(node['children'], dict):
                    node['children'] = self._convert_tree_to_list(node['children'])
                result.append(node)
        
        # Sort directories first, then files
        result.sort(key=lambda x: (x['type'] != 'directory', x['name'].lower()))
        
        return result
    
    def _generate_tree_html(self, tree_data: Dict, result: Any) -> str:
        """Generate HTML for interactive tree visualization."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Tree Visualization - Deep Research Tool</title>
    <style>
        {self._get_tree_css()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🌳 Interactive Tree Visualization</h1>
            <p class="subtitle">Folder structure with {result.total_files:,} files across {result.total_directories:,} directories</p>
            <div class="controls">
                <button id="expandAll" class="btn">Expand All</button>
                <button id="collapseAll" class="btn">Collapse All</button>
                <button id="showStats" class="btn">Show Stats</button>
                <input type="text" id="searchInput" placeholder="Search files..." class="search-input">
            </div>
        </header>
        
        <div class="tree-container">
            <div id="tree" class="tree">
                {self._generate_tree_html_recursive(tree_data, 0)}
            </div>
        </div>
        
        <div id="statsPanel" class="stats-panel" style="display: none;">
            <h3>Statistics</h3>
            <div id="statsContent"></div>
        </div>
    </div>
    
    <script>
        {self._get_tree_javascript()}
    </script>
</body>
</html>"""
    
    def _generate_tree_html_recursive(self, node: Dict, depth: int) -> str:
        """Generate HTML for tree nodes recursively."""
        indent = "  " * depth
        node_id = f"node_{hash(node['path'])}"
        
        # Determine icon based on type
        if node['type'] == 'directory':
            icon = "📁"
        elif node['type'] == 'file':
            icon = self._get_file_icon(node.get('metadata', {}).get('extension', ''))
        elif node['type'] == 'category':
            icon = "📂"
        else:
            icon = "📄"
        
        # Build node HTML
        html = f'{indent}<div class="tree-node" id="{node_id}" data-depth="{depth}" data-type="{node["type"]}">\n'
        html += f'{indent}  <div class="node-content" onclick="toggleNode(\'{node_id}\')">\n'
        html += f'{indent}    <span class="node-icon">{icon}</span>\n'
        html += f'{indent}    <span class="node-name">{node["name"]}</span>\n'
        
        # Add metadata if available
        if 'metadata' in node:
            metadata = node['metadata']
            if 'file_count' in metadata:
                html += f'{indent}    <span class="node-count">({metadata["file_count"]:,} files)</span>\n'
            if 'size_mb' in metadata:
                html += f'{indent}    <span class="node-size">{metadata["size_mb"]} MB</span>\n'
            if 'percentage' in metadata:
                html += f'{indent}    <span class="node-percentage">{metadata["percentage"]}%</span>\n'
        
        html += f'{indent}  </div>\n'
        
        # Add children if any
        if node.get('children'):
            html += f'{indent}  <div class="node-children" id="children_{node_id}" style="display: none;">\n'
            for child in node['children']:
                html += self._generate_tree_html_recursive(child, depth + 1)
            html += f'{indent}  </div>\n'
        
        html += f'{indent}</div>\n'
        
        return html
    
    def _get_file_icon(self, extension: str) -> str:
        """Get appropriate icon for file extension."""
        icon_map = {
            'py': '🐍',
            'js': '📜',
            'ts': '📘',
            'html': '🌐',
            'css': '🎨',
            'json': '📋',
            'md': '📝',
            'txt': '📄',
            'pdf': '📕',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'png': '🖼️',
            'gif': '🖼️',
            'svg': '🖼️',
            'mp4': '🎬',
            'mp3': '🎵',
            'zip': '📦',
            'tar': '📦',
            'gz': '📦',
            'exe': '⚙️',
            'dmg': '💿',
            'app': '📱'
        }
        
        return icon_map.get(extension.lower(), '📄')
    
    def _get_tree_css(self) -> str:
        """Get CSS styles for tree visualization."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: #f8f9fa; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .header h1 { font-size: 2.2em; margin-bottom: 10px; color: #2c3e50; }
        .subtitle { color: #7f8c8d; font-size: 1.1em; margin-bottom: 15px; }
        .controls { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
        .btn { padding: 8px 16px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
        .btn:hover { background: #2980b9; }
        .search-input { padding: 8px 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; min-width: 200px; }
        .tree-container { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px; overflow-x: auto; }
        .tree { font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace; font-size: 14px; }
        .tree-node { margin: 2px 0; }
        .node-content { display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .node-content:hover { background: #f0f0f0; }
        .node-icon { margin-right: 8px; font-size: 16px; }
        .node-name { flex: 1; font-weight: 500; }
        .node-count { color: #7f8c8d; font-size: 12px; margin-left: 8px; }
        .node-size { color: #27ae60; font-size: 12px; margin-left: 8px; font-weight: bold; }
        .node-percentage { color: #e74c3c; font-size: 12px; margin-left: 8px; font-weight: bold; }
        .node-children { margin-left: 20px; border-left: 1px solid #eee; padding-left: 10px; }
        .stats-panel { background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px; margin-top: 20px; }
        .stats-panel h3 { margin-bottom: 15px; color: #2c3e50; }
        .expanded .node-children { display: block !important; }
        .expanded .node-content::before { content: "▼ "; }
        .collapsed .node-content::before { content: "▶ "; }
        .highlight { background: #fff3cd !important; }
        .file-node { color: #666; }
        .directory-node { color: #2c3e50; font-weight: 600; }
        .category-node { color: #8e44ad; font-weight: 600; }
        """
    
    def _get_tree_javascript(self) -> str:
        """Get JavaScript for tree interactivity."""
        return """
        let treeData = null;
        
        // Load tree data
        fetch('tree_data.json')
            .then(response => response.json())
            .then(data => {
                treeData = data;
                console.log('Tree data loaded:', data);
            })
            .catch(error => console.error('Error loading tree data:', error));
        
        // Toggle node expansion
        function toggleNode(nodeId) {
            const node = document.getElementById(nodeId);
            const children = document.getElementById('children_' + nodeId);
            
            if (children) {
                if (children.style.display === 'none') {
                    children.style.display = 'block';
                    node.classList.add('expanded');
                    node.classList.remove('collapsed');
                } else {
                    children.style.display = 'none';
                    node.classList.add('collapsed');
                    node.classList.remove('expanded');
                }
            }
        }
        
        // Expand all nodes
        document.getElementById('expandAll').addEventListener('click', function() {
            const allChildren = document.querySelectorAll('.node-children');
            const allNodes = document.querySelectorAll('.tree-node');
            
            allChildren.forEach(child => child.style.display = 'block');
            allNodes.forEach(node => {
                node.classList.add('expanded');
                node.classList.remove('collapsed');
            });
        });
        
        // Collapse all nodes
        document.getElementById('collapseAll').addEventListener('click', function() {
            const allChildren = document.querySelectorAll('.node-children');
            const allNodes = document.querySelectorAll('.tree-node');
            
            allChildren.forEach(child => child.style.display = 'none');
            allNodes.forEach(node => {
                node.classList.add('collapsed');
                node.classList.remove('expanded');
            });
        });
        
        // Show statistics
        document.getElementById('showStats').addEventListener('click', function() {
            const statsPanel = document.getElementById('statsPanel');
            const statsContent = document.getElementById('statsContent');
            
            if (statsPanel.style.display === 'none') {
                if (treeData) {
                    statsContent.innerHTML = generateStatsHTML(treeData);
                }
                statsPanel.style.display = 'block';
            } else {
                statsPanel.style.display = 'none';
            }
        });
        
        // Search functionality
        document.getElementById('searchInput').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const allNodes = document.querySelectorAll('.node-name');
            
            allNodes.forEach(node => {
                const nodeElement = node.closest('.tree-node');
                if (node.textContent.toLowerCase().includes(searchTerm)) {
                    nodeElement.classList.add('highlight');
                    // Expand parent nodes
                    let parent = nodeElement.parentElement;
                    while (parent && parent.classList.contains('node-children')) {
                        parent.style.display = 'block';
                        parent.previousElementSibling.classList.add('expanded');
                        parent.previousElementSibling.classList.remove('collapsed');
                        parent = parent.parentElement.parentElement;
                    }
                } else {
                    nodeElement.classList.remove('highlight');
                }
            });
        });
        
        // Generate statistics HTML
        function generateStatsHTML(data) {
            let html = '<div class="stats-grid">';
            
            // Basic stats
            html += '<div class="stat-item">';
            html += '<h4>Basic Statistics</h4>';
            html += '<p>Total Files: ' + data.metadata.total_files.toLocaleString() + '</p>';
            html += '<p>Total Directories: ' + data.metadata.total_directories.toLocaleString() + '</p>';
            html += '<p>Max Depth: ' + data.metadata.max_depth + '</p>';
            html += '</div>';
            
            // File type distribution
            const fileTypes = {};
            const categories = {};
            let totalSize = 0;
            
            function analyzeNode(node) {
                if (node.type === 'file' && node.metadata) {
                    const ext = node.metadata.extension || 'no-extension';
                    fileTypes[ext] = (fileTypes[ext] || 0) + 1;
                    
                    const category = node.metadata.category || 'unknown';
                    categories[category] = (categories[category] || 0) + 1;
                    
                    totalSize += node.metadata.size_bytes || 0;
                }
                
                if (node.children) {
                    node.children.forEach(analyzeNode);
                }
            }
            
            analyzeNode(data);
            
            // Top file types
            html += '<div class="stat-item">';
            html += '<h4>Top File Types</h4>';
            const topFileTypes = Object.entries(fileTypes)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            topFileTypes.forEach(([ext, count]) => {
                html += '<p>.' + ext + ': ' + count.toLocaleString() + ' files</p>';
            });
            html += '</div>';
            
            // Top categories
            html += '<div class="stat-item">';
            html += '<h4>Top Categories</h4>';
            const topCategories = Object.entries(categories)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            topCategories.forEach(([category, count]) => {
                html += '<p>' + category + ': ' + count.toLocaleString() + ' files</p>';
            });
            html += '</div>';
            
            // Size information
            html += '<div class="stat-item">';
            html += '<h4>Size Information</h4>';
            html += '<p>Total Size: ' + (totalSize / (1024 * 1024)).toFixed(2) + ' MB</p>';
            html += '<p>Average File Size: ' + (totalSize / data.metadata.total_files / 1024).toFixed(2) + ' KB</p>';
            html += '</div>';
            
            html += '</div>';
            return html;
        }
        
        // Initialize tree
        document.addEventListener('DOMContentLoaded', function() {
            // Add initial styling
            const allNodes = document.querySelectorAll('.tree-node');
            allNodes.forEach(node => {
                const type = node.dataset.type;
                if (type === 'file') {
                    node.classList.add('file-node');
                } else if (type === 'directory') {
                    node.classList.add('directory-node');
                } else if (type === 'category') {
                    node.classList.add('category-node');
                }
            });
        });
        """