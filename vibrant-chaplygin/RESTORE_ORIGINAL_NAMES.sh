#!/bin/bash
# RESTORE ORIGINAL NAMES
# Uses RENAME_BACKUP_MAPPING.csv to undo all renames

cd ~/Documents/pythons

echo "🔄 RESTORING ORIGINAL FILENAMES"
echo "================================"
echo ""

# Read CSV and reverse the moves
tail -n +2 RENAME_BACKUP_MAPPING.csv | while IFS=, read -r original new purpose flatten; do
    # Remove quotes if present
    original=$(echo "$original" | tr -d '"')
    new=$(echo "$new" | tr -d '"')

    if [ -f "$new" ]; then
        echo "Restoring: $new → $original"
        mv "$new" "$original"
    fi
done

echo ""
echo "✅ Restoration complete!"
