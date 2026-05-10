#!/bin/bash
# Quick search aliases for common queries

INDEX_SCRIPT="/Users/steven/pythons/query_content_index.py"

# Find video-related functions
find_video_funcs() {
    python3 "$INDEX_SCRIPT" "video" --type function --search-in content --limit 20
}

# Find transcription functions
find_transcribe_funcs() {
    python3 "$INDEX_SCRIPT" "transcribe|transcription" --type function --search-in regex --limit 20
}

# Find analysis functions
find_analyze_funcs() {
    python3 "$INDEX_SCRIPT" "analyze|analysis" --type function --search-in regex --limit 20
}

# Find OpenAI-related code
find_openai_code() {
    python3 "$INDEX_SCRIPT" "openai" --type all --search-in content --limit 20
}

# Find large Python files
find_large_py_files() {
    python3 "$INDEX_SCRIPT" ".py" --type file --language .py --min-size-kb 50 --min-functions 10 --limit 20
}

# Find functions without docstrings (needs custom logic)
find_undocumented() {
    python3 "$INDEX_SCRIPT" "" --type function --output json | \
    python3 -c "
import json, sys
data = json.load(sys.stdin)
undoc = [f for f in data.get('functions', []) if not f.get('docstring', '').strip()]
print(f'Found {len(undoc)} functions without docstrings')
for f in undoc[:20]:
    print(f\"  {f.get('name')} in {f.get('file_name')}\")
"
}

# Show codebase statistics
show_stats() {
    python3 "$INDEX_SCRIPT" --stats
}

# Main menu
case "$1" in
    video) find_video_funcs ;;
    transcribe) find_transcribe_funcs ;;
    analyze) find_analyze_funcs ;;
    openai) find_openai_code ;;
    large) find_large_py_files ;;
    undocumented) find_undocumented ;;
    stats) show_stats ;;
    *) 
        echo "Usage: $0 {video|transcribe|analyze|openai|large|undocumented|stats}"
        echo ""
        echo "Quick searches:"
        echo "  video       - Find video-related functions"
        echo "  transcribe  - Find transcription functions"
        echo "  analyze     - Find analysis functions"
        echo "  openai      - Find OpenAI-related code"
        echo "  large       - Find large Python files"
        echo "  undocumented - Find functions without docstrings"
        echo "  stats       - Show codebase statistics"
        ;;
esac
