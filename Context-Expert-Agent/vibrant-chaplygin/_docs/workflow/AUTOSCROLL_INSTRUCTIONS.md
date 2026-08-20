# ?? Auto-Scroll Suno Extractor

## Extract ALL songs with automatic scrolling!

---

## ?? SUPER SIMPLE - 3 STEPS

### Step 1: Open Suno HTML
```bash
open ~/main.html
```

### Step 2: Open Dev Console
Press: **Cmd + Option + I** (Mac) or **F12** (Windows)

### Step 3: Paste Script & Watch Magic!
The script is **already in your clipboard!**

Just:
1. Click in console
2. Press **Cmd + V**
3. Press **Enter**
4. **Wait** - it will auto-scroll and extract!

---

## ?? What It Does:

1. **Auto-scrolls** through the page (loads all songs)
2. **Extracts** all song data:
   - Title
   - Duration
   - Tags/Style
   - Version (v4/v5)
   - Plays, Likes, Comments
   - URLs (song, audio, image)
3. **Downloads** CSV to ~/Downloads/
4. **Copies** JSON to clipboard
5. **Shows** preview in console

---

## ?? How Long It Takes:

- **Small pages** (~20 songs): 10-20 seconds
- **Medium pages** (~100 songs): 1-2 minutes
- **Large pages** (~500 songs): 3-5 minutes

**You'll see progress in console:**
```
Scroll 1: Found 20 songs...
Scroll 2: Found 40 songs...
Scroll 3: Found 60 songs...
? Finished scrolling!
```

---

## ?? After Extraction:

**CSV auto-downloads to:**
```
~/Downloads/suno-songs-[timestamp].csv
```

**Open it:**
```bash
cd ~/Downloads
open suno-songs-*.csv
```

**Or move to workspace:**
```bash
mv ~/Downloads/suno-songs-*.csv ~/workspace/music-empire/extracted-data/
```

---

## ?? Repeat for All Files:

**Run on each HTML file:**

1. **main.html:**
   ```bash
   open ~/main.html
   # Paste script, wait for extraction
   ```

2. **evolves.html:**
   ```bash
   open ~/evolves.html
   # Paste script, wait for extraction
   ```

3. **suno1.html:**
   ```bash
   open ~/Music/nocTurneMeLoDieS/suno1.html
   # Paste script, wait for extraction
   ```

4. **suno2.html:**
   ```bash
   open ~/Music/nocTurneMeLoDieS/suno2.html
   # Paste script, wait for extraction
   ```

5. **suno3.html:**
   ```bash
   open ~/Music/nocTurneMeLoDieS/suno3.html
   # Paste script, wait for extraction
   ```

**Result:** 5 CSV files with ALL your song data!

---

## ?? Pro Tips:

### View Extracted Data in Console:
```javascript
// Type in console after extraction:
extractedSongs              // View all data
extractedSongs.length       // Count songs
extractedSongs[0]          // View first song
```

### Filter Songs:
```javascript
// Find songs with "Moonlit" in title
extractedSongs.filter(s => s.title.includes('Moonlit'))

// Find longest songs
extractedSongs.filter(s => s.duration.startsWith('4:'))

// Find v5 songs
extractedSongs.filter(s => s.version === 'v5')
```

### Download Again:
```javascript
// If download failed, run this:
downloadCSV(convertToCSV(extractedSongs), 'my-songs.csv')
```

---

## ?? Expected Results:

After running on all 5 files:
- ? 5 CSV files in Downloads
- ? All song data extracted
- ? Ready to merge and analyze

**Total songs:** ~200-500+ (depending on your collection)

---

## ? Quick Reference:

| Step | Command |
|------|---------|
| 1. Open HTML | `open ~/main.html` |
| 2. Open Console | `Cmd + Option + I` |
| 3. Paste Script | Script already in clipboard! |
| 4. Run | Press `Enter` |
| 5. Wait | Auto-scrolls and extracts |

**Script location:** `~/AUTO_SCROLL_EXTRACTOR.js`

**Instructions:** `~/AUTOSCROLL_INSTRUCTIONS.md`

---

## ?? Ready to Go!

The script is **already in your clipboard!**

Just:
1. Open ~/main.html
2. Open console (Cmd+Option+I)
3. Paste (Cmd+V)
4. Press Enter
5. Watch the magic! ?

**Let it scroll and extract!** ??
