# Handoff: Media Dedupe & LLM Tooling Snapshot

## What We Did
- **Scanned document/media counts**: Collected html/pdf/md/txt and csv/mp3/mp4 counts/sizes across key dirs (Documents, workspace, Library, Pictures, Downloads, GitHub, pythons, etc.) to see where content concentrates.
- **Detected CSV duplicates**: 399 hash-groups across Documents/Downloads/GitHub/workspace/Library/etc.; many consolidated copies (e.g., `vidiq_santrel`, `affiliates.csv`, `image.csv`, `WhisperTextOutput`).
- **Detected media duplicates (global)**: 164 hash-groups across Movies/Music/Pictures/Library/Documents/Downloads; many iMessage/MobileSMS caches, Ai-Art-Mp4 dupes, CapCut temp assets.
- **Focused Music/Movies analysis**: 24 duplicate groups (Ai-Art-Mp4 mp3 pairs, Stray tracks, TaskAde/podcast tracks, CapCut temps, Movies/mp4 vs Ai-Art-Mp4).
- **Enriched manifest**: Added duration/bitrate/mtime/size per duplicate media file.  
  - Path: `pythons/media-dup-manifest.csv`
- **Move plan (no actions executed)**: Source → dest mapping with action hints (`move/skip`) so it is reversible.  
  - Path: `pythons/media-move-plan.csv` (27 entries)
- **LLM/API inventory**: Highlighted advanced scripts in `~/pythons` (multi-provider, multi-modal, transcription, image/video pipelines).

## Key Findings (Media)
- Ai-Art-Mp4 audio tracks duplicated between `Movies/Ai-Art-Mp4/` and `Movies/Ai-Art-Mp4/mp3/` → move audio to `Music` (or `Movies/HeKaTe-saLome/mp3`) and remove duplicates.
- Stray tracks duplicated (`Movies/Movies - Stray*` vs `Movies/stray/*`) → keep one set (prefer `Music`).
- TaskAde/podcast/“Introducing Your AI Sales Agent” tracks duplicated in Movies vs Music → keep Music copies.
- Movies/mp4 duplicates of Ai-Art-Mp4 videos → keep in `Movies/Ai-Art-Mp4`, drop `Movies/mp4` copies.
- CapCut temp assets (`empty_audio2s.mp3`, generate_resources mp4s) → safe to prune or stage; keep at most one.
- iMessage/MobileSMS caches (seen in global scan) are disposable once a canonical copy exists.

## Files to Use
- `pythons/media-dup-manifest.csv` — reference details (hash, size, mtime, duration, bitrate, folder hint).
- `pythons/media-move-plan.csv` — reversible mapping (source, dest, action). Use to stage/move or roll back.

## Suggested Next Steps
1) **Stage moves (safe)**: Apply `media-move-plan.csv` into a staging area, e.g., `~/organize/dupes/media/{mp3,mp4}/`, so originals remain until verified.
2) **Promote canonicals**: After review, move staged files into their canonical homes (`Music`, `Movies/Ai-Art-Mp4`, or `Movies/HeKaTe-saLome/mp3`), then remove duplicates/caches.
3) **Broader CSV cleanup**: If desired, generate a full duplicate CSV move plan similar to media and consolidate into `workspace/csvs-consolidated`.
4) **LLM tooling quick-start (optional)**: Document installs/env for:  
   - `multi-llm-orchestrator.py` (provider routing),  
   - `Multi-Modal.py` (chat+transcription),  
   - `transcribe/transcribe-analyze-local.py` (multi-backend speech),  
   - `openai-batch-image-seo-pipeline.py`,  
   - `gpt-vision-image-describer.py`.

## Reversibility
- Both manifests preserve source/dest paths. If a move is performed, the CSV serves as the restore map (swap columns to undo).

## Status
- No files moved or deleted; only analysis and plan CSVs created.
