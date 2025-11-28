# Conversation Handoff (Media, CSV, LLM Utilities)

## What We Did
- Cataloged text/doc/media across home dir; biggest volumes in Documents, workspace, Library, Pictures, Movies, Music.
- Deduplicated CSVs (399 hash groups) and media (164 global; 24 focused in Music/Movies), keeping everything untouched.
- Built reversible move plans (no moves executed) plus a detailed media manifest with duration/bitrate/mtime hashes.
- Drafted LLM quick-start (now with provider/model cheat sheet, env keys, and sample invocations) and a cache prune plan for CapCut/iMessage data.

## Key Artifacts (all in `pythons`)
- `media-dup-manifest.csv`: Media inventory with path, duration, bitrate, mtime, hash.
- `media-move-plan.csv`: 27 staged moves; keep videos in `Movies/Ai-Art-Mp4`, audio in `Music` (fallback `Movies/HeKaTe-saLome/mp3`); CapCut temps flagged.
- `csv-move-plan.csv`: 438 mappings (399 groups); destination `workspace/csvs-consolidated/<filename>` prioritized: workspace > Documents/CsV > Documents > GitHub > Downloads > iCloud.
- `cache-prune-plan.csv`: 7 entries (CapCut temps, iMessage/MobileSMS caches) marked `delete_after_canonical_verified`.
- `LLM_QUICKSTART.md`: Updated with provider/model defaults (OpenAI/Groq/DeepSeek/Anthropic/Gemini/OpenRouter/Azure), env vars, TTS/STT keys, and ready-to-run commands for orchestrator, multimodal chat, STT driver, vision caption, SEO batch.
- `HANDOFF_MEDIA_DUPES_AND_LLM.md`: Narrative summary of findings and plans.

## Media Rules Recap
- Canonical video: `Movies/Ai-Art-Mp4`.
- Canonical audio: `Music` (or `Movies/HeKaTe-saLome/mp3` if you prefer).
- Ai-Art-Mp4 mp3 pairs -> move to `Music`.
- Movies/mp4 dupes -> move into `Movies/Ai-Art-Mp4`.
- Treat `Library/Containers/...MobileSMS` and `Library/Messages/Attachments` as disposable caches once canonicals verified; same for CapCut temps.

## CSV Rules Recap
- Keep one canonical copy per hash in `workspace/csvs-consolidated`.
- Use `csv-move-plan.csv` for reversible moves; do not delete sources until verified.

## Suggested Next Steps
1) Run the CSV move plan into `workspace/csvs-consolidated` (dry-run/staging first if desired), keep source copies until spot-checking.
2) Stage media moves per `media-move-plan.csv`, verify in target locations, then prune CapCut/iMessage caches per `cache-prune-plan.csv`.
3) Optionally add your preferred provider/model presets to `LLM_QUICKSTART.md` and keep a tiny sample run per script as smoke test.
4) After moves, regenerate manifests to confirm no orphan duplicates remain.
