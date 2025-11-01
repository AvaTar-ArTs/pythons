"""Lightweight JSON configuration loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_json_config(path: Path) -> Dict[str, Any]:
    """Load a JSON config file, raising a helpful error on failure."""

    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Config file not found: {path}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in config file {path}: {exc}") from exc

