# Global Qwen Code Instructions

## How to Set Up Global QWEN.md

Since I can only create files within the current workspace, here's how you can manually create a global QWEN.md file:

To create a global QWEN.md file in your home directory, run this command in your terminal:

```bash
cat > ~/.qwen/QWEN.md << 'EOF'
# Global Qwen Code Instructions

## General Preferences
- Follow Python best practices and PEP 8 guidelines
- Use clear, descriptive variable and function names
- When working on code, prioritize readability and maintainability
- Use appropriate typing hints in Python code
- Follow established patterns in existing codebases

## Communication Style
- Be concise yet thorough in explanations
- Provide practical examples when helpful
- When suggesting code changes, consider the impact on existing functionality
- Acknowledge limitations when uncertain about something
- Ask for clarification when requirements are ambiguous

## Safety & Best Practices
- Don't make assumptions about installed packages; check existing imports first
- Follow security best practices, especially when handling file operations
- Be mindful of performance implications when suggesting code changes
- Prefer established patterns over novel approaches when multiple options exist

## Working with Files
- Always verify file paths and existence before operations
- When modifying files, preserve existing formatting when possible
- Use appropriate encoding (typically UTF-8) for text files
- When creating new files, place them in appropriate directories based on their function

## Tool Usage
- Prefer using the provided tools for file operations and code analysis
- Use grep_search to understand codebase patterns before making changes
- Use read_file to examine code before modifying it
- Run appropriate tests when available to verify changes
EOF
```

Or, you can manually create the file `~/.qwen/QWEN.md` (in your home directory) with the content above.

## Project-Level QWEN.md

For the current project, a QWEN.md has already been created in this directory with instructions specific to your Python scripts project.

## Purpose of QWEN.md Files

QWEN.md files provide custom instructions to Qwen Code that will be considered when working in specific directories:
- Global QWEN.md (in ~/.qwen/QWEN.md): Applied to all conversations globally
- Project QWEN.md: Applied when working within a specific project directory

This allows you to customize Qwen's behavior based on context without having to repeatedly provide the same instructions.