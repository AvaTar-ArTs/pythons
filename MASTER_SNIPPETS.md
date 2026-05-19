# 🏆 AVATARARTS Master Code Snippets

This document contains the "Golden Versions" of frequently used functions across the 4,000+ scripts in this ecosystem. 

**Usage:** Use these snippets as the standard implementation for all new scripts.

---

## 🛠️ Decorators & Utilities

### 1. Robust Retry Decorator
*Extracted from: tools/core_shared_libs/coding_standards.py*
```python
from functools import wraps
import time
from typing import Callable, Any

def retry_decorator(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry function execution on failure."""
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
```

### 2. Performance Timing Decorator
```python
import time
from functools import wraps

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper
```

### 3. Environment Loader (.env.d)
```python
import os
from pathlib import Path

def load_env_d():
    """Load all .env files from ~/.env.d directory."""
    env_d_path = Path.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        if line.startswith("export "): line = line[7:]
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")
```

---

## 📸 Visual Intelligence Snippets

### 4. Advanced Text Overlay (Shadow Logic)
*Extracted from: media_processing/image/imagenarator.py*
```python
from PIL import ImageDraw

def draw_shadow_text(draw, position, text, font, text_color, shadow_color="black", thickness=2):
    """Draws text with a high-contrast multi-offset shadow border."""
    x, y = position
    # Draw shadow in 4 directions for thick border effect
    for i in range(1, thickness + 1):
        draw.text((x - i, y - i), text, font=font, fill=shadow_color)
        draw.text((x + i, y - i), text, font=font, fill=shadow_color)
        draw.text((x - i, y + i), text, font=font, fill=shadow_color)
        draw.text((x + i, y + i), text, font=font, fill=shadow_color)
    # Draw main text
    draw.text(position, text, font=font, fill=text_color)
```

---

*This library is a living document. Add new unique functional DNA as it is discovered.*
\n--- \n\n## 📦 The Avatar Core Module\nAll of the above snippets are now available in a single import:\n\n```python\nfrom avatar_utils import load_env_d, timing_decorator, get_unique_file_path\n```
