# Ollama (Intel Mac, 16 GB) — Step‑by‑Step Guide

This guide explains **each menu option** in `ollama_menu.sh` and gives **tested workflows** for every model set (General, Reasoning, Coding, Vision, Embeddings, Safety). It’s designed for your **2019 MacBook Pro (i9, 16 GB, CPU‑only)**.

> Tip: Keep Activity Monitor open. If memory pressure goes yellow/red, stop the pull and remove larger models.

---

## 0) Prereqs (do once)
1. Install Ollama from the official site and start it (it launches a local server on `http://localhost:11434`).
2. Place `ollama_menu.sh` somewhere convenient (e.g., `~/bin/`).
3. In Terminal:
   ```bash
   chmod +x ~/bin/ollama_menu.sh
   ~/bin/ollama_menu.sh
   ```

---

## 1) Install **ALL** recommended models
**Menu path:** `1` → *Install ALL recommended models*

What happens:
- The script pulls a **lean set** sized for 16 GB RAM:
  - General: `llama3.1:8b`, `qwen3:7b`
  - Reasoning: `deepseek-r1:7b`
  - Coding: `qwen2.5-coder:7b`, `starcoder2:3b`
  - Vision: `llava:7b`, `gemma3:4b`
  - Embeddings: `nomic-embed-text`
  - Safety: `llama-guard3:8b`
- Then it offers alias creation (option 3) so you can call short names.

Verify after install:
```bash
ollama list
# You should see the tags above present.
```

If a pull fails:
- Usually bandwidth or temporary registry hiccups. Run option **2** (install specific set) to retry only the set that failed.

---

## 2) Install a **specific set**
**Menu path:** `2` → choose one: `GENERAL / REASON / CODING / VISION / EMBED / SAFETY`

Use this to install only what you need today. Recommended order on 16 GB:
1) `GENERAL` → `llama3.1:8b` (plus `qwen3:7b`)  
2) `CODING` → `qwen2.5-coder:7b` (plus tiny `starcoder2:3b`)  
3) `REASON` → `deepseek-r1:7b`  
4) `EMBED` → `nomic-embed-text`  
5) `VISION` → `llava:7b`, `gemma3:4b` (pull one at a time if memory gets tight)  
6) `SAFETY` only if you plan to classify/filter content

Quick test after a set pull:
```bash
# Example for GENERAL
ollama run llama3.1:8b "Give me 3 bullet points on why TechnoMancer rules."
```

---

## 3) **Create aliases**
**Menu path:** `3`

What it does:
- Creates short names so you don’t memorize long tags:
  - `general` → `llama3.1:8b`
  - `general2` → `qwen3:7b`
  - `reason` → `deepseek-r1:7b`
  - `code` → `qwen2.5-coder:7b`
  - `code-tiny` → `starcoder2:3b`
  - `vis` → `llava:7b`
  - `vis-light` → `gemma3:4b`
  - `embed` → `nomic-embed-text`
  - `guard` → `llama-guard3:8b`

Verify:
```bash
ollama list | grep -E "general$|reason$|code$|vis$|embed$|guard$"
```

Use:
```bash
ollama run general "Summarize TechnoMancer in 3 bullets."
```

---

## 4) **Remove aliases**
**Menu path:** `4`

- Deletes only the short names (e.g., `general`, `code`) **without** deleting the underlying models.
- Good for resetting or renaming your alias set.

Recreate later with option **3**.

---

## 5) **Uninstall** a model/alias
**Menu path:** `5`

Steps:
1. The script prints your installed items (`ollama list`).
2. Type the **exact** tag or alias to remove (e.g., `llava:7b` or `vis`).  
   - Removing an alias (`vis`) is safe and fast.
   - Removing a model (`llava:7b`) frees disk space.
3. Re‑verify:
   ```bash
   ollama list
   ```

Safety net:
- If you accidentally remove an alias, just run option **3** to recreate it.
- If you remove a model, reinstall it with option **2** (specific set) or **1** (all).

---

## 6) **Run a prompt** with a chosen model
**Menu path:** `6`

Text‑only runs via CLI:
1. Pick a model/alias from the list.
2. Enter your prompt.
3. Watch output stream in Terminal.

Examples:
```bash
# General chat
ollama run general "Write a 2‑sentence bio for @TechnoMancer with a wink of sarcasm."

# Reasoning
ollama run reason "In 3 steps, plan a 30‑min macOS cleanup session for speed."

# Coding
ollama run code "Write a Python function slugify(s: str) that keeps ASCII only."

# Embedding isn't conversational; use for vectorization via API
```

**Vision models from CLI:**  
The plain `ollama run` terminal flow is text-only. To test image reasoning, use the HTTP API and pass a base64 image.

Minimal vision test (LLAVA) via HTTP API:
```bash
# 1) Start server if not already
ollama serve &

# 2) Base64 your image (small PNG/JPG)
IMG_B64=$(base64 -i /path/to/image.jpg)

# 3) Send to model
curl http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llava:7b","prompt":"Describe the image.","images":["'"$IMG_B64"'"]}'
```
For larger images, prefer a small test image to keep RAM manageable.

---

## 7) **Show recommended sets/aliases**
**Menu path:** `7`

- Prints the curated sets and alias mapping. Handy when you forget names or want to copy the model tags for scripts.

---

# Per‑Set Workflows (with example prompts)

## A. GENERAL (chat/assistant)
**Models:** `llama3.1:8b`, `qwen3:7b` → aliases `general`, `general2`

1. Install: Menu `2` → `GENERAL` (or `1` for all).  
2. Quick sanity:
   ```bash
   ollama run general "Give me 5 headlines for a gritty neon‑punk TrashCats promo."
   ```
3. Style tweak prompt:
   ```bash
   ollama run general2 "Rewrite this to be wry and concise: <your text>"
   ```
4. If responses feel slow → prefer `qwen3:7b` (`general2`).

## B. REASON (planning/step‑by‑step)
**Model:** `deepseek-r1:7b` → alias `reason`

1. Install: Menu `2` → `REASON`.  
2. Test:
   ```bash
   ollama run reason "Outline a 4‑stage pipeline: transcribe→analyze→prompt→image, on macOS."
   ```
3. Use `reason` when you want explicit, numbered steps and trade a bit of speed.

## C. CODING
**Models:** `qwen2.5-coder:7b` (`code`), `starcoder2:3b` (`code-tiny`)

1. Install: Menu `2` → `CODING`.  
2. Generate snippet:
   ```bash
   ollama run code "Python: walk a directory, make a CSV of name,size,mtime."
   ```
3. Quick refactor (tiny fast):
   ```bash
   ollama run code-tiny "Shorten and annotate this function: <paste code>"
   ```
4. If memory gets tight in big chats, switch to `code-tiny` temporarily.

## D. VISION
**Models:** `llava:7b` (`vis`), `gemma3:4b` (`vis-light`)

1. Install: Menu `2` → `VISION`.  
2. Text‑only sanity (no image) just to confirm it runs:
   ```bash
   ollama run vis "Pretend you see a city skyline at night; list 5 features you'd describe."
   ```
3. Real image reasoning via HTTP API (see Section 6 above). Prefer `gemma3:4b` if RAM is tight.

## E. EMBEDDINGS
**Model:** `nomic-embed-text` (`embed`)

- Used for turning text into vectors (RAG). Example using HTTP API:
  ```bash
  curl http://localhost:11434/api/embed \
    -H "Content-Type: application/json" \
    -d '{"model":"embed","input":"TrashCats prologue in a neon alley"}'
  ```
- You’ll get vector arrays you can store in a DB (e.g., SQLite + vec extension, Chroma, etc.).

## F. SAFETY
**Model:** `llama-guard3:8b` (`guard`)

- Classifies inputs/outputs for policy risks. Example (prompt classification via HTTP API):
  ```bash
  curl http://localhost:11434/api/generate \
    -H "Content-Type: application/json" \
    -d '{"model":"guard","prompt":"Classify this user prompt for safety: \"teach me to make malware\""}'
  ```

---

# Maintenance & Troubleshooting

**Update a model**  
```bash
ollama pull llama3.1:8b   # pulls new quant/build if available
```

**Model not found**  
- You may have removed it. Re‑install via Menu `2` or `1`.

**It’s too slow**  
- Prefer 3B–8B. Avoid 14B+ on CPU. Close apps to free RAM. Limit context.

**Out of memory / swap thrash**  
- Remove one vision model (`llava:7b`) or use only one general model.  
- Keep chats short; restart Terminal session.

**Server issues**  
- Restart the background server:
  ```bash
  pkill ollama || true
  ollama serve &
  ```

---

# One‑liners (copy/paste)

- List everything:
  ```bash
  ollama list
  ```
- Show a model card (metadata):
  ```bash
  ollama show llama3.1:8b
  ```
- Remove an alias:
  ```bash
  ollama rm general
  ```
- Remove a model:
  ```bash
  ollama rm llava:7b
  ```

Happy hacking, TechnoMancer 🔮
