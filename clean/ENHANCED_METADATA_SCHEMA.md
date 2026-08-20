# Enhanced Metadata Schema for Document Inventory

## Overview

This schema extends the basic `doc-source-evolved.py` output (4 columns) with intelligent analysis, relationships, and business intelligence from AutoTagger and MCP integration (20+ columns).

---

## Column Categories

### A. Basic Inventory (from doc-source-evolved.py)
Original output that remains as foundation:

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `filename` | string | `How-To.md` | Original filename |
| `file_size` | string | `4.37 KB` | Human-readable size |
| `creation_date` | string | `05-11-26` | File creation date (MM-DD-YY) |
| `original_path` | string | `/Users/steven/my-supremepowers` | Directory containing file |

---

### B. File Type & Classification (from autotagger-lite)

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `file_extension` | string | `.md` | File extension |
| `category` | string | `markdown` | Auto-detected category (14 types) |
| `primary_type` | string | `documentation` | Primary classification |
| `mime_type` | string | `text/markdown` | MIME type for file |
| `encoding` | string | `utf-8` | Text encoding detected |

**Categories Available**:
- Programming: `python`, `javascript`, `typescript`, `shell`, `java`, `c`, `cpp`, `rust`, `go`
- Markup: `markdown`, `html`, `xml`, `yaml`, `json`
- Data: `csv`, `tsv`, `sql`, `config`
- Documents: `pdf`, `doc`, `docx`, `txt`, `odt`
- Media: `image`, `audio`, `video`
- Web: `css`, `scss`, `less`
- Archive: `zip`, `tar`, `gz`
- Other: `binary`, `unknown`

---

### C. Content Analysis (from v3-dev autotagger)

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `intelligent_category` | string | `architecture`, `skill`, `agent-definition` | AI-assigned semantic category |
| `confidence_score` | float | 0.92 | Confidence in categorization (0-1) |
| `description` | string | "Infrastructure patterns for superpowers ecosystem" | Generated description |
| `key_concepts` | string (csv) | "agents,skills,hooks,orchestration" | Extracted key terms |
| `content_hash` | string | `a1b2c3d4e5f6...` | SHA256 hash for change detection |
| `lines_of_code` | integer | 1200 | Line count (if code/text) |
| `complexity_score` | float | 0.65 | Code/content complexity (0-1) |

---

### D. Business Intelligence (from v3-dev/v6)

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `predicted_business_value` | float | 8.5 | Business value score (0-10) |
| `integration_potential` | boolean | true | Has integration with other tools |
| `integration_targets` | string (csv) | `agents,mcp-server,hooks` | What it could integrate with |
| `estimated_effort` | string | `medium` | Implementation effort: `low/medium/high` |
| `maturity_level` | string | `production` | `experimental/alpha/beta/production` |
| `roi_potential` | float | 7.2 | Return-on-investment potential (0-10) |

---

### E. Ecosystem Integration (from MCP analysis)

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `agent_affinity` | string (csv) | `frontend-architect,backend-architect` | Relevant agents |
| `skill_affinity` | string (csv) | `brainstorming,test-driven-development` | Relevant skills |
| `command_related` | string (csv) | `activate-agents,list-skills` | Related MCP commands |
| `dependencies` | string (csv) | `core/orchestration,lib/agent-loader` | Files it depends on |
| `dependents` | string (csv) | `mcp-server/tools,extensions/supremepower` | Files that depend on it |
| `agent_tier` | string | `Tier-0-Canonical` | Agent/skill tier if applicable |

---

### F. Change Tracking (from autotagger-lite)

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `last_modified` | string | `05-11-26 22:41` | Last modification timestamp |
| `modification_count` | integer | 5 | Number of changes since baseline |
| `moved_from` | string | `/old/location/file.md` | Previous path if moved |
| `status` | string | `stable` | `new/modified/stable/deleted` |
| `last_scan_date` | string | `05-11-26` | Date of last inventory scan |

---

### G. Quality Metrics (from content analysis)

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `documentation_score` | float | 0.88 | Quality of documentation (0-1) |
| `test_coverage` | float | 0.75 | Code test coverage if applicable |
| `code_standards` | string | `compliant` | `compliant/warnings/violations` |
| `security_score` | float | 0.95 | Security analysis result (0-1) |
| `accessibility_score` | float | 0.82 | Accessibility compliance (0-1) |

---

### H. Relationship & Metadata

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `related_files` | string (csv) | `CHANGELOG.md,ARCHITECTURE.md` | Similar/related files |
| `tags` | string (csv) | `core,production,critical` | User/system tags |
| `ownership` | string | `backend-architect` | Responsible team/agent |
| `last_reviewed` | string | `04-15-26` | Last review date |
| `review_status` | string | `approved` | `pending/approved/needs-update` |

---

## Full Schema Example

```csv
filename,file_size,creation_date,original_path,file_extension,category,primary_type,mime_type,intelligent_category,confidence_score,description,key_concepts,content_hash,lines_of_code,complexity_score,predicted_business_value,integration_potential,integration_targets,estimated_effort,maturity_level,roi_potential,agent_affinity,skill_affinity,command_related,dependencies,dependents,agent_tier,last_modified,modification_count,moved_from,status,documentation_score,test_coverage,code_standards,security_score,accessibility_score,related_files,tags,ownership,last_reviewed,review_status

activate-agents.ts,3.5 KB,05-11-26,/Users/steven/my-supremepowers/mcp-server/src/tools,ts,typescript,code,text/typescript,mcp-tool,0.95,"MCP tool for agent activation based on user message",agents;mcp;orchestration;activation,a1b2c3d4...,75,0.42,9.2,true,agents;skills;commands,low,production,8.8,studio-coach;backend-architect,agent-creation-guidance;agent-development,handleActivateAgents,core/orchestration;lib/agent-loader,extensions/supremepower;tests,Tier-0-Canonical,05-11-26 22:41,3,,stable,0.85,0.88,compliant,0.98,0.92,fetch-skills.ts;list-skills.ts,core;production;critical,studio-coach,05-10-26,approved

How-To.md,4.37 KB,05-11-26,/Users/steven/my-supremepowers,md,markdown,documentation,text/markdown,architecture-guide,0.88,"Architecture and governance guidance for superpowers ecosystem",architecture;governance;patterns;tiers,e5f6g7h8...,120,0.35,8.1,true,skills;agents;hooks,medium,production,7.9,system-architect;xeo-strategist,writing-plans;brainstorming,activate-agents;list-skills,CLAUDE.md;CHANGELOG.md,all skills,Tier-0-Canonical,05-11-26 22:15,12,,stable,0.92,n/a,compliant,0.95,0.88,CLAUDE.md;README.md;ROADMAP.md,documentation;governance,system-architect,05-10-26,approved

test-driven-development.md,8.5 KB,05-08-26,/Users/steven/my-supremepowers/skills/test-driven-development,md,markdown,documentation,text/markdown,skill-definition,0.91,"Skill module defining TDD workflow: Red-Green-Refactor",skill;tdd;workflow;testing,i9j0k1l2...,280,0.38,8.6,true,agents;commands;hooks,low,production,8.2,test-writer-fixer;code-reviewer,test-driven-development;verification-before-completion,handleActivateAgents,SKILL.md;metadata.json,extensions/supremepower,Tier-0-Canonical,05-11-26 22:30,8,,stable,0.89,n/a,compliant,0.96,0.90,brainstorming.md;verification-before-completion.md,core;production;skill,test-writer-fixer,05-11-26,approved
```

---

## Data Population Strategy

### Phase 1: Auto-Population
- ✅ Columns A, B: Automatically extracted by doc-source-evolved.py + autotagger-lite
- ✅ Columns C, D: Generated by v3-dev intelligent analysis
- ✅ Columns E (partial): MCP server introspection
- ✅ Columns F: autotagger-lite historical tracking
- ✅ Columns G (partial): Static analysis tools (ESLint, pytest, etc.)

### Phase 2: Manual/Semi-Automatic
- ⚠️ Columns H: User tagging, team assignment
- ⚠️ Quality scores: Review-based adjustments
- ⚠️ Ownership: Team assignment

### Phase 3: Continuous Updates
- 🔄 Change tracking (F): Auto-updated on each scan
- 🔄 Confidence scores: Re-calculated as content changes
- 🔄 Dependents: Updated when files are created/modified

---

## Implementation Notes

### Size Normalization
All `*_size` columns converted to consistent units (bytes, with human-readable variant in separate column):
- `file_size_bytes`: 4567
- `file_size`: "4.56 KB"

### Score Normalization
All scoring systems normalized to 0-1.0 range for consistency:
- `confidence_score`: 0.0 to 1.0 (categorical confidence)
- `complexity_score`: 0.0 to 1.0 (code/content complexity)
- `business_value`: 0.0 to 1.0 (converted from 0-10 scale)
- `documentation_score`: 0.0 to 1.0 (quality rating)

### Relationship Handling
All relationship columns use comma-separated values with minimal whitespace:
- `dependencies`: `file1.js,file2.js,dir/file3.py` (no spaces)
- `related_files`: `CHANGELOG.md,README.md`
- `agent_affinity`: `agent-1,agent-2,agent-3`

### Datetime Format
All dates/timestamps use ISO 8601 with local timezone:
- Date only: `05-11-26` (MM-DD-YY)
- Date+Time: `05-11-26 22:41` (MM-DD-YY HH:MM)
- Full: `2026-05-11T22:41:35+00:00`

---

## Benefits of Enhanced Schema

| Benefit | Enabled By | Use Case |
|---------|-----------|----------|
| **Intelligent Navigation** | Categories A-E | Find related files, understand purpose |
| **Impact Analysis** | Columns E (dependencies) | Change what breaks? |
| **Team Ownership** | Column H (ownership) | Who's responsible? |
| **Priority Selection** | Column D (business value) | What to work on first? |
| **Change Tracking** | Column F | What changed? When? Why? |
| **Quality Assurance** | Column G | Is this production-ready? |
| **Integration Planning** | Column D (integration targets) | What can we connect? |
| **Knowledge Discovery** | Column E (agent/skill affinity) | Which agents/skills apply? |
| **Compliance/Audit** | Columns G-H | Are we following standards? |
| **Strategic Planning** | Columns D-E (ROI, effort) | Should we build/buy/partner? |

---

## CSV Export Format

Final CSV will be optimized for:
- ✅ Excel/Google Sheets import (all columns string or numeric)
- ✅ AirTable database import (field type mapping)
- ✅ JavaScript/Python analysis (clean headers, consistent formatting)
- ✅ SQL import (normalizable schema)
- ✅ Power BI/Looker visualization (numeric KPIs normalized)

