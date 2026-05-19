"""
Summary of avatar_utils.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import os
import time
from pathlib import Path
from functools import wraps
from typing import Callable, Tuple, Union
from datetime import datetime

# --- Configuration & Environment ---


def load_env_d():
    """
    Standardizes loading of environment variables from ~/.env.d directory.
    Handles 'export' statements and strips quotes automatically.
    """
    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            os.environ[key.strip()] = (
                                value.strip().strip('"').strip("'")
                            )
            except Exception as e:
                print(f"Warning: Error loading {env_file}: {e}")


# --- Decorators ---


def timing_decorator(func):
    """Measures and prints function execution time."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result

    return wrapper


def retry_decorator(max_retries: int = 3, delay: float = 1.0):
    """Retries function execution on failure with a configurable delay."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator


# --- File & Directory Operations ---


def get_unique_file_path(base_path: Union[str, Path]) -> Path:
    """Prevents file overwrites by appending a counter if the file exists."""
    path = Path(base_path)
    if not path.exists():
        return path
    base, ext = path.stem, path.suffix
    counter = 1
    while True:
        new_path = path.parent / f"{base}_{counter}{ext}"
        if not new_path.exists():
            return new_path
        counter += 1


def get_creation_date(filepath: Union[str, Path]) -> str:
    """Returns formatted creation date of a file."""
    try:
        path = Path(filepath)
        return datetime.fromtimestamp(path.stat().st_ctime).strftime("%m-%d-%y")
    except Exception:
        return "Unknown"


# --- Visual Intelligence (PIL required) ---


def draw_shadow_text(
    draw,
    position: Tuple[int, int],
    text: str,
    font,
    text_color,
    shadow_color="black",
    thickness: int = 2,
):
    """Draws text with a high-contrast multi-offset shadow border."""
    x, y = position
    for i in range(1, thickness + 1):
        draw.text((x - i, y - i), text, font=font, fill=shadow_color)
        draw.text((x + i, y - i), text, font=font, fill=shadow_color)
        draw.text((x - i, y + i), text, font=font, fill=shadow_color)
        draw.text((x + i, y + i), text, font=font, fill=shadow_color)
    draw.text(position, text, font=font, fill=text_color)


# --- UI & Feedback ---


def print_header(text: str, width: int = 80):
    """Prints a standardized, visible CLI header."""
    print(f"\n{'=' * width})")
    print(f"{text.center(width)})")
    print(f"{'=' * width}\n")
