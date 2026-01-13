from tinydb import Query, TinyDB

db = TinyDB("log/db.json")
table = db.table("created_videos")
table.insert({"url": "www.example.com", "id": "00"})
