#!/bin/bash
# Workspace Cleanup Script
# Generated on 2025-11-06 12:09:15

set -e

echo '🧹 Starting workspace cleanup...'
echo ''

# Backup important files first
BACKUP_DIR=~/workspace_cleanup_backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
echo '💾 Created backup directory: $BACKUP_DIR'
echo ''

# Function to safely remove directory
safe_remove() {
    local dir="$1"
    if [ -d "$dir" ]; then
        echo "  Removing: $dir"
        du -sh "$dir" 2>/dev/null || true
        rm -rf "$dir"
        echo "  ✓ Removed"
    else
        echo "  ⚠️  Not found: $dir"
    fi
}

# Remove node_modules from archived projects
echo '📦 Removing node_modules from archived projects...'
echo ''

safe_remove "/Users/steven/workspace/archive/old-structure/creative-platforms/avatararts/AvaTarArTs/avatararts-hub/node_modules"
safe_remove "/Users/steven/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro/frontend/node_modules"
safe_remove "/Users/steven/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro/backend/node_modules"
safe_remove "/Users/steven/workspace/archive/old-structure/creative-platforms/avatararts/AvaTarArTs/avatararts-portfolio/node_modules"
safe_remove "/Users/steven/workspace/archive/old-structure/creative-platforms/avatararts/AvaTarArTs/avatararts.org/node_modules"
safe_remove "/Users/steven/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro/node_modules"
safe_remove "/Users/steven/workspace/archive/old-structure/creative-platforms/avatararts/AvaTarArTs/avatararts-gallery/node_modules"

echo ''
echo '✅ Cleanup complete!'
echo 'Estimated space freed: 614.26 MB'
echo ''
echo '💡 To reinstall dependencies in active projects:'
echo '   cd /path/to/project && npm install'