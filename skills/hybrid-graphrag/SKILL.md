---
name: hybrid-graphrag
description: Advanced knowledge retrieval combining Vector Search with Knowledge Graphs for deep context understanding.
license: MIT
compatibility:
  - claude-code
  - codex
  - cursor
metadata:
  version: "1.0.0"
  category: rag-systems
  author: AFO Kingdom
  philosophy_scores:
    truth: 97
    goodness: 95
    beauty: 92
    serenity: 90
---

# Hybrid GraphRAG

Next-generation retrieval combining vectors and graphs.

## Architecture

```
Query → [Vector Search] + [Graph Traversal] → [Merged Context] → Answer
              ↓                    ↓
        [Qdrant]            [Neo4j]
```

## Capabilities

- `graph_traversal`: Navigate knowledge graph
- `entity_extraction`: Identify entities in text
- `relationship_mapping`: Build entity relationships
- `hybrid_search`: Combined vector + graph search
