"""Shared helpers for chat-based OpenAI interactions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional

from openai import OpenAI

# Constants
CONSTANT_512 = 512



@dataclass(frozen=True)
class ChatPrompt:
    system: str
    user_template: str


def render_user_prompt(template: str, *, variables: Mapping[str, Any]) -> str:
    """Format the user template with given variables, providing a helpful error."""

    try:
        return template.format(**variables)
    except KeyError as exc:
        missing = exc.args[0]
        raise ValueError(f"Missing template variable '{missing}' for user prompt") from exc


def run_chat_completion(
    client: OpenAI,
    *,
    system_prompt: str,
    user_prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: int = CONSTANT_512,
    extra_messages: Optional[Iterable[Dict[str, Any]]] = None,
) -> str:
    """Execute a chat completion request and return stripped content."""

    messages = [{"role": "system", "content": system_prompt}]
    if extra_messages:
        messages.extend(extra_messages)
    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

