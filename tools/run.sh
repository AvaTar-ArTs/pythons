
#!/usr/bin/env bash
set -euo pipefail

FILELIST="${1:-urls.txt}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[info] Using Python: $($PYTHON_BIN -V || true)"
echo "[info] Installing Python deps (this may take a minute)..."
$PYTHON_BIN -m pip install --upgrade pip >/dev/null
$PYTHON_BIN -m pip install -r requirements.txt

echo "[info] Ensuring Playwright browsers are installed..."
$PYTHON_BIN -m playwright install chromium

echo "[info] Starting downloader..."
$PYTHON_BIN gemini_storybook_downloader.py --file "$FILELIST"