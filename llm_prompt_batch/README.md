# LLM Prompt Batch Runner

**Gap filled:** Searches like “run OpenAI prompts from file” / “batch ChatGPT API python” return **notebooks and broken snippets**—few clean CLIs you can sell as a product.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."
```

## Usage

**Plain text** — one prompt per line:

```bash
python3 run_prompts.py prompts.txt -o results.jsonl --model gpt-4o-mini
```

**Dry run** (no API key):

```bash
python3 run_prompts.py prompts.txt --dry-run
```

**JSONL** input — each line `{"prompt": "..."}`:

```bash
python3 run_prompts.py jobs.jsonl -o out.jsonl
```

## Listing copy angle

“Batch LLM runner: file in → JSONL out, minimal deps, your API key stays local.”
