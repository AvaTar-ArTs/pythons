#!/usr/bin/env python3
"""Compatibility entry point delegating to the repository's canonical launcher."""
from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "pythons_sort.py"), run_name="__main__")
