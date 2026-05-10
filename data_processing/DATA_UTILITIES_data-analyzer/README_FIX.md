# analyzer_prompt_cli.py (Fix)

This fixes your errors:
- `IndexError: list index out of range` (no more `sys.argv[1]` without args)
- `AttributeError: module 'sys' has no attribute 'arg'` (typo)
- Replaces interactive `input()` with `--video` or `--video-dir` flags.

## Usage

### Single file
```bash
conda activate hekate
python analyzer_prompt_cli.py   --video "/Users/steven/Movies/HeKaTe-saLome/input.mp4"   --outdir "/Users/steven/Movies/HeKaTe-saLome"   --segment-seconds 300
```

### Whole directory
```bash
conda activate hekate
python analyzer_prompt_cli.py   --video-dir "/Users/steven/Movies/invideo"   --segment-seconds 300
```

Outputs go to `transcript/` and `analysis/` beside each input file unless you pass `--outdir`.

## Notes
- Requires: `ffmpeg`, `python-dotenv`, `openai` Python package, and `OPENAI_API_KEY` in env or `~/.env`.
- If you want to switch the model: `export ANALYZER_MODEL=gpt-4o-mini` (or another available model).
