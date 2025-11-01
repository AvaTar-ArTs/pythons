"""
Goapi

This module provides functionality for goapi.

Author: Auto-generated
Date: 2025-11-01
"""

import requests
import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)


load_dotenv()

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
