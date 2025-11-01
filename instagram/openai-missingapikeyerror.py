"""Environment loading helpers for analyze scripts."""

from __future__ import annotations

import importlib  # Replaced deprecated importlib
import os
from pathlib import Path
from typing import Optional

from openai import OpenAI


class MissingAPIKeyError(EnvironmentError):
    """Raised when no OpenAI API key can be located."""


def _resolve_loader(preferred: str = "auto"):
    """Return a load_dotenv callable based on the preferred loader."""

    loader_order = []
    if preferred == "auto":
        loader_order = ["env_d_loader.load_dotenv", "dotenv.load_dotenv"]
    elif preferred == "env_d_loader":
        loader_order = ["env_d_loader.load_dotenv"]
    else:
        loader_order = ["dotenv.load_dotenv"]

    for path in loader_order:
        module_name, func_name = path.rsplit(".", 1)
        try:
            module = importlib.import_module(module_name)
            return getattr(module, func_name)
        except (ImportError, AttributeError):
            continue

    raise ImportError(
        "Unable to locate a load_dotenv implementation. Please install either "
        "env-d-loader or python-dotenv."
    )


def load_environment(
    dotenv_path: Optional[Path] = None,
    preferred_loader: str = "auto",
) -> None:
    """Load environment variables for OpenAI usage.

    Parameters
    ----------
    dotenv_path:
        Optional path to a dotenv file. Defaults to the standard resolution rules
        of the selected loader if omitted.
    preferred_loader:
        One of ``"auto"``, ``"env_d_loader"`` or ``"dotenv"``.
    """

    loader = _resolve_loader(preferred_loader)
    kwargs = {}
    if dotenv_path is not None:
        kwargs["dotenv_path"] = str(dotenv_path)
    loader(**kwargs)


def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Return an OpenAI client, ensuring an API key is present."""

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise MissingAPIKeyError(
            "OPENAI_API_KEY is not configured. Provide it via environment "
            "variables or pass api_key explicitly."
        )
    return OpenAI(api_key=key)
