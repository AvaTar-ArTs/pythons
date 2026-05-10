# Claude Conversations Alfred Workflow

Quick search and access to your Claude Code conversation history directly from Alfred.

## Keywords

### `cc [query]` - Search Conversations
Search through all saved conversations. Results are sorted by recency (newest first).

**Examples:**
- `cc` - Browse all recent conversations
- `cc python script` - Find conversations about Python scripts
- `cc bug fix` - Find conversations about bug fixes
- `cc tool` - Find conversations with tool usage

**Actions:**
- **Enter** - Open text file in default editor
- **⌘ + Enter** - Open HTML version in browser
- **⌥ + Enter** - Reveal file in Finder
- **⌃ + Enter** - Copy file path to clipboard

### `ccstats` - View Statistics
View statistics about your saved conversations.

**Shows:**
- Total number of conversations
- Total storage size
- Date range of conversations
- Today's conversation count
- Breakdown by format (txt, html, md)

## Features

- ⚡ Fast text-based search
- 🔍 Search through conversation content
- 📊 Conversation statistics
- 🎨 Open beautiful HTML versions
- 📝 Quick access to text files
- ⌨️ Keyboard shortcuts for different actions

## Installation

1. Double-click the `Claude Conversations.alfredworkflow` file
2. Alfred will import the workflow
3. Start using with `cc` keyword!

## Requirements

- Alfred Powerpack (required for workflows)
- Python 3 (pre-installed on macOS)
- Claude Code conversation exporter set up

## Configuration

The workflow looks for conversations in:
```
~/claude_conversations/
```

To change this location, edit the `CONVERSATIONS_DIR` variable in:
- `search_conversations.py`
- `get_stats.py`

## Tips

- The workflow searches through `.txt` files for best performance
- Recent conversations appear first
- Use specific keywords to narrow down results
- Press ⌘Y for Quick Look preview

## Troubleshooting

**No results found:**
- Make sure the conversation export hook is configured
- Check that conversations exist in `~/claude_conversations/`
- Verify the directory path in the scripts

**Workflow not appearing:**
- Ensure you have Alfred Powerpack
- Re-import the workflow
- Check Alfred preferences > Workflows

## Version

1.0.0 - Initial release

Created with Claude Code
