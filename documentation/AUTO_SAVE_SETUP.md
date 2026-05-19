# Auto-Save Conversation Setup

Automatically save conversations when you type keywords like "exit", "bye", or "save"!

---

## 🎯 What This Does

**Automatic Save Triggers:**
- Type `exit` → Saves conversation
- Type `bye` → Saves conversation
- Type `save` → Saves conversation
- Type `done` → Saves conversation
- Type `quit` → Saves conversation
- Type `goodbye` → Saves conversation

**You'll see a notification:**
```
💾 Conversation Saved!
Exported to ~/claude/conversations/
```

---

## ⚙️ Configuration

Add **both hooks** to your Claude Code settings for complete coverage:

### Option 1: Full Configuration (Recommended)

```json
{
  "hooks": {
    "UserPromptSubmit": {
      "command": "/Users/steven/Documents/python/auto_save_on_exit.py"
    },
    "SessionEnd": {
      "command": "/Users/steven/Documents/python/conversation_exporter.py"
    }
  }
}
```

**This gives you:**
- ✅ Manual save: Type "save" or "exit" anytime
- ✅ Auto save: When session ends naturally
- ✅ Complete coverage: Never lose a conversation

---

### Option 2: Manual Only

If you only want keyword-triggered saves:

```json
{
  "hooks": {
    "UserPromptSubmit": {
      "command": "/Users/steven/Documents/python/auto_save_on_exit.py"
    }
  }
}
```

---

### Option 3: Auto Only

If you only want session-end saves:

```json
{
  "hooks": {
    "SessionEnd": {
      "command": "/Users/steven/Documents/python/conversation_exporter.py"
    }
  }
}
```

---

## 🚀 How to Add to Settings

### Step 1: Locate Settings File

Claude Code settings are typically at:
```bash
~/.config/claude/settings.json
```

Or check your Claude Code documentation for the exact location.

### Step 2: Edit Settings

Open the settings file:
```bash
# Using your preferred editor
code ~/.config/claude/settings.json
# or
vim ~/.config/claude/settings.json
# or
nano ~/.config/claude/settings.json
```

### Step 3: Add Hooks Section

If you already have a `hooks` section, merge the configuration.
If not, add the complete configuration from Option 1 above.

**Example full settings file:**
```json
{
  "editor": "code",
  "theme": "dark",
  "hooks": {
    "UserPromptSubmit": {
      "command": "/Users/steven/Documents/python/auto_save_on_exit.py"
    },
    "SessionEnd": {
      "command": "/Users/steven/Documents/python/conversation_exporter.py"
    }
  }
}
```

### Step 4: Save and Restart

1. Save the settings file
2. Restart Claude Code
3. Test by typing "save" in your next conversation!

---

## 🧪 Testing

### Test Manual Save
```
You: save
```

You should see:
```
💾 Conversation Saved!
Exported to ~/claude/conversations/
```

Then check:
```bash
ls ~/claude/conversations/
```

### Test Auto Save

Just end your session normally, and the conversation will be saved automatically.

---

## 🎯 Usage Examples

### During Conversation
```
You: Can you help me with Python?
Claude: Sure! What do you need?
You: Thanks, that helps. save
```
→ 💾 Conversation saved immediately!

### Natural Exit
```
You: Thanks for the help!
Claude: You're welcome!
You: bye
```
→ 💾 Conversation saved immediately!

### Quick Save
```
You: save
```
→ 💾 Conversation saved immediately (then continue chatting)

---

## 📋 Supported Keywords

All case-insensitive:
- `save` - Save conversation
- `exit` - Save and implies you're done
- `bye` - Save and implies you're done
- `goodbye` - Save and implies you're done
- `done` - Save and implies you're done
- `quit` - Save and implies you're done

**Also works if keyword starts message:**
- `save this please` ✓
- `exit now` ✓
- `bye, thanks!` ✓

---

## 🔧 Customization

### Add More Keywords

Edit `/Users/steven/Documents/python/auto_save_on_exit.py`:

```python
# Around line 12
SAVE_KEYWORDS = ['exit', 'bye', 'save', 'done', 'quit', 'goodbye', 'thanks', 'thx']
```

Add any keywords you commonly use!

### Change Notification

Edit the notification message:

```python
# Around line 55
"notification": {
    "title": "💾 Your Custom Title!",
    "message": "Your custom message here"
}
```

### Change Output Directory

Edit `/Users/steven/Documents/python/conversation_exporter.py`:

```python
# Change CONVERSATIONS_DIR or set env var
CONVERSATIONS_DIR = Path.home() / "your_custom_path"
```

---

## 🔍 Verification

### Check Scripts Exist
```bash
ls -lh /Users/steven/Documents/python/auto_save_on_exit.py
ls -lh /Users/steven/Documents/python/conversation_exporter.py
```

Both should be executable (`-rwxr-xr-x`)

### Test Exporter Directly
```bash
echo '{"transcript_path": "/path/to/test.json"}' | python3 /Users/steven/Documents/python/auto_save_on_exit.py
```

### Check Output
```bash
ls ~/claude/conversations/
```

---

## ⚠️ Troubleshooting

### Hook Not Firing

**Check 1: Settings Correct**
```bash
cat ~/.config/claude/settings.json | grep -A 5 hooks
```

**Check 2: Scripts Executable**
```bash
chmod +x /Users/steven/Documents/python/auto_save_on_exit.py
chmod +x /Users/steven/Documents/python/conversation_exporter.py
```

**Check 3: Python Available**
```bash
which python3
python3 --version
```

### No Notification Appearing

Claude Code might not support notifications on your platform. The conversation will still be saved even if you don't see the notification.

### Wrong Directory

Check symlink:
```bash
ls -la ~/claude_conversations
```

Should point to `~/claude/conversations/`

### Permission Denied

```bash
chmod +x /Users/steven/Documents/python/*.py
```

---

## 📊 How It Works

### UserPromptSubmit Hook Flow
```
1. You type message
2. Hook receives message before Claude sees it
3. Script checks for keywords
4. If keyword found → Run exporter
5. Show notification
6. Allow message through to Claude
7. Continue conversation or exit
```

### SessionEnd Hook Flow
```
1. Session ends (close terminal, exit Claude Code, etc.)
2. Hook triggers automatically
3. Export conversation
4. Save files
5. Done
```

---

## 🎁 Benefits

### With Both Hooks
- ✅ Manual control when you want it
- ✅ Automatic backup when you forget
- ✅ Never lose important conversations
- ✅ Quick save mid-conversation
- ✅ Instant search with Alfred

### Use Cases

**Quick saves during long sessions:**
```
You: <working on complex problem>
You: save
You: <continue working>
```

**Natural exits:**
```
You: Thanks for all the help! bye
```
→ Saves automatically

**Emergency saves:**
```
You: exit
```
→ Saves immediately

---

## 🔗 Integration with Other Tools

### Alfred Workflow
After saving, search immediately:
```
⌘ + Space → cc keyword
```

### Terminal
```bash
# View latest conversation
ls -lt ~/claude/conversations/ | head -1

# Open latest HTML
open $(ls -t ~/claude/conversations/*.html | head -1)
```

---

## 📚 Related Documentation

- Main README: `~/claude/README.md`
- Exporter README: `/Users/steven/Documents/python/CONVERSATION_EXPORTER_README.md`
- Setup Guide: `/Users/steven/Documents/python/SETUP_GUIDE.md`
- Quick Reference: `~/claude/QUICK_REFERENCE.md`

---

## 🎯 Quick Setup Checklist

- [ ] Scripts exist and are executable
- [ ] Added hooks to Claude Code settings
- [ ] Restarted Claude Code
- [ ] Tested with "save" command
- [ ] Verified files appear in `~/claude/conversations/`
- [ ] Tested Alfred search with `cc`

---

## ✨ Pro Tips

1. **Save frequently during long sessions**
   ```
   You: save
   ```
   Creates checkpoint you can reference later

2. **Use descriptive last messages**
   ```
   You: Great debugging session on API errors. save
   ```
   Makes it easier to find later

3. **Combine with Alfred**
   ```
   You: save
   ⌘ + Space → cc
   ```
   Immediately verify it was saved

4. **Archive strategy**
   ```bash
   # Monthly archives
   mkdir -p ~/claude/conversations/archive/2025-10
   mv ~/claude/conversations/conversation_202510* ~/claude/conversations/archive/2025-10/
   ```

---

## 🎊 You're All Set!

With this setup, you'll **never lose a conversation** again!

Just type any of these magic words:
- `save`
- `exit`
- `bye`
- `done`

And your conversation is instantly saved and searchable! 🚀

---

*Created: 2025-10-26*
*Auto-save system by Claude Code*
