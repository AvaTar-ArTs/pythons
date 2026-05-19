#!/usr/bin/env python3
"""
Clean Script to extract Qwen conversations with minimal overhead
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re
import sqlite3
from collections import Counter


class CleanQwenManager:
    def __init__(self):
        self.base_dir = Path.home() / ".qwen" / "projects"
        self.db_path = Path.home() / ".clean_qwen_conversations.db"
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
                message_count INTEGER,
                duration_seconds REAL
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
    
    def store_in_database(self, conversation_data, session_id, project_name):
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
    
    def generate_clean_html_report(self):
        """Generate a clean HTML report focusing on conversations."""
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
    <title>Qwen Conversations - Clean Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        .session {
            border: 1px solid #eee;
            margin: 15px 0;
            padding: 15px;
            border-radius: 4px;
        }
        .session-header {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .message {
            margin: 10px 0;
            padding: 8px;
            border-radius: 3px;
        }
        .user {
            background-color: #e3f2fd;
            border-left: 3px solid #2196f3;
            padding-left: 10px;
        }
        .assistant {
            background-color: #f3e5f5;
            border-left: 3px solid #9c27b0;
            padding-left: 10px;
        }
        .system {
            background-color: #e8f5e8;
            border-left: 3px solid #4caf50;
            padding-left: 10px;
        }
        .timestamp {
            font-size: 0.8em;
            color: #666;
        }
        .summary {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Qwen Conversations - Clean Report</h1>
        <div class="summary">
            <p><strong>Total Sessions:</strong> ''' + str(len(sessions)) + '''</p>
            <p><strong>Generated:</strong> ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
        </div>'''
        
        for session in sessions:
            session_id, project_name, msg_count, start_time, end_time = session
            
            html += f'''
        <div class="session">
            <div class="session-header">
                <strong>Session:</strong> {session_id[:12]}...<br>
                <strong>Project:</strong> {project_name}<br>
                <strong>Messages:</strong> {msg_count} | <strong>Time:</strong> {start_time[:19] if start_time else 'N/A'} to {end_time[:19] if end_time else 'N/A'}
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
                    css_class = 'system'
                
                html += f'''
            <div class="message {css_class}">
                <div class="timestamp">[{formatted_time}] {msg_type.upper()}:</div>
                <div>{content.replace(chr(10), '<br>')}</div>
            </div>'''
            
            html += '''
        </div>'''
        
        html += '''
    </div>
</body>
</html>'''
        
        conn.close()
        return html
    
    def run_extraction(self):
        """Main function to extract all Qwen conversations and generate clean HTML report."""
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
                    conversation_data = self.extract_conversations_from_jsonl(jsonl_file)
                    
                    if conversation_data:
                        session_id = conversation_data[0].get('session_id', 'unknown')
                        
                        # Store in database
                        self.store_in_database(conversation_data, session_id, project_name)
                        
                except Exception as e:
                    print(f"Error processing {jsonl_file}: {str(e)}")
        
        # Generate the clean HTML report
        html_report = self.generate_clean_html_report()
        
        # Write the HTML report to a file
        output_file = Path.home() / "qwen_conversations_clean.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"\nClean HTML export completed! Conversations saved to: {output_file}")
        
        # Get summary stats
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM conversations')
        total_sessions = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_messages = cursor.fetchone()[0]
        conn.close()
        
        print(f"Total sessions in report: {total_sessions}")
        print(f"Total messages in report: {total_messages}")


def main():
    manager = CleanQwenManager()
    manager.run_extraction()


if __name__ == "__main__":
    main()