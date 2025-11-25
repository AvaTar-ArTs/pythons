# AI API Keys Inventory (Sanitized)

This inventory lists where AI- and cloud-related API keys are stored and their current status. All secret values have been removed from version control and should live only in private environment files or secret managers.

## LLM / Text Generation Services
- **OpenAI:** Active; keys stored in `~/.env.d/llm-apis.env`, `~/.env.d/MASTER_CONSOLIDATED.env`, `~/.secrets/.ai-apis.env`, `~/.config/fabric/.env`, and `~/.codex/.env`. Values redacted.
- **Anthropic (Claude):** Active; multiple keys across `~/.env.d/llm-apis.env`, `~/.env.d/MASTER_CONSOLIDATED.env`, `~/.secrets/.ai-apis.env`, `~/.codex/.env`. Values redacted.
- **XAI (Grok):** Active; keys stored in `~/.env.d/.grok/settings.json`, `~/.secrets/.ai-apis.env`, `~/.codex/.env`. Values redacted.
- **Groq:** Active; keys stored in `~/.env.d/llm-apis.env`, `~/.secrets/.ai-apis.env`, `~/.config/fabric/.env`, `~/.codex/.env`. Values redacted.
- **Perplexity:** Active; keys stored in `~/.env.d/llm-apis.env`, `~/.codex/.env`. Values redacted.
- **Gemini (Google):** Active; keys stored in `~/.env.d/llm-apis.env`, `~/.env.d/gemini.env`, `~/.codex/.env`. Values redacted.
- **DeepSeek:** Active; keys stored in `~/.env.d/llm-apis.env`, `~/.secrets/.ai-apis.env`. Values redacted.
- **Mistral:** Active; keys stored in `~/.env.d/llm-apis.env`, `~/.config/fabric/.env`, `~/.codex/.env`. Values redacted.
- **Cohere:** Active; keys stored in `~/.env.d/llm-apis.env`. Values redacted.
- **OpenRouter:** Active; key stored in `~/.env.d/llm-apis.env`. Values redacted.
- **Together AI:** Active; key stored in `~/.env.d/llm-apis.env`. Values redacted.
- **Cerebras:** Active; key stored in `~/.env.d/llm-apis.env`. Values redacted.
- **HuggingFace:** Active; key stored in `~/.codex/.env`. Values redacted.
- **Venice AI:** Active; key stored in `~/.config/fabric/.env`. Values redacted.
- **Silicon Cloud:** Active; key stored in `~/.config/fabric/.env`. Values redacted.
- **AIML API:** Active; key stored in `~/.config/fabric/.env`. Values redacted.

## IDE / Development Tools
- **Cursor:** Active; token stored in `~/.config/Cursor/User/settings.json`. Value redacted.
- **Copilot / GH extensions:** Active; tokens stored within local tool configs. Values redacted.

## Media / Vision Services
- **Leonardo.Ai, Midjourney, Ideogram, Imagga:** Active; credentials stored in `~/.codex/.env` or corresponding config files. Values redacted.
- **ElevenLabs, Stability, Suno, Pexels, Imgur:** Active; credentials stored in `~/.codex/.env` or service-specific env files. Values redacted.

## Cloud / Infrastructure
- **Azure OpenAI:** Active; key stored in `~/.env.d/MASTER_CONSOLIDATED.env`. Value redacted.
- **AWS:** Active; keys stored in `~/.codex/.env`. Values redacted.

## Other Services
- **Ngrok:** Active; tokens stored in `~/.codex/.env`. Values redacted.
- **GitHub:** Active; token stored in `~/.config/cursor-agent/config.json`. Value redacted.

## Notes
- Keep all secrets in environment files or a secret manager; never commit raw keys to the repository.
- If new keys are added, record only locations and statuses here—omit or mask the actual values.
- Regenerate this document after secret rotations, ensuring outputs are scrubbed before committing.
