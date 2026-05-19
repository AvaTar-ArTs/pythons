"""
Summary of createdb.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

from tinydb import TinyDB

db = TinyDB("log/db.json")
table = db.table("created_videos")
table.insert({"url": "www.example.com", "id": "00"})
