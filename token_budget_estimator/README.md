# Token & budget estimator (batch prompts)

**Why it’s unique:** Buyers batch LLM work but **fear bill shock**. This CLI estimates **input tokens** (tiktoken when installed, rough fallback otherwise) and prints **rough USD** using editable default price tables—*before* any API calls.

## Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python3 token_estimator.py prompts.txt --model-hint gpt-4o-mini
python3 token_estimator.py jobs.jsonl -o per_prompt.csv
```

**Listing angle:** “Know your batch cost before you spend—prompt file in, token + USD table out.”

**Disclaimer:** Dollar amounts use **example** `DEFAULT_PRICES` in the script—**update** for current provider pricing before selling.
