#!/usr/bin/env python3
"""
Script to extract Qwen conversations from .qwen project directories and generate an HTML report
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re
import hashlib


def extract_conversations_from_jsonl(jsonl_file_path):
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


def format_content(content):
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


def escape_html(text):
    """Escape HTML special characters."""
    if not isinstance(text, str):
        text = str(text)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")


def format_conversation_as_html(conversation_data, session_id, project_name):
    """Format conversation data into HTML."""
    if not conversation_data:
        return ""
    
    html = []
    html.append('<div class="conversation-session">')
    html.append(f'<h3>Session: {escape_html(session_id)}</h3>')
    html.append(f'<p><strong>Project:</strong> {escape_html(project_name)}</p>')
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
        html.append(f'<div class="message-header">[{escape_html(formatted_time)}] {escape_html(formatted_msg_type)}:</div>')
        
        # Format content for readability
        formatted_content = format_content(content)
        html.append(f'<div class="message-content">{escape_html(formatted_content).replace(chr(10), "<br/>")}</div>')
        html.append('</div>')  # Close message div
    
    html.append('</div>')  # Close messages div
    html.append('</div>')  # Close conversation-session div
    
    return "\n".join(html)


def generate_html_report(session_info, all_conversations_html):
    """Generate the complete HTML report."""
    # Generate a hash of the content to determine if we need to update
    content_hash = hashlib.md5((str(session_info) + all_conversations_html).encode()).hexdigest()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Qwen Conversation History</title>
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Qwen Conversation History</h1>
        <div class="metadata">
            <p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total conversations:</strong> {len(session_info)}</p>
            <p><strong>Time range:</strong> {session_info[0]['start_time'][:19] if session_info else 'N/A'} to {session_info[-1]['end_time'][:19] if session_info else 'N/A'}</p>
        </div>
        
        <div class="stats">
            <h3>Conversation Summary</h3>
            <table class="summary-table">
                <thead>
                    <tr>
                        <th>Session ID</th>
                        <th>Project</th>
                        <th>Messages</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                    </tr>
                </thead>
                <tbody>"""
    
    for session in session_info:
        start_time = session['start_time'][:19] if len(session['start_time']) > 19 else session['start_time']  # Truncate ISO time
        end_time = session['end_time'][:19] if len(session['end_time']) > 19 else session['end_time']
        html += f"""
                    <tr>
                        <td>{escape_html(session['session_id'][:19])}</td>
                        <td>{escape_html(session['project_name'])}</td>
                        <td>{session['messages_count']}</td>
                        <td>{escape_html(start_time)}</td>
                        <td>{escape_html(end_time)}</td>
                    </tr>"""
    
    html += """
                </tbody>
            </table>
        </div>
        
        <div class="conversations">
            <h2>Detailed Conversations</h2>
            """ + all_conversations_html + """
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """Main function to extract all Qwen conversations and generate HTML report."""
    base_dir = Path.home() / ".qwen" / "projects"
    
    if not base_dir.exists():
        print(f"Directory {base_dir} does not exist.")
        return
    
    # Find all project directories
    project_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
    
    all_conversations_html = []
    session_info = []  # Store session metadata for summary
    
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
                conversation_data = extract_conversations_from_jsonl(jsonl_file)
                
                if conversation_data:
                    session_id = conversation_data[0].get('session_id', 'unknown')
                    formatted_conv_html = format_conversation_as_html(
                        conversation_data, 
                        session_id,
                        project_name
                    )
                    all_conversations_html.append(formatted_conv_html)
                    
                    # Store session info for summary
                    session_info.append({
                        'session_id': session_id,
                        'project_name': project_name,
                        'messages_count': len(conversation_data),
                        'start_time': conversation_data[0].get('timestamp', 'Unknown'),
                        'end_time': conversation_data[-1].get('timestamp', 'Unknown'),
                        'file_path': str(jsonl_file)
                    })
                    
            except Exception as e:
                print(f"Error processing {jsonl_file}: {str(e)}")
    
    # Sort sessions by start time for chronological order
    def sort_sessions_by_time(session):
        start_time = session.get('start_time')
        if start_time != 'Unknown':
            try:
                return datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            except ValueError:
                return datetime.min
        return datetime.min
    
    session_info.sort(key=sort_sessions_by_time)
    
    # Generate the HTML report
    html_report = generate_html_report(session_info, "\n".join(all_conversations_html))
    
    # Write the HTML report to a file
    output_file = Path.home() / "qwen_conversations_export.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"\nHTML export completed! Conversations saved to: {output_file}")
    print(f"Total conversations extracted: {len(all_conversations_html)}")
    print(f"Time range: {session_info[0]['start_time'][:19] if session_info else 'N/A'} to {session_info[-1]['end_time'][:19] if session_info else 'N/A'}")


if __name__ == "__main__":
    main()