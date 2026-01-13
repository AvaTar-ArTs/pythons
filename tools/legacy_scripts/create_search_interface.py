#!/usr/bin/env python3
"""
Create searchable HTML interface for all exports
"""
from pathlib import Path
import html as html_lib
from datetime import datetime

def create_html_interface():
    print("🔍 CREATING SEARCH INTERFACE")
    print("=" * 70)
    
    # Paths
    cursor_dir = Path.home() / "Documents" / "cursor-chats-export"
    paste_dir = Path.home() / "Documents" / "paste-clipboard-FULL-export"
    output_dir = Path.home() / "Documents" / "unified-search"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nCreating unified search interface...\n")
    
    # Read all cursor chats
    cursor_files = list(cursor_dir.glob("*.md"))
    cursor_files = [f for f in cursor_files if f.name != "README.md"]
    
    # Read all paste files
    paste_files = list(paste_dir.glob("clipboard_*.md"))
    
    print(f"Found {len(cursor_files)} Cursor chats")
    print(f"Found {len(paste_files)} Paste clipboard days\n")
    
    # Create HTML search page
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unified Export Search</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2563eb;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .search-box {
            margin: 30px 0;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #2563eb;
        }
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }
        .tab {
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 16px;
            color: #666;
            transition: all 0.3s;
        }
        .tab.active {
            color: #2563eb;
            border-bottom: 2px solid #2563eb;
            margin-bottom: -2px;
        }
        .file-list {
            max-height: 600px;
            overflow-y: auto;
        }
        .file-item {
            padding: 15px;
            margin: 10px 0;
            background: #f9fafb;
            border-left: 4px solid #2563eb;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .file-item:hover {
            background: #eff6ff;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
        }
        .file-item.hidden {
            display: none;
        }
        .file-name {
            font-weight: 600;
            color: #1e40af;
            margin-bottom: 5px;
        }
        .file-meta {
            font-size: 14px;
            color: #666;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        .no-results {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        code {
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Unified Export Search</h1>
        <p class="subtitle">Search across all your Cursor chats and Paste clipboard history</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">""" + str(len(cursor_files)) + """</div>
                <div class="stat-label">Cursor Chats</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(len(paste_files)) + """</div>
                <div class="stat-label">Clipboard Days</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(len(cursor_files) + len(paste_files)) + """</div>
                <div class="stat-label">Total Files</div>
            </div>
        </div>
        
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔎 Search for anything... (e.g., python, organize, code)" autofocus>
        </div>
        
        <div class="tabs">
            <button class="tab active" data-tab="all">All Files</button>
            <button class="tab" data-tab="cursor">Cursor Chats Only</button>
            <button class="tab" data-tab="paste">Clipboard Only</button>
        </div>
        
        <div class="file-list" id="fileList">
            <div class="no-results" id="noResults" style="display: none;">
                No results found. Try a different search term.
            </div>
        </div>
    </div>
    
    <script>
        const cursorFiles = """ + str([{
            'name': f.name,
            'path': f'../cursor-chats-export/{f.name}',
            'type': 'cursor'
        } for f in cursor_files]) + """;
        
        const pasteFiles = """ + str([{
            'name': f.name,
            'path': f'../paste-clipboard-FULL-export/{f.name}',
            'type': 'paste'
        } for f in paste_files]) + """;
        
        const allFiles = [...cursorFiles, ...pasteFiles];
        let currentFilter = 'all';
        
        function renderFiles(files, searchTerm = '') {
            const fileList = document.getElementById('fileList');
            const noResults = document.getElementById('noResults');
            
            let filtered = files;
            
            // Filter by tab
            if (currentFilter !== 'all') {
                filtered = filtered.filter(f => f.type === currentFilter);
            }
            
            // Filter by search term
            if (searchTerm) {
                filtered = filtered.filter(f => 
                    f.name.toLowerCase().includes(searchTerm.toLowerCase())
                );
            }
            
            fileList.innerHTML = '';
            
            if (filtered.length === 0) {
                noResults.style.display = 'block';
                return;
            }
            
            noResults.style.display = 'none';
            
            filtered.forEach(file => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.innerHTML = `
                    <div class="file-name">${file.name}</div>
                    <div class="file-meta">
                        <span>${file.type === 'cursor' ? '💬 Cursor Chat' : '📋 Clipboard Day'}</span>
                    </div>
                `;
                item.onclick = () => window.open(file.path, '_blank');
                fileList.appendChild(item);
            });
        }
        
        // Initialize
        renderFiles(allFiles);
        
        // Search input
        document.getElementById('searchInput').addEventListener('input', (e) => {
            renderFiles(allFiles, e.target.value);
        });
        
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentFilter = tab.dataset.tab;
                renderFiles(allFiles, document.getElementById('searchInput').value);
            });
        });
    </script>
</body>
</html>"""
    
    # Write HTML file
    html_path = output_dir / "index.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created search interface")
    print(f"   Location: {html_path}")
    print(f"\n📂 Open with:")
    print(f"   open {html_path}")

if __name__ == "__main__":
    create_html_interface()
