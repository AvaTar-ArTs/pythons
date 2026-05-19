#!/usr/bin/env python3
"""
Ultra-clean Script to extract unique Qwen conversations
Removes duplicates and repetitive entries
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re
import sqlite3
from difflib import SequenceMatcher


class UltraCleanQwenManager:
    def __init__(self):
        self.base_dir = Path.home() / ".qwen" / "projects"
        self.db_path = Path.home() / ".ultra_clean_qwen_conversations.db"
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for storing unique conversation data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                project_name TEXT,
                start_time TEXT,
                end_time TEXT,
                message_count INTEGER,
                duration_seconds REAL
            )
        ''')
        
        # Create unique messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unique_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                message_type TEXT,
                content TEXT,
                content_hash TEXT UNIQUE,
                FOREIGN KEY (session_id) REFERENCES conversations (session_id)
            )
        ''')
        
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
                                'project_name': entry.get('cwd', 'unknown')
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
    
    def is_duplicate_content(self, content, existing_contents, threshold=0.85):
        """Check if content is a duplicate of existing content."""
        content_lower = content.lower().strip()
        
        # Check for exact matches first
        if content_lower in existing_contents:
            return True
        
        # Check for near-duplicates using similarity
        for existing in existing_contents:
            similarity = SequenceMatcher(None, content_lower, existing).ratio()
            if similarity > threshold:
                return True
        
        return False
    
    def store_unique_conversations(self, conversation_data, session_id, project_name):
        """Store only unique conversation data in the SQLite database."""
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
            (session_id, project_name, start_time, end_time, message_count, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            project_name,
            conversation_data[0].get('timestamp', ''),
            conversation_data[-1].get('timestamp', ''),
            len(conversation_data),
            duration_seconds
        ))
        
        # Get existing content hashes to check for duplicates
        cursor.execute('SELECT content FROM unique_messages')
        existing_contents = [row[0].lower().strip() for row in cursor.fetchall()]
        
        # Insert only unique messages
        unique_count = 0
        for entry in conversation_data:
            content = entry.get('content', '').strip()
            if content and not self.is_duplicate_content(content, existing_contents):
                try:
                    cursor.execute('''
                        INSERT INTO unique_messages (session_id, timestamp, message_type, content, content_hash)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        session_id,
                        entry.get('timestamp', ''),
                        entry.get('type', ''),
                        content,
                        hash(content)
                    ))
                    existing_contents.append(content.lower())
                    unique_count += 1
                except sqlite3.IntegrityError:
                    # Skip if content hash already exists
                    continue
        
        conn.commit()
        conn.close()
        
        return unique_count
    
    def generate_ultra_clean_html_report(self):
        """Generate an ultra-clean HTML report focusing only on unique conversations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all sessions ordered by start time
        cursor.execute('''
            SELECT session_id, project_name, message_count, start_time, end_time
            FROM conversations
            ORDER BY start_time
        ''')
        sessions = cursor.fetchall()
        
        html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qwen Conversations - Ultra Clean Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #ffffff;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .summary {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 25px;
            border-left: 4px solid #3498db;
        }
        .session {
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            overflow: hidden;
        }
        .session-header {
            background-color: #f1f3f4;
            padding: 12px 15px;
            font-weight: bold;
            border-bottom: 1px solid #dee2e6;
        }
        .message {
            padding: 12px 15px;
            border-bottom: 1px solid #f1f3f4;
        }
        .message:last-child {
            border-bottom: none;
        }
        .user {
            background-color: #e3f2fd;
        }
        .assistant {
            background-color: #f3e5f5;
        }
        .system {
            background-color: #e8f5e8;
            font-size: 0.9em;
        }
        .timestamp {
            font-size: 0.85em;
            color: #6c757d;
            margin-bottom: 5px;
        }
        .content {
            white-space: pre-wrap;
        }
        .no-messages {
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Qwen Conversations - Ultra Clean Report</h1>
        <div class="summary">
            <p><strong>Total Unique Sessions:</strong> ''' + str(len(sessions)) + '''</p>
            <p><strong>Generated:</strong> ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
            <p><em>This report contains only unique, non-duplicate conversations.</em></p>
        </div>'''
        
        for session in sessions:
            session_id, project_name, msg_count, start_time, end_time = session
            
            html += f'''
        <div class="session">
            <div class="session-header">
                Session: {session_id[:12]}... | Project: {project_name} | {msg_count} messages | {start_time[:19] if start_time else 'N/A'} to {end_time[:19] if end_time else 'N/A'}
            </div>'''
            
            # Get unique messages for this session
            cursor.execute('''
                SELECT timestamp, message_type, content
                FROM unique_messages
                WHERE session_id = ?
                ORDER BY timestamp
            ''', (session_id,))
            
            messages = cursor.fetchall()
            
            if messages:
                for msg in messages:
                    timestamp, msg_type, content = msg
                    formatted_time = timestamp[:19] if timestamp else 'Unknown'
                    
                    # Determine CSS class based on message type
                    css_class = msg_type.lower().replace(' ', '-')
                    if css_class == 'tool-result':
                        css_class = 'system'
                    
                    html += f'''
            <div class="message {css_class}">
                <div class="timestamp">[{formatted_time}] {msg_type.upper()}:</div>
                <div class="content">{content.replace(chr(10), '<br>')}</div>
            </div>'''
            else:
                html += '<div class="no-messages">No unique messages found for this session</div>'
            
            html += '''
        </div>'''
        
        html += '''
    </div>
</body>
</html>'''
        
        conn.close()
        return html
    
    def run_extraction(self):
        """Main function to extract unique Qwen conversations and generate clean HTML report."""
        if not self.base_dir.exists():
            print(f"Directory {self.base_dir} does not exist.")
            return
        
        # Find all project directories
        project_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]
        
        total_unique_messages = 0
        for project_dir in project_dirs:
            project_name = project_dir.name
            chats_dir = project_dir / "chats"
            
            if not chats_dir.exists():
                continue
                
            # Process all JSONL files in the chats directory
            jsonl_files = list(chats_dir.glob("*.jsonl"))
            
            for jsonl_file in jsonl_files:
                print(f"Processing {jsonl_file}")
                
                try:
                    conversation_data = self.extract_conversations_from_jsonl(jsonl_file)
                    
                    if conversation_data:
                        session_id = conversation_data[0].get('session_id', 'unknown')
                        
                        # Store only unique conversations in database
                        unique_count = self.store_unique_conversations(conversation_data, session_id, project_name)
                        total_unique_messages += unique_count
                        
                except Exception as e:
                    print(f"Error processing {jsonl_file}: {str(e)}")
        
        # Generate the ultra-clean HTML report
        html_report = self.generate_ultra_clean_html_report()
        
        # Write the HTML report to a file
        output_file = Path.home() / "qwen_conversations_ultra_clean.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"\nUltra clean HTML export completed! Conversations saved to: {output_file}")
        
        # Get summary stats
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_sessions = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM unique_messages')
        total_unique_messages_db = cursor.fetchone()[0]
        conn.close()
        
        print(f"Total unique sessions in report: {total_sessions}")
        print(f"Total unique messages in report: {total_unique_messages_db}")


def main():
    manager = UltraCleanQwenManager()
    manager.run_extraction()


if __name__ == "__main__":
    main()