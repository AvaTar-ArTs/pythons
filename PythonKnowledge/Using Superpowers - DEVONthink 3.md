# Using Superpowers (DEVONthink 3 “Supreme Powers” Brainstorming)

Location: `/Users/steven/my-supremepowers/devonthink-using-superpowers.md`

This is an opinionated, creative-but-practical playbook for turning DEVONthink 3 into an **operating system for documents, research, and action**.

It includes:
- A “superpowers” catalog (capabilities)
- Concrete daily/weekly routines
- Recommended **Smart Rules** and **Script Menu** actions (based on the scripts you already have installed)
- A gap-bridge section: what people are asking for / trends, and how to cover the missing pieces

---

## 0) North Star

**DEVONthink’s superpower is not storing files. It’s converting messy inputs into retrievable knowledge with: search + metadata + automation + reuse.**

Your decision to **import** (not index) means DEVONthink becomes the “system of record.” That’s a great match for:
- consistent full‑text search
- stable links
- To Go sync
- long-term archival

---

## 1) The Supreme Powers (capabilities)

### SP1 — The Inbox that eats chaos
**Definition:** everything lands somewhere predictable, gets processed, and never disappears.

**Implementation:**
- Use an Inbox/Incoming group as your capture funnel.
- Process with Smart Rules + a daily manual review pass.

**Your installed automation that supports this:**
- Smart Rule script: **File Items.scpt** (auto-file based on `@GroupName` in title)

---

### SP2 — “Auto-file by @” (Evernote-like filing, but faster)
**Definition:** you can file a record without touching the mouse by naming it.

**Mechanic:** Name items like:
- `ACME contract renewal @Legal`
- `Paper - diffusion models @Reading`
- `Receipt - Delta @Finance`

Then run a Smart Rule (or batch process) using **File Items.scpt**:
- finds (or creates) group `Legal`, `Reading`, etc.
- moves the record
- optionally strips the `@...` suffix

**This is one of the highest ROI workflows in DEVONthink.**

---

### SP3 — Auto-tags from content (the “make it findable later” spell)
**Definition:** every imported doc gets a few decent tags with minimal effort.

**Your installed automation:**
- Smart Rule script: **Assign Tags.scpt**
  - extracts keywords
  - applies up to `pMaxTags` (default 5)
  - note: it also adds *parent groups* into tags (path-as-tags). If you don’t want that, we can tweak the script.

---

### SP4 — Research enrichment (DOI → full citation metadata)
**Definition:** PDFs become “smart papers” with title/authors/date/journal/DOI.

**Your installed automation:**
- Smart Rule script: **Download Bibliographic Metadata.scpt**
  - finds DOI
  - downloads JSON metadata
  - renames record to paper title
  - fills custom metadata fields (authors, journal, etc.)

**Use for:** academic papers, reports with DOIs, anything you’ll cite or revisit.

---

### SP5 — Time travel / tickler / remind me
**Definition:** you can defer attention without losing the item.

**Your installed automation:**
- Smart Rule scripts: **Remind Me Tomorrow.scpt**, **Remind Me Next Week.scpt**, **Remove Reminder.scpt**

**Pattern:**
- Add reminder metadata/date
- Smart Group “Due today/overdue” becomes your resurfacing engine

---

### SP6 — The “Everything is searchable” engine
**Definition:** scans, images, and PDFs behave like text.

**Mechanics (DT features):** OCR + indexing + PDF text extraction.
**Operational habit:** treat OCR as a *pipeline stage* (not a one-off action).

---

### SP7 — Visual orientation (favicons/thumbnails)
**Definition:** web captures and feeds become scannable lists.

**Your installed automation:**
- Smart Rule script: **Add Favicons.scpt**

---

### SP8 — Email that opens the original message (not a reply)
**Definition:** imported Mail messages can link back to Apple Mail.

**Your installed menu script:**
- **Set Email URL to Message ID.scpt**
  - converts URL to `message://...` so it opens the original in Mail

---

### SP9 — Integrity / safety spells (verify + optimize)
**Definition:** you trust the database.

**Your installed menu scripts include:**
- **Verify file integrity of databases**
- **Verify & Optimize Databases**

**Weekly habit:** run verify/optimize when the system is idle.

---

## 2) Daily / Weekly “Using Superpowers” routines

### Daily (10–20 min)
1. **Dump** anything into Inbox (don’t organize at capture time).
2. **Fast triage pass:**
   - rename with `@Destination` where obvious
   - add 1–3 manual tags for “project/context”
3. Run Smart Rules (or a batch process) in this order:
   1) **File Items** (move to correct group)
   2) **Assign Tags** (auto-keyword tags)
   3) Optional: **Add Favicons** for web captures
4. Scan a Smart Group like “Untagged” / “Unfiled” (we can create it).

### Weekly (30–60 min)
1. Maintenance:
   - Verify/Optimize database (idle time)
2. Research enrichment:
   - run **Download Bibliographic Metadata** on new papers
3. Review resurfaced items:
   - “Remind me next week” queue
   - overdue reminders

---

## 3) DEVONthink workflow playbook (opinionated defaults)

### Recommended high-level groups
- **00 Inbox** (or use DEVONthink’s Incoming group)
- **10 Projects**
- **20 Areas** (ongoing responsibilities: health, finances, family, etc.)
- **30 Research**
- **40 Reference**
- **90 Archive**

Minimal hierarchy. Lean on tags + smart groups.

### Recommended tag scheme (simple)
- `status/*` → `status/inbox`, `status/reading`, `status/done`, `status/waiting`
- `type/*` → `type/receipt`, `type/paper`, `type/contract`, `type/idea`
- `project/*` → active projects
- `topic/*` → your durable taxonomy

---

## 4) Smart Rules & Menu Scripts: what to use (your existing library)

### Smart Rules (you already have scripts for these)
- **Auto-file by @** → `File Items.scpt`
- **Auto-tag** → `Assign Tags.scpt`
- **Enrich papers** → `Download Bibliographic Metadata.scpt`
- **Add favicons** → `Add Favicons.scpt`
- **Tickler** → `Remind Me Tomorrow/Next Week`

### Menu scripts (high value)
- **Set Email URL to Message ID** (fix email URLs)
- **Verify/Optimize** (maintenance)

---

## 5) “Bridge the gap”: trends + what people are asking for (and how to cover it)

### Observed trend themes (from DEVONtechnologies Community “Latest”)
The forum’s latest topics show recurring demand around:
- **Automation rules** (e.g. date-change rules, scripting edge cases)
- **Markdown workflows** (creating/handling Markdown notes on Mac + To Go)
- **PDF annotation issues** and interoperability with other PDF apps
- **Email import** errors and best practices
- **Search syntax / ranking** (diacritics, ordering, field memory cleanup)
- **AI + PKM** (users exploring AI-wiki style navigation and “what would you do with an MCP server?”)
- **Sync/mobile** feature requests (To Go chat enhancements, UI requests)

### Gap: “I want DEVONthink to behave like a modern AI PKM assistant”
**Bridge:** create an internal “AI Wiki” inside DEVONthink:
- One “Home” Markdown note that links to:
  - Projects
  - Areas
  - Research maps
  - Smart Groups (Saved Searches)
- Use consistent tags and create Smart Groups that act like “dynamic pages”.

### Gap: “Better capture + cleaner metadata automatically”
**Bridge:**
- Standardize naming patterns (`@Destination`, date prefixes)
- Run **Assign Tags** + (optional) a custom tag normalizer (we can write)

### Gap: “Mobile friction (To Go) — can’t do heavy automation there”
**Bridge:**
- Make mobile capture lightweight:
  - tag with `status/inbox`
  - minimal naming
- Let Mac run the heavy Smart Rules during the next sync.

---

## 6) Creative “superpowers” you can add next (we can implement)

### New Superpower ideas (high ROI)
1. **The Naming Standardizer**
   - rename PDFs as `YYYY-MM-DD — Title — Source`
2. **The Receipt Wizard**
   - detect amounts/dates/vendors and fill custom metadata
3. **The Reading Queue Builder**
   - smart group: PDFs tagged `status/reading` sorted by date added
4. **The “Project Radar” Dashboard**
   - per-project smart group: `tag:project/X AND (unread OR modified:last 14 days)`
5. **The “Link Hygiene” routine**
   - find dead links, missing URLs, web archives

---

## 7) Operational safety notes
- Importing means your database is precious: ensure backups.
- If your database lives on an external volume, avoid unplugging while DT is open.
- Run Verify/Optimize periodically.

---

## Appendix A — Evidence: scripts confirmed on your Mac
These scripts were found in:
- `/Users/steven/Library/Application Scripts/com.devon-technologies.think3/Smart Rules/`
- `/Users/steven/Library/Application Scripts/com.devon-technologies.think3/Menu/`

And were decompiled to readable AppleScript under:
- `/Users/steven/tmp/devonthink_scripts/extracted/`
