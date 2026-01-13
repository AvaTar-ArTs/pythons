# ?? AI Assistant Instructions for This Repository

## ?? MANDATORY: Session Handoff Protocol

**ALWAYS create a comprehensive handoff prompt before ending any session.**

### Required Steps Before Session End:

1. **Create HANDOFF_PROMPT.md** in repository root
2. **Copy to clipboard** using `pbcopy`
3. **Commit to git** with descriptive message
4. **Confirm to user** that handoff is ready

### Handoff Prompt Template:

```markdown
# ?? HANDOFF PROMPT - Session [DATE]

## ?? CONTEXT SUMMARY
[Brief overview of session focus]

## ? COMPLETED WORK
[Detailed list of all tasks completed]

## ?? READY TO USE
[Commands and examples for immediate use]

## ?? KEY DIRECTORIES & FILES
[All relevant file paths and locations]

## ?? KNOWN ISSUES
[Any warnings, edge cases, or pending problems]

## ?? TECHNICAL DETAILS
[Important code changes, configurations, etc.]

## ?? REPOSITORY STATS
[Current state of the repo]

## ?? NEXT STEPS (IF NEEDED)
[Suggested follow-up actions]

## ?? QUICK COMMANDS
[Copy-paste ready commands]

## ?? IMPORTANT FILES TO REFERENCE
[Key documentation paths]

## ? VERIFICATION
[Checklist of what was tested/verified]
```

### Implementation:

```bash
# 1. Create handoff
cat > HANDOFF_PROMPT.md << 'EOF'
[... full handoff content ...]
EOF

# 2. Copy to clipboard
cat HANDOFF_PROMPT.md | pbcopy

# 3. Commit
git add HANDOFF_PROMPT.md
git commit -m "?? Add session handoff prompt"

# 4. Confirm
echo "? Handoff created, copied to clipboard, and committed!"
```

---

## ?? Repository-Specific Context

### Project Type:
- **760+ Python automation scripts**
- Focus areas: transcription, AI, automation, web scraping, media processing
- Heavy use of APIs (OpenAI, Anthropic, Deepgram, etc.)

### Environment Setup:
- **Python:** 3.12
- **Package Manager:** Mamba (conda alternative)
- **Shell:** Zsh on macOS
- **Environment Variables:** Modular system in `~/.env.d/`

### Key Directories:
- `transcribe/` - Audio/video transcription pipeline (30 scripts)
- `_analysis/` - Analysis reports and CSVs
- `_docs/` - Documentation and references
- `_library/` - Reusable Python modules
- `_backups/` - Backup scripts

### Coding Standards:
- ? Use descriptive variable names (not `CONSTANT_*`)
- ? Proper Python pathlib usage (not `Path("\n").join()`)
- ? Timestamp format: `MM:SS-MM:SS` (not `HH:MM:SS -- HH:MM:SS`)
- ? Clean console output (use `print()` not undefined `logger`)
- ? Environment variables loaded from `~/.env.d/`

### Git Workflow:
- **Branch:** master
- **Commit Style:** Emoji prefixes (?? ?? ? ?? ?? etc.)
- **Always:** Stage, commit with descriptive message
- **Ask before:** Pushing to remote

---

## ?? Common Tasks

### When Fixing Bugs:
1. Read the file completely
2. Identify all instances of the bug
3. Fix all at once (prefer batch operations)
4. Test if possible
5. Commit with clear message
6. Update handoff

### When Organizing Code:
1. Use `git mv` for moving files
2. Create README.md in new folders
3. Update any scripts that reference moved files
4. Verify no broken imports
5. Commit organization changes

### When Adding Features:
1. Check if similar code exists
2. Follow existing patterns
3. Add to relevant documentation
4. Test the feature
5. Commit with feature description

---

## ?? Session End Checklist

Before ending ANY session:

- [ ] All TODOs marked as completed
- [ ] All changes committed to git
- [ ] HANDOFF_PROMPT.md created
- [ ] Handoff copied to clipboard via `pbcopy`
- [ ] Handoff committed to git
- [ ] Git status clean (or explained)
- [ ] User informed of handoff location
- [ ] Summary provided to user

---

## ?? Important Notes

1. **Never push to remote** without user confirmation
2. **Always use parallel tool calls** when possible (read multiple files at once)
3. **Batch operations** are preferred (fixing 16 files > fixing 16 times)
4. **Document everything** - this repo is complex and needs good docs
5. **Test when possible** - especially for critical scripts
6. **Ask about .gitignore** for new file types (screenshots, logs, etc.)

---

## ?? User Preferences

- **Commands:** Display without line numbers for easy copy-paste
- **Organization:** Clean, logical folder structures
- **Documentation:** Comprehensive markdown files
- **Commits:** Frequent, descriptive, emoji-prefixed
- **Handoffs:** Detailed, actionable, copy-paste ready

---

**Last Updated:** 2025-11-05  
**Purpose:** Ensure consistent, high-quality AI assistance across sessions
