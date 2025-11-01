"""
Download 29

This module provides functionality for download 29.

Author: Auto-generated
Date: 2025-11-01
"""

import httplib2
from googleapiclient.discovery import Resource, build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from .constants import (
    CLIENT_SECRETS_FILE,
    MISSING_CLIENT_SECRETS_MESSAGE,
    YOUTUBE_API_SCOPES,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)
from .utils import get_local_path


def get_authenticated_service() -> Resource:
    """get_authenticated_service function."""

    flow = flow_from_clientsecrets(
        get_local_path(CLIENT_SECRETS_FILE),
        scope=YOUTUBE_API_SCOPES,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
    )

    storage = Storage(get_local_path("creds-oauth2.json"))
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()),
    )
