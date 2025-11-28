# LLM / API Quick Start (pythons/)

# Scripts to Know
- `multi-llm-orchestrator.py` — central router for OpenAI/Claude/DeepSeek/Groq/OpenRouter/etc.
- `Multi-Modal.py` — chat + transcription + multi-provider audio (OpenAI/Anthropic/Gemini/Groq/AssemblyAI/Deepgram).
- `transcribe/transcribe-analyze-local.py` — STT driver with backends: groq/openai/anthropic/gemini/deepseek/ollama.
- `openai-batch-image-seo-pipeline.py` — OpenAI image pipeline with SEO metadata.
- `gpt-vision-image-describer.py` — vision captioning via OpenAI.
- Also useful: `openai-text-generator.py`, `openai-content-analyzer.py`, `thinketh-tts-*` (OpenAI TTS), `youtube/youtube-media-processing-video-extract_simple.py`.

# Environment
- Auto-loads `.env` (dotenv).
- Core keys: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` (Gemini), `GROQ_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_DEPLOYMENT`.
- Audio/STT: `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY`.
- Optional routing: `DEFAULT_MODEL`, `PROVIDER_PRIORITY`, provider-specific model overrides if present in the script.

# Install (minimal)
```bash
python -m pip install --upgrade pip
python -m pip install openai anthropic google-generativeai groq deepgram-sdk assemblyai python-dotenv requests tenacity tqdm
```

# Provider + Model Cheat Sheet (suggested defaults/fallbacks)
- OpenAI: primary `gpt-4o`, fast/cheap `gpt-4o-mini`; vision `gpt-4o(-mini)-vision`; audio `whisper-1`.
- Groq: `mixtral-8x7b`, `llama-3.1-70b-versatile` (chat); `whisper-large-v3` (STT).
- DeepSeek: `deepseek-chat` (fast), `deepseek-coder` (code).
- Anthropic: `claude-3-5-sonnet` (strong), `claude-3-haiku` (cheap/fast).
- Gemini: `gemini-1.5-pro` (general/vision), `gemini-1.5-flash` (fast).
- OpenRouter (fronts many): match model name to provider above; set `OPENROUTER_API_KEY`.
- Azure OpenAI: same models but use `AZURE_OPENAI_*` vars + `--provider azure`.

# Usage Examples
- Orchestrator (OpenAI default):  
  `python multi-llm-orchestrator.py --provider openai --model gpt-4o --prompt "Hello"`  
  Swap provider/model as needed: `--provider groq --model mixtral-8x7b`, `--provider openrouter --model claude-3-haiku`.
- Multi-Modal chat:  
  `python Multi-Modal.py --task chat --provider openai --model gpt-4o-mini --message "Summarize this repo"`  
  Transcription: `python Multi-Modal.py --task transcribe --provider groq --model whisper-large-v3 --audio-path input.mp3`
- Transcribe driver:  
  `python transcribe/transcribe-analyze-local.py --backend groq --audio path/to/file.mp3 --model whisper-large-v3`  
  OpenAI alt: `python transcribe/transcribe-analyze-local.py --backend openai --audio file.mp3 --model whisper-1`
- Vision describe:  
  `python gpt-vision-image-describer.py --image path/to/img.jpg --provider openai --model gpt-4o-mini`
- Image SEO batch:  
  `python openai-batch-image-seo-pipeline.py --input images/ --out seo.csv --model gpt-4o-mini --dry-run`
- TTS (example thinketh):  
  `python thinketh-tts-main.py --model gpt-4o-mini-tts --voice alloy --text "Sample"` (check `--help` for specific flags)

# Gotchas and Quick Checks
- Run `python <script> --help` first; many support `--dry-run`, `--preview`, or `--limit 1`.
- Watch provider limits: image size caps, batch size, token limits, and rate limits. Add retries if flags exist.
- Keep `.env` close (repo root or `$HOME`) so keys are auto-loaded; avoid passing keys on CLI history.
- Validate with a tiny sample before long runs; confirm output paths (`--out`, `--output-dir`) exist or are writable.
