"""
Sheets

This module provides functionality for sheets.

Author: Auto-generated
Date: 2025-11-01
"""

# Constants
CONSTANT_100 = 100

#!/usr/bin/env python3
"""
Google Sheets helpers using gspread.
Supports OAuth Installed App (client_secret.json) or Service Account (service_account.json).

Functions:
- ensure_worksheet(spreadsheet, title) -> Worksheet
- replace_rows(worksheet, fieldnames, rows)
- append_unique_by_key(worksheet, fieldnames, rows, unique_key='songLink')

The worksheet will have header row = fieldnames in order.
"""

from __future__ import annotations
import os
from typing import List, Dict, Optional
import gspread
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google.oauth2.credentials import Credentials as UserCredentials
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _load_client() -> gspread.Client:
    """
    Priority:
      1) service_account.json
      2) token.json (OAuth) + client_secret.json if refresh needed
      3) client_secret.json (start OAuth flow if token missing)
    """
    if os.path.exists("service_account.json"):
        creds = ServiceAccountCredentials.from_service_account_file(
            "service_account.json", scopes=SCOPES
        )
        return gspread.authorize(creds)

    token_path = "token.json"
    client_secret = "client_secret.json"
    creds = None
    if os.path.exists(token_path):
        creds = UserCredentials.from_authorized_user_file(token_path, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    if not creds:
        if not os.path.exists(client_secret):
            raise FileNotFoundError(
                "No credentials found. Provide service_account.json or client_secret.json (OAuth)."
            )
        # Run local OAuth flow
        import google.auth.transport.requests
        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)


def open_spreadsheet(sheet_id: str):
    """open_spreadsheet function."""

    gc = _load_client()
    return gc.open_by_key(sheet_id)

    """ensure_worksheet function."""


def ensure_worksheet(spreadsheet, title: str):
    try:
        ws = spreadsheet.worksheet(title)
    except gspread.exceptions.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=title, rows=CONSTANT_100, cols=20)
    return ws
    """set_header function."""


def set_header(ws, fieldnames: List[str]):
    ws.resize(rows=1)  # keep header row only
    ws.update("A1", [fieldnames])


def replace_rows(ws, fieldnames: List[str], rows: List[Dict[str, str]]):
    """Replace entire worksheet content with header + rows."""
    set_header(ws, fieldnames)
    if not rows:
        return
    values = [[r.get(k, "") for k in fieldnames] for r in rows]
    ws.append_rows(values, value_input_option="USER_ENTERED")


def append_unique_by_key(
    ws, fieldnames: List[str], rows: List[Dict[str, str]], unique_key: str = "songLink"
):
    """Append only new rows by unique_key (default: songLink)."""
    existing = ws.get_all_records()  # list of dicts
    seen = set()
    for r in existing:
        val = r.get(unique_key, "")
        if val:
            seen.add(val)

    to_add = []
    for r in rows:
        keyval = r.get(unique_key, "")
        if keyval and keyval not in seen:
            to_add.append([r.get(k, "") for k in fieldnames])
            seen.add(keyval)

    if to_add:
        ws.append_rows(to_add, value_input_option="USER_ENTERED")
