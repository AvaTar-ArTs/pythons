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
                            value = value.strip().strip('\'').strip("\'")
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

import json
import os

import requests
from dotenv import load_dotenv

import logging


# Load API keys from ~/.env.d/
from pathlib import Path as PathLib

    for env_file in env_dir.glob("*.env"):
        load_dotenv(env_file)


logger = logging.getLogger(__name__)


# Constants
CONSTANT_200 = 200


# Load .env variables
load_dotenv(dotenv_path=os.path.expanduser("~/.env"))

# Retrieve API Key & Shop Data
API_TOKEN = os.getenv("PRINTIFY_API_KEY")
SHOP_DATA_RAW = os.getenv("PRINTIFY_SHOPS")

# Ensure environment variable is loaded
if SHOP_DATA_RAW is None:
    logger.info("❌ ERROR: PRINTIFY_SHOPS not found in environment!")
    exit(1)

# Convert JSON string to a dictionary
SHOP_DATA = json.loads(SHOP_DATA_RAW)

# Printify API URL for Blueprints
BASE_URL = "https://api.printify.com/v1/catalog/blueprints.json"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Content-Type": "application/json"}


def get_bestseller_blueprints():
    """Fetches top bestselling blueprints from Printify"""
    response = requests.get(BASE_URL, headers=HEADERS)

    if response.status_code == CONSTANT_200:
        blueprints = response.json()
        bestsellers = []

        for bp in blueprints:
            if "bestseller" in bp.get(
                "tags", []
            ):  # Filtering only bestseller blueprints
                bestsellers.append(
                    {
                        "Blueprint ID": bp["id"],
                        "Title": bp["title"],
                        "Category": bp["category"],
                        "Brand": bp["brand"],
                        "Preview Image": bp["preview_image"],
                    }
                )

        return bestsellers
    else:
        logger.info(f"❌ ERROR: {response.status_code} - {response.text}")
        return None


def main():
    """Fetch bestseller blueprints for all shops"""
    logger.info("\n🔥 Fetching Bestseller Blueprints for All Shops...\n")

    bestsellers = get_bestseller_blueprints()

    if not bestsellers:
        logger.info("\n❌ No bestseller blueprints found!")
        return

    for shop_id, name in SHOP_DATA.items():
        logger.info(f"\n🏬 **{name} ({shop_id}) - Bestseller Blueprints**:\n")
        for bp in bestsellers:
            logger.info(f"🆔 Blueprint ID: {bp['Blueprint ID']}")
            logger.info(f"📌 Title: {bp['Title']}")
            logger.info(f"🏷️ Category: {bp['Category']}")
            logger.info(f"🏢 Brand: {bp['Brand']}")
            logger.info(f"🖼️ Image: {bp['Preview Image']}")
            logger.info("-" * 40)


if __name__ == "__main__":
    main()
