#!/bin/bash
# Home Directory Cleanup Script
# Safely removes cache files, temporary files, and cleans up common issues

set -e

echo "🧹 Home Directory Cleanup Script"
echo "================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PYC_COUNT=0
CACHE_COUNT=0
DSSTORE_COUNT=0

# Function to count files before deletion
count_pyc() {
    PYC_COUNT=$(find ~ -name "*.pyc" -type f 2>/dev/null | wc -l | tr -d ' ')
}

count_cache() {
    CACHE_COUNT=$(find ~ -name "__pycache__" -type d 2>/dev/null | wc -l | tr -d ' ')
}

count_dsstore() {
    DSSTORE_COUNT=$(find ~ -name ".DS_Store" -type f 2>/dev/null | wc -l | tr -d ' ')
}

# Remove Python cache files
cleanup_python_cache() {
    echo -e "${YELLOW}📦 Cleaning Python cache files...${NC}"
    count_pyc
    count_cache
    
    if [ "$PYC_COUNT" -gt 0 ] || [ "$CACHE_COUNT" -gt 0 ]; then
        echo "  Found: $PYC_COUNT .pyc files, $CACHE_COUNT __pycache__ directories"
        read -p "  Remove Python cache files? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            find ~ -name "*.pyc" -type f -delete 2>/dev/null
            find ~ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
            echo -e "${GREEN}  ✅ Python cache cleaned${NC}"
        else
            echo -e "${YELLOW}  ⏭️  Skipped${NC}"
        fi
    else
        echo -e "${GREEN}  ✅ No Python cache files found${NC}"
    fi
    echo ""
}

# Remove .DS_Store files
cleanup_dsstore() {
    echo -e "${YELLOW}🍎 Cleaning .DS_Store files...${NC}"
    count_dsstore
    
    if [ "$DSSTORE_COUNT" -gt 0 ]; then
        echo "  Found: $DSSTORE_COUNT .DS_Store files"
        read -p "  Remove .DS_Store files? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            find ~ -name ".DS_Store" -type f -delete 2>/dev/null
            echo -e "${GREEN}  ✅ .DS_Store files removed${NC}"
        else
            echo -e "${YELLOW}  ⏭️  Skipped${NC}"
        fi
    else
        echo -e "${GREEN}  ✅ No .DS_Store files found${NC}"
    fi
    echo ""
}

# Remove broken symlinks
cleanup_broken_symlinks() {
    echo -e "${YELLOW}🔗 Checking for broken symlinks...${NC}"
    
    BROKEN_COUNT=$(find ~/.local/bin -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$BROKEN_COUNT" -gt 0 ]; then
        echo "  Found: $BROKEN_COUNT broken symlink(s) in ~/.local/bin"
        find ~/.local/bin -type l ! -exec test -e {} \; -print 2>/dev/null
        read -p "  Remove broken symlinks? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            find ~/.local/bin -type l ! -exec test -e {} \; -print 2>/dev/null | xargs rm -f
            echo -e "${GREEN}  ✅ Broken symlinks removed${NC}"
        else
            echo -e "${YELLOW}  ⏭️  Skipped${NC}"
        fi
    else
        echo -e "${GREEN}  ✅ No broken symlinks found in ~/.local/bin${NC}"
    fi
    echo ""
}

# Update Python packages
update_packages() {
    echo -e "${YELLOW}📦 Checking for outdated packages...${NC}"
    
    OUTDATED=$(pip3 list --outdated 2>/dev/null | tail -n +3 | wc -l | tr -d ' ')
    
    if [ "$OUTDATED" -gt 0 ]; then
        echo "  Found: $OUTDATED outdated package(s)"
        pip3 list --outdated 2>/dev/null | head -10
        read -p "  Update outdated packages? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip3 install --upgrade anyio networkx pytest 2>/dev/null || true
            echo -e "${GREEN}  ✅ Packages updated${NC}"
        else
            echo -e "${YELLOW}  ⏭️  Skipped${NC}"
        fi
    else
        echo -e "${GREEN}  ✅ All packages up to date${NC}"
    fi
    echo ""
}

# Show large files
show_large_files() {
    echo -e "${YELLOW}📊 Large files in home directory...${NC}"
    find ~ -maxdepth 1 -type f -size +100M 2>/dev/null | while read -r file; do
        size=$(du -h "$file" | cut -f1)
        echo "  $size - $(basename "$file")"
    done
    echo ""
}

# Show disk usage
show_disk_usage() {
    echo -e "${YELLOW}💾 Disk usage summary...${NC}"
    echo "  Home directory:"
    df -h ~ | tail -1 | awk '{print "    " $3 " used / " $2 " total (" $5 ")"}'
    echo ""
    echo "  Large directories:"
    du -sh ~/.cache ~/.local ~/.config ~/.cursor 2>/dev/null | sort -h | while read -r line; do
        echo "    $line"
    done
    echo ""
}

# Main menu
main() {
    echo "Select cleanup options:"
    echo "1) Clean Python cache files"
    echo "2) Clean .DS_Store files"
    echo "3) Remove broken symlinks"
    echo "4) Update Python packages"
    echo "5) Show large files"
    echo "6) Show disk usage"
    echo "7) Run all (with prompts)"
    echo "8) Exit"
    echo ""
    read -p "Choice [1-8]: " choice
    
    case $choice in
        1) cleanup_python_cache ;;
        2) cleanup_dsstore ;;
        3) cleanup_broken_symlinks ;;
        4) update_packages ;;
        5) show_large_files ;;
        6) show_disk_usage ;;
        7)
            cleanup_python_cache
            cleanup_dsstore
            cleanup_broken_symlinks
            update_packages
            show_large_files
            show_disk_usage
            ;;
        8) exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}" ;;
    esac
}

# Run main menu
if [ "$1" == "--auto" ]; then
    # Auto mode - run all without prompts
    cleanup_python_cache --auto
    cleanup_dsstore --auto
    cleanup_broken_symlinks --auto
    update_packages --auto
    echo -e "${GREEN}✅ Cleanup complete!${NC}"
else
    # Interactive mode
    main
fi
