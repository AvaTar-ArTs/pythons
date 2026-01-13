#!/bin/bash
# Project Consolidation Script
# Generated on 2025-11-06 12:10:31

set -e

echo '📦 Starting project consolidation...'
echo ''

# Create backup
BACKUP_DIR=~/project_consolidation_backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
echo '💾 Backup directory: $BACKUP_DIR'
echo ''

# Archive duplicate projects
ARCHIVE_DIR=~/consolidated_archives_$(date +%Y%m%d)
mkdir -p $ARCHIVE_DIR

# Consolidation 1: heavenlyhands
echo 'Processing: heavenlyhands'
echo '  Keeping: workspace/heavenlyhands-complete'

# Archive: workspace/archive/old-structure/projects/heavenlyhands
if [ -d "~/workspace/archive/old-structure/projects/heavenlyhands" ]; then
    echo '  Archiving: workspace/archive/old-structure/projects/heavenlyhands'
    tar -czf "$ARCHIVE_DIR/heavenlyhands.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/projects/heavenlyhands")" "$(basename "~/workspace/archive/old-structure/projects/heavenlyhands")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/projects/heavenlyhands"
fi

# Consolidation 2: cleanconnect
echo 'Processing: cleanconnect'
echo '  Keeping: workspace/cleanconnect-complete'

# Archive: workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro
if [ -d "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro" ]; then
    echo '  Archiving: workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro'
    tar -czf "$ARCHIVE_DIR/cleanconnect-pro.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro")" "$(basename "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro"
fi

# Consolidation 3: ai-recipe-generator
echo 'Processing: ai-recipe-generator'
echo '  Keeping: workspace/passive-income-empire/ai-recipe-generator'

# Archive: workspace/archive/old-structure/revenue-projects/passive-income/passive-income-empire/ai-recipe-generator
if [ -d "~/workspace/archive/old-structure/revenue-projects/passive-income/passive-income-empire/ai-recipe-generator" ]; then
    echo '  Archiving: workspace/archive/old-structure/revenue-projects/passive-income/passive-income-empire/ai-recipe-generator'
    tar -czf "$ARCHIVE_DIR/ai-recipe-generator.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/revenue-projects/passive-income/passive-income-empire/ai-recipe-generator")" "$(basename "~/workspace/archive/old-structure/revenue-projects/passive-income/passive-income-empire/ai-recipe-generator")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/revenue-projects/passive-income/passive-income-empire/ai-recipe-generator"
fi

# Archive: workspace/archive/old-structure/projects/passive-income/ai-recipe-generator
if [ -d "~/workspace/archive/old-structure/projects/passive-income/ai-recipe-generator" ]; then
    echo '  Archiving: workspace/archive/old-structure/projects/passive-income/ai-recipe-generator'
    tar -czf "$ARCHIVE_DIR/ai-recipe-generator.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/projects/passive-income/ai-recipe-generator")" "$(basename "~/workspace/archive/old-structure/projects/passive-income/ai-recipe-generator")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/projects/passive-income/ai-recipe-generator"
fi

# Consolidation 4: dall-e
echo 'Processing: dall-e'
echo '  Keeping: workspace/avatararts-complete/DaLL-E'

# Archive: workspace/archive/reference-files/avatararts-steven-docs/DaLL-E
if [ -d "~/workspace/archive/reference-files/avatararts-steven-docs/DaLL-E" ]; then
    echo '  Archiving: workspace/archive/reference-files/avatararts-steven-docs/DaLL-E'
    tar -czf "$ARCHIVE_DIR/DaLL-E.tar.gz" -C "$(dirname "~/workspace/archive/reference-files/avatararts-steven-docs/DaLL-E")" "$(basename "~/workspace/archive/reference-files/avatararts-steven-docs/DaLL-E")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/reference-files/avatararts-steven-docs/DaLL-E"
fi

# Consolidation 5: cleanconnect
echo 'Processing: cleanconnect'
echo '  Keeping: workspace/heavenlyhands-complete/heavenlyHands/cleanconnect-pro'

# Archive: workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro
if [ -d "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro" ]; then
    echo '  Archiving: workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro'
    tar -czf "$ARCHIVE_DIR/cleanconnect-pro.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro")" "$(basename "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro"
fi

# Archive: workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro-enhanced
if [ -d "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro-enhanced" ]; then
    echo '  Archiving: workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro-enhanced'
    tar -czf "$ARCHIVE_DIR/cleanconnect-pro-enhanced.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro-enhanced")" "$(basename "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro-enhanced")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/revenue-projects/heavenlyhands-archived/heavenlyHands/cleanconnect-pro-enhanced"
fi

# Archive: workspace/archive/old-structure/revenue-projects/heavenlyhands/heavenlyHands/cleanconnect-pro-enhanced
if [ -d "~/workspace/archive/old-structure/revenue-projects/heavenlyhands/heavenlyHands/cleanconnect-pro-enhanced" ]; then
    echo '  Archiving: workspace/archive/old-structure/revenue-projects/heavenlyhands/heavenlyHands/cleanconnect-pro-enhanced'
    tar -czf "$ARCHIVE_DIR/cleanconnect-pro-enhanced.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/revenue-projects/heavenlyhands/heavenlyHands/cleanconnect-pro-enhanced")" "$(basename "~/workspace/archive/old-structure/revenue-projects/heavenlyhands/heavenlyHands/cleanconnect-pro-enhanced")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/revenue-projects/heavenlyhands/heavenlyHands/cleanconnect-pro-enhanced"
fi

# Archive: workspace/archive/old-structure/revenue-projects/cleanconnect/cleanconnect-pro
if [ -d "~/workspace/archive/old-structure/revenue-projects/cleanconnect/cleanconnect-pro" ]; then
    echo '  Archiving: workspace/archive/old-structure/revenue-projects/cleanconnect/cleanconnect-pro'
    tar -czf "$ARCHIVE_DIR/cleanconnect-pro.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/revenue-projects/cleanconnect/cleanconnect-pro")" "$(basename "~/workspace/archive/old-structure/revenue-projects/cleanconnect/cleanconnect-pro")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/revenue-projects/cleanconnect/cleanconnect-pro"
fi

# Archive: workspace/archive/old-structure/projects/heavenlyhands/cleanconnect-pro-enhanced
if [ -d "~/workspace/archive/old-structure/projects/heavenlyhands/cleanconnect-pro-enhanced" ]; then
    echo '  Archiving: workspace/archive/old-structure/projects/heavenlyhands/cleanconnect-pro-enhanced'
    tar -czf "$ARCHIVE_DIR/cleanconnect-pro-enhanced.tar.gz" -C "$(dirname "~/workspace/archive/old-structure/projects/heavenlyhands/cleanconnect-pro-enhanced")" "$(basename "~/workspace/archive/old-structure/projects/heavenlyhands/cleanconnect-pro-enhanced")"
    # Uncomment to delete after archiving:
    # rm -rf "~/workspace/archive/old-structure/projects/heavenlyhands/cleanconnect-pro-enhanced"
fi

echo ''
echo '✅ Consolidation complete!'
echo 'Archives saved to: $ARCHIVE_DIR'
echo ''
echo '💡 Review the archives, then uncomment the rm -rf lines to delete originals'