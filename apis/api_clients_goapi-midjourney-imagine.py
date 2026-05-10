# Load API keys from ~/.env.d/ (best practice - handles export statements, quotes, comments)
from pathlib import Path as PathLib

def load_env_d():
    """Load all .env files from ~/.env.d directory (sophisticated pattern from youtube-load.py)"""
    env_d_path = PathLib.home() / ".env.d"
    if env_d_path.exists():
        for env_file in env_d_path.glob("*.env"):
            try:
                with open(env_file) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            # Handle export statements
                            if line.startswith("export "):
                                line = line[7:]
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            # Skip source statements
                            if not key.startswith("source"):
                                os.environ[key] = value
            except Exception as e:
                # Logger not initialized yet, use print
                print(f"Warning: Error loading {env_file}: {e}")

load_env_d()

# Also load from ~/.env as fallback using dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.expanduser("~/.env"))
except ImportError:
    pass

import requests
import os
from dotenv import load_dotenv

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# load_dotenv()  # Now using ~/.env.d/

X_API_KEY = os.getenv("GOAPI_API_KEY")

endpoint = "https://api.goapi.ai/mj/v2/imagine"

headers = {"X-API-KEY": X_API_KEY}

data = {
    "prompt": "Wraith, a master of stealth and assassination, moves unseen through the Rogue Isles, his blades ﬁnding marks unseen until it's too late. His tale is one of vengeance and shadow, as he cuts a silent path through his enemies, from the treacherous jungles of Mercy Island to the dark alleys of St. Martial. Wraith's journey explores the depths of the Stalker's path, where invisibility and the element of surprise are wielded with deadly precision, illustrating that the most formidable threats are those unseen.",
    "aspect_ratio": "9:16",
    "process_mode": "mixed",
    "webhook_endpoint": "",
    "webhook_secret": "",
}

response = requests.post(endpoint, headers=headers, json=data)

logger.info(response.status_code)
logger.info(response.json())
