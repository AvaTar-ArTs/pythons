# Suno → Google Sheets Sync (macOS-ready)

Scrape **Suno** playlist tracks and write them **directly into a Google Sheet**.  
No manual CSV needed. Supports **append** or **replace** modes, OAuth or Service Account creds, and a **dry-run** for testing.

---

## ✨ What you get
- **Playwright** scraper with retries and human-like pacing
- **Google Sheets** writer (via `gspread`)
- Config-driven
- macOS run steps
- Dry-run to test Sheets pipeline without scraping

> Schema fields (column order):  
> `songName, songLink, length, author, authorLink, published, plays, likes, style, lyrics, playlist, version`

---

## 🛠 Setup (macOS)

1) **Create & activate a Python env (recommended)**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) **Install dependencies**
```bash
pip install -r requirements.txt
python -m playwright install
```

3) **Credentials (choose ONE)**

**Option A — OAuth (Installed App)**  
- In Google Cloud Console, enable the **Google Sheets API**.  
- Create **OAuth Client ID** (Desktop) and download as `client_secret.json` into this project folder.  
- First run will open a browser for consent and create `token.json` locally.

**Option B — Service Account**  
- Create a Service Account with **Sheets API** access.  
- Download JSON key as `service_account.json` into this project folder.  
- **Share your target Google Sheet** with the service account email (Editor).

4) **Config**
- Copy `config.sample.json` → `config.json`
- Put your playlist URLs and **sheet_id** (from the Google Sheet URL).  
  Example Sheet URL: `https://docs.google.com/spreadsheets/d/<SHEET_ID>/edit`

5) **Run**
```bash
# Dry-run (no browsing, sends sample rows to your Sheet)
python suno_to_sheet.py --config config.json

# Real scrape
# (disable dry_run in config or set "dry_run": false)
python suno_to_sheet.py --config config.json
```

> If you want to test scraping only (no Sheets), run:
```bash
python suno_scraper.py --urls https://suno.com/playlist/07653cdf-8f72-430e-847f-9ab8ac05af40 --dry-run --out test.json
```

---

## ⚙️ Config Options (`config.json`)

```json
{
  "suno_urls": ["https://suno.com/playlist/...."],
  "max_songs": 25,
  "headless": true,
  "dry_run": false,
  "sheet_id": "YOUR_GOOGLE_SHEET_ID",
  "worksheet": "Suno Data",
  "write_mode": "append",   // or "replace"
  "unique_key": "songLink"
}
```

- **write_mode**:  
  - `append` → only adds **new** rows (checks uniqueness by `songLink`)  
  - `replace` → overwrites the worksheet rows entirely
- **dry_run**: Generates a few sample rows and writes them to the Sheet (useful to verify auth + schema).

---

## 🔍 Adjusting Selectors
Suno’s frontend can change. If fields come back empty, tweak `SELECTORS` in `suno_scraper.py`:
```python
SELECTORS = {
  "playlist_song_links": "a[href^='/song/']",
  "song_title": "h1, .song-title, [data-testid='song-title']",
  "duration": ".duration, [data-testid='duration']",
  "author_name": "a[href^='/@'], .artist-name, [data-testid='artist-name']",
  "author_link": "a[href^='/@']",
  "published": "[data-testid='publish-date'], time",
  "plays": "[data-testid='plays'], .plays",
  "likes": "[data-testid='likes'], .likes",
  "style": "[data-testid='tags'], .genre-tags",
  "lyrics": ".lyrics, [data-testid='lyrics']",
  "version": "[data-testid='version'], .version-info",
}
```

---

## 🧰 Tips
- If rate-limited, re-run; the scraper has retries & brief human-like pauses.
- To speed up dev, set `"max_songs": 5`.
- Share the Google Sheet with your service account (if using that mode).

---

## 🧪 Troubleshooting
- **Auth errors**: Ensure the right creds file (`service_account.json` or `client_secret.json`) exists.
- **No rows written**: Check `sheet_id` and `worksheet` name; try `"replace"` once to reset headers.
- **Empty fields**: Update selectors; use `--headless` false in `config` to watch the browser.

---

## 📄 License
MIT
