#!/usr/bin/env python3
"""
Convert Cursor AI chat databases to Markdown format
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import html

def extract_chat(db_path):
    """Extract messages from a Cursor chat database"""
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get metadata
        cursor.execute("SELECT value FROM meta WHERE key = '0'")
        meta_row = cursor.fetchone()
        
        if not meta_row:
            return None
        
        # Decode metadata
        meta_hex = meta_row[0]
        meta_json = bytes.fromhex(meta_hex).decode('utf-8')
        meta = json.loads(meta_json)
        
        # Get all messages
        cursor.execute("SELECT id, data FROM blobs ORDER BY id")
        messages = []
        
        for row in cursor.fetchall():
            blob_id, data = row
            
            # Try to parse as JSON
            try:
                msg_json = json.loads(data.decode('utf-8'))
                if isinstance(msg_json, dict) and 'role' in msg_json:
                    messages.append(msg_json)
            except:
                pass
        
        conn.close()
        
        return {
            'meta': meta,
            'messages': messages
        }
    
    except Exception as e:
        print(f"Error processing {db_path}: {e}")
        return None

def format_message_content(content):
    """Extract text from message content (can be string or array)"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
            elif isinstance(item, str):
                text_parts.append(item)
        return '\n'.join(text_parts)
    return str(content)

def chat_to_markdown(chat_data):
    """Convert chat data to markdown format"""
    meta = chat_data['meta']
    messages = chat_data['messages']
    
    # Header
    created_ts = meta.get('createdAt', 0) / 1000
    created_date = datetime.fromtimestamp(created_ts).strftime('%Y-%m-%d %H:%M:%S')
    
    md = f"""# {meta.get('name', 'Unnamed Chat')}

**Created:** {created_date}  
**Mode:** {meta.get('mode', 'default')}  
**Model:** {meta.get('lastUsedModel', 'N/A')}  
**Messages:** {len(messages)}  

---

"""
    
    # Messages
    for i, msg in enumerate(messages, 1):
        role = msg.get('role', 'unknown')
        content = msg.get('content', '')
        
        # Extract text content
        text = format_message_content(content)
        
        # Format based on role
        if role == 'user':
            md += f"## 💬 User (Message {i})\n\n{text}\n\n---\n\n"
        elif role == 'assistant':
            md += f"## 🤖 Assistant (Message {i})\n\n{text}\n\n---\n\n"
        elif role == 'system':
            md += f"## ⚙️ System (Message {i})\n\n{text}\n\n---\n\n"
        else:
            md += f"## {role.title()} (Message {i})\n\n{text}\n\n---\n\n"
    
    return md

def main():
    print("🔄 CONVERTING CURSOR CHATS TO MARKDOWN")
    print("=" * 70)
    
    chats_dir = Path.home() / ".cursor" / "chats"
    output_dir = Path.home() / "Documents" / "cursor-chats-export"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all databases
    db_files = list(chats_dir.rglob("store.db"))
    print(f"\nFound {len(db_files)} chat databases")
    print(f"Output directory: {output_dir}\n")
    
    converted = 0
    failed = 0
    
    for i, db_file in enumerate(db_files, 1):
        chat_data = extract_chat(db_file)
        
        if chat_data and chat_data['messages']:
            # Create filename
            meta = chat_data['meta']
            created_ts = meta.get('createdAt', 0) / 1000
            date_str = datetime.fromtimestamp(created_ts).strftime('%Y%m%d_%H%M%S')
            name = meta.get('name', 'Unnamed').replace(' ', '_').replace('/', '-')
            
            # Limit filename length
            if len(name) > 30:
                name = name[:30]
            
            filename = f"{date_str}_{name}_{converted+1}.md"
            output_path = output_dir / filename
            
            # Convert to markdown
            markdown = chat_to_markdown(chat_data)
            
            # Save
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            
            converted += 1
            
            if converted % 5 == 0:
                print(f"   ✅ Converted {converted}/{len(db_files)} chats...")
        else:
            failed += 1
        
        if i % 10 == 0:
            print(f"   ... processed {i}/{len(db_files)} databases")
    
    print(f"\n{'='*70}")
    print(f"✅ CONVERSION COMPLETE!")
    print(f"{'='*70}")
    print(f"   Converted: {converted} chats")
    print(f"   Failed: {failed}")
    print(f"   Output: {output_dir}")
    print(f"\n💾 Total size: {sum(f.stat().st_size for f in output_dir.glob('*.md')) / (1024**2):.1f} MB")

if __name__ == "__main__":
    main()
