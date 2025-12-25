---
name: obsidian-librarian
description: Manages the Kingdom's Knowledge in Obsidian. Reads/writes notes, manages Daily Notes, and creates bi-directional links.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.0.0"
  category: memory-management
  author: AFO Kingdom
  vault_path: "~/Documents/Obsidian/AFO_Vault"
  philosophy_scores:
    truth: 96
    goodness: 98
    beauty: 95
    serenity: 99
allowed-tools:
  - mcp__afo-obsidian-mcp__read_note
  - mcp__afo-obsidian-mcp__write_note
  - mcp__afo-obsidian-mcp__search_notes
  - mcp__afo-obsidian-mcp__apply_template
---

# AFO Obsidian Librarian

The Royal Library of the AFO Kingdom, managing all knowledge in Obsidian with bi-directional linking and templates.

## Capabilities

| Capability | Description |
|------------|-------------|
| `read_note` | Read a note by path or title |
| `write_note` | Create or update a note |
| `search_notes` | Full-text search across vault |
| `append_daily_log` | Add entry to today's daily note |
| `link_notes` | Create bi-directional links |
| `get_backlinks` | Find all notes linking to a target |
| `apply_template` | Apply a template to create structured notes |

## Templates

### Daily Note Template
```markdown
---
date: {{date}}
tags: [daily, log]
---

# {{date:YYYY-MM-DD}}

## Morning Intentions
-

## Tasks
- [ ]

## Evening Reflection
-

## Trinity Score:
```

### Project Template
```markdown
---
project: {{title}}
status: active
created: {{date}}
tags: [project]
---

# {{title}}

## Overview

## Goals

## Progress Log

## Related
- [[]]
```

## Usage

```python
# Read a note
note = await librarian.read_note("Projects/AFO Kingdom.md")

# Write a note
await librarian.write_note(
    path="Daily/2025-12-25.md",
    content="# Christmas Day\n\n- Completed Phase 16",
    template="daily"
)

# Search notes
results = await librarian.search_notes("Trinity Score")

# Get backlinks
backlinks = await librarian.get_backlinks("AFO Kingdom")
```

## Integration with Context7

Notes can be indexed into Context7 for LLM context injection:
1. Notes are chunked and embedded
2. Stored in Qdrant vector database
3. Retrieved during RAG queries
