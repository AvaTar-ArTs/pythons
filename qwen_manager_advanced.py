#!/usr/bin/env python3
"""
Advanced Script to extract Qwen conversations with scheduling, search, and statistics
"""

import json
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import re
import hashlib
import gzip
import sqlite3
from collections import Counter
import argparse


class QwenConversationManager:
    def __init__(self):
        self.base_dir = Path.home() / ".qwen" / "projects"
        self.index_file_path = Path.home() / ".qwen_conversations_index.json"
        self.db_path = Path.home() / ".qwen_conversations.db"
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for storing conversation metadata and statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                project_name TEXT,
                file_path TEXT,
                start_time TEXT,
                end_time TEXT,
                message_count INTEGER,
                duration_seconds REAL,
                last_processed TEXT,
                tags TEXT
            )
        ''')
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                message_type TEXT,
                content TEXT,
                FOREIGN KEY (session_id) REFERENCES conversations (session_id)
            )
        ''')
        
        # Create index for faster searches
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_session_id ON messages(session_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_message_type ON messages(message_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)')
        
        conn.commit()
        conn.close()
    
    def extract_conversations_from_jsonl(self, jsonl_file_path):
        """Extract conversation data from a JSONL file."""
        conversation = []
        
        with open(jsonl_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        
                        # Extract relevant information
                        msg_type = entry.get('type')
                        timestamp = entry.get('timestamp')
                        message_parts = entry.get('message', {}).get('parts', [])
                        
                        # Format the message text
                        text_content = ""
                        for part in message_parts:
                            if 'text' in part:
                                text_content += part['text']
                            elif 'functionCall' in part:
                                func_call = part['functionCall']
                                text_content += f"[Function Call: {func_call.get('name', 'Unknown')}]"
                            elif 'functionResponse' in part:
                                func_resp = part['functionResponse']
                                text_content += f"[Function Response: {func_resp.get('name', 'Unknown')}]"
                        
                        if text_content:
                            conversation.append({
                                'type': msg_type,
                                'timestamp': timestamp,
                                'content': text_content.strip(),
                                'session_id': entry.get('sessionId', 'unknown'),
                                'project_name': entry.get('cwd', 'unknown'),
                                'file_path': str(jsonl_file_path)
                            })
                    except json.JSONDecodeError:
                        continue
        
        # Sort by timestamp if available
        def sort_by_timestamp(item):
            ts = item.get('timestamp')
            if ts:
                try:
                    return datetime.fromisoformat(ts.replace('Z', '+00:00'))
                except ValueError:
                    return datetime.min
            return datetime.min
        
        conversation.sort(key=sort_by_timestamp)
        return conversation
    
    def format_content(self, content):
        """Format content for better readability."""
        # Clean up repeated file paths that appeared in one of the conversations
        content = re.sub(r'/Users/steven/AVATARARTS/[^\n]*\n', '', content)
        
        # Remove excessive newlines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Clean up any remaining duplicate content
        lines = content.split('\n')
        unique_lines = []
        prev_line = ""
        for line in lines:
            if line.strip() != prev_line.strip():
                unique_lines.append(line)
                prev_line = line
        
        return '\n'.join(unique_lines).strip()
    
    def escape_html(self, text):
        """Escape HTML special characters."""
        if not isinstance(text, str):
            text = str(text)
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")
    
    def store_in_database(self, conversation_data, session_id, project_name, file_path):
        """Store conversation data in the SQLite database."""
        if not conversation_data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate duration
        duration_seconds = 0
        if len(conversation_data) >= 2:
            start_time = conversation_data[0].get('timestamp')
            end_time = conversation_data[-1].get('timestamp')
            if start_time and end_time:
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                    duration_seconds = (end_dt - start_dt).total_seconds()
                except:
                    pass
        
        # Insert or update conversation metadata
        cursor.execute('''
            INSERT OR REPLACE INTO conversations 
            (session_id, project_name, file_path, start_time, end_time, message_count, duration_seconds, last_processed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            project_name,
            file_path,
            conversation_data[0].get('timestamp', ''),
            conversation_data[-1].get('timestamp', ''),
            len(conversation_data),
            duration_seconds,
            datetime.now().isoformat()
        ))
        
        # Insert messages
        for entry in conversation_data:
            cursor.execute('''
                INSERT INTO messages (session_id, timestamp, message_type, content)
                VALUES (?, ?, ?, ?)
            ''', (
                session_id,
                entry.get('timestamp', ''),
                entry.get('type', ''),
                entry.get('content', '')
            ))
        
        conn.commit()
        conn.close()
    
    def get_existing_sessions_index(self):
        """Get the index of existing sessions from a JSON file."""
        if os.path.exists(self.index_file_path):
            with open(self.index_file_path, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}
    
    def save_sessions_index(self, sessions_index):
        """Save the index of sessions to a JSON file."""
        with open(self.index_file_path, 'w', encoding='utf-8') as f:
            json.dump(sessions_index, f, indent=2)
    
    def generate_statistics(self):
        """Generate statistics about conversations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total stats
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(message_count) FROM conversations')
        total_messages = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT MIN(start_time), MAX(end_time) FROM conversations')
        min_max_times = cursor.fetchone()
        time_range = f"{min_max_times[0][:10]} to {min_max_times[1][:10]}" if min_max_times[0] else "N/A"
        
        # Get project distribution
        cursor.execute('SELECT project_name, COUNT(*) FROM conversations GROUP BY project_name ORDER BY COUNT(*) DESC LIMIT 10')
        project_dist = cursor.fetchall()
        
        # Get message type distribution
        cursor.execute('SELECT message_type, COUNT(*) FROM messages GROUP BY message_type')
        msg_type_dist = cursor.fetchall()
        
        # Get top keywords
        cursor.execute('SELECT content FROM messages WHERE message_type = "user" LIMIT 1000')
        user_contents = [row[0] for row in cursor.fetchall()]
        all_text = ' '.join(user_contents)
        words = re.findall(r'\b\w{4,}\b', all_text.lower())
        top_keywords = Counter(words).most_common(20)
        
        conn.close()
        
        return {
            'total_sessions': total_sessions,
            'total_messages': total_messages,
            'time_range': time_range,
            'project_distribution': project_dist,
            'message_type_distribution': msg_type_dist,
            'top_keywords': top_keywords
        }
    
    def format_conversation_as_html(self, conversation_data, session_id, project_name):
        """Format conversation data into HTML."""
        if not conversation_data:
            return ""
        
        html = []
        html.append(f'<div class="conversation-session" id="session-{self.escape_html(session_id[:12])}">')
        html.append(f'<h3>Session: {self.escape_html(session_id)}</h3>')
        html.append(f'<p><strong>Project:</strong> {self.escape_html(project_name)}</p>')
        html.append(f'<p><strong>Messages:</strong> {len(conversation_data)}</p>')
        
        # Calculate duration if possible
        if len(conversation_data) >= 2:
            start_time = conversation_data[0].get('timestamp')
            end_time = conversation_data[-1].get('timestamp')
            if start_time and end_time:
                try:
                    start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                    duration = end_dt - start_dt
                    html.append(f'<p><strong>Duration:</strong> {duration}</p>')
                except:
                    pass
        
        html.append('<div class="messages">')
        
        for entry in conversation_data:
            timestamp = entry.get('timestamp', 'Unknown')
            msg_type = entry.get('type', 'Unknown')
            content = entry.get('content', '')
            
            # Format timestamp nicely
            if timestamp != 'Unknown':
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                except:
                    formatted_time = timestamp
            else:
                formatted_time = timestamp
            
            # Format the message type with consistent capitalization
            formatted_msg_type = msg_type.upper()
            if formatted_msg_type == 'USER':
                formatted_msg_type = 'USER'
                css_class = 'user-message'
            elif formatted_msg_type == 'ASSISTANT':
                formatted_msg_type = 'ASSISTANT'
                css_class = 'assistant-message'
            elif formatted_msg_type == 'SYSTEM':
                formatted_msg_type = 'SYSTEM'
                css_class = 'system-message'
            elif formatted_msg_type == 'TOOL_RESULT':
                formatted_msg_type = 'TOOL RESULT'
                css_class = 'tool-result-message'
            else:
                css_class = 'other-message'
            
            html.append(f'<div class="message {css_class}">')
            html.append(f'<div class="message-header">[{self.escape_html(formatted_time)}] {self.escape_html(formatted_msg_type)}:</div>')
            
            # Format content for readability
            formatted_content = self.format_content(content)
            html.append(f'<div class="message-content">{self.escape_html(formatted_content).replace(chr(10), "<br/>")}</div>')
            html.append('</div>')  # Close message div
        
        html.append('</div>')  # Close messages div
        html.append('</div>')  # Close conversation-session div
        
        return "\n".join(html)
    
    def generate_html_report(self, last_update_time, stats):
        """Generate the complete HTML report with search and statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all sessions ordered by start time
        cursor.execute('''
            SELECT session_id, project_name, message_count, start_time, end_time, duration_seconds
            FROM conversations
            ORDER BY start_time
        ''')
        sessions = cursor.fetchall()
        
        conn.close()
        
        # Generate JavaScript for search functionality
        js_script = '''
        <script>
        function searchConversations() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const sessions = document.getElementsByClassName('conversation-session');
            
            for (let session of sessions) {
                const content = session.innerHTML.toLowerCase();
                if (content.includes(searchTerm)) {
                    session.style.display = 'block';
                } else {
                    session.style.display = 'none';
                }
            }
        }
        
        function filterByProject() {
            const projectFilter = document.getElementById('projectFilter').value;
            const sessions = document.getElementsByClassName('conversation-session');
            
            for (let session of sessions) {
                if (projectFilter === '' || session.innerHTML.includes(projectFilter)) {
                    session.style.display = 'block';
                } else {
                    session.style.display = 'none';
                }
            }
        }
        
        function toggleSection(sectionId) {
            const section = document.getElementById(sectionId);
            if (section.style.display === 'none') {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
            }
        }
        </script>
        '''
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qwen Conversation History - Advanced Manager</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }}
        .controls {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .controls input, .controls select {{
            padding: 8px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .summary-table th, .summary-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        .summary-table th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        .summary-table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .conversation-session {{
            border: 1px solid #ddd;
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            background-color: #fafafa;
        }}
        .messages {{
            margin-top: 15px;
        }}
        .message {{
            margin: 10px 0;
            padding: 10px;
            border-radius: 4px;
        }}
        .user-message {{
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }}
        .assistant-message {{
            background-color: #f3e5f5;
            border-left: 4px solid #9c27b0;
        }}
        .system-message {{
            background-color: #e8f5e8;
            border-left: 4px solid #4caf50;
        }}
        .tool-result-message {{
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
        }}
        .other-message {{
            background-color: #f5f5f5;
            border-left: 4px solid #9e9e9e;
        }}
        .message-header {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .message-content {{
            white-space: pre-wrap;
        }}
        .metadata {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        .stats {{
            background-color: #e3f2fd;
            padding: 10px;
            border-radius: 4px;
            margin: 15px 0;
        }}
        .update-info {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 10px;
            border-radius: 4px;
            margin: 15px 0;
            color: #856404;
        }}
        .nav-menu {{
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        .nav-menu ul {{
            list-style-type: none;
            padding: 0;
        }}
        .nav-menu li {{
            display: inline-block;
            margin-right: 15px;
        }}
        .nav-menu a {{
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
        }}
        .nav-menu a:hover {{
            text-decoration: underline;
        }}
        .stat-card {{
            display: inline-block;
            width: 200px;
            margin: 10px;
            padding: 15px;
            background-color: #f1f8e9;
            border-radius: 4px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
        }}
        .stat-label {{
            font-size: 14px;
            color: #555;
        }}
        .toggle-button {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Qwen Conversation History - Advanced Manager</h1>
        <div class="update-info">
            <p><strong>Last Updated:</strong> {last_update_time}</p>
            <p><em>This report is automatically updated when new conversations are detected.</em></p>
        </div>
        
        <div class="nav-menu">
            <ul>
                <li><a href="#summary">Summary</a></li>
                <li><a href="#statistics">Statistics</a></li>
                <li><a href="#search">Search</a></li>
                <li><a href="#conversations">Conversations</a></li>
            </ul>
        </div>
        
        <div class="controls" id="search">
            <h3>Search & Filter</h3>
            <input type="text" id="searchInput" placeholder="Search conversations..." onkeyup="searchConversations()">
            <select id="projectFilter" onchange="filterByProject()">
                <option value="">All Projects</option>
        '''
        
        # Add project options to the filter
        unique_projects = set()
        for session in sessions:
            unique_projects.add(session[1])
        
        for project in sorted(unique_projects):
            html += f'        <option value="{self.escape_html(project)}">{self.escape_html(project)}</option>\n'
        
        html += '''      </select>
        </div>
        
        <div class="stats" id="statistics">
            <h3>Statistics</h3>
            <div class="stat-card">
                <div class="stat-value">{stats['total_sessions']}</div>
                <div class="stat-label">Total Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['total_messages']}</div>
                <div class="stat-label">Total Messages</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['time_range']}</div>
                <div class="stat-label">Time Range</div>
            </div>
            
            <h4>Project Distribution (Top 10)</h4>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Project</th>
                        <th>Sessions</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for project, count in stats['project_distribution']:
            html += f'''
                    <tr>
                        <td>{self.escape_html(project)}</td>
                        <td>{count}</td>
                    </tr>
            '''
        
        html += '''
                </tbody>
            </table>
            
            <h4>Message Types</h4>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Count</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for msg_type, count in stats['message_type_distribution']:
            html += f'''
                    <tr>
                        <td>{self.escape_html(msg_type)}</td>
                        <td>{count}</td>
                    </tr>
            '''
        
        html += '''
                </tbody>
            </table>
            
            <h4>Top Keywords (from user messages)</h4>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Keyword</th>
                        <th>Frequency</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for keyword, count in stats['top_keywords']:
            html += f'''
                    <tr>
                        <td>{self.escape_html(keyword)}</td>
                        <td>{count}</td>
                    </tr>
            '''
        
        html += '''
                </tbody>
            </table>
        </div>
        
        <div class="stats" id="summary">
            <h3>Conversation Summary</h3>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Session ID</th>
                        <th>Project</th>
                        <th>Messages</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Duration (sec)</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>'''
        
        for session in sessions:
            session_id, project_name, msg_count, start_time, end_time, duration = session
            session_id_short = session_id[:12]
            html += f'''
                    <tr>
                        <td><a href="#session-{self.escape_html(session_id_short)}">{self.escape_html(session_id[:19])}</a></td>
                        <td>{self.escape_html(project_name)}</td>
                        <td>{msg_count}</td>
                        <td>{start_time[:19] if start_time else 'N/A'}</td>
                        <td>{end_time[:19] if end_time else 'N/A'}</td>
                        <td>{f"{duration:.1f}" if duration else 'N/A'}</td>
                        <td><a href="#session-{self.escape_html(session_id_short)}">View</a></td>
                    </tr>'''
        
        html += '''
                </tbody>
            </table>
        </div>
        
        <div class="conversations" id="conversations">
            <h2>Detailed Conversations</h2>
            <button class="toggle-button" onclick="toggleSection('all-conversations')">Toggle All</button>
            <div id="all-conversations">'''
        
        # Get all conversations from DB to render
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for session in sessions:
            session_id = session[0]
            project_name = session[1]
            
            cursor.execute('''
                SELECT timestamp, message_type, content
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp
            ''', (session_id,))
            
            messages = cursor.fetchall()
            
            # Reconstruct conversation data format
            conversation_data = []
            for msg in messages:
                conversation_data.append({
                    'timestamp': msg[0],
                    'type': msg[1],
                    'content': msg[2]
                })
            
            html += self.format_conversation_as_html(conversation_data, session_id, project_name)
        
        conn.close()
        
        html += '''
            </div>
        </div>
    </div>
    ''' + js_script + '''
</body>
</html>'''
        
        return html
    
    def run_extraction(self, compress=False):
        """Main function to extract all Qwen conversations and generate HTML report."""
        if not self.base_dir.exists():
            print(f"Directory {self.base_dir} does not exist.")
            return
        
        # Load existing session index
        existing_sessions = self.get_existing_sessions_index()
        
        # Find all project directories
        project_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]
        
        session_info = []  # Store session metadata for summary
        new_sessions_found = 0
        
        for project_dir in project_dirs:
            project_name = project_dir.name
            chats_dir = project_dir / "chats"
            
            if not chats_dir.exists():
                continue
                
            # Process all JSONL files in the chats directory
            jsonl_files = list(chats_dir.glob("*.jsonl"))
            
            for jsonl_file in jsonl_files:
                # Check if this file has been processed before
                file_mtime = jsonl_file.stat().st_mtime
                file_path_str = str(jsonl_file)
                
                if file_path_str in existing_sessions:
                    if existing_sessions[file_path_str]['mtime'] >= file_mtime:
                        print(f"Skipping {jsonl_file} (already processed)")
                        continue  # Skip if file hasn't changed
                
                print(f"Processing {jsonl_file}")
                
                try:
                    conversation_data = self.extract_conversations_from_jsonl(jsonl_file)
                    
                    if conversation_data:
                        session_id = conversation_data[0].get('session_id', 'unknown')
                        
                        # Store in database
                        self.store_in_database(conversation_data, session_id, project_name, str(jsonl_file))
                        
                        # Store session info for summary
                        session_info.append({
                            'session_id': session_id,
                            'project_name': project_name,
                            'messages_count': len(conversation_data),
                            'start_time': conversation_data[0].get('timestamp', 'Unknown'),
                            'end_time': conversation_data[-1].get('timestamp', 'Unknown'),
                            'file_path': str(jsonl_file)
                        })
                        
                        # Update the index with this file's info
                        existing_sessions[file_path_str] = {
                            'session_id': session_id,
                            'project_name': project_name,
                            'mtime': file_mtime,
                            'processed_at': datetime.now().isoformat()
                        }
                        
                        new_sessions_found += 1
                        
                except Exception as e:
                    print(f"Error processing {jsonl_file}: {str(e)}")
        
        # Save the updated index
        self.save_sessions_index(existing_sessions)
        
        # Generate statistics
        stats = self.generate_statistics()
        
        # Generate the HTML report
        last_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        html_report = self.generate_html_report(last_update_time, stats)
        
        # Write the HTML report to a file
        output_file = Path.home() / "qwen_conversations_export_advanced.html"
        
        if compress:
            # Write compressed version
            compressed_file = Path.home() / "qwen_conversations_export_advanced.html.gz"
            with gzip.open(compressed_file, 'wt', encoding='utf-8') as f:
                f.write(html_report)
            print(f"\nCompressed HTML export completed! Conversations saved to: {compressed_file}")
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_report)
            print(f"\nHTML export completed! Conversations saved to: {output_file}")
        
        # Create backup of the previous version
        backup_file = Path.home() / f"qwen_conversations_export_advanced_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        if output_file.exists():
            shutil.copy2(output_file, backup_file)
            print(f"Backup created: {backup_file}")
        
        print(f"Total conversations in database: {stats['total_sessions']}")
        print(f"New or updated conversations processed: {new_sessions_found}")
        print(f"Time range: {stats['time_range']}")


def main():
    parser = argparse.ArgumentParser(description='Qwen Conversation Manager')
    parser.add_argument('--compress', action='store_true', help='Compress the output HTML file')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--reset', action='store_true', help='Reset the database and index')
    
    args = parser.parse_args()
    
    manager = QwenConversationManager()
    
    if args.reset:
        # Reset the database and index
        if os.path.exists(manager.db_path):
            os.remove(manager.db_path)
            print(f"Database reset: {manager.db_path}")
        
        if os.path.exists(manager.index_file_path):
            os.remove(manager.index_file_path)
            print(f"Index file reset: {manager.index_file_path}")
        
        manager.init_db()
        print("Database and index have been reset.")
        return
    
    if args.stats:
        # Show statistics only
        stats = manager.generate_statistics()
        print("Qwen Conversation Statistics:")
        print(f"Total Sessions: {stats['total_sessions']}")
        print(f"Total Messages: {stats['total_messages']}")
        print(f"Time Range: {stats['time_range']}")
        print("\nTop Projects:")
        for project, count in stats['project_distribution'][:10]:
            print(f"  {project}: {count} sessions")
        print("\nTop Keywords:")
        for keyword, count in stats['top_keywords'][:10]:
            print(f"  {keyword}: {count} occurrences")
        return
    
    # Run the full extraction
    manager.run_extraction(compress=args.compress)


if __name__ == "__main__":
    main()