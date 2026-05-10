import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Export Paste.app clipboard history to readable markdown format
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import shutil

# Core Data epoch (2001-01-01 00:00:00 UTC)
COREDATA_EPOCH = 978307200

def convert_coredata_timestamp(ts):
    """Convert Core Data timestamp to datetime"""
    if ts is None:
        return None
    return datetime.fromtimestamp(ts + COREDATA_EPOCH)

def export_paste_history():
    """Export all Paste.app clipboard history"""
    
    print("🔄 EXPORTING PASTE.APP CLIPBOARD HISTORY")
    print("=" * 70)
    
    # Paths
    db_path = Path.home() / "Library" / "Application Support" / "com.wiheads.paste-setapp" / "db.sqlite"
    output_dir = Path.home() / "Documents" / "paste-clipboard-export"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check database size
    db_size = db_path.stat().st_size / (1024**3)
    print(f"\nDatabase: {db_path.name}")
    print(f"Size: {db_size:.2f} GB")
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get total count
    cursor.execute("SELECT COUNT(*) FROM ZITEMENTITY")
    total_items = cursor.fetchone()[0]
    
    print(f"Total clipboard items: {total_items:,}")
    print(f"Output directory: {output_dir}\n")
    
    # Query all items with details
    query = """
    SELECT 
        Z_PK,
        ZTITLE,
        ZCREATEDAT,
        ZTIMESTAMP,
        ZIDENTIFIER,
        ZCHECKSUM,
        ZRAWTYPE,
        length(ZRAWPREVIEW) as preview_size
    FROM ZITEMENTITY
    ORDER BY ZCREATEDAT DESC
    """
    
    cursor.execute(query)
    items = cursor.fetchall()
    
    # Group by date
    items_by_date = {}
    
    for item in items:
        pk, title, created_ts, timestamp_ts, identifier, checksum, raw_type, preview_size = item
        
        if created_ts:
            created_dt = convert_coredata_timestamp(created_ts)
            date_key = created_dt.strftime('%Y-%m-%d')
            
            if date_key not in items_by_date:
                items_by_date[date_key] = []
            
            items_by_date[date_key].append({
                'id': pk,
                'title': title or '(no title)',
                'created': created_dt,
                'type': raw_type,
                'preview_size': preview_size
            })
    
    print(f"📅 Dates with clipboard activity: {len(items_by_date)}")
    print(f"   Earliest: {min(items_by_date.keys())}")
    print(f"   Latest: {max(items_by_date.keys())}\n")
    
    # Create index file
    index_md = f"""# Paste.app Clipboard History Export

**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Items:** {total_items:,}  
**Date Range:** {min(items_by_date.keys())} to {max(items_by_date.keys())}  
**Days:** {len(items_by_date)}  

---

## 📊 Statistics

```
Total Clipboard Items:  {total_items:,}
Original Database Size: {db_size:.2f} GB
Days with Activity:     {len(items_by_date)}
```

---

## 📁 Files by Date

Each day's clipboard history is in a separate file:

"""
    
    # Create individual day files
    created_files = 0
    total_exported = 0
    
    for date_key in sorted(items_by_date.keys(), reverse=True):
        items_list = items_by_date[date_key]
        
        # Create filename
        filename = f"clipboard_{date_key}.md"
        filepath = output_dir / filename
        
        # Create markdown
        md_content = f"""# Clipboard History - {date_key}

**Items:** {len(items_list)}  
**Date:** {date_key}  

---

"""
        
        for i, item in enumerate(items_list, 1):
            time_str = item['created'].strftime('%H:%M:%S')
            title = item['title'][:200]  # Limit title length
            
            md_content += f"""## Item {i} - {time_str}

**Time:** {time_str}  
**Title:** {title}  
**Type:** {item['type']}  
**Size:** {item['preview_size']} bytes  

---

"""
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        created_files += 1
        total_exported += len(items_list)
        
        # Add to index
        index_md += f"- [{date_key}](./{filename}) - {len(items_list)} items\n"
        
        if created_files % 30 == 0:
            print(f"   ✅ Created {created_files} day files ({total_exported:,} items)...")
    
    # Write index
    with open(output_dir / "INDEX.md", 'w', encoding='utf-8') as f:
        f.write(index_md)
    
    conn.close()
    
    # Calculate output size
    output_size = sum(f.stat().st_size for f in output_dir.glob('*.md')) / (1024**2)
    
    print(f"\n{'='*70}")
    print(f"✅ EXPORT COMPLETE!")
    print(f"{'='*70}")
    print(f"   Files created: {created_files + 1} (including INDEX.md)")
    print(f"   Items exported: {total_exported:,}")
    print(f"   Output size: {output_size:.1f} MB")
    print(f"   Original size: {db_size*1024:.0f} MB")
    print(f"   Compression: {db_size*1024/output_size:.0f}x smaller")
    print(f"\n📁 Location: {output_dir}")

try:
        export_paste_history()
except KeyboardInterrupt:
    logger.info("Execution interrupted by user")
    sys.exit(1)
except Exception as e:
    logger.error(f"An error occurred: {e}", exc_info=True)
    sys.exit(1)