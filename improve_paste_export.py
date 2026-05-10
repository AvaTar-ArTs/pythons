#!/usr/bin/env python3
"""
Enhanced Paste.app export - Extract ACTUAL clipboard content
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import plistlib
import re

COREDATA_EPOCH = 978307200

def convert_coredata_timestamp(ts):
    if ts is None:
        return None
    return datetime.fromtimestamp(ts + COREDATA_EPOCH)

def extract_text_from_pasteboard(blob_data):
    """Extract text content from pasteboard items blob"""
    if not blob_data:
        return None
    
    try:
        # Try to parse as plist
        plist = plistlib.loads(blob_data)
        
        # Look for text content in various formats
        if isinstance(plist, list):
            for item in plist:
                if isinstance(item, dict):
                    # Check for public.utf8-plain-text
                    if 'public.utf8-plain-text' in item:
                        text_data = item['public.utf8-plain-text']
                        if isinstance(text_data, bytes):
                            return text_data.decode('utf-8', errors='ignore')
                        elif isinstance(text_data, str):
                            return text_data
                    
                    # Check for public.plain-text
                    if 'public.plain-text' in item:
                        text_data = item['public.plain-text']
                        if isinstance(text_data, bytes):
                            return text_data.decode('utf-8', errors='ignore')
                        elif isinstance(text_data, str):
                            return text_data
                    
                    # Check for NSStringPboardType
                    if 'NSStringPboardType' in item:
                        text_data = item['NSStringPboardType']
                        if isinstance(text_data, bytes):
                            return text_data.decode('utf-8', errors='ignore')
                        elif isinstance(text_data, str):
                            return text_data
        
        return None
    
    except Exception as e:
        return None

def export_with_content():
    print("🔄 EXTRACTING ACTUAL CLIPBOARD CONTENT")
    print("=" * 70)
    
    db_path = Path.home() / "Library" / "Application Support" / "com.wiheads.paste-setapp" / "db.sqlite"
    output_dir = Path.home() / "Documents" / "paste-clipboard-FULL-export"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nDatabase: {db_path.name}")
    print(f"Output: {output_dir}\n")
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get items with their data
    query = """
    SELECT 
        i.Z_PK,
        i.ZTITLE,
        i.ZCREATEDAT,
        i.ZRAWTYPE,
        i.ZIDENTIFIER,
        length(i.ZRAWPREVIEW) as preview_size,
        d.ZRAWPASTEBOARDITEMS
    FROM ZITEMENTITY i
    LEFT JOIN ZITEMDATAENTITY d ON d.ZITEM = i.Z_PK
    ORDER BY i.ZCREATEDAT DESC
    """
    
    cursor.execute(query)
    total_items = cursor.rowcount
    
    print("Processing items with actual content...")
    
    items_by_date = {}
    extracted_count = 0
    text_count = 0
    
    for row in cursor.fetchall():
        pk, title, created_ts, raw_type, identifier, preview_size, raw_pasteboard = row
        
        if not created_ts:
            continue
        
        created_dt = convert_coredata_timestamp(created_ts)
        date_key = created_dt.strftime('%Y-%m-%d')
        
        # Extract actual content
        actual_content = None
        if raw_pasteboard:
            actual_content = extract_text_from_pasteboard(raw_pasteboard)
            if actual_content:
                text_count += 1
        
        if date_key not in items_by_date:
            items_by_date[date_key] = []
        
        items_by_date[date_key].append({
            'id': pk,
            'title': title or '(no title)',
            'created': created_dt,
            'type': raw_type,
            'content': actual_content,
            'has_content': actual_content is not None
        })
        
        extracted_count += 1
        
        if extracted_count % 1000 == 0:
            print(f"   ... processed {extracted_count} items ({text_count} with text)")
    
    conn.close()
    
    print(f"\n✅ Processed {extracted_count} items")
    print(f"   {text_count} items have extractable text content ({100*text_count/extracted_count:.1f}%)")
    
    # Create enhanced daily files
    print("\n📝 Creating enhanced daily files...")
    
    created_files = 0
    
    for date_key in sorted(items_by_date.keys(), reverse=True):
        items_list = items_by_date[date_key]
        
        filename = f"clipboard_{date_key}.md"
        filepath = output_dir / filename
        
        md_content = f"""# Clipboard History - {date_key}

**Items:** {len(items_list)}  
**Items with text:** {sum(1 for i in items_list if i['has_content'])}  
**Date:** {date_key}  

---

"""
        
        for i, item in enumerate(items_list, 1):
            time_str = item['created'].strftime('%H:%M:%S')
            title = item['title'][:100] if item['title'] else '(no title)'
            
            md_content += f"""## Item {i} - {time_str}

**Time:** {time_str}  
**Title:** {title}  
**Type:** {item['type']}  

"""
            
            if item['content']:
                # Limit content length for readability
                content = item['content']
                if len(content) > 1000:
                    content = content[:1000] + f"\n\n... [truncated, {len(item['content'])} total chars]"
                
                md_content += f"""**Content:**
```
{content}
```

"""
            else:
                md_content += "**Content:** _(not extractable - may be image/file)_\n\n"
            
            md_content += "---\n\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        created_files += 1
        
        if created_files % 30 == 0:
            print(f"   ... created {created_files} files")
    
    # Create enhanced index
    index_md = f"""# Paste.app Clipboard History - FULL EXPORT

**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Items:** {extracted_count:,}  
**Items with Text:** {text_count:,} ({100*text_count/extracted_count:.1f}%)  
**Date Range:** {min(items_by_date.keys())} to {max(items_by_date.keys())}  
**Days:** {len(items_by_date)}  

---

## 🎉 ENHANCED EXPORT

This export includes **ACTUAL CLIPBOARD CONTENT** extracted from the database!

### What's Included:
- ✅ Full text content (where available)
- ✅ Timestamps and metadata
- ✅ Code snippets
- ✅ URLs and links
- ✅ Commands and text

### What's NOT Included:
- ❌ Images (binary data)
- ❌ Files
- ❌ Rich formatting

---

## 📊 Statistics

```
Total Items:     {extracted_count:,}
With Text:       {text_count:,} ({100*text_count/extracted_count:.1f}%)
Days:            {len(items_by_date)}
```

---

## 📁 Files by Date

"""
    
    for date_key in sorted(items_by_date.keys(), reverse=True):
        items_list = items_by_date[date_key]
        with_text = sum(1 for i in items_list if i['has_content'])
        index_md += f"- [{date_key}](./{filename}) - {len(items_list)} items ({with_text} with text)\n"
    
    with open(output_dir / "INDEX.md", 'w', encoding='utf-8') as f:
        f.write(index_md)
    
    # Calculate final size
    output_size = sum(f.stat().st_size for f in output_dir.glob('*.md')) / (1024**2)
    
    print(f"\n{'='*70}")
    print(f"✅ ENHANCED EXPORT COMPLETE!")
    print(f"{'='*70}")
    print(f"   Files created: {created_files + 1}")
    print(f"   Items with text: {text_count:,} / {extracted_count:,}")
    print(f"   Output size: {output_size:.1f} MB")
    print(f"   Location: {output_dir}")

if __name__ == "__main__":
    export_with_content()
