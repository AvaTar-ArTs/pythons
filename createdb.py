"""
Createdb

This module provides functionality for createdb.

Author: Auto-generated
Date: 2025-11-01
"""

from tinydb import Query, TinyDB

db = TinyDB("log/db.json")
table = db.table("created_videos")
table.insert({"url": "www.example.com", "id": "00"})
