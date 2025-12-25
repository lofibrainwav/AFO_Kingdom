---
name: youtube-spec-gen
description: Converts YouTube tutorial transcripts to executable n8n workflow specifications using LLM processing.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.0.0"
  category: workflow-automation
  author: AFO Kingdom
  philosophy_scores:
    truth: 95
    goodness: 90
    beauty: 92
    serenity: 88
---

# YouTube to n8n Spec Generator

Transform YouTube tutorials into executable n8n workflow specifications automatically.

## Pipeline

```
[YouTube URL] → [Transcript Extraction] → [LLM Analysis] → [n8n Spec JSON]
```

## Usage

```python
result = await youtube_spec_gen.convert(
    url="https://youtube.com/watch?v=abc123",
    output_format="n8n"
)
```

## Output

Generates compliant n8n workflow JSON ready for import.
