---
name: strangler-integrator
description: Unifies isolated services (n8n, LangFlow) into the Gateway using Strangler Fig pattern for seamless frontend integration.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.0.0"
  category: integration
  author: AFO Kingdom
  philosophy_scores:
    truth: 95
    goodness: 99
    beauty: 94
    serenity: 98
---

# Strangler Fig Integrator

Gradual migration pattern for unifying distributed services.

## Pattern

```
[User] → [Gateway :3000] → [Proxy] → [n8n | LangFlow | APIs]
```

## Services Integrated

- n8n Workflow Engine
- LangFlow Visual Builder
- Internal APIs
- External Services

One URL to rule them all.
