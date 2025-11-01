"""
Youtube Test Authentication

This module provides functionality for youtube test authentication.

Author: Auto-generated
Date: 2025-11-01
"""

import google_auth_oauthlib.flow

import logging

logger = logging.getLogger(__name__)


CLIENT_SECRETS_FILE = "client_secret.json"  # Ensure this file is in the same folder
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def test_authentication():
    """Tests OAuth authentication with YouTube."""
    try:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES
        )
        credentials = flow.run_local_server(port=0)
        logger.info("✅ Authentication successful!")
    except Exception as e:
        logger.info("❌ Authentication failed:", str(e))


if __name__ == "__main__":
    test_authentication()
