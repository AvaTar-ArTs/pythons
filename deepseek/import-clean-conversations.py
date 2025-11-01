"""
Data Processing Json Deepseek 12

This module provides functionality for data processing json deepseek 12.

Author: Auto-generated
Date: 2025-11-01
"""


import logging

logger = logging.getLogger(__name__)


# Constants
CONSTANT_160 = 160

#!/usr/bin/env python3
"""
Deepseek Importer v3
- Clean transcripts with ISO timestamps, attachments section, and fenced code handling.
- Collapsible raw JSON via <details>.
- Optional conversation grouping by year (tags include year).
"""
import argparse, datetime, json, re, yaml
from pathlib import Path

def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "-", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "item"
def to_iso(dt):
    if isinstance(dt, (int, float)):
        try: return datetime.datetime.fromtimestamp(dt).isoformat()
        except Exception: return ""
    if isinstance(dt, str):
        for fmt in ("%Y-%m-%d","%Y/%m/%d","%Y-%m-%d %H:%M","%Y-%m-%dT%H:%M:%S","%Y-%m-%dT%H:%M:%S.%fZ","%Y-%m-%dT%H:%M:%S%z"):
            try: return datetime.datetime.strptime(dt, fmt).isoformat()
            except Exception: continue
        return dt
    if isinstance(dt, datetime.datetime): return dt.isoformat()
    return ""

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_text(path: Path, s: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(s, encoding="utf-8")

def clean_fences(txt: str) -> str:
    return (txt or "").replace("```", "`\u200b``")

def render_user(user: dict) -> str:
    name = user.get("name") or user.get("username") or user.get("displayName") or "User"
    email = user.get("email") or user.get("mail") or ""
    bio = user.get("bio") or user.get("about") or user.get("summary") or ""
    created = user.get("created_at") or user.get("createdAt") or user.get("created") or ""
    updated = user.get("updated_at") or user.get("updatedAt") or ""
    fm = {
        "title": f"{name} • Profile",
        "description": f"Profile for {name}.",
        "tags": ["profile","deepseek"],
        "date": (created or datetime.date.today().isoformat()),
        "updated": (updated or datetime.datetime.now().isoformat(timespec="seconds")),
        "toc": True
    }
    parts = ["---", yaml.safe_dump(fm, sort_keys=False).strip(), "---", "", f"# {name}", ""]
    if bio: parts.append(bio.strip() + Path("\n"))
    parts.append("## Details")
    if email: parts.append(f"- **Email:** {email}")
    if created: parts.append(f"- **Created:** {created}")
    if updated: parts.append(f"- **Updated:** {updated}")
    extras = {k:v for k,v in user.items() if k not in {"name","username","displayName","email","mail","bio","about","summary","created_at","createdAt","created","updated_at","updatedAt"}}
    if extras:
        parts += ["", "<details><summary>Raw User JSON</summary>", "", "```json", json.dumps(extras, indent=2, ensure_ascii=False), "```", "</details>", ""]
    return Path("\n").join(parts)

def render_msg(m: dict) -> str:
    role = m.get("role") or m.get("sender") or m.get("from") or "user"
    ts = to_iso(m.get("timestamp") or m.get("created_at") or m.get("time") or "")
    txt = m.get("content") or m.get("text") or m.get("message") or ""
    if isinstance(txt, (dict, list)):
        txt = "```json\n" + json.dumps(txt, indent=2, ensure_ascii=False) + "\n```"
    attachments = m.get("attachments") or m.get("files") or []
    attach_md = []
    if isinstance(attachments, list) and attachments:
        attach_md.append("**Attachments**")
        for a in attachments:
            name = str(a.get("name") or a.get("filename") or a.get("url") or "file")
            url = a.get("url") or ""
            attach_md.append(f"- [{name}]({url})" if url else f"- {name}")
    body = f"**{role}** • {ts}\n\n{clean_fences(str(txt))}\n"
    if attach_md: body += Path("\n") + Path("\n").join(attach_md) + Path("\n")
    body += Path("\n---\n")
    return body

def render_conversation(conv: dict) -> str:
    cid = conv.get("id") or conv.get("_id") or conv.get("uuid") or ""
    title = conv.get("title") or conv.get("name") or (cid and f"Conversation {cid}") or "Conversation"
    created = conv.get("created_at") or conv.get("createdAt") or conv.get("start_time") or ""
    updated = conv.get("updated_at") or conv.get("updatedAt") or conv.get("last_activity") or ""
    year = (str(created)[:4] if created else None)
    tags = ["conversation","deepseek"]
    if year and year.isdigit(): tags.append(year)
    msgs = conv.get("messages") or conv.get("chat") or conv.get("history") or []
    if not msgs and isinstance(conv.get("data"), dict): msgs = conv["data"].get("messages", [])
    lines = [render_msg(m) for m in msgs]
    desc = conv.get("description") or (msgs and (str((msgs[0].get('content') if isinstance(msgs[0].get('content'), str) else ''))[:CONSTANT_160] + "…")) or "Conversation transcript."
    fm = {"title": title, "description": desc, "tags": tags, "date": (created or datetime.date.today().isoformat()), "updated": (updated or datetime.datetime.now().isoformat(timespec="seconds")), "toc": True}
    body = ["---", yaml.safe_dump(fm, sort_keys=False).strip(), "---", "", f"# {title}", "", "## Transcript", ""]
    body.append(Path("\n").join(lines) if lines else "_No messages found._\n")
    body += ["", "<details><summary>Raw Conversation JSON</summary>", "", "```json", json.dumps(conv, indent=2, ensure_ascii=False), "```", "</details>", ""]
    return Path("\n").join(body)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--conversations", required=True)
    ap.add_argument("--out", default="content")
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    user_data = read_json(Path(args.user))
    user_obj = user_data.get("user") if isinstance(user_data, dict) and isinstance(user_data.get("user"), dict) else (user_data if isinstance(user_data, dict) else {})
    write_text(out / "user-profile.md", render_user(user_obj))

    conv_data = read_json(Path(args.conversations))
    conversations = []
    if isinstance(conv_data, dict):
        if isinstance(conv_data.get("conversations"), list):
            conversations = conv_data["conversations"]
        else:
            for v in conv_data.values():
                if isinstance(v, list): conversations.extend(v)
    elif isinstance(conv_data, list):
        conversations = conv_data

    count = 0
    for conv in conversations:
        title = conv.get("title") or conv.get("name") or conv.get("id") or "conversation"
        slug = slugify(title)[:80] or "conversation"
        write_text(out / f"conversation-{slug}.md", render_conversation(conv))
        count += 1
    logger.info(f"Wrote user and {count} conversation pages to {out.resolve()}")

if __name__ == "__main__":
    main()
