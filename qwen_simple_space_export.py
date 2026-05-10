#!/usr/bin/env python3
"""
Simple Qwen Conversation Manager - Portable Export
Consolidated tool for managing Qwen conversations in one clean space
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sqlite3


class SimpleQwenManager:
    def __init__(self):
        self.base_dir = Path.home() / ".qwen" / "projects"
        self.db_path = Path.home() / ".simple_qwen.db"
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for storing conversation data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                project_name TEXT,
                start_time TEXT,
                end_time TEXT,
                message_count INTEGER
            )
        ''')
        
        # Create messages table with content hash to prevent duplicates
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
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
    
    def extract_and_store(self):
        """Extract conversations and store them in the database."""
        if not self.base_dir.exists():
            print(f"Directory {self.base_dir} does not exist.")
            return
        
        # Find all project directories
        project_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]
        
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
                    self.process_jsonl_file(jsonl_file, project_name)
                except Exception as e:
                    print(f"Error processing {jsonl_file}: {str(e)}")
    
    def process_jsonl_file(self, jsonl_file, project_name):
        """Process a single JSONL file and store its content."""
        conversation = []
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
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
                                'session_id': entry.get('sessionId', 'unknown')
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
        
        if conversation:
            session_id = conversation[0]['session_id']
            
            # Store in database
            self.store_conversation(conversation, session_id, project_name)
    
    def store_conversation(self, conversation_data, session_id, project_name):
        """Store conversation data in the SQLite database."""
        if not conversation_data:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert or update conversation metadata
        cursor.execute('''
            INSERT OR REPLACE INTO conversations 
            (session_id, project_name, start_time, end_time, message_count)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            session_id,
            project_name,
            conversation_data[0].get('timestamp', ''),
            conversation_data[-1].get('timestamp', ''),
            len(conversation_data)
        ))
        
        # Insert messages, ignoring duplicates based on content hash
        for entry in conversation_data:
            content = entry.get('content', '').strip()
            content_hash = hash(content)  # Simple hash to detect duplicates
            
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO messages (session_id, timestamp, message_type, content, content_hash)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    entry.get('timestamp', ''),
                    entry.get('type', ''),
                    content,
                    content_hash
                ))
            except sqlite3.IntegrityError:
                # Skip if content hash already exists
                continue
        
        conn.commit()
        conn.close()
    
    def generate_report(self):
        """Generate a simple HTML report."""
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
    <title>Qwen Conversations - Simple Space</title>
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
            max-width: 1000px;
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
            margin-bottom: 25px;
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
        }
        .tool-result {
            background-color: #fff3e0;
        }
        .timestamp {
            font-size: 0.85em;
            color: #6c757d;
            margin-bottom: 5px;
        }
        .content {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Qwen Conversations - Simple Space</h1>
        <div class="summary">
            <p><strong>Total Sessions:</strong> ''' + str(len(sessions)) + '''</p>
            <p><strong>Generated:</strong> ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
        </div>'''
        
        for session in sessions:
            session_id, project_name, msg_count, start_time, end_time = session
            
            html += f'''
        <div class="session">
            <div class="session-header">
                Session: {session_id[:12]}... | Project: {project_name} | {msg_count} messages
            </div>'''
            
            # Get messages for this session
            cursor.execute('''
                SELECT timestamp, message_type, content
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp
            ''', (session_id,))
            
            messages = cursor.fetchall()
            
            for msg in messages:
                timestamp, msg_type, content = msg
                formatted_time = timestamp[:19] if timestamp else 'Unknown'
                
                # Determine CSS class based on message type
                css_class = msg_type.lower().replace(' ', '-')
                if css_class == 'tool-result':
                    css_class = 'tool-result'
                
                html += f'''
            <div class="message {css_class}">
                <div class="timestamp">[{formatted_time}] {msg_type.upper()}:</div>
                <div class="content">{content.replace(chr(10), '<br>')}</div>
            </div>'''
            
            html += '''
        </div>'''
        
        html += '''
    </div>
</body>
</html>'''
        
        conn.close()
        return html
    
    def run(self):
        """Run the complete process."""
        print("Extracting and storing Qwen conversations...")
        self.extract_and_store()
        
        print("Generating report...")
        html_report = self.generate_report()
        
        # Write the HTML report to a file
        output_file = Path.home() / "qwen_simple_space.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"\nSimple Qwen space created: {output_file}")
        
        # Get summary stats
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_sessions = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_messages = cursor.fetchone()[0]
        conn.close()
        
        print(f"Total sessions: {total_sessions}")
        print(f"Total messages: {total_messages}")


def main():
    manager = SimpleQwenManager()
    manager.run()


if __name__ == "__main__":
    main()